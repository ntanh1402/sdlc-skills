from .support import RuleTest

CREATE = "pay/services/SVC-pay/EP-pay-create.md"
REFUND = "pay/services/SVC-pay/EP-pay-refund.md"
TABLE = "pay/datastores/DB-main/TBL-payments.md"
INDEX = "pay/datastores/IDX-payments/overview.md"
CHANGE = "pay/change-requests/CR-1/overview.md"
FEATURE = "pay/features/FEAT-pay/overview.md"
CHANGE_TASK = "pay/change-requests/CR-1/TASK-pay-003.md"
FEATURE_TASK = "pay/features/FEAT-pay/TASK-pay-002.md"
ENTRY = "\n\n# Pending changes\n\n* [CR-1](../../change-requests/CR-1/overview.md) — modified — adds `couponCode`."


class PendingTest(RuleTest):
    def found(self):
        return {(item.rule, item.path) for item in self.findings()}

    # 1. presence
    def test_active_concept_must_not_have_the_section(self):
        self.edit(CREATE, "status: Modifying", "status: Active")
        self.assertRule("pending.presence", CREATE)

    def test_pending_status_needs_the_section(self):
        self.edit(CREATE, ENTRY, "")
        self.assertIn(("pending.presence", CREATE), self.found())

    # 2. open parent
    def test_entry_for_a_finished_change_request(self):
        self.edit(CHANGE, "status: Approved", "status: Implemented")
        self.assertIn(("pending.parent-open", CREATE), self.found())

    def test_entry_for_a_released_feature(self):
        self.edit(FEATURE, "status: InDev", "status: Released")
        self.assertIn(("pending.parent-open", REFUND), self.found())

    # 3. declared by the parent
    def test_change_request_delta_must_list_the_concept_with_the_same_qualifier(self):
        self.edit(CREATE, "— modified — adds", "— removed — drops")
        self.edit(CREATE, "status: Modifying", "status: Removing")
        self.assertIn(("pending.undeclared", CREATE), self.found())

    def test_feature_architecture_must_link_the_concept(self):
        self.edit(FEATURE, ", [EP-pay-refund](../../services/SVC-pay/EP-pay-refund.md)", "")
        self.assertRule("pending.undeclared", REFUND)

    # 4. no missing entry, from the delta
    def test_delta_concept_without_an_entry(self):
        self.edit(
            CHANGE,
            "— modified — adds `couponCode`.\n",
            "— modified — adds `couponCode`.\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md) — modified — adds a column.\n",
        )
        self.assertRule("pending.missing-delta", TABLE)

    def test_delta_concept_is_exempt_once_its_tasks_are_done(self):
        self.edit(CHANGE_TASK, "status: Todo", "status: Done")
        self.edit(CREATE, ENTRY, "")
        self.edit(CREATE, "status: Modifying", "status: Active")
        self.assertRule("pending.request-implemented", CHANGE)

    # 5. no missing entry, from Tasks
    def test_unfinished_task_scope_without_an_entry(self):
        self.edit(
            FEATURE_TASK,
            "— new — the endpoint.",
            "— new — the endpoint.\n* [IDX-payments](../../datastores/IDX-payments/overview.md) — modified — a new field.",
        )
        self.assertRule("pending.missing-task", INDEX)

    def test_task_and_entry_must_use_the_same_qualifier(self):
        self.edit(CHANGE_TASK, "— modified — the new field.", "— removed — the new field.")
        self.assertRule("pending.missing-task", CREATE)

    def test_message_names_no_qualifier_when_the_task_has_none(self):
        self.edit(FEATURE_TASK, "— new — the endpoint.", "— built — the endpoint.")
        found = self.findings()
        self.assertIn(("pending.missing-task", REFUND), {(item.rule, item.path) for item in found})
        self.assertEqual([item.message for item in found if "None" in item.message], [])

    def test_done_task_scope_needs_no_entry(self):
        self.assertNotIn(("pending.missing-task", TABLE), self.found())

    # 6. no leftover entry
    def test_entry_left_after_every_covering_task_is_done(self):
        self.edit(CHANGE_TASK, "status: Todo", "status: Done")
        self.assertReported("pending.leftover", CREATE)

    # 7. status agrees with the entries
    def test_new_entry_needs_planned(self):
        self.edit(REFUND, "status: Planned", "status: Modifying")
        self.assertRule("pending.status", REFUND)

    def test_new_wins_over_modified(self):
        self.edit(
            REFUND,
            "— new — not built yet.",
            "— new — not built yet.\n* [CR-1](../../change-requests/CR-1/overview.md) — modified — also changed.",
        )
        self.edit(
            CHANGE,
            "— modified — adds `couponCode`.\n",
            "— modified — adds `couponCode`.\n* [EP-pay-refund](../../services/SVC-pay/EP-pay-refund.md) — modified — also changed.\n",
        )
        self.assertClean()

    def test_removed_wins_over_modified(self):
        self.edit(CREATE, ENTRY, ENTRY + "\n* [FEAT-pay](../../features/FEAT-pay/overview.md) — removed — replaced by a new endpoint.")
        self.assertRule("pending.status", CREATE)
        self.edit(CREATE, "status: Modifying", "status: Removing")
        self.assertClean()


    # 8. the parent follows its Tasks
    def test_change_request_with_every_task_done_must_be_implemented(self):
        self.edit(CHANGE_TASK, "status: Todo", "status: Done")
        self.assertReported("pending.request-implemented", CHANGE)

    def test_implemented_change_request_with_every_task_done(self):
        self.edit(CHANGE_TASK, "status: Todo", "status: Done")
        self.edit(CHANGE, "status: Approved", "status: Implemented")
        self.edit(CREATE, ENTRY, "")
        self.edit(CREATE, "status: Modifying", "status: Active")
        self.assertClean()

    def test_change_request_with_no_task_is_not_asked_to_be_implemented(self):
        self.remove(CHANGE_TASK)
        self.assertNotIn("pending.request-implemented", {rule for rule, _ in self.found()})

    def test_feature_in_dev_with_every_task_done_is_a_warning(self):
        self.edit(FEATURE_TASK, "status: Todo", "status: Done")
        found = [(item.rule, item.path, item.severity) for item in self.findings()]
        self.assertIn(("pending.feature-built", FEATURE, "warning"), found)

    def test_feature_with_an_open_task_is_not_reported_as_built(self):
        self.assertNotIn("pending.feature-built", {rule for rule, _ in self.found()})

    # 9. a removal that is built
    def test_removing_concept_with_no_section_must_become_deprecated(self):
        self.edit(CREATE, ENTRY, "")
        self.edit(CREATE, "status: Modifying", "status: Removing")
        found = self.found()
        self.assertIn(("pending.removing-file", CREATE), found)
        self.assertNotIn(("pending.presence", CREATE), found)
        messages = [item.message for item in self.findings() if item.rule == "pending.removing-file" and item.path == CREATE]
        self.assertIn("set the status to Deprecated", messages[0])
        self.assertNotIn("delete", messages[0])

    def test_removing_folder_concept_is_reported_once(self):
        self.edit(INDEX, "status: Active", "status: Removing")
        messages = [item.message for item in self.findings() if item.rule == "pending.removing-file" and item.path == INDEX]
        self.assertEqual(len(messages), 1)

    def test_a_removed_concept_kept_as_deprecated_is_accepted(self):
        self.edit(CREATE, ENTRY, "")
        self.edit(CREATE, "status: Modifying", "status: Deprecated")
        found = self.found()
        self.assertNotIn(("pending.removing-file", CREATE), found)
        self.assertNotIn(("pending.presence", CREATE), found)

    def test_removing_concept_with_an_entry_is_not_reported_as_built(self):
        self.edit(CREATE, "— modified — adds", "— removed — drops")
        self.edit(CREATE, "status: Modifying", "status: Removing")
        self.assertNotIn("pending.removing-file", {rule for rule, _ in self.found()})


class SupersessionTest(RuleTest):
    def test_superseded_decision_must_say_so(self):
        self.edit("pay/decisions/ADR-001.md", "status: Superseded", "status: Accepted")
        self.assertRule("supersession.status", "pay/decisions/ADR-001.md")

    def test_superseded_status_needs_a_superseding_decision(self):
        self.edit("pay/decisions/ADR-002.md", "\n\n# Supersedes\n\n* [ADR-001](ADR-001.md)", "")
        self.assertRule("supersession.status", "pay/decisions/ADR-001.md")
