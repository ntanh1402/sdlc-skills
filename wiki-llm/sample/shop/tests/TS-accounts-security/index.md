# Accounts Security Suite

* [Overview](overview.md) - Security tests for hashing, rate limiting, and enumeration.

# Test cases

* [Login rate limited](TC-login-rate-limited.md) - Prove repeated failed authentication is throttled.
* [No user enumeration](TC-no-user-enumeration.md) - Prove login does not disclose whether an account exists.
* [Password never plaintext](TC-password-never-plaintext.md) - Prove credentials never persist or appear in logs as plaintext.
* [Session expires](TC-session-expires.md) - Prove expired sessions cannot authorize profile access.

# History

* [Change log](log.md) - History of Accounts Security Suite.
