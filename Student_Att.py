import pandas as pd
import CW_Preprocessing
import matplotlib.pyplot as plt
import numpy as np


def get_student_att_fig(sid, modules_selected):
    combined_df = pd.DataFrame()
    for module in modules_selected:
        module_data = CW_Preprocessing.get_module_data_sql(module)
        att_df = CW_Preprocessing.wide_to_long(module_data, sid=sid)
        combined_df = pd.concat([combined_df, att_df])

    pivot_table = pd.pivot_table(combined_df,
                           values="att",
                           index="week",
                           columns="module",
                           aggfunc=np.mean
                               )
    pivot_table = pivot_table*100
    pivot_table = pivot_table.round(0)

    cellcolors = []
    for row in range(pivot_table.shape[0]):
        row_colors = []
        for col in range(pivot_table.shape[1]):
            if pivot_table.iloc[row, col] <= 25:
                row_colors.append("#DB3236")
            elif 25 < pivot_table.iloc[row, col] <= 75:
                row_colors.append("#F4C20D")
            elif 75 < pivot_table.iloc[row, col] <= 100:
                row_colors.append("#3CBA54")
            else:
                row_colors.append("#FFFFFF")

        cellcolors.append(row_colors)

    gs_kw = dict(width_ratios=[1, 1.4])
    fig, ax = plt.subplots(1, 2, gridspec_kw=gs_kw)
    ax[0].axis('off')
    ax[0].axis('tight')
    ax[0].table(cellText=pivot_table.values, cellColours=cellcolors, rowLabels=pivot_table.index, colLabels=pivot_table.columns, loc='center')
    # ax[1].set_ylabel("Attendance%")
    pivot_table.plot(kind="bar", ax=ax[1])

    return fig
if __name__ == "__main__":
    get_student_att_fig([21], ["22COA111", "22COA122"])
