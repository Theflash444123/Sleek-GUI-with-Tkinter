import sqlite3
import pandas as pd
import os
import numpy as np

# keeping all the raw dataframes in a dictionary
count = 0
module_register_dict = {}
for root, dirs, files in os.walk(os.path.abspath("cop504cwdata")):
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(root, file)
            module_register_dict[count] = {
                "module_name": file[:-18],
                "org_df": pd.read_csv(file_path)
            }
            count += 1
del count, root, dirs, files, file, file_path

session_details_headers = ["module", "session_id", "semester", "week", "day", "date", "time", "session_type", "lab_code"]

for module_key, module_data in module_register_dict.items():

    all_sessions_details_df = pd.DataFrame(columns=session_details_headers)
    org_df_columns = module_data["org_df"].columns
    sid = org_df_columns[0]
    all_sessions = org_df_columns[1:]

    session_id = 1
    session_rename_dict = {sid: "sid"}
    for session in all_sessions:
        session_rename_dict[session] = session_id
        session_details = session.strip().split("\n")
        session_week = session_details[0].strip().split(".")
        day_date = session_details[1].strip().split(" ")

        session_details_dict = {
            "module": module_data["module_name"],
            "session_id": session_id,
            "semester": session_week[0],
            "week": session_week[1],
            "day": day_date[0],
            "date": day_date[1][1:-1],
            "time": session_details[2],
            "session_type": session_details[3],
            "lab_code": session_details[4] if len(session_details) == 5 else None

        }

        all_sessions_details_df = all_sessions_details_df.append(session_details_dict, ignore_index=True)
        all_sessions_details_df[["session_id"]] = all_sessions_details_df[["session_id"]].astype(int)

        session_id += 1

    preprocessed_df = module_data["org_df"].rename(columns=session_rename_dict)
    preprocessed_df = preprocessed_df.dropna(axis=1, how='all')
    preprocessed_df = preprocessed_df.replace("Ex", np.NAN)
    preprocessed_df = preprocessed_df.replace("GPS", True)
    preprocessed_df = preprocessed_df.replace("X", False)
    module_data["preprocessed_df"] = preprocessed_df
    module_data["session_details"] = all_sessions_details_df


pre_processed_data = {}

session_df = pd.DataFrame()
for module in module_register_dict.values():
    session_df = pd.concat([session_df, module["session_details"]])

# connection = sqlite3.connect("database.db")
# preprocessed_df.to_sql("cleaned_df", connection)
# session_df.to_sql("session_df", connection)
#
# df2 = pd.read_sql_query("SELECT * FROM cleaned_df", connection)
#








