## About the transformation step

Since the pipeline relies on a star schema, the transformation step will create dimension and fact tables.

After cleaning the data, the pipeline ingests the .csv files from ".data/clean" to a GCS bucket as the input data.

This pipeline step starts with external tables created with the Terraform IaC. These tables are the staging area for the downstream data.

On the ["models/core"](https://github.com/NicolasImagawa/diseases-income-pipeline/tree/main/dbt/models/core) folder, there are all the SQL files regarding the dimensions and fact tables. Since the dataset is not large and the time dimension is yearly, there was no need to partition the tables. However, the tables are clustered whenever a upstream table will be filtered intensively on a set of columns.

For instance, the ["fact_disease.sql"](https://github.com/NicolasImagawa/diseases-income-pipeline/blob/main/dbt/models/core/fact_disease.sql) file is clusterized by the following columns: "question_id", "data_value_unit", "stratification_cat_1" and "stratification_id_1". This helps filtering its downtream table, ["sum_disease.sql"](https://github.com/NicolasImagawa/diseases-income-pipeline/blob/main/dbt/models/core/sum_disease.sql) which filters its upstream counterpart on the columns previously mentioned.

This pattern occurs for all the tables on the dataset/schema.

Since some of the data is unlikely to change, such as CPI values and states names, the `cpi_2022_2025`, `states_num` and `states tables` are seeded through dbt.

In case there is need to access the data lineage, one can do so by typing the following commands on the dbt project folder:

```
dbt docs generate
```

And, then:

```
dbt docs serve
```

The lineage shall be given on `http://localhost:8080`

> [!NOTE]
> It is important to note that the staging, fact and dimensional models are not incremental. This means the tables will be rebuilt every time we run the models. If we plan to ingest data in specific intervals (e.g. each day) then these models should use the 'Incremental' table configuration. For the purpose of this project using a table configuration is enough.
