import pandas as pd
import CW_Preprocessing
import numpy as np
import matplotlib.pyplot as plt


def get_module_att_fig(module_name, week_list):

    # week = ["W5"]
    # module_name = "22COA122"

    module_data = CW_Preprocessing.get_module_data_sql(module_name)
    att_df = CW_Preprocessing.wide_to_long(module_data)
    att_df = att_df[att_df.week.isin(week_list)]

    gb_att_df = att_df.groupby(["time", "lab_code", "session_type"], as_index=False)
    module_att_table = gb_att_df.agg({"att": "mean"})
    module_att_table["att"] = (module_att_table["att"]*100).round(1)

    cellcolors = []
    for row in range(module_att_table.shape[0]):
        row_colors = []
        for col in range(module_att_table.shape[1]):
            if col ==3:
                if module_att_table.iloc[row, col] <= 25:
                    row_colors.append("#DB3236")
                elif 25 < module_att_table.iloc[row, col] <= 75:
                    row_colors.append("#F4C20D")
                elif 75 < module_att_table.iloc[row, col] <= 100:
                    row_colors.append("#3CBA54")
                else:
                    row_colors.append("#FFFFFF")
            else:
                row_colors.append("#FFFFFF")
        cellcolors.append(row_colors)

    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=module_att_table.values, cellColours=cellcolors, colLabels=module_att_table.columns, loc='center')

    return fig


if __name__ == "__main__":
    get_module_att_fig("22COA122", ["W5"])
