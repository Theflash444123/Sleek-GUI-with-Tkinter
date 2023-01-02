import sqlite3
import pandas as pd
import os
import numpy as np

# keeping all the raw dataframes in a dictionary
module_register_dict = {}
for root, dirs, files in os.walk(os.path.abspath("cop504cwdata")):
    for file in files:
        module_name = file[:-18]
        if file.endswith(".csv"):
            file_path = os.path.join(root, file)
            module_register_dict[module_name] = {
                "org_df": pd.read_csv(file_path)
            }
del root, dirs, files, file, file_path

session_details_headers = ["semester_week", "day_date", "time", "session_type", "lab_code"]

for module_key, module_data in module_register_dict.items():

    org_df = module_data["org_df"]
    session_rename_id = pd.Series(org_df.columns[1:])
    session_rename_id = dict((v, k) for k, v in session_rename_id.iteritems())
    sessions_df = pd.Series(org_df.columns[1:]).str.split(pat="\n", n=-1, expand=True).drop(columns=[5])
    sessions_df = sessions_df.set_axis(session_details_headers, axis=1, copy=False)
    sessions_df[['semester', 'week']] = sessions_df.semester_week.str.split(pat=".", expand=True)
    sessions_df[['day', 'date']] = sessions_df.day_date.str.split(pat=" ", expand=True)
    sessions_df = sessions_df.drop(columns=["semester_week", "day_date"])
    sessions_df = sessions_df[["semester", "week", "day", "date", "time", "session_type", "lab_code"]]

    clean_df = module_data["org_df"].rename(columns=session_rename_id)
    clean_df = clean_df.replace("Ex", np.NAN)
    clean_df = clean_df.replace("GPS", True)
    clean_df = clean_df.replace("X", False)
    module_data["clean_df"] = clean_df
    module_data["sessions_df"] = sessions_df

connection = sqlite3.connect("database.db")








