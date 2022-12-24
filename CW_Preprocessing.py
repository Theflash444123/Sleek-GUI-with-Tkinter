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
                "name": file,
                "df": pd.read_csv(file_path)
            }
            count += 1
del count

session_headers = ["session/week", "day/date", "time", "session_type", "lab_code"]
first_cols = ["sid", "atd", ""]
for key, value in module_register_dict.items():
    module_register_dict[key]["df_list"] = []
    all_columns = value["df"].columns
    sid = all_columns[0]
    all_sessions = all_columns[1:]
    for session in all_sessions:
        session_details = session.strip().split("\n")
        session_df = value["df"][[sid, session]]
        session_df.rename(columns={sid: "sid", session: "atd"}, inplace=True)
        for i, h in enumerate(session_headers):
            try:
                session_df[h] = session_details[i]
            except:
                session_df[h] = np.NAN
       
        module_register_dict[key]["df_list"].append(session_df)

    combined_df = pd.concat(module_register_dict[key]["df_list"])
    combined_df[["day", "date"]] = combined_df["day/date"].str.split(" ", expand=True)
    combined_df.drop("day/date", axis='columns', inplace=True)
    combined_df[["session", "week"]] = combined_df["session/week"].str.split(".", expand=True)
    combined_df.drop("session/week", axis='columns', inplace=True)
    module_register_dict[key]["combined_df"] = combined_df

    del session_df, all_columns, all_sessions, combined_df








