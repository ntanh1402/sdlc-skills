# General

* [Overview](overview.md) - Security cases of the auth surface, tied to no single story.

# Test cases

* [Login rate limited](TC-1-login-rate-limited.md) - Prove repeated failed authentication is throttled.
* [No user enumeration](TC-2-no-user-enumeration.md) - Prove login does not disclose whether an account exists.
* [Password never plaintext](TC-3-password-never-plaintext.md) - Prove credentials never persist or appear in logs as plaintext.
* [Session expires](TC-4-session-expires.md) - Prove expired sessions cannot authorize profile access.

# History

* [Change log](log.md) - History of General.
