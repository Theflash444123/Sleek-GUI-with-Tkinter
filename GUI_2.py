from tkinter import *
from CW_Preprocessing import *

root = Tk()
root.geometry('600x450')
root.title('Attendance Tracking System')


def get_title_frame(title):
    title_frame = Frame(root, width=600, height=50, bg="#b8b6b6")
    title_label = Label(title_frame, text=title, font=("Trebuchet MS", 14), bg="#b8b6b6")
    title_label.pack()
    title_frame.pack()
    title_frame.pack_propagate(0)


def clear_window():
    for widget in root.winfo_children():
        if not widget.winfo_name() == "!menu":
            widget.destroy()


def student_att_tracking_window():
    clear_window()
    get_title_frame(title="STUDENT ATTENDANCE TRACKING")


def module_att_tracking_window():
    clear_window()
    get_title_frame(title="MODULE ATTENDANCE TRACKING")


def poor_att_tracking_window():
    clear_window()
    get_title_frame(title="POOR ATTENDANCE TRACKING")


def update_selected_modules():
    """
    This function will give the user functionality of updating the database of selected modules which are present inside
    the data folder.
    :return:
    """
    clear_window()
    get_title_frame(title="UPDATE DATABASE")

    f1 = Frame(root)
    f1l1 = Label(f1, text="Available CSV Files", font=("Trebuchet MS", 10))
    f1l1.grid(row=1, column=1, sticky="w")
    f1.pack()
    f1.pack_propagate(0)


def update_all_modules():
    """
    This function will enable the user to update the entire database at once, so if any new data(Attendance CSV files)
    are added to the data folder selecting this option from the menu will update the data of that module into the database.
    :return:
    """
    csv_filepaths = get_csv_filepaths(data_folder_name="cop504cwdata")
    for filepath in csv_filepaths:
        module_data = get_module_data(filepath)
        try:
            module_data_to_sql(module_data)
        except Exception as e:
            print(e)


menu = Menu(root)
root.config(menu=menu)

attd_menu = Menu(menu)
menu.add_cascade(label='Attendance Tracking', menu=attd_menu)
attd_menu.add_command(label='Student Tracking', command=student_att_tracking_window)
attd_menu.add_command(label='Module Tracking', command=module_att_tracking_window)
attd_menu.add_command(label='Poor Attendance Tracking', command=poor_att_tracking_window)
attd_menu.add_separator()
attd_menu.add_command(label='Exit', command=root.quit)

db_menu = Menu(menu)
menu.add_cascade(label='Database Operations', menu=db_menu)
db_menu.add_command(label='Update Selected Modules', command=update_selected_modules)
db_menu.add_command(label='Update All modules', command=update_all_modules)
db_menu.add_separator()

mainloop()