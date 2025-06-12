# GCPRI

GCP Resource Inventory (GCPRI) is a simple utility for collecting an
inventory of GCP resources across one or more scopes (projects, folders
or organizations). It uses the
[Cloud Asset API](https://cloud.google.com/asset-inventory/docs/apis) to
query all resources and outputs the results as JSON or CSV.

## Installation

```bash
pip install -r requirements.txt
```

You must also ensure that the Cloud Asset API is enabled and that the
calling account has sufficient permissions (typically `roles/viewer`).

## Authentication

The script uses Application Default Credentials to call the Cloud
Asset API. You can authenticate by either setting the
`GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of a
service account key file or by logging in with `gcloud`:

```bash
gcloud auth application-default login
```

Verify that the credentials work by listing resources with `gcloud`:

```bash
gcloud asset search-all-resources --scope="projects/PROJECT_ID" --limit=1
```

## Usage

```bash
python -m gcpri PROJECT_ID [ANOTHER_PROJECT] \
    --folders FOLDER_ID [ANOTHER_FOLDER] \
    --organizations ORG_ID [ANOTHER_ORG] \
    --output inventory.json
```

Pass folder or organization IDs with the `--folders` and `--organizations`
flags. Each may be specified multiple times. Use `--format csv` to output a
CSV file instead of JSON. Pass `--verbose` to see informational logs during
execution.

## License

This project is licensed under the [MIT License](LICENSE).
