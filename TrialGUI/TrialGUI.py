import tkinter as tk
from tkinter import ttk

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------

selectionbar_color = '#eff5f6'
sidebar_color = '#F5E1FD'
header_color = '#53366b'
visualisation_frame_color = "#ffffff"

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
        self.header.place(relx=0.3, rely=0, relwidth=0.7, relheight=0.1)

        # ---------------- SIDEBAR -----------------------
        # CREATING FRAME FOR SIDEBAR
        self.sidebar = tk.Frame(self, bg=sidebar_color)
        self.sidebar.place(relx=0, rely=0, relwidth=0.3, relheight=1)

        # UNIVERSITY LOGO AND NAME
        self.brand_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.brand_frame.place(relx=0, rely=0, relwidth=1, relheight=0.15)
        self.uni_logo = icon.subsample(9)
        logo = tk.Label(self.brand_frame, image=self.uni_logo, bg=sidebar_color)
        logo.place(x=5, y=20)

        uni_name = tk.Label(self.brand_frame,
                            text='ABC',
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
                                     sub_menu_heading='SUBMENU 1',
                                     sub_menu_options=["Display Frame1",
                                                       "Display Frame2",
                                                       ]
                                     )
        att_submenu.options["Display Frame1"].config(
            command=lambda: self.show_frame(Frame1)
        )
        att_submenu.options["Display Frame2"].config(
            command=lambda: self.show_frame(Frame2)
        )

        att_submenu.place(relx=0, rely=0.025, relwidth=1, relheight=0.3)

        # --------------------  MULTI PAGE SETTINGS ----------------------------

        container = tk.Frame(self)
        container.config(highlightbackground="#808080", highlightthickness=0.5)
        container.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)

        self.frames = {}

        for F in (Frame1,
                  Frame2,
                  ):
            
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame(Frame1)

    def show_frame(self, cont):
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
        frame.tkraise()


# ------------------------ MULTIPAGE FRAMES ------------------------------------


class Frame1(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Frame 1', font=("Arial", 15))
        label.pack()


class Frame2(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Frame 2', font=("Arial", 15))
        label.pack()


# ----------------------------- CUSTOM WIDGETS ---------------------------------

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


app = TkinterApp()
app.mainloop()
