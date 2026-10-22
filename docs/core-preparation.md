# Home Assistant Core contribution

I have opened three linked PRs:

- [Core integration and tests](https://github.com/home-assistant/core/pull/187986)
- [Integration and action documentation](https://github.com/home-assistant/home-assistant.io/pull/49636)
- [Google Docs branding](https://github.com/home-assistant/brands/pull/11357)

I modeled the integration on Google Sheets: the same OAuth setup, one document per entry, Home Assistant token refresh, and actions with config-entry selectors. The append and read actions are the basic functionality. An OAuth-only first PR would leave automations with no way to use the document.

## Differences in the Core version

- Integration files live under `homeassistant/components/google_docs`.
- The manifest uses Core documentation, category, and quality metadata. It pins `google-api-python-client==2.71.0`, the version already shared by Google Mail and Google Tasks.
- Setup and unload return `None`, as required by the Core development branch. The custom version returns `True` for Home Assistant 2026.10.2.
- OAuth messages reuse Core's shared translations. English translations are generated with Core's translation tooling.
- Tests use Core's native test helpers and integration import paths.
- Google grouping, code owners, strict typing, requirements, and generated metadata are included in the Core PR.
- The quality-scale file covers Bronze requirements and records entity-related exemptions.

I kept the same document operations and two actions. Selecting existing documents, additional tabs, formatting, and document creation actions remain outside this contribution.

## Validation

All 52 tests pass against the Core development checkout on Python 3.14.8, with 100% statement and branch coverage. The configured hooks pass for all changed files, including Ruff, Pylint, mypy, hassfest, and requirement generation.

The full repository lint run was interrupted after WSL became unresponsive under memory pressure. Validation then completed for the changed files. Upstream CI results are available in the Core PR.

I also tested the custom integration against a real Google document through Home Assistant, including Unicode append and exact readback. The custom version includes local branding in its `brand` directory; the Core version uses the separate branding PR.

The contribution is under review. The custom integration remains available for local testing.
