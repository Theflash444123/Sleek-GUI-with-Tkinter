import sqlite3
import pandas as pd
import os
import numpy as np

"""
code for browsing through all the files in cop504cwdata, all the files with .csv extension will be read and the 
details will be stored in a dictionary module_atd_register_dict

The details include:
module_name: this is obtained from the file name 
org_df: This is the dataframe in its raw format, as given in csv file.

Further details will be stored in this dictionary after processing the org_df.
"""
count = 0
module_atd_register_dict = {}
for root, dirs, files in os.walk(os.path.abspath("cop504cwdata")):
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(root, file)
            org_df = pd.read_csv(file_path)

            module_atd_register_dict[count] = {
                "module_name": file[:-18],
                "org_df": org_df
            }
            count += 1
del count

session_details_headers = ["semester", "week", "day", "date", "time", "session_type", "lab_code"]

module_details = {
    "module_id": [],
    "module_name": []
}

for module_id, module_data in module_atd_register_dict.items():
    module_details["module_id"].append(module_id)
    module_details["module_name"].append(module_data["module_name"])
    """
    all_sessions_details_df: This dataframe will store all the details of the sessions that we have obtained after 
    breaking down the header from the original data.For each session the values will be appended to this dataframe.
    
    all_session_atd_df_list: this is list that will be appended with the attendance details of each session and later on 
    all the individual dataframes of session will be combined to get a concatenated dataframe.
    """
    all_sessions_details_df = pd.DataFrame(columns=session_details_headers)
    all_sessions_atd_df_list = []
    org_df_columns = module_data["org_df"].columns
    sid = org_df_columns[0]
    all_sessions = org_df_columns[1:]

    session_id = 1

    for session in all_sessions:
        session_details = session.strip().split("\n")
        session_week = session_details[0].strip().split(".")
        day_date = session_details[1].strip().split(" ")

        session_details_dict = {
            "module_id": module_id,
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

        session_atd_df = module_data["org_df"][[sid, session]]
        session_atd_df.rename(columns={sid: "student_id", session: "atd"}, inplace=True)
        session_atd_df["session_id"] = int(session_id)
        all_sessions_atd_df_list.append(session_atd_df)

        session_id += 1

    all_sessions_combined_atd_df = pd.concat(all_sessions_atd_df_list)
    all_sessions_combined_atd_df["module_id"] = int(module_id)
    all_sessions_combined_atd_df = all_sessions_combined_atd_df[["student_id", "module_id", "session_id", "atd"]]

    module_atd_register_dict[module_id]["combined_atd_df"] = all_sessions_combined_atd_df
    module_atd_register_dict[module_id]["session_details"] = all_sessions_details_df

"""
module_details_df: This is the dataframe containing the details of the modules.
session_df: 
atd_df: 
"""
module_details_df = pd.DataFrame(module_details)
session_df = pd.DataFrame()
atd_df = pd.DataFrame()
for module in module_atd_register_dict.values():
    print(module)
    session_df = pd.concat([session_df, module["session_details"]])
    atd_df = pd.concat([atd_df, module["combined_atd_df"]])


# Creating SQL data base and creating tables
connection = sqlite3.connect("CWDatabase.db")
module_details_df.to_sql("module_details", connection)
session_df.to_sql("session_details", connection)
atd_df.to_sql("attendance_details", connection)











