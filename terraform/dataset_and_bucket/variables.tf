variable "credentials_path" {
    description = "path to creds on json file."
    default = "/opt/airflow/credentials.json"
}

variable "location" {
    description = "Bucket location"
    default = "US"
}

#--------Bucket Section--------
variable "bq_project_id" {
    description = "GCP project ID"
    default = "diseases-and-income-us"
}

variable "region" {
    description = "Project region"
    default = "us-central1"
}

variable "bucket_name" {
    description = "Bucket name"
    default = "diseases-and-income-us-nimagawa"
}

variable "standard" {
    description = "Bucket Standard"
    default = "STANDARD"
}

variable "public_access_prevention" {
    description = "Public access prevention enforcement"
    default = "enforced"
}
