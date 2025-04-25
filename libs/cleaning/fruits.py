def clean_fruits():
    import pandas as pd
    from pathlib import Path
    import json

    json_path = "./config/paths.json"
    with open(json_path) as json_file:
        paths = json.load(json_file)
        
    filepath = Path(paths["fruits"]["raw"])

    if not filepath.exists():
        raise FileNotFoundError(f"File {filepath} was not found.")

    CHUNK_SIZE = 8192
    encode = "utf-8"

    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"FileNotFoundError: File {filepath} was not found.")

    df.columns = ['fruit', 'form', 'retail_price', 'retail_price_unit', 'yield','cup_equivalent_size', 'cup_equivalent_unit', 'cup_equivalent_price']

    zeroes = (df["retail_price"] == 0).sum()
    negative = (df["retail_price"] < 0).sum()
    nones = (df["retail_price"] == None).sum()
    distinct_units = pd.Series(df["retail_price_unit"]).unique()
    no_names = pd.Series(df["fruit"] == None).sum()

    sum_errors = zeroes + negative + nones + no_names
    units_qt = len(distinct_units)

    print(f"\nNumber of zeroes in the file: {zeroes}.")
    print(f"Number of negative values in the file: {negative}.")
    print(f"Number of None values in the file: {nones}.")
    print(f"Number of distinct units: {units_qt}. The expected value is 2.")
    print(f"Number of fruits missings: {no_names}. Expected value is 0\n")


    try:
        if(sum_errors != 0 or units_qt != 2):
            raise ValueError("some of the data is wrong. Please check if the cleaning is working correctly.\n")
        df.to_csv("./data/clean/fruits_prices.csv", header=True, chunksize=CHUNK_SIZE, index = False, encoding=encode)
        print("Cleaning done succefully, please check it at ./data/clean/\n")
    except PermissionError:
        print(f"ERROR - Permission denied, please check if the administrador gave you the correct permissions for this operation.")
    except FileNotFoundError:
        print(f"ERROR - file not found, please check the script for possible errors.")
    except Exception as e:
        print(f"An unexpected error has occurred: {e}")
