# ELT pipeline for income and health issues correlations across the USA

## Overview
This project creates an end-to-end pipeline for income and health issues data in the US. This pipeline can run on multiple machines by using Docker to containerize it.

## Tools used on the project
The data tools can be ilustrated by the following image:

![image](https://github.com/user-attachments/assets/78381c16-e94f-4dbd-ba51-7c02ffb81e64)

- Extraction: Python scripts to fetch data from multiple API sources;
- Cleaning: done with pandas, prototyped with Jupyter Notebook;
- IaC tools: Terraform is utilized to create a GCS bucket and the Data Warehouse (BigQuery) initial dataset and tables;
- Storage: In the cloud, with GCS Bucket;
- Data Warehouse: BigQuery;
- Transformation: runs on dbt, also includes testing;
- Orchestration: Every step of the pipeline is managed by Apache Airflow;
- Data visualization: Looker.

## Data Cleaning
The data was cleansed and adapted to follow the same pattern when required. For instance, columns with null values were removed for the pipeline downstream components and columns such as questionid had to be adjusted to follow the pattern "ABC01".

Also, the column names were changed to standardize dimensions across the dataset/schema.

Since US territories were considered by the data source, more than 50 were expected on the cleaning output. On this case, 55 States and territories were considered.

Finally, all the outputs were saved as .csv files.

> [!NOTE]
> The data cleaning was prototyped with Jupyter Notebook and is located on the "Notebook Prototypes" files.

## Transformation 
As stated before, dbt transforms the data in the warehouse in order to create a star schema. First, the external tables are utilized as a staging area for the dimension tables.
Then, the fact tables for diseases, behavior, fruit and vegetable prices are created. The lineage is shown below, for more details please check the dbt folder.

![image](https://github.com/user-attachments/assets/dcfd2603-6522-4cca-91f2-c8f7e194bbd6)

## Orchestration DAGs
Multiple DAGs were developed in order to achieve modularity in the pipeline. Therefore, the project has 5 DAGs:

![image](https://github.com/user-attachments/assets/7f8c670d-cb97-4d38-997d-1e17a907669d)

The 1st DAG can trigger its subsequent and so on, making the end-to-end operation easier for the user.

## Data visualization

## Running the project
> [!IMPORTANT]
> Please make sure the GCP credentials file is on the project's root and won't available to public access

Before running the project, please make sure that you have:
1. A GCP (Google Cloud Platform account) with billing enabled;
2. Create a project on GCP 
3. A GCP service account with the following permissions:
   - BigQuery Admin
   - Storage Admin
4. The GCP credentials file saved to the project's root on your machine.
5. Renamed the file from item 4 to "credentials.json"
