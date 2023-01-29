#Created by: Nikhil Polpakkara
import pandas as pd
import sqlite3
import os
from os import listdir
import numpy as np
from tkinter import filedialog

filepath = r"C:\Users\Admin\OneDrive - Loughborough University\Loughborough Uni\Programming for datascience\Coursework\dataset"

def color_cells(val):
    """
    This function returns a color based on a specific value

    Parameters
    ----------
    val :   float
            Value based on which the color has to be rturned

    Returns
    -------
    str :   Color hex code as a string

    """
    if isinstance(val, (int, float)):
        if val < 50:
            return '#B81D13'
        elif val >= 50 and val<80:
            return '#EFB700'
        elif val >=80:
            return '#008450'
        else:
            return '#e7e5e6'
    else:
        return '#e7e5e6'

def sql_tables(db ="CWDatabase.db"):
    """
    This function connects with a database to retrieve the modules,tables\
    and sqllite3 connection for further operation

    Parameters
    ----------
    db : str, optional
        Name of the database to connect to. The default is "CWDatabase.db".

    Returns
    -------
    table_list : list
        List of tables in the database.
    modules : list
        Module names in the database..
    connection : sqlite3.Connection
        
    """
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor.execute(sql_query)
    table_list = cursor.fetchall()
    modules = []
    for i in range(0,len(table_list),2):
        modules.append(table_list[i][0][-8:])
    
    return table_list, modules ,connection
    connection.close()

def module_data():
    """
    Returns the list of students and weeks available in the database.
    Can be expanded to retrieve other module attributes

    Returns
    -------
    student_list : dictionary
        Data containing Student ID for each module.
    week_list : dictionary
        Data containing Week number for each module.

    """
    table_list,modules,connection = sql_tables()
    student_list = {}
    week_list = {}
    for module in modules:
        sql_query1 = f"SELECT Student_ID FROM att_{module}"
        sql_query2 = f"SELECT Week FROM session_{module}"
        df_attendance = pd.read_sql_query(sql_query1,connection)
        df_session = pd.read_sql_query(sql_query2,connection)
        student_list[module] = list(df_attendance["Student_ID"].unique())
        week_list[module] = list(df_session["Week"].unique())
    
    return student_list , week_list
    connection.close()


def data_to_update(path = filepath):
    """
    This function returns the filenames of the data of specific module that
    is not currently available in the database need to be updated

    Parameters
    ----------
    path : str, optional
        Filepath containing the location of raw data which needs to be
        updated to the database. The default is filepath.

    Returns
    -------
    filenames : str
        Filenames to be processed and updated to the SQLlite database.

    """
    
    filenames = listdir(path)
    files = [path+"\\"+filename for filename in filenames\
             if filename.endswith(".csv")]
    existing_modules = sql_tables()[1]
    
    filenames = []
    for file in files:
        if os.path.basename(file)[:8] not in existing_modules:
            filenames.append(file)
            
    return filenames
    
    

def data_cleaning(path):
    """
    This function reads the csv file and cleans the raw data from the csv file and update the data
    into sqllite database

    Parameters
    ----------
    path : str
        complete filename.

    Returns
    -------
    df_final_cleaned : pandas dataframe
        Cleaned dataset containing Student's attendance 
    df_session : pandas dataframe
        Cleaned dataset containing session details of the module
    name : str
        Module name.

    """    
    
    name = os.path.basename(path)[:8]
    df_raw = pd.read_csv(path)
    
    df_cleaned = df_raw.set_index(df_raw.columns[0])
    # df_cleaned = df_cleaned.T
    df_cleaned = df_cleaned.replace("Ex",np.nan)    # replacing the attendance
    df_cleaned.replace("GPS", True ,inplace = True) # with boolean and nan
    df_cleaned.replace("X", False ,inplace = True)
    df_cleaned = df_cleaned.dropna(axis = 1, how = "all") # removing rwos and
    df_cleaned = df_cleaned.dropna(axis = 0, how = "all") # columns with all Nan values

    # Creating a new sessions dataframe to link cleaned dataframe columns
    # with session details
    
    df_session = pd.DataFrame(list(df_cleaned.columns))
    df_session = df_session[0].str.split("\n",expand=True)
    df_session[["Day","Date"]] = df_session[1].str.split(expand=True)
    df_session[["Start_time",2,"End_time"]] = \
                                        df_session[2].str.split(expand=True)
    df_session[["Semester","Week"]] = \
                    df_session[0].apply(lambda x: pd.Series(str(x).split(".")))
    df_session["Semester"] = \
        df_session["Semester"].apply( \
                                    lambda x: pd.Series(str(x)[1])).astype(int)
    df_session["Week"] = df_session["Week"].apply(\
                                    lambda x: pd.Series(str(x)[1])).astype(int)
    df_session["Date"] = df_session["Date"].apply(lambda x: pd.Series(x[1:-1]))
    col_dict = {3:"Class",4:"Room"}
    df_session.rename(columns= col_dict,inplace = True)
    df_session.index.name = "Session_id"
    df_session = df_session.drop([0,1,2,5], axis = 1)
    df_cleaned.columns = list(range(0,len(df_session)))
    df_cleaned = df_cleaned.T
    df_cleaned.reset_index(inplace=True)
    df_cleaned.columns.values[0] = "Session_id"
    
    df_cleaned = pd.melt(df_cleaned,
                               id_vars="Session_id",
                               value_vars=df_cleaned.columns[1:])
    df_cleaned.columns.values[1] = "Student_ID"
    df_cleaned.columns.values[2] = "Attendance"

    
    return ( df_cleaned,df_session,name)

def df_to_sql_table(df_cleaned,df_session,name):
    """
    Converts the cleaned dataframes into sql table and updates it
    into the database

    Parameters
    ----------
    df_cleaned : pandas dataframe
        Cleaned dataset containing Student's attendance. 
    df_session : pandas dataframe
        Cleaned dataset containing session details of the module.
    name : str
        Module name.

    Returns
    -------
    None.

    """
    
    connection = sqlite3.connect("CWDatabase.db")
    att = str("att_"+name)
    session = str("session_"+name)
    att_dtype = {"index": "INTEGER",
                 "Session_id": "INTEGER",
                 "Student_ID": "INTEGER",
                 "Attendance":"BOOLEAN"}
    session_dtype = {"Session_id": "INTEGER",
                     "Class":"VARCHAR(20)",
                     "Room":"VARCHAR(20)",
                     "Day":"VARCHAR(20)",
                     "Date":"DATE",
                     "Start_time":"DATETIME",
                     "End_time":"VARCHAR(20)",
                     "Semester":"INTEGER",
                     "Week":"INTEGER"}
    df_cleaned.to_sql(att,connection,if_exists = 'replace',
                      dtype= att_dtype)
    df_session.to_sql(session,connection,
                      if_exists = 'replace',dtype=session_dtype)

    # cursor.close()
    connection.close()

def add_data():
    """
    Prompts the user to select a specific file from the computer to be updated
    into the sql database.
    This function will replace the data in the database for the specific
    module even if it is already existing in the database.

    Returns
    -------
    name_list : TYPE
        DESCRIPTION.

    """
    
    files = filedialog.askopenfilename(title  =
                                       "Enter the csv files for each module", 
                                       #title = "File Selection",
                                       filetypes = [("CSV files", "*.csv")],
                                       multiple = True)
    if len(files) == 0:
        name_list = False
    else:
        name_list = []
        for file in files:
            name = os.path.basename(file)[:8]
            name_list.append(name)
        for file in files:
            df1,df2,name = data_cleaning(file)
            df_to_sql_table(df1,df2,name)
        else:
            print("DATABASE UPTO DATE")
    
    return name_list

def sql_data(module,db ="CWDatabase.db"):
    connection = sqlite3.connect(db)
    if module in sql_tables()[1]:
        sql_query1 = f"SELECT * FROM att_{module};"
        sql_query2 = f"SELECT * FROM session_{module};"
        df_st_att = pd.read_sql_query(sql_query1,connection)
        df_session = pd.read_sql_query(sql_query2,connection)
        return df_st_att, df_session

def data_processing():
    """
    This function runs the data cleaning and processing for files present in
    the raw data storing folder which are not updated in the database

    Returns
    -------
    name_list : list
        List containing names of modules updated into the database.

    """
    
    files = data_to_update()
    for file in files:
        df1,df2,name = data_cleaning(file)
        df_to_sql_table(df1,df2,name)
    
    name_list = []
    for file in files:
        name = os.path.basename(file)[:8]
        name_list.append(name)
    
    return name_list

# if __name__ == "__main__":
#     main()
data_processing()
    

