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
del count

session_details_headers = ["semester", "week", "day", "date", "time", "session_type", "lab_code"]

module_details = {
    "module_id": [],
    "module_name": []
}

for key, value in module_register_dict.items():
    module_details["module_id"].append(key)
    module_details["module_name"].append(value["module_name"])

    all_sessions_details_df = pd.DataFrame(columns=session_details_headers)
    all_sessions_atd_df_list = []
    org_df_columns = value["org_df"].columns
    sid = org_df_columns[0]
    all_sessions = org_df_columns[1:]

    session_id = 1

    for session in all_sessions:
        session_details = session.strip().split("\n")
        session_week = session_details[0].strip().split(".")
        day_date = session_details[1].strip().split(" ")

        session_details_dict = {
            "module_id": key,
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
        all_sessions_details_df[["module_id", "session_id"]] = all_sessions_details_df[["module_id", "session_id"]].astype(int)
        all_sessions_details_df = all_sessions_details_df[["module_id", "session_id"] + session_details_headers]

        session_atd_df = value["org_df"][[sid, session]]
        session_atd_df.rename(columns={sid: "student_id", session: "atd"}, inplace=True)
        session_atd_df["session_id"] = int(session_id)
        all_sessions_atd_df_list.append(session_atd_df)

        session_id += 1

    all_sessions_combined_atd_df = pd.concat(all_sessions_atd_df_list)
    all_sessions_combined_atd_df["module_id"] = int(key)
    all_sessions_combined_atd_df = all_sessions_combined_atd_df[["student_id", "module_id", "session_id", "atd"]]

    module_register_dict[key]["combined_atd_df"] = all_sessions_combined_atd_df
    module_register_dict[key]["session_details"] = all_sessions_details_df

module_details_df = pd.DataFrame(module_details)

pre_processed_data = {}

session_df = pd.DataFrame()
atd_df = pd.DataFrame()
for module in module_register_dict.values():
    print(module)
    session_df = pd.concat([session_df, module["session_details"]])
    atd_df = pd.concat([atd_df, module["combined_atd_df"]])
    










