# IMPORTS
import ntpath
import sqlite3
import pandas as pd
import os
import numpy as np


#########################   DATABASE PREPARATIONS ##################################

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
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                csv_filepaths.append(file_path)
    return csv_filepaths


def get_sessions_from_column(org_df):
    session_details_headers = ["semester_week", "day_date", "time", "session_type", "lab_code"]
    sessions_df = pd.Series(org_df.columns[1:]).str.split(pat="\n", n=-1, expand=True).drop(columns=[5])
    sessions_df = sessions_df.set_axis(session_details_headers, axis=1, inplace=False)
    sessions_df[['semester', 'week']] = sessions_df.semester_week.str.split(pat=".", expand=True)
    sessions_df[['day', 'date']] = sessions_df.day_date.str.split(pat=" ", expand=True)
    sessions_df[['start_time', 'end_time']] = sessions_df.time.str.split(pat="-", expand=True)
    sessions_df = sessions_df[["semester", "week", "day", "date", "time", "session_type", "lab_code"]]
    sessions_df = sessions_df.reset_index().rename(columns={"index": "session_id"})
    return sessions_df


def get_clean_att_df(org_df):
    session_rename_id = pd.Series(org_df.columns[1:])
    session_rename_id = dict((v, k) for k, v in session_rename_id.iteritems())
    clean_df = org_df.rename(columns=session_rename_id)
    clean_df = clean_df.rename(columns={clean_df.columns[0]: "sid"})
    clean_df = clean_df.replace("Ex", np.NAN)
    clean_df = clean_df.replace("GPS", True)
    clean_df = clean_df.replace("X", False)
    clean_df = clean_df.dropna(thresh=1)
    clean_df = clean_df.dropna(axis=1, how="all")
    return clean_df


def get_module_data_csv(csv_filepath):
    org_df = pd.read_csv(csv_filepath)
    module_data = {
        "name": ntpath.basename(csv_filepath)[:-18],
        "clean_df": get_clean_att_df(org_df),
        "sessions_df": get_sessions_from_column(org_df),
    }

    return module_data


def module_data_to_sql(module_data):
    module_name = module_data["name"]
    connection = sqlite3.connect("database.db")
    try:
        module_data["clean_df"].to_sql("att_" + module_name, connection, index=False)
        module_data["sessions_df"].to_sql("sessions_" + module_name, connection, index=False)
    except:
        pass


#########################   DATA TRANSFORMATION ###############################


def wide_to_long(module_data, sid="all"):
    att_df = module_data["att"]
    if not sid == "all":
        att_df = att_df[att_df.sid.isin(sid)]
    sessions_list = att_df.columns[1:]
    long_att_df = pd.DataFrame()
    for session in sessions_list:
        session_att_df = att_df[["sid", session]]
        session_att_df = session_att_df.rename(columns={session: "att"})
        session_att_df["session_id"] = int(session)
        session_att_df["module"] = module_data["name"]
        session_att_df = session_att_df[["module", "session_id", "sid", "att"]]
        long_att_df = pd.concat([long_att_df, session_att_df])

    sessions_df = module_data["sessions"]
    sessions_df = sessions_df[sessions_df.session_id.isin([int(x) for x in long_att_df.session_id])]
    session_att_df = pd.merge(long_att_df, sessions_df, how="outer", on="session_id")

    return session_att_df


#########################   DATABASE QUERIES ##################################


def get_modules_list():
    connection = sqlite3.connect("database.db")
    sql_query = """
    SELECT name FROM sqlite_master  
    WHERE type='table';"""
    cursor = connection.cursor()
    all_tables = cursor.execute(sql_query)
    modules = []
    for t in all_tables:
        table_name = t[0]
        if "att" in table_name:
            modules.append(table_name[4:])

    return modules


def get_sessions_sql(module_name):
    connection = sqlite3.connect("database.db")
    sessions_query = f"SELECT * FROM {'sessions_' + module_name};"
    sessions_df = pd.read_sql(sessions_query, connection)
    return sessions_df


def get_att_sql(module_name):
    connection = sqlite3.connect("database.db")
    att_query = f"SELECT * FROM {'att_' + module_name};"
    att_df = pd.read_sql(att_query, connection)
    return att_df


def get_module_data_sql(module_name):
    sql_data = {
        "name": module_name,
        "att": get_att_sql(module_name),
        "sessions": get_sessions_sql(module_name)
    }
    return sql_data


def get_module_weeks(module_name):
    df = get_sessions_sql(module_name)
    weeks = list(df["week"].unique())
    return weeks

#########################   TESTING  ##################################


if __name__ == "__main__":
    data = {}
    csv_filepaths = get_csv_filepaths("cop504cwdata")
    for filepath in csv_filepaths:
        module_data = get_module_data_csv(filepath)
        # data[module_data["name"]] = module_data
        module_data_to_sql(module_data)
