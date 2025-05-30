# ELT pipeline for income and health issues correlations across the USA

## Overview
This project creates an end-to-end pipeline for income and health issues correlation data in the US for the year 2021 and adjusts food prices considering inflation. This pipeline can run on multiple machines by using `Docker` to containerize it.

if you simply want to run this project, jump to the ["Running the project" section.](#running-the-project)

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

In order to optimize storage, the dim_behavior and dim_diseases table use integers instead of strings and any unnecessary data from the extracted data. When necessary, any further details are obtained with other dimensional tables created and applied to the downstream data.

Also, the column names were changed to standardize dimensions across the dataset/schema.

Since US territories were considered by the data source, more than 50 were expected on the cleaning output. On this case, 55 States and territories were considered.

Finally, all the outputs were saved as .csv files.

> [!NOTE]
> The data cleaning was prototyped with Jupyter Notebook and is located on the ["Notebook Prototypes"](https://github.com/NicolasImagawa/diseases-income-pipeline/tree/main/Notebook%20prototypes) files.

## Transformation 
As stated before, dbt transforms the data in the warehouse in order to create a star schema. First, the external tables are utilized as a staging area for the dimension tables.
Then, the fact tables for diseases, behavior, fruit and vegetable prices are created. The lineage is shown below, for more details please check the [dbt folder](https://github.com/NicolasImagawa/diseases-income-pipeline/tree/main/dbt).

![image](https://github.com/user-attachments/assets/dcfd2603-6522-4cca-91f2-c8f7e194bbd6)

## Orchestration DAGs
Multiple DAGs were developed in order to achieve modularity in the pipeline.

![image](https://github.com/user-attachments/assets/7f8c670d-cb97-4d38-997d-1e17a907669d)

The 1st DAG can trigger its subsequent and so on, making the end-to-end operation easier for the user.

## Data visualization
There are many correlation analysis to be done with the pipeline results. For instance, one can see what states had the adults (18 to 44 years) with the lowest fruits comsuption for 2021 and if these same places will have the highest diabetes cases per 100,000 people and considering an 15 to 25 thousand USD income.

![image](https://github.com/user-attachments/assets/e6e3debc-f2c1-4541-b69b-568e44e96e5f)
\
\
\
![image](https://github.com/user-attachments/assets/3bd6464e-1358-4ed9-bc61-6ad455b3cf98)

\
Also, the pipeline provides vegetable and fruits prices adjusted to inflation, in order to analyze how hard it is to buy food that is technically healthy.
\
\
![image](https://github.com/user-attachments/assets/453528ce-23a0-46c5-ad81-2515e440d3d9)

From the data shown above, some states with the least vegetable consumption do appear in the diabetes chart, like Texas and New Mexico. However, diabetes may develop further on many people and the data shows only adults and not elderly people.
Also, the vegetable charts shows that the most expensive items are not that commom on the average North American nutrition and dishes such as Aspargus, Olivia and Okra. Therefore, any analyzis regarding socioeconomical relations between health and income must seek other patterns.

## Running the project
> [!IMPORTANT]
> Please make sure the GCP credentials file is on the project's root and won't be available to public access.

Before running the project, please make sure that you have:
1. Cloned this repo
2. A GCP (Google Cloud Platform account) with billing enabled;
3. Create a project on GCP 
4. A GCP service account with the following permissions:
   - BigQuery Admin
   - Storage Admin
5. The GCP credentials file saved to the project's root on your machine;
6. Renamed the file from item 4 to "credentials.json";
7. Docker installed on your machine.

After the above instructions, run the following command on the project's root directory:

```
./run_pipeline.sh
```

Then, access airflow on the following port:

```
http://localhost:8081
```

Use "airflow" on both "Username" and "Password"

Finally, run the DAGs to see the pipeline in action!

### Further improvements

- CI/CD implementation;
- Year partitioning, in case the dataset grows to large;
- Unit and Integration tests
