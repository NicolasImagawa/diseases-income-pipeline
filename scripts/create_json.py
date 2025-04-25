# project name
    # profiles.yml
    # schema.yml
    # terraform files

# bucket name
    # terraform files

# "table"/schema name:
    # profiles.yml
    # schema.yml
    # terraform files

import argparse
import json

def main(params):
    config_dict = {
        "project": params.project,
        "dataset": params.dataset,
        "bucket": params.bucket
    }

    configs = json.dumps(config_dict, indent = 4)

    output_paths = ["./terraform/dataset_and_bucket/dataset_bucket_config.json", "./terraform/tables/ext_tables_config.json"]

    for path in output_paths:
        with open(path, "w") as output:
            output.write(configs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Defining parameters for the project.')

    parser.add_argument('--project', default="diseases-and-income-us", help = 'GCP project name')
    parser.add_argument('--dataset', default="main", help = 'Dataset/schema name')
    parser.add_argument('--bucket', default="diseases-and-income-us-nimagawa", help = 'GCS bucket name, must be unique across all of GCS.')

    args = parser.parse_args()

    main(args)