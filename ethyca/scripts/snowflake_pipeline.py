"""
Move data from the CSV files into a Snowflake instance.
"""
from os import environ as env
from typing import Dict, List

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

FOLDERS_TO_LOAD = ["fides", "fideslang", "fidesops"]
FILES_TO_LOAD = ["forks", "stargazers", "views_clones_aggregate"]


def get_snowflake_engine() -> Engine:
    "Build a snowflake sqlalchemy connection."
    connection_string = env["SNOWFLAKE_CONN_STR"]
    engine = create_engine(connection_string)
    return engine


def upload_csv_files(engine: Engine):
    """
    Uploads CSV files into Snowflake.

    Also adds a "source" column to each dataframe before uploading
    """
    for folder_name in FOLDERS_TO_LOAD:
        for file_name in FILES_TO_LOAD:
            print("------")
            file_path = f"../{folder_name}/ghrs-data/{file_name}.csv"
            print(f"Loading {file_path}...")
            csv_df = pd.read_csv(f"../{folder_name}/ghrs-data/{file_name}.csv")
            csv_df["source"] = folder_name
            print(f"Uploading file to table: {file_name}")
            csv_df.to_sql(file_name, engine, if_exists="append", index=False)


if __name__ == "__main__":
    engine = get_snowflake_engine()
    upload_csv_files(engine)
