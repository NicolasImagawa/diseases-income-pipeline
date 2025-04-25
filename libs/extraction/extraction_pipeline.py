def extract_data(url, output):
    import requests
    from pathlib import Path

    url = url
    TIMEOUT = 5
    CHUNK_SIZE = 8192 #8 kB

    response = requests.get(url, timeout = TIMEOUT)
    response.raise_for_status()

    output_path = Path(f"{output}")

    with open(output_path, 'wb') as f:
        try:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
            print(f"File behavior.csv successfully written to {output_path}")
        except requests.exceptions.Timeout:
            print(f"Timeout after {TIMEOUT} seconds. Please check if the extraction path stills exists and if it's online.")
        except FileNotFoundError:
            print(f"File not found, please check the given path.")
        except PermissionError:
            print(f"Permission denied, please check if the administrador gave you the correct permissions for this operation.")
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")
        print("----------------------------")