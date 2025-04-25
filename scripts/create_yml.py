import argparse
import yaml

def main(params):
    config_dict = {
        "project": params.project,
        "dataset": params.dataset
    }

    profiles_path = "./templates/profiles.txt"
    with open(profiles_path, "r") as profile_file:
        profiles_template = profile_file.read()

    schema_path = "./templates/schema.txt"   
    with open(schema_path, "r") as schema_file:
        schema_template = schema_file.read()

    profile_edit = profiles_template.format(**config_dict)
    schema_edit = schema_template.format(**config_dict)

    output_paths = ["./dbt/profiles.yml", "./dbt/models/core/schema.yml"]

    with open(output_paths[0], "w") as profile_output:
        yaml_profile = yaml.safe_load(profile_edit)
        yaml.dump(yaml_profile, profile_output, sort_keys=False)

    with open(output_paths[1], "w") as schema_output:
        yaml_profile = yaml.safe_load(schema_edit)
        yaml.dump(yaml_profile, schema_output, sort_keys=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Defining parameters for the project.')

    parser.add_argument('--project', default="diseases-and-income-us", help = 'GCP project name')
    parser.add_argument('--dataset', default="main", help = 'Dataset/schema name')

    args = parser.parse_args()

    main(args)