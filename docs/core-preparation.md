# Preparing a Home Assistant Core contribution

The runtime code follows `google_sheets`: a service integration, UI OAuth flow, one document ID as each entry's unique ID, HA-managed token refresh, and actions with config-entry selectors. The API calls use Google's published Python client rather than hand-written HTTP requests. No private credentials or account tokens belong in the source tree.

The local adapter is under `custom_components/google_docs`. For a Core contribution, move it to `homeassistant/components/google_docs`, remove the custom manifest `version`, update the documentation URL to the integration's Home Assistant documentation, and add the current integration category. The boolean setup/unload return values match HA 2026.10.2; adapt those signatures to the Core development branch when preparing the PR.

Tests already follow `tests/components/google_docs`. In Core, change custom-component imports and patch targets to `homeassistant.components.google_docs` and use the test helpers of the target Core checkout. Keep token-flow, API transport, error, entry-isolation, and text-extraction coverage. Regenerate English translations through Core's translation tooling instead of maintaining `translations/en.json` by hand.

Before submission:

- Agree on an action-only initial integration with Core maintainers. Current first-PR guidance asks for one platform and no custom actions; the older Google Sheets integration is a precedent, not approval for a new action-only integration.
- Meet Bronze rules and add a complete `quality_scale.yaml`, with explicit reasons for entity-related exemptions. Do not claim a quality tier until Core's checks and review support it.
- Add `google_docs` to `homeassistant/brands/google.json`, run hassfest, and include generated metadata changes.
- Add Google Docs icon/logo assets to the brands repository.
- Add a Home Assistant documentation page with setup, permissions, action examples, first-tab behavior, errors, and removal instructions.
- Confirm the Google API client's version against all integrations sharing the requirement. Avoid upgrading that shared requirement as an incidental part of the new integration.
- Run Core's tests, hassfest, typing, formatting, and requirement-generation checks on the target branch.
- Have the human contributor review, understand, and explain the complete change before submitting it.

Optional features such as selecting existing documents, other tabs, formatting, templates, and document creation actions are outside the first local version. Keep them separate if added later.

References: [Google Sheets source](https://github.com/home-assistant/core/tree/2026.10.2/homeassistant/components/google_sheets), [new integrations](https://contributors.home-assistant.io/core/integrations/create/), [quality scale](https://contributors.home-assistant.io/core/quality-scale/), [library requirements](https://contributors.home-assistant.io/core/integrations/api-library/), and [integration brands](https://contributors.home-assistant.io/core/integrations/brands/).
