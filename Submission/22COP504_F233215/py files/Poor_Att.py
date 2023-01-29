#Created by: Nikhil Polpakkara
import sys
import pandas as pd
import sqlite3
import numpy as np
from CW_Preprocessing import *
import matplotlib.pyplot as plt

plt.ioff()

def poor_attendance(student = None, sel_module = None):
    """
    

    Parameters
    ----------
    student : int, optional
        Student ID. The default is None.
    sel_module : str, optional
        Select module. The default is None.
        By default all the modules are selected

    Returns
    -------
    df_final : panadas dataframe
        dataframe of students with poor attendance.
    plot : TYPE
        DESCRIPTION.

    """
    if sel_module == None:
        table_list, sel_module, connection = sql_tables() 
    else:
        connection = sql_tables()[2] 
    df_attended_list = []
    df_total_list = []
    module_avg = {}
    for module in sel_module:
        sql_query = f'select Student_ID,Week,\
        count(Attendance) as tot_classes,\
        sum(Attendance) as att_classes \
        from att_{module} inner join session_{module} \
        on att_{module}.Session_id = session_{module}.Session_id \
        group by week, Student_ID'
        df = pd.read_sql_query(sql_query,connection)
        if df.empty:
            message= f"Student ID not present in {module}"
            print(message)
        else:
            df_total = df.pivot(index = "Student_ID",
                                columns = "Week",
                                values = "tot_classes")
            df_attended = df.pivot(index = "Student_ID",
                                   columns = "Week",
                                   values = "att_classes")
            df_total_list.append(df_total)
            df_attended_list.append(df_attended)
            module_avg[module] = (df_attended.sum(axis=0,skipna=True)/
                                    df_total.sum(axis=0,skipna=True))*100
            
    df_module_avg = round(pd.DataFrame(module_avg),2)
    df_module_avg = df_module_avg.reset_index()
    df_module_avg["Week"] = [f"W{df_module_avg.at[i,'Week']}"
                             for i,r in df_module_avg.iterrows()]
    df_attended = pd.concat(df_attended_list)
    df_attended["Average"] = df_attended.sum(axis=1,skipna=True)
    df_attended = df_attended.groupby("Student_ID").agg(sum)
    df_attended.loc["Class Average"] = df_attended.sum(axis=0,skipna=True)
    df_total = pd.concat(df_total_list)
    df_total["Average"] = df_total.sum(axis=1,skipna=True)
    df_total = df_total.groupby("Student_ID").agg(sum)
    df_total .loc["Class Average"] = df_total .sum(axis=0,skipna=True)  
    df = df_attended/df_total*100
    df = df.sort_values(by = "Average", ascending=True)
    df_first_row = df.loc["Class Average"]
    df_final = pd.concat([pd.DataFrame(df_first_row).T,
                          df.drop("Class Average")],
                         ignore_index=False)
    df_final.columns.values[:-1] = [f"W{i}" for i in
                                    range(1, len(df.columns))]
    df_final.reset_index(inplace=True)
    df_final.columns.values[0]= "Student_ID"
    df_final = df_final[df_final["Average"]<=df_final.at[0,"Average"]]
    df_final = round(df_final,2)

    if student == None:
        df_clean = df_final[df_final["Average"]!=0]
        poor_10_students = list(df_clean["Student_ID"][1:6])
        student = poor_10_students
        
    else:
        pass
    
    student_df = pd.concat([df_final[df_final["Student_ID"] 
                                     == "Class Average" ],
                            df_final[df_final["Student_ID"].isin(student)]],
                            axis=0)
    student_df = student_df.T
    student_df.columns = student_df.iloc[0,:]
    student_df= student_df.iloc[1:-1,:]
    student_df.reset_index(inplace = True)


    student_df.plot(x ="Week",
                    y = student_df.columns[2:],
                    ax =ax,kind = "line",marker = 'x')
    df_module_avg.plot(x ="Week", y =df_module_avg.columns[1:],
                                   kind = "line",ax=ax,
                                   linestyle = "dotted")
    student_df.plot.scatter(x = "Week",
                            y = "Class Average",
                            ax= ax,label="Class Average",
                            c="#FF00FF")

    ax.set_ylabel("Attendance %")
    ax.set_ylim(-5,110)
    fig.set_facecolor("#f0f0f0")
    # plt.show()
    return df_final, fig
    connection.close() 

        
