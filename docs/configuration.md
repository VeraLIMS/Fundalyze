# Configuration & Secrets

Fundalyze reads configuration from the `config/` directory at startup. Two optional files are supported:

1. **`.env`** – environment variables such as API tokens.
2. **`settings.json`** – user preferences in JSON format.

Both files are ignored by Git so you can safely store credentials locally.

## Creating `config/.env`
Example contents:
```env
# API keys
OPENBB_TOKEN=your-openbb-key
FMP_API_KEY=your-fmp-key
DIRECTUS_URL=https://your-directus.example.com
DIRECTUS_TOKEN=secret-token
CF_ACCESS_CLIENT_ID=your-client-id
CF_ACCESS_CLIENT_SECRET=your-client-secret

# Optional collection names
DIRECTUS_PORTFOLIO_COLLECTION=portfolio
DIRECTUS_GROUPS_COLLECTION=groups
OUTPUT_DIR=output
```
To obtain an OpenBB API token visit the
[OpenBB documentation](https://docs.openbb.co/platform/getting_started/api_requests)
and sign up for an account. Once acquired, run the **OpenBB API Token** wizard
inside the Settings Manager to store the token. The `get_openbb()` helper uses this
token to log in whenever OpenBB data is requested. The Settings Manager also
 provides wizards for configuring your **Directus connection** and **Notes
 directory**. Another wizard sets the **Output Directory** used for reports.
 A **Cloudflare Access** wizard stores the `CF_ACCESS_CLIENT_ID` and
 `CF_ACCESS_CLIENT_SECRET` variables required when your Directus instance is
 protected by Cloudflare Access. These map to the `CF-Access-Client-Id` and
 `CF-Access-Client-Secret` HTTP headers.
 Similarly, obtain a Financial Modeling Prep key from
 [fmp](https://financialmodelingprep.com/) and run the **FMP API Key** wizard
 to store it in `.env`. If you already exported these variables in your shell,
 the **Quick Setup** wizard can write them all to `.env` in one go.
`modules.config_utils` automatically loads this file using [python-dotenv](https://github.com/theskumar/python-dotenv) whenever `load_settings()` is called.

## Creating `config/settings.json`
This file stores additional preferences that are not secrets. A minimal example:
```json
{
  "currency": "USD",
  "timezone": "UTC"
}
```
The timezone can be changed later by running the **Timezone** wizard inside the
Settings Manager. Additional wizards help configure Directus connectivity and the notes directory.
`load_settings()` returns the parsed dictionary so other modules can access these values.

## Directus Field Mapping
`config/directus_field_map.json` defines how local field names map to your Directus collections.
Each key is a collection name with a dictionary mapping local column names to the
corresponding Directus field. Adjust this file if you rename fields or add new
attributes to Directus.

## Initial Setup
1. Clone the repository and run one of the `bootstrap_env` scripts to create a virtual environment and install dependencies.
2. Populate `config/.env` and optionally `config/settings.json` as shown above.
3. Launch the CLI with:
   ```bash
   python scripts/main.py
   ```
The application will pick up your configuration automatically on startup.
