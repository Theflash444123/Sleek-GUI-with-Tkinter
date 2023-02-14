import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

from CW_Preprocessing import *
from Student_Att import *
from Module_Att import *
from Poor_Att import *

# import ipynb
# from ipynb.fs.defs.CW_Preprocessing import *
# from ipynb.fs.defs.Student_Att import *
# from ipynb.fs.defs.Module_Att import *
# from ipynb.fs.defs.Poor_Att import *


# -------------------------- DEFINING GLOBAL VARIABLES -------------------------

selectionbar_color = '#eff5f6'
sidebar_color = '#F5E1FD'
header_color = '#53366b'
visualisation_frame_color = "#ffffff"
plt.ioff()

# ------------------------------- ROOT WINDOW ----------------------------------


class TkinterApp(tk.Tk):
    """
     The class creates a header and sidebar for the application. Also creates
     two submenus in the sidebar, one for attendance overview with options to
     track students and modules, view poor attendance and another for
     database management, with options to update and add new modules to the
     database.
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Attendance Tracking App")

        # ------------- BASIC APP LAYOUT -----------------

        self.geometry("1100x700")
        self.resizable(0, 0)
        self.title('Attendance Tracking System')
        self.config(background=selectionbar_color)
        icon = tk.PhotoImage(file='images\\LU_logo.png')
        self.iconphoto(True, icon)

        # ---------------- HEADER ------------------------

        self.header = tk.Frame(self, bg=header_color)
        self.header.config(
            highlightbackground="#808080",
            highlightthickness=0.5
        )
        self.header.place(relx=0.3, rely=0, relwidth=0.7, relheight=0.1)

        # ---------------- SIDEBAR -----------------------
        # CREATING FRAME FOR SIDEBAR
        self.sidebar = tk.Frame(self, bg=sidebar_color)
        self.sidebar.config(
            highlightbackground="#808080",
            highlightthickness=0.5
            )
        self.sidebar.place(relx=0, rely=0, relwidth=0.3, relheight=1)

        # UNIVERSITY LOGO AND NAME
        self.brand_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.brand_frame.place(relx=0, rely=0, relwidth=1, relheight=0.15)
        self.uni_logo = icon.subsample(9)
        logo = tk.Label(self.brand_frame, image=self.uni_logo, bg=sidebar_color)
        logo.place(x=5, y=20)

        uni_name = tk.Label(self.brand_frame,
                            text='Loughborough',
                            bg=sidebar_color,
                            font=("", 15, "bold")
                            )
        uni_name.place(x=55, y=27, anchor="w")

        uni_name = tk.Label(self.brand_frame,
                            text='University', 
                            bg=sidebar_color,
                            font=("", 15, "bold")
                            )
        uni_name.place(x=55, y=60, anchor="w")

        # SUBMENUS IN SIDE BAR(ATTENDANCE OVERVIEW, DATABASE MANAGEMENT)

        # # Attendance Submenu
        self.submenu_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.submenu_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.85)
        att_submenu = SidebarSubMenu(self.submenu_frame,
                                     sub_menu_heading='ATTENDANCE OVERVIEW',
                                     sub_menu_options=["Student Tracking",
                                                       "Module Tracking",
                                                       "Poor Attendance"
                                                       ]
                                     )
        att_submenu.options["Student Tracking"].config(
            command=lambda: self.show_frame(StudentTracking, "Student Tracking")
        )
        att_submenu.options["Module Tracking"].config(
            command=lambda: self.show_frame(ModuleTracking, "Module Tracking")
        )
        att_submenu.options["Poor Attendance"].config(
            command=lambda: self.show_frame(PoorAttTracking, "Poor Attendance")
        )
        att_submenu.place(relx=0, rely=0.025, relwidth=1, relheight=0.3)

        # # Database Management
        db_submenu = SidebarSubMenu(self.submenu_frame,
                                    sub_menu_heading='DATABASE MANAGEMENT',
                                    sub_menu_options=["Database Overview",
                                                      "Update Database",
                                                      "Add New Module"
                                                      ]
                                    )
        db_submenu.options["Database Overview"].config(
            command=lambda: self.show_frame(DatabaseOverview, "Module Details")
        )
        db_submenu.options["Update Database"].config(
            command=lambda: DatabaseOverview.update_databases(update_all=True)
        )
        db_submenu.options["Add New Module"].config(
            command=lambda: DatabaseOverview.add_new_module()
        )
        db_submenu.place(relx=0, rely=0.4, relwidth=1, relheight=0.3)

        # --------------------  MULTI PAGE SETTINGS ----------------------------

        container = tk.Frame(self)
        container.config(highlightbackground="#808080", highlightthickness=0.5)
        container.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)

        self.frames = {}

        for F in (StudentTracking,
                  ModuleTracking, 
                  PoorAttTracking,
                  DatabaseOverview):
            
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame(StudentTracking, "Home")

    def show_frame(self, cont, title):
        """
        The function 'show_frame' is used to raise a specific frame (page) in
        the tkinter application and update the title displayed in the header.

        Parameters:
        cont (str): The name of the frame/page to be displayed.
        title (str): The title to be displayed in the header of the application.

        Returns:
        None
        """
        frame = self.frames[cont]
        for widget in self.header.winfo_children():
            widget.destroy()
        label = tk.Label(self.header,
                         text=title,
                         font=("Helvetica", 17),
                         bg=header_color,
                         fg="white")
        label.pack(side=tk.LEFT, padx=10)
        frame.tkraise()


# ------------------------ MULTIPAGE FRAMES ------------------------------------


class StudentTracking(tk.Frame):
    """
    The StudentTracking class creates a user interface for selecting the modules
    and student ID to display the weekly attendance for the selected student in
    the selected modules.

    Attributes:
    - selection_bar (Frame): a frame that contains the dropdown menu for
      selecting modules and an entry field for student ID
    - modules_dd (MultiselectDropdown): dropdown to select multiple modules
    - sid_entry (Entry): an entry field for the student ID
    - display_button (CustomButton): a button to display the results
    - plot_frame (Frame): a frame to hold the plotted results
    """
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.config(bg=visualisation_frame_color)

        # SELECTION BAR
        self.selection_bar = tk.Frame(self, bg=selectionbar_color)
        self.modules_dd = MultiselectDropdown(self.selection_bar,
                                              "Select Modules",
                                              get_modules_list()
                                              )
        self.modules_dd.pack(side=tk.LEFT)
        sep = StylerObjects.separator(self.selection_bar)
        sep.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=7)
        self.selection_bar.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        self.sid_label = tk.Label(self.selection_bar, text="Enter Student ID",
                                  bg=selectionbar_color
                                  )
        self.sid_label.pack(side=tk.LEFT, padx=5)
        self.sid_entry = ttk.Entry(self.selection_bar)
        self.sid_entry.pack(side=tk.LEFT, padx=5)

        self.display_button = CustomButton(self.selection_bar)
        self.display_button.add_command(lambda: self.view_results())
        self.display_button.pack(side=tk.LEFT, padx=5)

        # PLOT FRAME
        self.plot_frame = tk.Frame(self, bg=visualisation_frame_color)
        self.plot_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

    def view_results(self):
        """
        this function is called when the display button is clicked.
        It first checks that the user has entered a student ID and selected
        at least one module. If the input is valid, it creates an instance of
        the StudentAtt class and plots the results in the plot_frame.
        """
        sid = self.sid_entry.get()
        try:
            sid = int(sid)
        except Exception as e:
            messagebox.showinfo(title=None,
                                message="Please Select Student ID")
            raise

        modules_selected = self.modules_dd.get_selected_items()
        if len(modules_selected) == 0:
            messagebox.showinfo(title=None,
                                message="Please Select atleast one module"
                                )
            raise

        fig = StudentAtt([sid], modules_selected).plot()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)


class ModuleTracking(tk.Frame):
    """
    The ModuleTracking class creates a user interface for selecting the module
    and week that allows the user to track attendance for a specific module on a
    weekly basis.

    Attributes:
    - selection_bar (Frame): a frame that contains the dropdown for
      selecting modules and a dropdown for week.
    - modules_cb (Combobox): dropdown to select module.
    - week_dd (Combobox): dropdown to select week.
    - display_button (CustomButton): a button to display the results
    - plot_frame (Frame): a frame to hold the plotted results
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg=visualisation_frame_color)

        self.selection_bar = tk.Frame(self, bg=selectionbar_color)
        self.modules_cb = CustomCombobox(self.selection_bar,
                                         items_list=get_modules_list(),
                                         display_text="Select Module"
                                         )
        self.modules_cb.pack(side=tk.LEFT, padx=5)
        sep = StylerObjects.separator(self.selection_bar)
        sep.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=7)
        self.selection_bar.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        self.week_dd = CustomCombobox(parent=self.selection_bar,
                                      items_list=[],
                                      display_text="Please Select Week"
                                      )
        self.week_dd.pack(side=tk.LEFT, padx=5)
        self.week_dd.add_command(lambda: self.update_week_dd())

        self.display_button = CustomButton(self.selection_bar)
        self.display_button.add_command(lambda: self.view_results())
        self.display_button.pack(side=tk.LEFT, padx=5)

        self.plot_frame = tk.Frame(self, bg=visualisation_frame_color)
        self.plot_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

    def update_week_dd(self):
        """
        updates the options available in the week dropdown to match the weeks
        available for the selected module
        """
        modules_selected = self.modules_cb.get()

        if modules_selected == self.modules_cb.display_text or modules_selected == "":
            messagebox.showinfo(title=None, message="Please Select a Module")
            raise
        else:
            weeks = ModuleRecord(modules_selected).week_list()
            self.week_dd.update_list(weeks)

    def view_results(self):
        """
        gets the selected module name and week from the selection bar, and calls
        the get_module_att_fig() function to displays the chart in the plot frame.
        """
        week = self.week_dd.get()
        if week == self.week_dd.display_text:
            messagebox.showinfo(title=None, message="Please Select Week")
            raise
        else:
            pass

        module_name = self.modules_cb.get()
        fig = get_module_att_fig(module_name, [week])
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)


class PoorAttTracking(tk.Frame):
    """
        A class for creating a GUI frame that allows the user to track
        poor attendance in a class.

        Attributes:
            modules_selected (List): list of selected modules
            poor_att (object): instance of the "PoorAtt" class.
            nb_frame (tk.Frame): frame for packing notebook.
            nb (ttk.Notebook): notebook widget for switching between table and
            scatter plot
            table_tab (tk.Frame): tab for table visualization
            scatter_tab (tk.Frame): tab for scatter plot visualization
            table_tab_selectionbar (tk.Frame): selection bar for selecting
            modules in table tab.
            modules_dd (MultiselectDropdown): dropdown menu for selecting modules.
            table_tab_display_frame (tk.Frame): frame for displaying the table.
            view_table_button (CustomButton): button for updating table
            canvas (tk.Canvas): canvas for displaying table.
            student_selection_bar (tk.Frame): selection bar for selecting
            students in scatter plot tab.
            student_selection_cb (CustomCombobox): combobox for selecting
            students and adding them to scatter plot.
        """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg=visualisation_frame_color)
        self.modules_selected = []
        self.poor_att = pd.DataFrame()
        self.img = None

        # ------------- NOTEBOOK FOR TABLE AND SCATTER PLOT --------------------

        self.nb_frame = tk.Frame(self, bg=visualisation_frame_color)
        self.nb_frame.pack(expand=True, fill=tk.BOTH)

        self.nb = ttk.Notebook(self.nb_frame)
        self.table_tab = tk.Frame(self.nb, bg=visualisation_frame_color)
        self.scatter_tab = tk.Frame(self.nb, bg=visualisation_frame_color)
        self.nb.add(self.table_tab, text='Table')
        self.nb.add(self.scatter_tab, text='Scatter Plots')
        self.nb.pack(expand=True, fill=tk.BOTH)

        # --------- TABLE PANE----------------
        self.table_tab_selectionbar = tk.Frame(self.table_tab,
                                               bg=selectionbar_color
                                               )
        self.modules_dd = MultiselectDropdown(self.table_tab_selectionbar,
                                              text="Select Modules",
                                              items_list=get_modules_list()
                                              )
        self.modules_dd.pack(side=tk.LEFT, padx=5)

        sep = StylerObjects.separator(self.table_tab_selectionbar)
        sep.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=7)
        self.table_tab_selectionbar.place(relx=0, rely=0, relwidth=1,
                                          relheight=0.1
                                          )

        self.table_tab_display_frame = tk.Frame(self.table_tab)
        self.table_tab_display_frame.place(relx=0, rely=0.1, relwidth=1,
                                           relheight=0.9
                                           )
        self.view_table_button = CustomButton(self.table_tab_selectionbar,
                                              "Update\nTable"
                                              )
        self.view_table_button.add_command(lambda: self.generate_table())
        self.view_table_button.pack(side=tk.RIGHT, padx=20)

        self.canvas = tk.Canvas(self.table_tab_display_frame, bg='#FFFFFF',
                                width=500, height=1600,
                                scrollregion=(0, 0, 0, 1600)
                                )
        vbar = tk.Scrollbar(self.table_tab_display_frame, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=vbar.set)

        # --------- SCATTER PLOT PANE ----------------

        self.student_selection_bar = tk.Frame(self.scatter_tab,
                                              bg=selectionbar_color
                                              )
        self.student_selection_bar.place(relx=0, rely=0, relwidth=1,
                                         relheight=0.1
                                         )
        text_label = tk.Label(self.student_selection_bar,
                              text="Select Student ID for scatter plot",
                              bg=selectionbar_color
                              )
        text_label.place(relx=0, rely=0.3)
        self.student_selection_cb = CustomCombobox(self.student_selection_bar,
                                                   items_list=[]
                                                   )
        self.student_selection_cb.place(relx=0.3, rely=0.3)
        self.student_selection_cb.enbl_mltpl_sel()
        self.student_selection_cb.post_selection_command = lambda: self.generate_scatter(
            sid_list=[int(x) for x in list(
                self.student_selection_cb.selected_items.keys())])
        # ----------------------------------------------------------------------
        self.generate_table()
        self.generate_scatter()

    def generate_table(self):
        """
        Generates table of poor attendance information for selected modules
        """
        self.modules_selected = self.modules_dd.get_selected_items()
        self.poor_att = PoorAtt(self.modules_selected)
        avg_att = round(self.poor_att.selected_modules_df.att.mean() * 100, 2)
        avg_att_label = tk.Label(self.table_tab_selectionbar,
                                 text="Average Att % " + str(avg_att),
                                 bg=selectionbar_color
                                 )
        avg_att_label.pack(side=tk.LEFT, padx=5)
        self.poor_att.get_n_students_table()

        img_filepath = 'PA.png'
        self.img = ImageTk.PhotoImage(Image.open(img_filepath))
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.student_selection_cb.update_list(
            updated_list=list(self.poor_att.students_weekly_avg_att.index)
        )

    def generate_scatter(self, sid_list=None):
        """
        Generates a scatter plot of attendance information for selected student IDs.
        """
        scatter_fig, axs = self.poor_att.get_scatter_plot(sid_list)
        canvas = FigureCanvasTkAgg(scatter_fig, master=self.scatter_tab)
        canvas.get_tk_widget().place(relx=0, rely=0.1, relwidth=1,
                                     relheight=0.9
                                     )


class DatabaseOverview(tk.Frame):
    """
    The class creates a frame that gives an overview of the database, including
    what modules are present in the database and their details.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg=selectionbar_color)

        self.selection_bar = tk.Frame(self, bg=selectionbar_color)
        self.modules_cb = CustomCombobox(self.selection_bar,
                                         items_list=get_modules_list(),
                                         display_text="Select Module"
                                         )
        self.modules_cb.pack(side=tk.LEFT, padx=10)
        self.display_button = CustomButton(self.selection_bar)
        self.display_button.add_command(
            lambda: self.display_module_sessions(self.modules_cb.get()))
        self.display_button.pack(side=tk.LEFT, padx=5)
        self.selection_bar.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        self.plot_frame = tk.Frame(self)
        self.plot_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

    def display_module_sessions(self, module_name):
        """
        This function takes a module_name as a parameter  and uses the matplotlib
        library to create a table of the sessions of the selected module.
        """
        fig, ax = plt.subplots()
        figure = ax.get_figure()
        figure.set_size_inches(7, 6)
        df = ModuleRecord(module_name).get_sessions_sql()
        ax.axis('off')
        ax.axis('tight')
        ax.table(cellText=df.values,
                 colWidths=[1/16,1/16,1/16, 1/8,1/8,1/8,1/8,1/8],
                 rowLabels=df.index,
                 colLabels=df.columns,
                 cellLoc="center",
                 loc='center'
                 ).scale(1.1, 1.2)
        ax.set_xlabel("X-axis", fontsize=14)
        ax.set_ylabel("Y-axis", fontsize=14)
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.get_tk_widget().place(relx=0, rely=0, relheight=1, relwidth=1)

    @staticmethod
    def update_databases(update_all=False):
        """
        updates the database, with an option to replace existing data
        """
        if update_all is True:
            replace = messagebox.askyesno(
                "CONFIRMATION",
                "Do you want to replace existing data"
                )
            cw_preprocessing_main(replace)
            messagebox.showinfo(title=None, message="Database Updated")

    @staticmethod
    def add_new_module():
        """
        allows the user to add new module data to the database by selecting a
        csv file.
        """
        filepath = filedialog.askopenfilename()
        if not filepath.endswith(".csv"):
            messagebox.showinfo(title=None,
                                message="Please select a csv file"
                                )
        else:
            RawData(filepath).to_sql_db()
            messagebox.showinfo(title=None,
                                message="Database Updated"
                                )

# ----------------------------- CUSTOM WIDGETS ---------------------------------


class MultiselectDropdown(tk.Frame):
    """
    Creates a multi-select dropdown menu.

    Attributes:
    -parent(Frame): The parent frame in which the dropdown menu will be created.
    -text(str): The text that will be displayed on the dropdown button.
    -items_list(list): A list of items that will be displayed in the dropdown menu.
    """
    def __init__(self, parent, text, items_list):
        tk.Frame.__init__(self, parent)
        self.text = text
        self.items_list = items_list
        self.menubutton = tk.Menubutton(self, text=self.text + " 🡫",
                                        bg="white"
                                        )
        self.menu = tk.Menu(self.menubutton, tearoff=False, bg="white")
        self.menubutton.configure(menu=self.menu)
        self.menubutton.config(bg=selectionbar_color)
        self.menubutton.pack()
        self.choices = {}

        self.create_dropdown()

    def create_dropdown(self):
        """
        Creates the checkbuttons for each item in the items_list and adds it to
        the menu widget.
        """
        for choice in self.items_list:
            self.choices[choice] = tk.IntVar(value=1)
            self.menu.add_checkbutton(label=choice,
                                      variable=self.choices[choice],
                                      onvalue=1, offvalue=0
                                      )

    def get_selected_items(self):
        """
        Returns a list of items that are selected by the user from the dropdown
        menu.
        """
        selected_items = []
        for name, var in self.choices.items():
            if var.get() == 1:
                selected_items.append(name)
        return selected_items

    def deselect_all(self):
        """
        Deselects all the items in dropdown .
        """
        for name, var in self.choices.items():
            var.set(0)


class CustomCombobox(tk.Frame):
    """
    A custom tkinter combobox widget that allows for multiple selections.
    """
    def __init__(self, parent, items_list=[], display_text="default"):
        tk.Frame.__init__(self, parent)
        self.display_text = display_text
        self.cb_var = tk.StringVar(value=display_text)
        self.items_list = items_list
        self.combobox = ttk.Combobox(self, textvariable=self.cb_var,
                                     values=items_list
                                     )
        self.combobox.pack(side=tk.LEFT)
        self.selected_items = {}
        self.postselection_command = None

    def get(self):
        """
        Returns the current selection of the combobox.
        """
        return self.cb_var.get()

    def update_list(self, updated_list):
        """
        updates the items_list of combobox.
        """
        self.combobox.config(values=updated_list)

    def add_command(self, command):
        """
        adds a command function that will be called after an item is selected.
        """
        self.combobox.config(postcommand=command)

    def enbl_mltpl_sel(self):
        """
        enables multiple selections in the combobox.
        """
        self.combobox.bind("<<ComboboxSelected>>", self.add_selection)

    def add_selection(self, event):
        """
        This function is called when an item is selected from the combobox.
        It checks if the selected item is not the default display text and if
        the item is not already present in the selected items list. If the item
        is not present in the list, it creates a dictionary object for the
        selected item with a label and a button. The label displays the selected
        item and the button is used to remove the selection.
        """
        selected_item = self.cb_var.get()
        if not selected_item == self.display_text:
            if selected_item not in list(self.selected_items.keys()):
                self.selected_items[selected_item] = {
                    "label": tk.Label(self, text=selected_item),
                    "Button": tk.Button(self, text=" X", bg=selectionbar_color,
                                        bd=0, foreground='red', cursor='hand2',
                                        command=lambda: self.remove_selection(
                                            id=selected_item
                                        )
                                        )
                }
                self.update_selection(self.selected_items[selected_item])
                self.post_selection_command()

    def update_selection(self, dict):
        """
        Update the UI with the selected item
        """
        dict["label"].pack(side=tk.LEFT)
        dict["Button"].pack(side=tk.LEFT)

    def remove_selection(self, id):
        """
        Remove a selected item from the selected_items dictionary and update
        the UI.
        """
        self.selected_items[id]["label"].pack_forget()
        self.selected_items[id]["Button"].pack_forget()
        del self.selected_items[id]
        self.post_selection_command()

    def post_selection_command(self):
        """
        Execute the command added after an item is selected.
        """
        if self.postselection_command:
            self.postselection_command
        else:
            pass


class SidebarSubMenu(tk.Frame):
    """
    A submenu which can have multiple options and these can be linked with
    functions.
    """
    def __init__(self, parent, sub_menu_heading, sub_menu_options):
        """
        parent: The frame where submenu is to be placed
        sub_menu_heading: Heading for the options provided
        sub_menu_operations: Options to be included in sub_menu
        """
        tk.Frame.__init__(self, parent)
        self.config(bg=sidebar_color)
        self.sub_menu_heading_label = tk.Label(self,
                                               text=sub_menu_heading,
                                               bg=sidebar_color,
                                               fg="#333333",
                                               font=("Arial", 10)
                                               )
        self.sub_menu_heading_label.place(x=30, y=10, anchor="w")

        sub_menu_sep = ttk.Separator(self, orient='horizontal')
        sub_menu_sep.place(x=30, y=30, relwidth=0.8, anchor="w")

        self.options = {}
        for n, x in enumerate(sub_menu_options):
            self.options[x] = tk.Button(self,
                                        text=x,
                                        bg=sidebar_color,
                                        font=("Arial", 9, "bold"),
                                        bd=0,
                                        cursor='hand2',
                                        activebackground='#ffffff',
                                        )
            self.options[x].place(x=30, y=45 * (n + 1), anchor="w")


class CustomButton(tk.Frame):
    def __init__(self, parent, text="Display"):
        tk.Frame.__init__(self, parent)
        self.button = tk.Button(self,
                                text=text,
                                font=("", 9, "bold"),
                                bg=header_color,
                                fg="white",
                                cursor='hand2',
                                # command=lambda: self.view_results()
                                )
        self.button.pack()

    def add_command(self, command):
        self.button.config(command=command)


class StylerObjects:

    def __init__(self, parent):
        pass

    def separator(self):
        line_style = ttk.Style()
        line_style.configure("Line.TSeparator", background="#000000")
        sep = ttk.Separator(self,
                            orient=tk.VERTICAL, style="Line.TSeparator"
                            )
        return sep

    def title(self, text="text"):
        title = tk.Label(self, text=text, font=("", 14, "bold"))
        return title

    def heading(self, text="text"):
        heading = tk.Label(self, text=text, font=("", 12, "bold"))
        return heading

    def sub_heading(self, text="text"):
        sub_heading = tk.Label(self, text=text, font=("", 10, "bold"))
        return sub_heading

    def body(self, text):
        body = tk.Label(self, text=text, font=("", 8))
        return body


app = TkinterApp()
app.mainloop()
