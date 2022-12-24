import sqlite3
import pandas as pd
import os

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






