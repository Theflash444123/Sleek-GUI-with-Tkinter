#Created by: Nikhil Polpakkara
import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from CW_Preprocessing import *
import matplotlib.pyplot as plt
plt.ioff()


# module = "22COA122"#"22COA111" #"22COA122"
# week = 2

def module_attendance(week,module):
    """
    This function returns a table with attendance details
    of a module grouped by week

    Parameters
    ----------
    week : str
        Week number.
    module : str
        Name of the module.

    Returns
    -------
    matplotlib.figure.Figure : Table containing the attendance details by
    week and module
       

    """
    
    table_list, modules, connection = sql_tables() 
    sql_query =f"select Start_time,Room,Class,sum(Attendance) as classes_att, count(Attendance) as tot_att \
    from session_{module} inner join att_{module} \
    on att_{module}.Session_id = session_{module}.Session_id \
    where week={week} \
    group by Start_time"
    df = pd.read_sql_query(sql_query,connection)
    if df.empty:
        message= f"Week {week} is not present in the {module}.Please enter a valid week number"
        return message
    else:
        df["Attendance %"] = round((df["classes_att"]/df["tot_att"])*100,1)
        df.drop(["classes_att","tot_att"],axis=1,inplace=True)
        colors = df.applymap(color_cells)
        fig,ax = plt.subplots(figsize=(6, 3))
        fig.patch.set_facecolor('#e7e5e6')
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values,colLabels=df.columns,cellColours=colors.values, loc = 'center',cellLoc='center')
        table.scale(1,2)
        return fig
        
        connection.close()
# if __name__ == "__main__":
# week = int(input("Enter week number : "))
# module = input("Enter module name : ")
# fig = module_attendance(week,module)    
# plt.show()
