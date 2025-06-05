# Configuration Directory

This folder holds all runtime configuration files for Fundalyze. The
application loads these files on startup via `modules.config_utils` and
`modules.data` helpers.

## `.env`
Environment variables such as API keys. See [docs/configuration.md](../docs/configuration.md)
for a full list of supported variables.

## `settings.json`
Optional user preferences loaded alongside `.env`.

## `directus_field_map.json`
Defines how local column names map to fields in your Directus collections.
The file structure is:

```json
{
  "collections": {
    "collection_name": {
      "fields": {
        "Local Column": {
          "type": "string",
          "mapped_to": "directus_field"
        }
      }
    }
  }
}
```
- **collections** – top-level object keyed by Directus collection name.
- **fields** – maps each local column to its metadata.
- **mapped_to** – name of the target Directus field.

See `directus_field_map.schema.json` for the formal JSON schema.

## `term_mapping.json`
Maps canonical sector or industry names to lists of synonyms used when
normalizing data across APIs. Each key is the canonical term and the value
is an array of aliases. Refer to `term_mapping.schema.json` for the schema.

## `finance_api.yaml`
Optional settings for a custom finance API. Fields include:
- `base_url` – root API endpoint.
- `api_key` – authentication token if required.
- `endpoints` – dictionary of endpoint paths used by custom scripts.

Modify these files to adapt Fundalyze to your environment. Any unknown files
in this directory are ignored by version control so you can safely add
private configuration.
