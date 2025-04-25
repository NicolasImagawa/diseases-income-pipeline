# ELT pipeline for income and health issues correlations across the USA

## Overview
This project creates an end-to-end pipeline for income and health issues data in the US. This pipeline can run on multiple machines by using Docker to containerize it.

## Tools used on the project
The tools can be ilustrated by the following image:

![image](https://github.com/user-attachments/assets/c16db90b-888b-4a86-84e7-a01c2f808283)

- Extraction: Python scripts to fetch data from multiple API sources;
- Cleaning: done with pandas, prototyped with Jupyter Notebook;
- IaC tools: Terraform is utilized to create a GCS bucket and the Data Warehouse (BigQuery) initial dataset and tables;
- Storage: In the cloud, with GCS Bucket;
- Data Warehouse: BigQuery;
- Transformation: runs on dbt, also includes testing;
- Orchestration: Every step of the pipeline is managed by Apache Airflow.

## Running the project
Before running the project, please make sure that you have:
1. A GCP (Google Cloud Platform account) with billing enabled;
2. Create a project on GCP 
3. A GCP service account with the following permissions:
   3.1. BigQuery Admin
   3.2. Storage Admin
4. The GCP credentials json file saved to the project's root on your machine.

## Transformation 

## Orchestration DAGs


