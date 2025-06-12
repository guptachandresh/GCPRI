import argparse
import json
import logging
from typing import List, Dict

from google.cloud import asset_v1


def list_assets(project_id: str) -> List[Dict]:
    client = asset_v1.AssetServiceClient()
    scope = f"projects/{project_id}"
    assets = []
    request = asset_v1.ListAssetsRequest(
        parent=scope,
        content_type=asset_v1.ContentType.RESOURCE,
    )
    for asset in client.list_assets(request=request):
        resource = getattr(asset, "resource", None)
        location = None
        if resource is not None:
            location = getattr(resource, "location", None)
            if location is None and getattr(resource, "data", None):
                try:
                    location = resource.data.get("location")
                except Exception:
                    location = None
        assets.append(
            {
                "asset_type": asset.asset_type,
                "name": asset.name,
                "project": project_id,
                "location": location,
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
        "--verbose",
        action="store_true",
        help="Increase output verbosity",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(message)s",
    )

    all_records = []
    for pid in args.project_ids:
        logging.info("Collecting assets for %s...", pid)
        records = list_assets(pid)
        logging.info("Found %d assets in %s", len(records), pid)
        all_records.extend(records)

    write_output(all_records, args.format, args.output)
    logging.info("Wrote %d records to %s", len(all_records), args.output)


if __name__ == "__main__":
    main()
