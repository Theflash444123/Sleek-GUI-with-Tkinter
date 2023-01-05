# IMPORTS
import ntpath
import sqlite3
import pandas as pd
import os
import numpy as np

# DATAFRAME PREPARATIONS


def get_csv_filepaths(data_folder_name):
    """
    This function is to get all the file paths of the csv files present inside the data folder, so that the user can know
    how many modules data is present inside the data folder.
    :param data_folder_name: Name of the folder in which the csv files are kept.
    :return: return a list containing absolute filepaths of all the CSV's present inside data folder.
    """
    csv_filepaths = []
    for root, dirs, files in os.walk(os.path.abspath(data_folder_name)):
        for file in files:
            module_name = file[:-18]
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                csv_filepaths.append(file_path)
    return csv_filepaths


def get_module_data(csv_filepath):
    module_data = {}

    session_details_headers = ["semester_week", "day_date", "time", "session_type", "lab_code"]
    org_df = pd.read_csv(csv_filepath)
    sessions_df = pd.Series(org_df.columns[1:]).str.split(pat="\n", n=-1, expand=True).drop(columns=[5])
    sessions_df = sessions_df.set_axis(session_details_headers, axis=1, copy=False)
    sessions_df[['semester', 'week']] = sessions_df.semester_week.str.split(pat=".", expand=True)
    sessions_df[['day', 'date']] = sessions_df.day_date.str.split(pat=" ", expand=True)
    sessions_df = sessions_df.drop(columns=["semester_week", "day_date"])
    sessions_df = sessions_df[["semester", "week", "day", "date", "time", "session_type", "lab_code"]]
    sessions_df = sessions_df.reset_index().rename(columns={"index": "session_id"})

    session_rename_id = pd.Series(org_df.columns[1:])
    session_rename_id = dict((v, k) for k, v in session_rename_id.iteritems())
    clean_df = org_df.rename(columns=session_rename_id)
    clean_df = clean_df.replace("Ex", np.NAN)
    clean_df = clean_df.replace("GPS", True)
    clean_df = clean_df.replace("X", False)
    clean_df = clean_df.dropna(thresh=1)

    module_data["name"] = ntpath.basename(csv_filepath)[:-18]
    module_data["clean_df"] = clean_df
    module_data["sessions_df"] = sessions_df

    return module_data


def module_data_to_sql(module_data):
    module_name = module_data["name"]
    connection = sqlite3.connect("database.db")
    module_data["clean_df"].to_sql(module_name + "_atd", connection)
    module_data["sessions_df"].to_sql(module_name + "_sessions", connection)


if __name__ == "__main__":
    data = {}
    csv_filepaths = get_csv_filepaths("cop504cwdata")
    for filepath in csv_filepaths:
        module_data = get_module_data(filepath)
        data[module_data["name"]] = module_data

# df = data["22COA122"]["sessions_df"]
# a = df.groupby(["week", "day", "session_type"])
# df = df[df.session_type=="Computer Lab"]
# a = df.groupby(["week", "day"])
#
# for i in a:
#     print(i[1].session_id)








