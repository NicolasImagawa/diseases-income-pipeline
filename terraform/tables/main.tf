terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.29.0"
    }
  }
}

locals {
  json_data = jsondecode(file("${path.module}/ext_tables_config.json"))
}

provider "google" {
  credentials = var.credentials_path
  project = local.json_data.project
  region = var.region
}

resource "google_bigquery_table" "default" {
  for_each = local.external_tables
  dataset_id = local.json_data.dataset
  table_id   = each.key

  labels = {
    env = "default"
  }

  external_data_configuration {
    autodetect    = true
    source_format = "CSV"

    csv_options {
      quote = "\""
      allow_quoted_newlines = true
      encoding = "UTF-8"
    }

    source_uris = [
      each.value.source_uri
    ]
  }
}

resource "google_bigquery_table" "exception" {
  for_each = local.exception_tables
  dataset_id = local.json_data.dataset
  table_id   = each.key

  labels = {
    env = "default"
  }

  external_data_configuration {
    autodetect    = false
    source_format = "CSV"

    schema = <<EOF
[
  {
    "name": "topic_id",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "Topic ID"
  },
  {
    "name": "question_id",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "Question ID"
  }
]
EOF

    csv_options {
      quote = "\""
      allow_quoted_newlines = true
      encoding = "UTF-8"
      skip_leading_rows = 1
    }

    source_uris = [
      each.value.source_uri
    ]
  }
}
