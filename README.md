# GCPRI

GCP Resource Inventory (GCPRI) is a simple utility for collecting an
inventory of GCP resources across one or more projects. It uses the
[Cloud Asset API](https://cloud.google.com/asset-inventory/docs/apis) to
query all resources and outputs the results as JSON or CSV.

## Installation

```bash
pip install -r requirements.txt
```

You must also ensure that the Cloud Asset API is enabled and that the
calling account has sufficient permissions (typically `roles/viewer`).

## Usage

```bash
python -m gcpri PROJECT_ID [ANOTHER_PROJECT] --output inventory.json
```

Use `--format csv` to output a CSV file instead of JSON. To load the results
into BigQuery, supply a table name with `--bq-table`:

```bash
python -m gcpri my-project --output inv.json --bq-table mydataset.inventory
```

You can also filter by asset type using one or more `--asset-type` flags.
