# Google Docs for Home Assistant

Google Docs provides actions to append and read text in a Google document. It follows the Home Assistant Google Sheets integration: each setup entry creates one document named **Home Assistant**, and actions select that entry. You can rename the document in Google Docs and rename the entry in Home Assistant.

This is an experimental custom integration being tested locally before a possible Home Assistant Core contribution. It is developed and tested against Home Assistant 2026.10.2. Google Docs remains a cloud service and needs an internet connection.

## Setup

1. In the Google Cloud project used for your existing Home Assistant Google integrations, enable the [Google Docs API](https://console.cloud.google.com/apis/library/docs.googleapis.com).
2. Download this repository and copy `custom_components/google_docs` into your Home Assistant configuration's `custom_components` directory, then restart Home Assistant.
3. Open **Settings > Devices & services > Add integration > Google Docs**.
4. Supply your existing Google OAuth client ID and secret if requested. The OAuth client must be a Web application with `https://my.home-assistant.io/redirect/oauth` among its authorized redirect URIs.
5. Authorize your Google account. Setup creates one document and displays its link.

For Google OAuth apps in Testing, Google may expire refresh tokens after seven days. The same Google Cloud OAuth setup guidance as [Google Sheets](https://www.home-assistant.io/integrations/google_sheets/) applies.

The requested scope is `https://www.googleapis.com/auth/drive.file`, the same limited scope used by Google Sheets. This integration only targets the document belonging to the selected entry. It cannot select arbitrary existing documents.

The custom integration appears as **Google Docs** in the integration picker. The built-in Google grouping is Core metadata and is not modified by this installation.

The integration includes its Google Docs icon in the `brand` directory, which Home Assistant serves locally.

## Append text

Use `google_docs.append_text` and choose the document entry in the action editor:

```yaml
action: google_docs.append_text
data:
  config_entry: YOUR_GOOGLE_DOCS_ENTRY_ID
  text: |
    {{ now().isoformat() }}: The washing machine finished.
```

Text is appended exactly as supplied, immediately before Google's mandatory final document newline. The YAML `|` includes a trailing newline, so consecutive calls produce separate paragraphs. No timestamp, formatting, or newline is added automatically. Templates are evaluated by Home Assistant before the action runs.

## Read text

`google_docs.get_text` returns data to a script or automation:

```yaml
- action: google_docs.get_text
  data:
    config_entry: YOUR_GOOGLE_DOCS_ENTRY_ID
  response_variable: document
- variables:
    current_text: "{{ document.text }}"
```

The response contains `document_id`, `title`, and `text`. Text includes paragraphs, table cells, and table-of-contents text in document order. Google's final mandatory newline is removed; other newlines are preserved. Formatting, images, headers, footers, and footnotes are not returned.

Both actions operate on the **first document tab**. This is explicit because Google Docs can contain several tabs. Other tabs are not read or changed. Long documents are returned in full, so avoid placing their content in a sensor state or recording private document text in logs or notifications.

## Errors and removal

Expired authorization starts the normal reauthentication flow. Reauthentication reconnects the existing document and never creates a replacement. Deleted or inaccessible documents produce an error. Temporary connection failures during setup retry automatically.

Append requests are not automatically retried. If a request times out after Google has accepted it, inspect the document before repeating the action to avoid duplicate text.

Removing the integration entry leaves the Google document in Drive. Delete that document separately if it is no longer needed. To uninstall the custom integration, remove its entries, delete `custom_components/google_docs`, and restart Home Assistant. Remove its Application Credentials separately if no longer needed.

## Development

Tests use the real Home Assistant 2026.10.2 runtime and Google's official Python client. Google HTTP requests are mocked and sockets are disabled. Test dependencies are pinned in `pyproject.toml` and resolved in `uv.lock`. Run development commands on Linux, including WSL on Windows.

```sh
uv sync --locked --group test
uv run pytest --cov=custom_components.google_docs --cov-branch --cov-report=term-missing --cov-fail-under=100
uv run ruff check .
uv run ruff format --check .
```

The Google client requirement accepts the version already used by Home Assistant's Google Mail and Tasks integrations. Tests pin that shared version to 2.71.0. Each operation creates and closes its own client inside the executor, keeping blocking work out of Home Assistant's event loop and avoiding shared HTTP transports across threads.

CI runs the test suite, coverage, Ruff, and hassfest. [Testing notes](docs/testing.md) record the initial automated checks and live Google Docs test. Report problems through [GitHub issues](https://github.com/moryoav/ha-google-docs/issues).

The module layout mirrors a Core integration. [Core preparation notes](docs/core-preparation.md) describe the remaining upstream work. No Core contribution or acceptance is implied by this local installation.
