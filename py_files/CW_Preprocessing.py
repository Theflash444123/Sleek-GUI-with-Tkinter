# IMPORTS
import ntpath
import sqlite3
import pandas as pd
import os
import numpy as np


#########################   DATABASE PREPARATIONS ##############################


def get_csv_filepaths(data_folder_name):
    """
    This function returns a list of file paths for all CSV files present inside
    the specified folder.

    parameters:
    data_folder_name(str): Name of the folder in which the csv files are kept.

    returns:
    list: A list containing absolute filepaths of all the CSV's present inside
    specified folder.
    """
    csv_filepaths = []
    for root, dirs, files in os.walk(os.path.abspath(data_folder_name)):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                csv_filepaths.append(file_path)
    return csv_filepaths


def get_modules_list():
    """
    This function returns a list of modules present in sql database.
    """
    connection = sqlite3.connect("CWDatabase.db")
    sql_query = """
    SELECT name FROM sqlite_master  
    WHERE type='table'"""
    cursor = connection.cursor()
    all_tables = cursor.execute(sql_query)
    modules = []
    for t in all_tables:
        table_name = t[0]
        if "att" in table_name:
            modules.append(table_name[4:])
    connection.close()
    return modules


class RawData:
    """
    This class provides methods for processing and storing raw data. It includes
    methods for cleaning, transforming, and storing data to SQL Database.
    """
    def __init__(self, filepath, database="CWDatabase.db"):
        self.database_name = database
        self.filepath = filepath
        self.raw_df = pd.read_csv(self.filepath)
        self.module_name = ntpath.basename(self.filepath)[:-18]

    def extract_sessions(self):
        """
        Extract session details from column
        """
        session_details_headers = ["semester_week", "day_date",
                                   "time", "session_type",
                                   "lab_code"]
        sessions_df = pd.Series(self.raw_df.columns[1:]
                                ).str.split(pat="\n",
                                            n=-1,
                                            expand=True
                                            ).drop(columns=[5])

        sessions_df = sessions_df.set_axis(session_details_headers,
                                           axis=1,
                                           inplace=False)
        sessions_df[[
            'semester',
            'week']] = sessions_df.semester_week.str.split(pat=".", expand=True)
        sessions_df[[
            'day',
            'date']] = sessions_df.day_date.str.split(pat=" ", expand=True)
        sessions_df[[
            'start_time',
            'end_time']] = sessions_df.time.str.split(pat="-", expand=True)
        sessions_df = sessions_df[[
            "semester", "week", "day", "date",
            "time", "session_type", "lab_code"]]
        sessions_df = sessions_df.reset_index().rename(
            columns={"index": "session_id"})
        return sessions_df

    def clean(self):
        """
        clean raw data
        """
        session_rename_id = pd.Series(self.raw_df.columns[1:])
        session_rename_id = dict((v, k) for k, v in session_rename_id.iteritems())
        clean_df = self.raw_df.rename(columns=session_rename_id)
        clean_df = clean_df.rename(columns={clean_df.columns[0]: "sid"})
        clean_df = clean_df.replace("Ex", np.NAN)
        clean_df = clean_df.replace("GPS", True)
        clean_df = clean_df.replace("X", False)
        clean_df = clean_df.dropna(how="all", subset=clean_df.columns[1:])
        clean_df = clean_df.dropna(axis=1, how="all")
        return clean_df

    def to_sql_db(self, replace=False):
        """
        For transferring the clean data and the session details to sql database
        """
        connection = sqlite3.connect(self.database_name)
        clean_df = self.clean()
        sessions_df = self.extract_sessions()

        try:
            att_dtype = {f"{col}": "BOOLEAN" for col in clean_df.columns[1:]}
            att_dtype["sid"] = "INTEGER"
            clean_df.to_sql(
                "att_" + self.module_name,
                connection,
                index=False,
                dtype=att_dtype
            )
            sessions_df.to_sql(
                "sessions_" + self.module_name,
                connection,
                index=False
            )

        except:
            if replace is True:
                print(f"Replacing{self.module_name}")
                clean_df.to_sql(
                    "att_" + self.module_name,
                    connection,
                    index=False,
                    if_exists='replace'
                )

                sessions_df.to_sql(
                    "sessions_" + self.module_name,
                    connection,
                    index=False,
                    if_exists='replace'
                )
            else:
                pass

        connection.close()


class ModuleRecord:
    """
    This class provides methods for processing data from a SQL database.
    It includes methods for querying, and transforming data.

    Parameters:
        module_name: Name of the module
    """
    def __init__(self, module_name, database="CWdatabase.db"):
        self.database_name = database
        self.module_name = module_name
        self.sessions = self.get_sessions_sql()
        self.att = self.get_att_sql()

    def get_sessions_sql(self):
        """
        get sessions table as a pandas dataframe
        """
        connection = sqlite3.connect(self.database_name)
        sessions_query = f"SELECT * FROM {'sessions_' + self.module_name}"
        sessions_df = pd.read_sql(sessions_query, connection)
        connection.close()
        return sessions_df

    def get_att_sql(self):
        """
        get attendance table as a pandas dataframe
        """
        connection = sqlite3.connect(self.database_name)
        att_query = f"SELECT * FROM {'att_' + self.module_name}"
        att_df = pd.read_sql(att_query, connection)
        connection.close()
        return att_df

    def week_list(self):
        """
        get list of weeks for selected module
        """
        df = self.sessions
        weeks = list(df["week"].unique())
        return weeks

    def wide_to_long(self, sid="all"):
        """
        This function transforms the attendance table and sessions table into
        a single dataframe to make the analysis easy in pandas because pandas
        is not relational.
        """
        att_df = self.att
        if not sid == "all":
            att_df = att_df[att_df.sid.isin(sid)]
        sessions_list = att_df.columns[1:]
        long_att_df = pd.DataFrame()
        for session in sessions_list:
            session_att_df = att_df[["sid", session]]
            session_att_df = session_att_df.rename(columns={session: "att"})
            session_att_df["session_id"] = int(session)
            session_att_df["module"] = self.module_name
            session_att_df = session_att_df[["module",
                                             "session_id",
                                             "sid",
                                             "att"]]
            long_att_df = pd.concat([long_att_df, session_att_df])

        sessions_df = self.sessions
        sessions_df = sessions_df[sessions_df.session_id.isin(
            [int(x) for x in long_att_df.session_id])]
        long_df = pd.merge(long_att_df, sessions_df,
                           how="outer",
                           on="session_id")

        return long_df


def cw_preprocessing_main(replace=False):
    csv_filepaths = get_csv_filepaths("cop504cwdata")
    for filepath in csv_filepaths:
        RawData(filepath).to_sql_db(replace=replace)

#########################   TESTING  ##################################


if __name__ == "__main__":
    cw_preprocessing_main()
