def clean_diseases():
    import pandas as pd
    from pathlib import Path
    import json

    json_path = "./config/paths.json"
    with open(json_path) as json_file:
        paths = json.load(json_file)

    path = Path(paths["diseases"]["raw"])

    if not path.exists:
        raise FileNotFoundError(f"File {path} was not found.")

    df = pd.read_csv(path)

    df.columns = ['year_start', 'year_end', 'state_abr', 'state_name', 'data_source', 
                'topic', 'question', 'response', 'data_value_unit', 'data_value_type',
                'data_value', 'data_value_alt', 'data_value_footnote_symbol', 
                'data_value_footnote', 'low_confidence_limit', 'high_confidence_limit', 
                'stratification_cat_1', 'stratification_1', 'stratification_cat_2', 
                'stratification_2', 'stratification_cat_3', 'stratification_3', 
                'geolocation', 'location_id', 'topic_id', 'question_id', 'response_id',
                'data_value_type_id', 'stratification_cat_id_1', 'stratification_id_1', 
                'stratification_cat_id_2', 'stratification_id_2',
                'stratification_cat_id_3', 'stratification_id_3']


    filtered_df = df.drop(columns = ["response","response_id","stratification_2","stratification_id_2","stratification_cat_2","stratification_cat_id_2","stratification_3","stratification_id_3","stratification_cat_3","stratification_cat_id_3"])
    filtered_df = filtered_df.drop(columns = ["geolocation", "location_id"])


    filtered_df = filtered_df[filtered_df["data_value_footnote"].isna()]
    filtered_df = filtered_df[filtered_df["data_value"].notna()]
    filtered_df = filtered_df.drop(columns = ["data_value_footnote", "data_value_footnote_symbol"])


    filtered_df = filtered_df[filtered_df["state_abr"].notna()]
    filtered_df = filtered_df[filtered_df["state_abr"] != None]

    filtered_df = filtered_df[filtered_df["state_name"].notna()]
    filtered_df = filtered_df[filtered_df["state_name"] != None]


    #Since most of the data was checked in the analysis section, we may start the creation of files for the dimension tables.
    states_df = filtered_df[["state_name"]].drop_duplicates().sort_values(by=["state_name"]).reset_index()
    states_df["state_num"] = [i for i in range(1,len(states_df) + 1)]
    states_df = states_df[["state_num", "state_name"]]


    #Since most of the data was checked in the analysis section, we may start the creation of files for the dimension tables.
    states_num_df = filtered_df[["state_abr"]].drop_duplicates().sort_values(by=["state_abr"]).reset_index()
    states_num_df["state_num"] = [i for i in range(1,len(states_df) + 1)]
    states_num_df = states_num_df[["state_num", "state_abr"]]


    topic_df = filtered_df[["topic", "topic_id"]].drop_duplicates().sort_values(by=["topic"]).reset_index()
    topic_df["topic_num"] = [i for i in range(1, len(topic_df) + 1)]

    topicid_df = topic_df[["topic_num", "topic_id"]]
    topic_df = topic_df[["topic_num", "topic"]]


    question_df = filtered_df[["question_id", "question"]].drop_duplicates().sort_values(by=["question_id"]).reset_index()
    question_df["question_num"] = [i for i in range(1, len(question_df) + 1)]

    questionid_df = question_df[["question_num", "question_id"]]
    question_df = question_df[["question_num", "question"]]


    topic_question_df = filtered_df[["topic_id", "question_id"]].drop_duplicates().sort_values(by=["topic_id"]).reset_index()
    topic_question_df = topic_question_df[["topic_id", "question_id"]]


    topicid_questionid_df = pd.merge(questionid_df, topic_question_df, how = "inner", on = ["question_id"])
    topicid_questionid_df = pd.merge(topicid_df, topicid_questionid_df, how = "inner", on = ["topic_id"])
    topicid_questionid_df = topicid_questionid_df[["topic_num", "question_num"]]


    datatype_df = filtered_df[["data_value_type_id", "data_value_type"]].drop_duplicates().sort_values(by=["data_value_type_id", "data_value_type"]).reset_index()
    datatype_df["data_value_type_num"] = [i for i in range(1, len(datatype_df) + 1)]

    datatypeid_df = datatype_df[["data_value_type_num", "data_value_type_id"]]
    datatype_df = datatype_df[["data_value_type_num", "data_value_type"]]


    datatypeunit_df = filtered_df[["data_value_unit"]].drop_duplicates().sort_values(by=["data_value_unit"]).reset_index()
    datatypeunit_df["datatypeunit_num"] = [i for i in range(1, len(datatypeunit_df) + 1)]
    datatypeunit_df = datatypeunit_df[["datatypeunit_num", "data_value_unit"]]


    datatype_datatypeunit_df = filtered_df[["data_value_type_id", "data_value_unit"]].drop_duplicates().sort_values(by=["data_value_type_id", "data_value_unit"]).reset_index()
    datatype_datatypeunit_df = pd.merge(datatype_datatypeunit_df, datatypeunit_df, how = "inner", on = ["data_value_unit"])
    datatype_datatypeunit_df = pd.merge(datatype_datatypeunit_df, datatypeid_df, how = "inner", on = ["data_value_type_id"])
    datatype_datatypeunit_df = datatype_datatypeunit_df[["datatypeunit_num", "data_value_type_num"]].sort_values(by = ["datatypeunit_num"])


    stratification_df = filtered_df[["stratification_cat_1", "stratification_cat_id_1"]].drop_duplicates().sort_values(by=["stratification_cat_1", "stratification_cat_id_1"]).reset_index()
    stratification_df["stratification_num"] = [i for i in range(1, len(stratification_df) + 1)]

    stratificationcatid_df = stratification_df[["stratification_num", "stratification_cat_id_1"]]
    stratification_df = stratification_df[["stratification_num", "stratification_cat_1"]]


    stratification_id_df = filtered_df["stratification_id_1"].drop_duplicates().reset_index()
    stratification_id_df["stratification_id_num"] = [i for i in range(1, len(stratification_id_df) + 1)]
    stratification_id_df = stratification_id_df[["stratification_id_num", "stratification_id_1"]]


    stratification_stratification_id_df = filtered_df[["stratification_cat_id_1", "stratification_id_1"]].drop_duplicates().sort_values(by=["stratification_cat_id_1", "stratification_id_1"]).reset_index()
    stratification_stratification_id_df = pd.merge(stratification_stratification_id_df, stratificationcatid_df, how = "inner", on = ["stratification_cat_id_1"])
    stratification_stratification_id_df = pd.merge(stratification_stratification_id_df, stratification_id_df, how = "inner", on = ["stratification_id_1"])

    stratification_stratification_id_df = stratification_stratification_id_df[["stratification_num", "stratification_id_num"]]


    # ## Modifying the original df
    # In order to save storage, many columns on the "filtered_df" could have int as its data type. This what this section aims to do.
    mod_df = filtered_df


    mod_df = pd.merge(mod_df, states_num_df, how = "inner", on=["state_abr"])


    mod_df = mod_df[['year_start', 'year_end', 'state_num', 'data_source',
        'topic', 'question', 'data_value_unit', 'data_value_type', 'data_value',
        'data_value_alt', 'low_confidence_limit', 'high_confidence_limit',
        'stratification_cat_1', 'stratification_1', 'topic_id', 'question_id',
        'data_value_type_id', 'stratification_cat_id_1', 'stratification_id_1'
        ]]


    mod_df = pd.merge(mod_df, topicid_df, how = "inner", on=["topic_id"])


    mod_df = mod_df[['year_start', 'year_end', 'state_num', 'data_source', 'topic_num',
        'question', 'data_value_unit', 'data_value_type', 'data_value',
        'data_value_alt', 'low_confidence_limit', 'high_confidence_limit',
        'stratification_cat_1', 'stratification_1', 'question_id',
        'data_value_type_id', 'stratification_cat_id_1', 'stratification_id_1']]


    mod_df = pd.merge(mod_df, questionid_df, how = "inner", on = ["question_id"])


    mod_df = mod_df[['year_start', 'year_end', 'state_num', 'data_source', 'topic_num',
        'question_num', 'data_value_unit', 'data_value_type', 'data_value',
        'data_value_alt', 'low_confidence_limit', 'high_confidence_limit',
        'stratification_cat_1', 'stratification_1',
        'data_value_type_id', 'stratification_cat_id_1', 'stratification_id_1']]


    mod_df = pd.merge(mod_df, datatypeid_df, how = "inner", on = ["data_value_type_id"])


    mod_df = mod_df[['year_start', 'year_end', 'state_num', 'data_source', 'topic_num',
        'question_num', 'data_value_unit', 'data_value_type_num', 'data_value',
        'data_value_alt', 'low_confidence_limit', 'high_confidence_limit',
        'stratification_cat_1', 'stratification_1',
        'stratification_cat_id_1', 'stratification_id_1']]


    mod_df = pd.merge(mod_df, datatype_datatypeunit_df, how = "inner", on = ["data_value_type_num"])


    mod_df = mod_df[['year_start', 'year_end', 'state_num', 'data_source', 'topic_num',
        'question_num', 'datatypeunit_num', 'data_value_type_num', 'data_value',
        'data_value_alt', 'low_confidence_limit', 'high_confidence_limit',
        'stratification_cat_1', 'stratification_1', 'stratification_cat_id_1',
        'stratification_id_1']]


    mod_df = pd.merge(mod_df, stratification_df, how = "inner", on = ["stratification_cat_1"])


    mod_df = mod_df[[
        'year_start', 'year_end', 'state_num', 'data_source', 'topic_num',
        'question_num', 'datatypeunit_num', 'data_value_type_num', 'stratification_num', 'data_value',
        'data_value_alt', 'low_confidence_limit', 'high_confidence_limit',
        'stratification_1','stratification_id_1'
        ]]


    mod_df = pd.merge(mod_df, stratification_id_df, how = "inner", on = ["stratification_id_1"])


    mod_df = mod_df[[
        'year_start', 'year_end', 'state_num', 'data_source', 'topic_num',
        'question_num', 'datatypeunit_num', 'data_value_type_num',
        'stratification_num', 'stratification_id_num', 'data_value', 'data_value_alt',
        'low_confidence_limit', 'high_confidence_limit'
        ]]


    path = "./data/clean/"
    files = [
            "topic", "topicid", "question", "questionid", "topic_question", "topicid_questionid", "datatype", "datatypeid", 
            "datatypeunit", "datatype_datatypeunit", "stratification", "stratification_id", "stratificationcatid", "stratification_stratification_id",
            "dim_disease"
            ]

    encode = "utf-8"
    CHUNK_SIZE = 8192


    dataframes = {
        files[0]: topic_df,
        files[1]: topicid_df,
        files[2]: question_df,
        files[3]: questionid_df,   
        files[4]: topic_question_df,
        files[5]: topicid_questionid_df,
        files[6]: datatype_df,
        files[7]: datatypeid_df,
        files[8]: datatypeunit_df,
        files[9]: datatype_datatypeunit_df,
        files[10]: stratification_df,
        files[11]: stratification_id_df,
        files[12]: stratificationcatid_df,
        files[13]: stratification_stratification_id_df,
        files[14]: mod_df
    }


    for file, df in dataframes.items():
        try:
            df.to_csv(path_or_buf = f"{path}/{file}.csv", header=True, encoding = encode, index = False, chunksize=CHUNK_SIZE)
            print(f"Saved file to {path} as {file}.csv")
        except ValueError as error:
            print(f"Couldn't save {file}.csv to {path}, the following error occurred:\n{error}")
        print("----------------------------")

    print("\n***Now processing seeds for dbt...***\n")

    seeds_path = "./dbt/seeds/"
    seeds = [
            "states", "states_num"
            ]

    seed_dataframes = {
        seeds[0]: states_df,
        seeds[1]: states_num_df
    }

    for seed, df in seed_dataframes.items():
        try:
            df.to_csv(path_or_buf = f"{seeds_path}/{seed}.csv", header=True, encoding = encode, index = False, chunksize=CHUNK_SIZE)
            print(f"Saved file to {seeds_path} as {seed}.csv")
        except PermissionError:
            print(f"ERROR - Permission denied, please check if the administrador gave you the correct permissions for this operation.")
        except FileNotFoundError:
            print(f"ERROR - {file} not found, please check the script for possible errors.")
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")
        print("----------------------------")
