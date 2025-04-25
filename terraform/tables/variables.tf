variable "credentials_path" {
    description = "path to creds on json file."
    default = "/opt/airflow/credentials.json"
}

variable "location" {
    description = "Bucket location"
    default = "US"
}

variable "bq_project_id" {
    description = "GCP project ID"
    default = "diseases-and-income-us"
}

variable "region" {
    description = "Project region"
    default = "us-central1"
}

#--------Dataset(schema) Section--------
variable "dataset_id" {
    description = "Public access prevention enforcement"
    default = "main"
}

#--------External tables Section--------
locals {
  json_config = jsondecode(file("${path.module}/ext_tables_config.json"))

  external_tables = {
    ext_dim_datatype_datatypeunit = {
      source_uri = "gs://${local.json_config.bucket}/datatype_datatypeunit.csv"
    },
    ext_dim_datatype = {
      source_uri = "gs://${local.json_config.bucket}/datatype.csv"
    },
    ext_dim_datatypeid = {
      source_uri = "gs://${local.json_config.bucket}/datatypeid.csv"
    },
    ext_dim_datatypeunit = {
      source_uri = "gs://${local.json_config.bucket}/datatypeunit.csv"
    },
    ext_dim_behavior = {
        source_uri = "gs://${local.json_config.bucket}/dim_behavior.csv"
    },
    ext_dim_disease = {
        source_uri = "gs://${local.json_config.bucket}/dim_disease.csv"
    },
    ext_dim_fruitsprices = {
        source_uri = "gs://${local.json_config.bucket}/fruits_prices.csv"
    },
    ext_dim_question = {
        source_uri = "gs://${local.json_config.bucket}/question.csv"
    },
    ext_dim_questionid = {
        source_uri = "gs://${local.json_config.bucket}/questionid.csv"
    },
    # ext_dim_states = {
    #     source_uri = "gs://${local.json_config.bucket}/states.csv"
    # },
    # ext_dim_states_num = {
    #     source_uri = "gs://${local.json_config.bucket}/states_num.csv"
    # },
    ext_dim_stratification = {
        source_uri = "gs://${local.json_config.bucket}/stratification.csv"
    },
    ext_dim_stratificationid = {
        source_uri = "gs://${local.json_config.bucket}/stratification_id.csv"
    },
    ext_dim_stratification_stratificationid = {
        source_uri = "gs://${local.json_config.bucket}/stratification_stratification_id.csv"
    },
    ext_dim_stratificationcatid = {
        source_uri = "gs://${local.json_config.bucket}/stratificationcatid.csv"
    },
    ext_dim_topic = {
        source_uri = "gs://${local.json_config.bucket}/topic.csv"
    },
    ext_dim_topicid = {
        source_uri = "gs://${local.json_config.bucket}/topicid.csv"
    },
    ext_dim_topicid_questionid = {
        source_uri = "gs://${local.json_config.bucket}/topicid_questionid.csv"
    },
    ext_dim_vegetableprices = {
        source_uri = "gs://${local.json_config.bucket}/vegetable_prices.csv"
    }
  }
  exception_tables = {
    ext_dim_topic_question = {
      source_uri = "gs://${local.json_config.bucket}/topic_question.csv"
    }
  }
}