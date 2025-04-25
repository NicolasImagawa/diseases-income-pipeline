def clean_behaviors():
    import pandas as pd
    from pathlib import Path
    import json

    json_path = "./config/paths.json"
    with open(json_path) as json_file:
        paths = json.load(json_file)

    path = Path(paths["behavior"]["raw"])

    if not path.exists():
        raise FileNotFoundError(f"File {path} was not found.")

    df = pd.read_csv(path)


    df.columns = ["year_start", "year_end", "state_abr", "state_name", "data_source", 
                "class", "topic", "question", "data_value_unit", "data_value_type",
                "data_value", "data_value_alt", "data_value_footnote_symbol",
                "data_value_footnote", "low_confidence_limit", "high_confidence_limit",
                "sample_size", "total", "Age(years)", "Education", "Sex", "Income",
                "Race/Ethnicity", "geolocation", "class_id", "topic_id", "question_id",
                "data_value_type_id", "location_id", "stratification_cat_1", 
                "stratification_1", "stratification_cat_id_1", "stratification_id_1"]


    behav_topic_df = df[["topic"]].drop_duplicates()
    behav_question_df = df[["question"]].drop_duplicates()


    behav_class_id_df = df[["class_id"]].drop_duplicates()
    behav_class_id_df = behav_class_id_df.replace(['PA', 'FV'], ['PAB', 'FVB'])


    behav_topic_id_df = df[["topic_id"]].drop_duplicates()


    behav_question_id_df = df[["question_id"]].drop_duplicates()


    behav_class_id_question_id_df = df[["class_id", "question_id"]].drop_duplicates()
    behav_class_id_question_id_df = behav_class_id_question_id_df.replace(['PA', 'FV'], ['PAB', 'FVB'])


    behav_class_id_question_id_df_ows = behav_class_id_question_id_df[(behav_class_id_question_id_df["class_id"] == "OWS")]
    behav_class_id_question_id_df_pa = behav_class_id_question_id_df[(behav_class_id_question_id_df["class_id"] == "PAB")]
    behav_class_id_question_id_df_fv = behav_class_id_question_id_df[(behav_class_id_question_id_df["class_id"] == "FVB")]


    behav_class_id_question_id_df_ows["aux_id"] = [f"{i:02d}" for i in range(1, len(behav_class_id_question_id_df_ows) + 1)]
    behav_class_id_question_id_df_pa["aux_id"] = [f"{i:02d}"  for i in range(1, len(behav_class_id_question_id_df_pa) + 1)]
    behav_class_id_question_id_df_fv["aux_id"] = [f"{i:02d}"  for i in range(1, len(behav_class_id_question_id_df_fv) + 1)]


    behav_class_id_question_id_df_ows["question_id_new"] = behav_class_id_question_id_df_ows["class_id"] + behav_class_id_question_id_df_ows["aux_id"]
    behav_class_id_question_id_df_pa["question_id_new"] = behav_class_id_question_id_df_pa["class_id"] + behav_class_id_question_id_df_pa["aux_id"]
    behav_class_id_question_id_df_fv["question_id_new"] = behav_class_id_question_id_df_fv["class_id"] + behav_class_id_question_id_df_fv["aux_id"]


    behav_class_id_question_id_df_ows = behav_class_id_question_id_df_ows[["class_id", "question_id_new"]]
    behav_class_id_question_id_df_pa = behav_class_id_question_id_df_pa[["class_id", "question_id_new"]]
    behav_class_id_question_id_df_fv = behav_class_id_question_id_df_fv[["class_id", "question_id_new"]]


    behav_class_id_question_id_df = pd.merge(behav_class_id_question_id_df, behav_class_id_question_id_df_ows, how = "outer", on = ["class_id"])
    behav_class_id_question_id_df = pd.merge(behav_class_id_question_id_df, behav_class_id_question_id_df_pa, how = "outer", on = ["class_id", "question_id_new"])
    behav_class_id_question_id_df = pd.merge(behav_class_id_question_id_df, behav_class_id_question_id_df_fv, how = "outer", on = ["class_id", "question_id_new"])


    behav_class_id_question_id_df = behav_class_id_question_id_df[["class_id", "question_id_new"]].drop_duplicates() \
                                                                                                .dropna()


    behav_class_id_question_id_df.columns = ["topic_id", "question_id"]
    behav_topic_id_question_id_df = behav_class_id_question_id_df


    behav_ctg_df = df[["stratification_cat_1"]].drop_duplicates().sort_values(by = ["stratification_cat_1"])
    behav_ctg_df["stratification_num"] = [i for i in range(1, len(behav_ctg_df) + 1)]


    behav_ctg_df = behav_ctg_df.replace('Age (years)', 'Age')


    behav_stratification_id = df[["stratification_id_1"]].drop_duplicates().sort_values(by = ["stratification_id_1"])
    behav_stratification_id["stratification_id_num"] = [i for i in range(1, len(behav_stratification_id) + 1)]


    seeds_path = "./dbt/seeds"
    states_num_df = pd.read_csv(f"{seeds_path}/states_num.csv")


    dim_path = "./data/clean"
    stratification_df = pd.read_csv(f"{dim_path}/stratification.csv")
    stratificationid_df = pd.read_csv(f"{dim_path}/stratification_id.csv")
    stratificationcatid_df = pd.read_csv(f"{dim_path}/stratificationcatid.csv")
    topic_df = pd.read_csv(f"{dim_path}/topic.csv")
    topicid_df = pd.read_csv(f"{dim_path}/topicid.csv")
    question_df = pd.read_csv(f"{dim_path}/question.csv")
    questionid_df = pd.read_csv(f"{dim_path}/questionid.csv")
    topicid_questionid_df = pd.read_csv(f"{dim_path}/topicid_questionid.csv")


    question_df = pd.merge(question_df, behav_question_df, how = "outer", on = ["question"]).sort_values(by = ["question_num"])
    question_df["question_num"] = [i for i in range(1, len(question_df) + 1)]



    questionid_df = pd.merge(questionid_df, behav_topic_id_question_id_df["question_id"], how = "outer", on = ["question_id"]) \
                    .sort_values(by = ["question_num"])
    questionid_df["question_num"] = [i for i in range(1, len(questionid_df) + 1)]
    questionid_df[(questionid_df["question_num"].isna()==True)]


    topic_df = pd.merge(topic_df, behav_topic_df, how = "outer", on = ["topic"]) \
                .sort_values(by = ["topic_num"])
    topic_df["topic_num"] = [i for i in range(1, len(topic_df) + 1)]
    topic_df = topic_df[["topic_num", "topic"]]
    topicid_df = pd.merge(topicid_df, behav_topic_id_question_id_df["topic_id"], how = "outer", on = ["topic_id"]).drop_duplicates() \
                                                                                                                .sort_values(by = ["topic_num"])
    topicid_df["topic_num"] = [i for i in range(1, len(topicid_df) + 1)]


    topicid_questionid_df_temp = pd.merge(topicid_questionid_df, questionid_df, how = "outer", on = ["question_num"])
    topicid_questionid_df_temp["topic_id"] = topicid_questionid_df_temp["question_id"].str[0:3]
    topicid_questionid_df_temp = pd.merge(topicid_questionid_df_temp, topicid_df, how = "outer", on = ["topic_id"])
    topicid_questionid_df_temp_y = topicid_questionid_df_temp[(topicid_questionid_df_temp["question_num"] >= 110)]
    topicid_questionid_df_temp_y = topicid_questionid_df_temp_y[["topic_num_y", "question_num"]]
    topicid_questionid_df_temp_y.columns = ["topic_num", "question_num"]
    topicid_questionid_df_temp_x = topicid_questionid_df_temp[(topicid_questionid_df_temp["question_num"] < 110)]
    topicid_questionid_df_temp_x = topicid_questionid_df_temp_x[["topic_num_x", "question_num"]]
    topicid_questionid_df_temp_x.columns = ["topic_num", "question_num"]
    topicid_questionid_df_temp = pd.concat([topicid_questionid_df_temp_x, topicid_questionid_df_temp_y])
    topicid_questionid_df = topicid_questionid_df_temp.astype({'topic_num': int, 'question_num': int})


    stratification_df = pd.merge(stratification_df, behav_ctg_df["stratification_cat_1"], how = "outer", on = ["stratification_cat_1"]).sort_values(by = ["stratification_num"])
    stratification_df["stratification_num"] = [i for i in range(1, len(stratification_df) + 1)]


    behav_stratificationcatid_df = df[["stratification_cat_id_1"]].drop_duplicates()
    behav_stratificationcatid_df = behav_stratificationcatid_df.replace(['OVR', 'AGEYR'], ['OVERALL', 'AGE'])


    stratificationcatid_df = pd.merge(stratificationcatid_df, behav_stratificationcatid_df, how = "outer", on = ["stratification_cat_id_1"]) \
                            .sort_values(by = ["stratification_num"])
    stratificationcatid_df["stratification_num"] = [i for i in range(1, len(stratificationcatid_df) + 1)]


    behav_stratification_id = df[["stratification_id_1"]].drop_duplicates()
    behav_stratification_id = behav_stratification_id.replace(["FEMALE", "AGEYR3544", "MALE", "AGEYR2534", "RACEWHT",
                                                            "RACEASN", "AGEYR1824", "RACEHPI", "RACENAA", "RACEHIS",
                                                            "RACEBLK", "AGEYR5564", "AGEYR65PLUS", "OVERALL", "AGEYR4554"],
                                                            ["SEXF", "AGE3544", "SEXM", "AGE2534", "WHT", 
                                                            "ASN", "AGE1824", "HAPI", "AIAN", "HIS",
                                                            "BLK", "AGE5564", "AGE65P", "OVR", "AGE4554"]
                                                            )


    stratificationid_df = pd.merge(stratificationid_df, behav_stratification_id, how = "outer", on = ["stratification_id_1"]) \
                            .sort_values(by = ["stratification_id_num"])
    stratificationid_df["stratification_id_num"] = [i for i in range(1, len(stratificationid_df) + 1)]


    df = pd.merge(df, states_num_df, how = "inner", on = ["state_abr"])
    df = pd.merge(df, question_df, how = "inner", on = ["question"])
    df = pd.merge(df, topic_df, how = "inner", on = ["topic"])
    df = pd.merge(df, stratification_df, how = "inner", on = ["stratification_cat_1"])


    df["stratification_id_1"] = df["stratification_id_1"].replace(["FEMALE", "AGEYR3544", "MALE", "AGEYR2534", "RACEWHT",
                                                            "RACEASN", "AGEYR1824", "RACEHPI", "RACENAA", "RACEHIS",
                                                            "RACEBLK", "AGEYR5564", "AGEYR65PLUS", "OVERALL", "AGEYR4554"],
                                                            ["SEXF", "AGE3544", "SEXM", "AGE2534", "WHT", 
                                                            "ASN", "AGE1824", "HAPI", "AIAN", "HIS",
                                                            "BLK", "AGE5564", "AGE65P", "OVR", "AGE4554"]
                                                            )
    df = pd.merge(df, stratificationid_df, how = "inner", on = ["stratification_id_1"])
    df["stratification_cat_id_1"] = df["stratification_cat_id_1"].replace(['OVR', 'AGEYR'], ['OVERALL', 'AGE'])
    df = pd.merge(df, stratificationcatid_df["stratification_cat_id_1"], how = "inner", on = ["stratification_cat_id_1"])
    df = df[(df["data_value_footnote"].isna())]
    df = df[(df["data_value_unit"].notna())]
    df = df[['year_start', 'year_end', 'state_num', 'topic_num', 
        'question_num', 'stratification_id_num', 'stratification_num', 'data_value_unit', 'data_value_type',
        'data_value', 'data_value_alt', 'total', 'Age(years)', 'Education', 'Sex', 'Income']]
    df = df[['year_start', 'year_end', 'state_num', 'topic_num', 
        'question_num', 'stratification_id_num', 'stratification_num', 'data_value_unit',
        'data_value', 'data_value_alt']]


    mod_df = df

    path = "./data/clean/"
    files = [
            "stratification", "stratification_id", "stratificationcatid", "topic", "topicid", "question", "questionid",  "topicid_questionid", 
            "dim_behavior"
            ]

    encode = "utf-8"
    CHUNK_SIZE = 8192

    dataframes = {
        files[0]: stratification_df,
        files[1]: stratificationid_df,
        files[2]: stratificationcatid_df,
        files[3]: topic_df,
        files[4]: topicid_df,
        files[5]: question_df,
        files[6]: questionid_df,
        files[7]: topicid_questionid_df,
        files[8]: mod_df
    }

    for file, df in dataframes.items():
        try:
            df.to_csv(path_or_buf = f"{path}/{file}.csv", header=True, encoding = encode, index = False, chunksize=CHUNK_SIZE)
            print(f"Saved file to {path} as {file}.csv")
        except PermissionError:
            print(f"ERROR - Permission denied, please check if the administrador gave you the correct permissions for this operation.")
        except FileNotFoundError:
            print(f"ERROR - {file} not found, please check the script for possible errors.")
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")
        print("----------------------------")
