# Task sizing

The size goes in the Task's `estimate` field.

| Size | Expected scope |
|---|---|
| XS | One configuration, migration step or small function |
| S | One contract or component behaviour |
| M | One vertical feature slice |
| L | A multi-component slice with one outcome; the largest allowed |
| XL | Several independent outcomes; must be split |

Split a Task when it has more than one independently demonstrable outcome,
more than one unrelated owner, or acceptance that cannot stay short. A size is
a planning signal, not a promise of elapsed time.
