# Testing notes

The initial local validation was completed on October 22, 2026, against Home Assistant 2026.10.2, Python 3.14.5, and google-api-python-client 2.71.0.

## Automated checks

- 52 tests passed with 100% statement and branch coverage of the integration.
- Ruff checks and formatting passed.
- Hassfest validated the integration metadata, action schemas, translations, dependencies, and icons.

Tests cover the complete OAuth setup flow, insufficient permissions, creation failures, reauthentication without replacing the document, multiple document entries, token refresh, permanent and transient errors, unloaded entries, Unicode text, and plain-text extraction. API transport tests use the real Google discovery client with mocked HTTP transport. Test sockets are disabled.

## Live Google Docs test

After enabling the Docs API and authorizing an account, the integration successfully created its document and loaded its configuration entry.

The live check used the Home Assistant actions to read the document, append one labeled test line containing Hebrew and an emoji, and read it again. The returned document ID matched the selected entry. The returned text exactly matched the original text plus the appended text, and the test line appeared once. Existing text was preserved.

Account identifiers, OAuth credentials, document IDs, private document links, and document contents are omitted from this record.

## Continued local testing

Continue checking real automations, token refresh over time, reauthentication, temporary network failures, document renaming, and multiple entries before deciding whether to propose a Core contribution. Additional tabs, document formatting, and arbitrary existing documents are outside the current feature scope.
