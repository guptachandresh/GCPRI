import argparse
import json
from typing import List, Dict

from google.cloud import asset_v1
from google.cloud import bigquery


def list_assets(project_id: str, asset_types: List[str] | None = None) -> List[Dict]:
    client = asset_v1.AssetServiceClient()
    scope = f"projects/{project_id}"
    assets = []
    request = asset_v1.ListAssetsRequest(
        parent=scope,
        content_type=asset_v1.ContentType.RESOURCE,
        asset_types=asset_types or [],
    )
    for asset in client.list_assets(request=request):
        assets.append(
            {
                "asset_type": asset.asset_type,
                "name": asset.name,
                "project": project_id,
                "location": asset.resource.location,
            }
        )
    return assets


def write_output(records: List[Dict], output_format: str, output_path: str):
    if output_format == "json":
        with open(output_path, "w") as fh:
            json.dump(records, fh, indent=2)
    elif output_format == "csv":
        import csv

        if records:
            fieldnames = list(records[0].keys())
        else:
            fieldnames = []
        with open(output_path, "w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
    else:
        raise ValueError(f"Unsupported format: {output_format}")


def write_bigquery(records: List[Dict], table: str):
    if not records:
        return
    client = bigquery.Client()
    table_ref = bigquery.TableReference.from_string(table)
    errors = client.insert_rows_json(table_ref, records)
    if errors:
        raise RuntimeError(f"BigQuery insertion errors: {errors}")


def main():
    parser = argparse.ArgumentParser(description="GCP Resource Inventory")
    parser.add_argument("project_ids", nargs="+", help="GCP project IDs to inventory")
    parser.add_argument(
        "--format",
        choices=["json", "csv"],
        default="json",
        help="Output format",
    )
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument(
        "--asset-type",
        action="append",
        dest="asset_types",
        help="Filter to specific asset type (repeatable)",
    )
    parser.add_argument(
        "--bq-table",
        help="BigQuery table to load results into (e.g. dataset.table)",
    )
    args = parser.parse_args()

    all_records = []
    for pid in args.project_ids:
        print(f"Collecting assets for {pid}...")
        records = list_assets(pid, asset_types=args.asset_types)
        print(f"Found {len(records)} assets in {pid}")
        all_records.extend(records)

    write_output(all_records, args.format, args.output)
    print(f"Wrote {len(all_records)} records to {args.output}")
    if args.bq_table:
        print(f"Loading {len(all_records)} records into {args.bq_table}...")
        write_bigquery(all_records, args.bq_table)


if __name__ == "__main__":
    main()
