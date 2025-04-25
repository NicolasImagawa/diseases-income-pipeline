terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.29.0"
    }
  }
}

locals {
  json_data = jsondecode(file("${path.module}/dataset_bucket_config.json"))
}

provider "google" {
  credentials = var.credentials_path
  project = local.json_data.project
  region = var.region
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = local.json_data.dataset
  friendly_name               = "main"
  description                 = "The main table of the project"
  location                    = var.location
  # default_table_expiration_ms = 3600000

  labels = {
    env = "default"
  }
}

resource "google_storage_bucket" "default" {
  name          = local.json_data.bucket
  location      = var.location
  force_destroy = true
  storage_class = var.standard
  public_access_prevention = var.public_access_prevention

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      days_since_noncurrent_time = 1
      send_age_if_zero = false
    }
  }
}