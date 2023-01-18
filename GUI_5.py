import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import pandas as pd

import CW_Preprocessing
import Student_Att
import Module_Att
import Poor_Att
import Poor_Att
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import PIL.Image, PIL.ImageTk

# ------------------------------------------- DEFINING GLOBAL VARIABLES ------------------------------------------------
selectionbar_color = '#eff5f6'
sidebar_color = '#F5E1FD'
header_color = '#53366b'
visualisation_frame_color = "#ffffff"
plt.ioff()


# -------------------------------------------------- ROOT WINDOW -------------------------------------------------------


class TkinterApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Attendance Tracking App")

        # ------------- BASIC APP LAYOUT --------------------

        self.geometry("900x600")
        self.resizable(0, 0)
        self.title('Attendance Tracking System')
        self.config(background=selectionbar_color)
        icon = tk.PhotoImage(file='images\\LU_logo.png')
        self.iconphoto(True, icon)

        # ------------- HEADER ------------------------------

        self.header = tk.Frame(self, bg=header_color)
        self.header.config(highlightbackground="#808080", highlightthickness=0.5)
        self.header.place(relx=0.3, rely=0, relwidth=0.7, relheight=0.1)

        # ------------- SIDEBAR -----------------------------

        self.sidebar = tk.Frame(self,
                                bg=sidebar_color
                                )
        self.sidebar.config(highlightbackground="#808080", highlightthickness=0.5)
        self.sidebar.place(relx=0, rely=0, relwidth=0.3, relheight=1)

        self.uni_logo = icon.subsample(10)
        logo = tk.Label(self.sidebar, image=self.uni_logo, bg=sidebar_color)
        logo.place(x=5, y=20)

        uniName = tk.Label(self.sidebar, text='Loughborough', bg=sidebar_color, font=("", 15, "bold"))
        uniName.place(x=55, y=27, anchor="w")

        uniName = tk.Label(self.sidebar, text='University', bg=sidebar_color, font=("", 15, "bold"))
        uniName.place(x=55, y=55, anchor="w")

        att_submenu = SidebarSubMenu(self.sidebar, 'ATTENDANCE OVERVIEW',
                                     ["Student Tracking", "Module Tracking", "Poor Attendance"]
                                     )
        att_submenu.options["Student Tracking"].config(command=lambda: self.show_frame(StudentTracking))
        att_submenu.options["Module Tracking"].config(command=lambda: self.show_frame(ModuleTracking))
        att_submenu.options["Poor Attendance"].config(command=lambda: self.show_frame(PoorAttTracking))
        att_submenu.place(relx=0, rely=1 / 6, relwidth=1, relheight=2 * 1 / 6)

        # --------------  MULTI PAGE SETTINGS ---------------

        container = tk.Frame(self)
        container.config(highlightbackground="#808080", highlightthickness=0.5)
        container.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)

        self.frames = {}

        for F in (HomePage, StudentTracking, ModuleTracking, PoorAttTracking):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# ----------------------------------------------- MULTIPAGE FRAMES -----------------------------------------------------


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg=selectionbar_color)


class StudentTracking(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config(bg=visualisation_frame_color)
        self.selection_bar = SelectionBar(self)
        self.selection_bar.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        self.sid_entry = tk.Label(self.selection_bar, text="Enter Student ID", bg=selectionbar_color)
        self.sid_entry.place(relx=0.3, rely=0.5, anchor="w")
        self.sid_entry = ttk.Entry(self.selection_bar)
        self.sid_entry.place(relx=0.45, rely=0.5, anchor="w")

        self.display_button = CustomButton(self.selection_bar)
        self.display_button.add_command(lambda: self.view_results())
        self.display_button.place(relx=0.67, rely=0.5, anchor="w")

        self.plot_frame = tk.Frame(self, bg=visualisation_frame_color)
        self.plot_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

    def view_results(self):
        sid = self.sid_entry.get()
        try:
            sid = int(sid)
        except Exception as e:
            messagebox.showinfo(title=None, message="Please Select Student ID")
            raise

        modules_selected = self.selection_bar.modules_dd.get_selected_items()
        if len(modules_selected) == 0:
            messagebox.showinfo(title=None, message="Please Select atleast one module")
            raise

        fig = Student_Att.get_student_att_fig([sid], modules_selected)
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)


class ModuleTracking(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg=visualisation_frame_color)

        self.selection_bar = SelectionBar(self)
        self.selection_bar.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        self.selection_bar.modules_dd.deselect_all()

        self.week_dd = CustomCombobox(parent=self.selection_bar, items_list=[], display_text="Please Select Week")
        self.week_dd.place(relx=0.3, rely=0.5, anchor="w")
        self.week_dd.add_command(lambda: self.update_week_dd())

        self.display_button = CustomButton(self.selection_bar)
        self.display_button.add_command(lambda: self.view_results())
        self.display_button.place(relx=0.55, rely=0.5, anchor="w")

        self.plot_frame = tk.Frame(self, bg=visualisation_frame_color)
        self.plot_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

    def update_week_dd(self):
        modules_selected = self.selection_bar.modules_dd.get_selected_items()
        print(modules_selected)
        if len(modules_selected) == 1:
            weeks = CW_Preprocessing.get_module_weeks(modules_selected[0])
            self.week_dd.update_list(weeks)
        elif len(modules_selected) == 0:
            messagebox.showinfo(title=None, message="Please Select a Module")
            raise
        elif len(modules_selected) > 1:
            messagebox.showinfo(title=None, message="Please Select only one Module")
            raise

    def view_results(self):
        week = self.week_dd.cb_var.get()
        if week == self.week_dd.display_text:
            messagebox.showinfo(title=None, message="Please Select Week")
            raise
        else:
            pass

        module_name = self.selection_bar.modules_dd.get_selected_items()[0]
        fig = Module_Att.get_module_att_fig(module_name, [week])
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)


class PoorAttTracking(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg=visualisation_frame_color)
        self.modules_selected = []
        self.poor_att = pd.DataFrame()
        self.below_avg_att = pd.DataFrame()
        self.img = None

        self.nb_frame = tk.Frame(self, bg=visualisation_frame_color)
        self.nb_frame.pack(expand=True, fill=tk.BOTH)

        self.nb = ttk.Notebook(self.nb_frame)
        self.table_tab = tk.Frame(self.nb, bg=visualisation_frame_color)
        self.scatter_tab = tk.Frame(self.nb, bg=visualisation_frame_color)
        self.nb.add(self.table_tab, text='Table')
        self.nb.add(self.scatter_tab, text='Scatter Plots')
        self.nb.pack(expand=True, fill=tk.BOTH)

        self.table_tab_selection_bar = SelectionBar(self.table_tab)
        self.table_tab_selection_bar.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        self.table_tab_display_frame = SelectionBar(self.table_tab)
        self.table_tab_display_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        self.view_table_button = CustomButton(self.table_tab_selection_bar, "Update\nTable")
        self.view_table_button.add_command(lambda: self.generate_table())
        self.view_table_button.place(relx=0.9, rely=0.5, anchor="w")
        self.canvas = tk.Canvas(self.table_tab_display_frame, bg='#FFFFFF', width=500, height=1600,scrollregion=(0, 0, 0, 1600))
        vbar = tk.Scrollbar(self.table_tab_display_frame, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=vbar.set)

        self.student_selection_bar = tk.Frame(self.scatter_tab, bg=selectionbar_color)
        self.student_selection_bar.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        text_label = tk.Label(self.student_selection_bar, text="Select Student ID for scatter plot", bg=selectionbar_color)
        text_label.place(relx=0, rely=0.3)
        self.student_selection_cb = CustomCombobox(self.student_selection_bar, items_list=[])
        self.student_selection_cb.place(relx=0.3, rely=0.3)
        self.student_selection_cb.enable_binding()
        self.student_selection_cb.post_selection_command = \
            lambda: self.generate_scatter(sid_list=[int(x) for x in list(self.student_selection_cb.selected_items.keys())])

        self.generate_table()
        self.generate_scatter()

    def generate_table(self):
        self.modules_selected = self.table_tab_selection_bar.modules_dd.get_selected_items()
        print(self.modules_selected)
        self.poor_att = Poor_Att.PoorAtt(self.modules_selected)
        self.poor_att.get_n_students_table()
        self.below_avg_att = self.poor_att.get_below_avg_att_df()
        print(self.below_avg_att)

        file = 'PA.png'
        self.img = PIL.ImageTk.PhotoImage(PIL.Image.open(file))
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.student_selection_cb.update_list(updated_list=list(self.poor_att.students_weekly_avg_att.index))

    def generate_scatter(self, sid_list=None):
        scatter_fig = self.poor_att.get_scatter_plot(sid_list)
        canvas = FigureCanvasTkAgg(scatter_fig, master=self.scatter_tab)
        canvas.get_tk_widget().place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

    def update_scatter(self):
        pass

# --------------------------------------------- CUSTOM WIDGETS ---------------------------------------------------------


class MultiselectDropdown(tk.Frame):
    def __init__(self, parent, text, items_list):
        tk.Frame.__init__(self, parent)
        self.text = text
        self.items_list = items_list
        # self.config(highlightbackground="black", highlightthickness=1)
        self.menubutton = tk.Menubutton(self, text=self.text + " 🡫", bg="white")
        self.menu = tk.Menu(self.menubutton, tearoff=False, bg="white")
        self.menubutton.configure(menu=self.menu)
        self.menubutton.pack()
        self.choices = {}

        self.create_dropdown()

    def create_dropdown(self):
        for choice in self.items_list:
            self.choices[choice] = tk.IntVar(value=1)
            self.menu.add_checkbutton(label=choice, variable=self.choices[choice],
                                      onvalue=1, offvalue=0
                                      )

    def get_selected_items(self):
        selected_items = []
        for name, var in self.choices.items():
            if var.get() == 1:
                selected_items.append(name)
        return selected_items

    def deselect_all(self):
        for name, var in self.choices.items():
            var.set(0)


class CustomCombobox(tk.Frame):
    def __init__(self, parent, items_list=[], display_text="default"):
        tk.Frame.__init__(self, parent)
        self.display_text = display_text
        self.cb_var = tk.StringVar(value=display_text)
        self.items_list = items_list
        self.combobox = ttk.Combobox(self, textvariable=self.cb_var, values=items_list)
        self.combobox.pack(side=tk.LEFT)
        self.selected_items = {}
        self.post_selection_command = None

    def update_list(self, updated_list):
        self.combobox.config(values=updated_list)

    def add_command(self, command):
        self.combobox.config(postcommand=command)

    def enable_binding(self):
        self.combobox.bind("<<ComboboxSelected>>", self.add_selection)

    def add_selection(self, event):
        selected_item = self.cb_var.get()
        if not selected_item == self.display_text:
            if selected_item not in list(self.selected_items.keys()):
                self.selected_items[selected_item] = {
                    "label": tk.Label(self, text=selected_item),
                    "Button": tk.Button(self, text=" X", bg=selectionbar_color, bd=0, foreground='red',cursor='hand2',
                                        command=lambda: self.remove_selection(id=selected_item))
                }
                self.update_selection(self.selected_items[selected_item])
                self.post_selection_command()

    def update_selection(self, dict):
        dict["label"].pack(side=tk.LEFT)
        dict["Button"].pack(side=tk.LEFT)

    def remove_selection(self, id):
        self.selected_items[id]["label"].pack_forget()
        self.selected_items[id]["Button"].pack_forget()
        del self.selected_items[id]
        self.post_selection_command()

    def post_selection_command(self):
        if self.post_selection_command:
            self.post_selection_command
        else:
            pass


class SidebarSubMenu(tk.Frame):
    def __init__(self, parent, sub_menu_heading, sub_menu_options):
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
                                        font=("Arial", 10, "bold"),
                                        bd=0,
                                        cursor='hand2',
                                        activebackground='#ffffff',
                                        )
            self.options[x].place(x=30, y=45 * (n + 1), anchor="w")


class SelectionBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.config(bg=selectionbar_color)
        modules_list = CW_Preprocessing.get_modules_list()
        self.modules_dd = MultiselectDropdown(self, "Select Modules", modules_list)
        self.modules_dd.menubutton.config(width=20, bg=selectionbar_color)
        self.modules_dd.place(relx=0.025, rely=0.5, anchor="w")

        self.line_style = ttk.Style()
        self.line_style.configure("Line.TSeparator", background="#000000")
        self.hf_sep = ttk.Separator(self, orient=tk.VERTICAL, style="Line.TSeparator")
        self.hf_sep.place(relx=0.25, rely=0.15, relheight=0.7)


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


app = TkinterApp()
app.mainloop()
