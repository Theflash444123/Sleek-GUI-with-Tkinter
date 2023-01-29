import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox

from CW_Preprocessing import *

# import ipynb
# from ipynb.fs.defs.CW_Preprocessing import *
from ipywidgets import widgets
from IPython import get_ipython


class StudentAtt:
    """
    A class for visualizing student attendance records.
    """
    def __init__(self, student_id, modules_selected):
        """
        Initializes the class with student_id and modules_selected.

        Parameters:
        student_id (int): The id of the student whose attendance records are to
        be visualized.
        modules_selected (list): A list of module codes for which the attendance
        records are to be visualized.
        """
        self.sid = student_id
        self.modules_selected = modules_selected
        self.selected_student_df = self.get_selected_student_df()
        self.pivot_table = self.pivot_table()

    def get_selected_modules_df(self):
        """
        Returns:
        DataFrame: A DataFrame containing attendance records of the selected
        modules for the given student.
        """
        selected_modules_df = pd.DataFrame()
        for module in self.modules_selected:
            att_df = ModuleRecord(module).wide_to_long()
            selected_modules_df = pd.concat([selected_modules_df, att_df])

        return selected_modules_df

    def get_selected_student_df(self):
        selected_modules_df = self.get_selected_modules_df()
        selected_student_df = selected_modules_df[
            selected_modules_df.sid.isin(self.sid)]
        return selected_student_df

    def pivot_table(self):
        """
        Returns:
        DataFrame: A pivot table for weekly average attendance for the selected
        modules for the given student.
        """
        selected_student_df = self.get_selected_student_df()
        pivot_table = pd.pivot_table(selected_student_df,
                                     values="att",
                                     index="week",
                                     columns="module",
                                     aggfunc=np.mean
                                     )
        pivot_table = pivot_table * 100
        pivot_table = pivot_table.round(0)
        return pivot_table

    def get_color_list(self):
        """
        returns a list of color codes for the cells of a pivot table.
        """
        cellcolors = []
        for row in range(self.pivot_table.shape[0]):
            row_colors = []
            for col in range(self.pivot_table.shape[1]):
                if self.pivot_table.iloc[row, col] <= 50:
                    row_colors.append("#DB3236")
                elif 50 < self.pivot_table.iloc[row, col] <= 75:
                    row_colors.append("#F4C20D")
                elif 75 < self.pivot_table.iloc[row, col] <= 100:
                    row_colors.append("#3CBA54")
                else:
                    row_colors.append("#FFFFFF")

            cellcolors.append(row_colors)
        return cellcolors

    def plot(self):
        """
        returns:
        matplotlib.figure: Plot having table and a bargraph as subplots.
        """
        cell_colors = self.get_color_list()
        gs_kw = dict(width_ratios=[1, 1.4])
        fig, ax = plt.subplots(1, 2, gridspec_kw=gs_kw)
        ax[0].axis('off')
        ax[0].axis('tight')
        ax[0].table(cellText=self.pivot_table.values,
                    cellColours=cell_colors,
                    rowLabels=self.pivot_table.index,
                    colLabels=self.pivot_table.columns, loc='center'
                    )
        ax[1].set_ylabel("Attendance%")
        plt.subplots_adjust(wspace=0.3)
        self.pivot_table.plot(kind="bar", ax=ax[1])
        return fig


def main_py():
    """
    This function will be executed if the file is run as a standalone
    .py script.
    """
    student_id = int(input("Please Enter Student ID"))
    StudentAtt(student_id=[student_id],
               modules_selected=get_modules_list()
               ).plot()


def main_ipynb(sid):
    """
    This function will be executed if the file is run as a standalone
    .ipynb script.
    """
    StudentAtt(student_id=[sid],
               modules_selected=get_modules_list()
               ).plot()


if __name__ == "__main__":
    """
    The script checks if the script is running in an ipython environment or 
    not and calls the appropriate main function. 
    """
    shell = get_ipython()
    if type(shell).__name__ == 'ZMQInteractiveShell':
        ipython = get_ipython()
        ipython.run_line_magic("matplotlib", "qt")
        sid_entry = widgets.Text(description='Student ID:')
        display(sid_entry)
        button = widgets.Button(description='Display')
        display(button)


        def on_button_clicked(b):
            sid = int(sid_entry.value)
            main_ipynb(sid)


        button.on_click(on_button_clicked)

    else:
        main_py()

