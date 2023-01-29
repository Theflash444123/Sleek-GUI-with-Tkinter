#Created by: Nikhil Polpakkara

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as tkFont
from PIL import ImageTk, Image

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk)
import matplotlib.pyplot as plt

from CW_Preprocessing import *
from Student_Att_New import *
from Poor_Att import *
from Module_Att_New  import *


plt.ioff()
image_path = r"C:\Users\Admin\OneDrive - Loughborough University\Loughborough Uni\Programming for datascience\Coursework\Images\New folder"
bg_path= r"C:\Users\Admin\OneDrive - Loughborough University\Loughborough Uni\Programming for datascience\Coursework\Images"

class Styler:
    """
    This class provides methods for styling various widgets in a tkinter
    application. It has methods to set background image, style buttons,
    labels, entry boxes, listboxes and create home button.
            
    """
    def __init__(self):
        pass
    
    def bkg_image(parent,controller,path):
        """
        The bkg_image method takes in a parent frame,
        a controller and an image path and sets the background of the frame.

        Parameters
        ----------
        parent : tk.Frame
                 The frame whose background image is being set
        controller : tk.Frame
                     The controller of the application
        path :  str
                the file path of the image to be used as background

        Returns
        -------
        None.

        """
        bkg = Image.open(bg_path+path)
        parent.bkg_img = ImageTk.PhotoImage(bkg)
        panel = tk.Label(parent, image = parent.bkg_img)
        panel.pack(fill="both", expand=True)
        
    def button_style(button,bg = "#3d155b",ft_size = 10,fg = "#ffffff"):
        ft = tkFont.Font(family='Times',size=ft_size)
        button.configure(bg = bg,
                                     font = ft,
                                     fg = fg,
                                     justify = "center",
                                     relief = "raised",
                                       )
    
    
    def label_style(label,bg = "#3d155b",ft_size = 10,fg = "#ffffff"):
        ft = tkFont.Font(family='Times',size=ft_size)
        label.configure(bg = bg,
                        font = ft,
                        fg = fg,
                        justify = "center",
                        relief = "flat",
                        borderwidth=0
                                  )
    def entry_box(data_entry, bg = "#f0f0f0"):
        ft = tkFont.Font(family='Times',size=10)
        data_entry.configure(bg = bg,
                        font = ft,
                        fg = "#333333",
                        justify = "center",
                        relief = "groove",
                        borderwidth = "1px")
        # data_entry.entry.place(x=x,y=y,width=w,height=h)
    
    def list_box(list_entry):
        ft = tkFont.Font(family='Times',size=10)
        list_entry.config(borderwidth =  "1px",
                          bg = '#e7e5e6',
                          fg= "#333333",
                          justify = "left",
                          font = ft )
        
    def home_button(preset_bt,controller,x=5,y=5,w = 30,h=30):
        home = Image.open(image_path+"\HOME.jpg") 
        home.resize((25,25),Image.ANTIALIAS)
        preset_bt.home = ImageTk.PhotoImage(home)
        home_bt = tk.Button(preset_bt,image = preset_bt.home,
                            command = lambda: controller.show_frame(main_page))
        home_bt.configure(relief = "flat",borderwidth=0,bg = "#000000") # #ae9ff4
        home_bt.place(x=x,y=y,width = w, height =h)
    # return home_bt

    def refresh_button(preset_bt,controller,x=45,y=5,w = 30,h=30):
        refresh = Image.open(image_path+"\REFRESH.jpg") 
        refresh.resize((25,25),Image.ANTIALIAS)
        preset_bt.refresh = ImageTk.PhotoImage(refresh)
        refresh_bt = tk.Button(preset_bt,image = preset_bt.refresh,
                               command = lambda: preset_bt.delete())
        refresh_bt.configure(relief = "flat",bg = "#000000")
        refresh_bt.place(x=x,y=y,width = w, height =h)
    # return refresh_bt



class tkinterApp(tk.Tk):
    """
    This is a class called tkinterApp which creates a Tkinter application
    The class has a container frame that is used to hold other frames within
    the application which are part of the various operations for Attendance 
    monitoring
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Attendance application")
        width=1100
        height=600
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2,
                                    (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (main_page,module_att,stud_att,poor_att,data_process):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(main_page)
        

    def show_frame(self, cont):
        """
        This function is used to change the currently visible frame in a
        tkinter application with multiple frames

        Parameters
        ----------
        cont :  str
                the name of the frame to be raised and shown to the user.

        Returns
        -------
        None.

        """
        frame = self.frames[cont]
        frame.tkraise()
         

         

class main_page(tk.Frame):
    """
    This class creates a frame that contains buttons to navigate to the
    various functions such as database update, module,student and
    low attendance tracking.It inherits from the tkinter Frame class 
    and has a constructor that initializes the frame and sets up the
    main page of the application
    """
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  
        Styler.bkg_image(self,controller,"\des16.jpg")
        def lb_img(path):
            img = Image.open(image_path+path)
            img = img.resize((50,50), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            # Create a Label Widget to display the text or Image
            label = tk.Label(self,image=img,borderwidth=0)
            label.image = img
            return label
        
        def bt_style(button):
            button["bg"] = "#3d155b"
            ft = tkFont.Font(family='Times',size=10)
            button["font"] = ft
            button["fg"] = "#ffffff"
            button["justify"] = "center"
            button["relief"] = "raised"
            return button
        

        
        
        label_1 = lb_img("\DATABASE1.jpg")
        label_1.place(x=215,y=90)


        Button_1=tk.Button(self,text="DATA ENTRY &\nPROCESSING",
                           command = lambda:controller.show_frame(data_process))
        Button_1 = bt_style(Button_1)
        Button_1.place(x=190,y=170,width=100,height=40)

        
        label_2 = lb_img("\STUDENT.jpg")
        label_2.place(x=426,y=90)

        Button_2=tk.Button(self,text =  "STUDENT\nATTENDANCE",
                           command = lambda: controller.show_frame(stud_att))
        Button_2 = bt_style(Button_2)   
        Button_2.place(x=400,y=170,width=100,height=40)


        # Create a Label Widget to display the text or Image
        label_3 = lb_img("\MODULE1.jpg")
        label_3.place(x=638,y=90)


        Button_3=tk.Button(self,text = "MODULE\nATTENDANCE",
                           command = lambda: controller.show_frame(module_att))
        Button_3 = bt_style(Button_3)
        Button_3.place(x=610,y=170,width=100,height=40)
        # Button_3["command"] = self.Button_3_command


        label_4 = lb_img("\ATTENDANCE1.jpg")
        label_4.place(x=843,y=90)


        Button_4=tk.Button(self,text = "CRITICAL\nATTENDANCE",
                           command = lambda: controller.show_frame(poor_att))
        Button_4 = bt_style(Button_4)
        Button_4.place(x=820,y=170,width=100,height=40)

        
        label_4=tk.Label(self,text = "ATTENDANCE MONITORING APPLICATION")
        Styler.label_style(label_4,bg="#ae9ff4", ft_size = 20,fg="#000000")
        label_4.place(x=0,y=0,width=1100,height=60)
        
class data_process(tk.Frame):
    """
    This class defines the frame that has buttons and labels to perform 
    database related tasks. These methods are used to perform tasks such as
    loading data from a csv file, updating the database,
    and displaying the current modules in the database
    """
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        self.frm2 = tk.Frame(self,bg="#3d155b",width=1100,height=125)
        self.frm2.pack(side="top", anchor="n",fill = tk.X)
        self.frm1 = tk.Frame(self,bg="#ae9ff4",width=300,height=400)
        self.frm1.pack(side="left", anchor="w",fill = tk.Y)
        # self.frm3 = tk.Frame(self,bg="#e7e5e6",width=800,height=450)
        # self.frm3.pack(side="left", anchor="s",fill = tk.Y,padx = 10,pady = 10) 
        
        self.notebook = ttk.Notebook(self,width=800,height=450,)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)

        
        self.notebook.add(self.tab1, text='STUDENT ATTENDANCE')
        self.notebook.add(self.tab2, text='SESSION DETAILS')
        self.notebook.pack(side="left", anchor="n",fill = tk.X)

        
        label_=tk.Label(self.frm2,text = "DATA PROCESSING AND MANAGEMENT")
        Styler.label_style(label_,bg = "#3d155b",ft_size =20)
        label_.place(x=250,y=0,width=600,height=50)
        
        
        Button_1=tk.Button(self.frm1,text="ADD CSV DATA",
                           command = self.load_csv)
        Styler.button_style(Button_1)
        Button_1.place(x=80,y=100,width=150,height=30)


        self.Button_2=tk.Button(self.frm1,text="UPDATE DATABASE",
                                command = self.database_update)
        Styler.button_style(self.Button_2)
        self.Button_2.place(x=80,y=50,width=150,height=30)
        # GButton_2["command"] = self.GButton_2_command
        

        self.ListBox_1=tk.Listbox(self.frm1,relief="flat")
        Styler.list_box( self.ListBox_1)
        self.ListBox_1.configure(bd=0)
        self.ListBox_1.place(x=80,y=150,width=150,height=200)
        self.modules = sql_tables()[1]
        if len(self.modules) == 0:
            self.ListBox_1.insert(0,"NO TABLES IN DATABASE")
        else:
            self.ListBox_1.insert(0,"MODULES IN DATABASE")
            for name in range(0,len(self.modules)):
                module = str(str(name+1)+" : "+str(self.modules[name]))
                self.ListBox_1.insert("end",module)
                
        Styler.refresh_button(self,controller)
        Styler.home_button(self,controller)    

    def loaded_modules(self):
        """
        Method to display the modules available in the database in a listbox 
        """
        
        if len(self.modules) == 0:
            self.ListBox_1.insert(0,"NO TABLES IN DATABASE")
        else:
            self.ListBox_1.insert(0,"MODULES DATA IN DATABASE")
            for name in range(0,len(self.modules)):
                module = str(str(name+1)+" : "+str(self.modules[name]))
                self.ListBox_1.insert("end",module)
    def load_csv(self):
        """
        Method to select a particular file for updation
        """
        names = add_data()
        if names == False:
            print("NO DATA SELECTED")
        else:
            if len(names) == 0:
                print("DATA ALREADY IN DATABASE")
            else:
                for name in range(0,len(names)):
                    modules = str(str(name+1)+" : "+str(names[name]))
                    self.ListBox_1.insert("end",modules)
    
    def database_update(self):
        """
        Method to update database with raw files available in the database folder
        """
        names = data_processing()
        if len(names) == 0:
            tk.messagebox.showinfo("Database","DATA UPTO DATE")
        else:
            for name in range(0,len(names)):
                modules = str(str(name+1)+" : "+str(names[name]))
                self.ListBox_1.insert("end",modules)
            tk.messagebox.showinfo("Database","DATABASE UPDATED ")
            
        
    def delete(self):
        try:
            self.ListBox_1.delete(1,tk.END)
            mods = sql_tables()[1]
            for name in range(0,len(mods)):
                module = str(str(name+1)+" : "+str(self.modules[name]))
                self.ListBox_1.insert("end",module)
        except:
            pass

class module_att(tk.Frame):
    """
    This class defines the user interface with buttons,labels and listbox 
    and sets up the module attendance page of the application. The class
    contains methods to display the attendance detailes of specefic module and
    week selection
    """
    def __init__(self, parent, controller):
        self.modules = sql_tables()[1]
        tk.Frame.__init__(self, parent)
        
        # Defining frames
        self.frm2 = tk.Frame(self,bg="#3d155b",width=1100,height=125)
        self.frm2.pack(side="top", anchor="n",fill = tk.X)
        self.frm1 = tk.Frame(self,bg="#ae9ff4",width=300,height=400)
        self.frm1.pack(side="left", anchor="w",fill = tk.Y)
        self.frm3 = tk.Frame(self,bg="#e7e5e6",width=800,height=450)
        self.frm3.pack(side="left", anchor="s",fill = tk.Y) 
        
        
        Styler.refresh_button(self,controller)
        Styler.home_button(self,controller)

        # Defining Labels,buttons,combobox and Listbox
        label_title=tk.Label(self.frm2,text = "MODULE ATTENDANCE")
        Styler.label_style( label_title,ft_size = 20)
        label_title.place(x=250,y=0,width=600,height=50)

        Label_2=tk.Label(self.frm1,text="ENTER MODULE")
        Styler.label_style(Label_2,bg ="#ae9ff4",fg = "#000000",ft_size=12)
        Label_2.place(x=80,y=30,width=150,height=30)
        
        
        self.combobox = tk.ttk.Combobox(self.frm1,
                                     state="readonly",
                                     values= self.modules,
                                     justify='center')
        self.combobox.place(x=80,y=60,width=150,height=30)
        self.combobox.bind("<<ComboboxSelected>>", self.update_listbox)
        
        
        
        Label_3=tk.Label(self.frm1,text="DATA SELECTED")
        Styler.label_style(Label_3,bg ="#ae9ff4",fg = "#000000",ft_size=12)
        Label_3.place(x=80,y=200,width=150,height=30)
        
        self.ListBox_1=tk.Listbox(self.frm1,selectmode='multiple')
        Styler.list_box(self.ListBox_1)
        self.ListBox_1.place(x=80,y=230,width=150,height=100)
        
        Label_1=tk.Label(self.frm1,text="ENTER WEEK NO:")
        Styler.label_style(Label_1,bg ="#ae9ff4",fg = "#000000",ft_size=12)
        Label_1.place(x=80,y=100,width=150,height=30)
        
        self.combobox_2 = ttk.Combobox(self.frm1,
                                       state="readonly",
                                       justify = "center"
                                       )
        self.combobox_2.place(x=80,y=130,width=150,height=30)



        self.Button_3=tk.Button(self.frm1,text = "DISPLAY RESULTS",
                                command = self.plot_data)
        Styler.button_style(self.Button_3)
        self.Button_3.place(x=80,y=350,width=150,height=30)

        
    def update_listbox(self, *args):
        """
        This method updates the listbox with the selected module from
        the combobox.It also updates the values of the combobox_2 with the
        weeks of the selected module.
        """
        self.ListBox_1.delete(0, tk.END)
        self.ListBox_1.insert(tk.END, self.combobox.get())
        selection = self.combobox.get()
        weeks = ["W"+str(i) for i in module_data()[1][selection]]
        self.combobox_2.config(values=weeks)

    def plot_data(self):
        """
        Method to display the plot of Module attendance for the selected week.
        It takes the selected week number and module name as input and calls
        the module_attendance function to get the data and plot it.
        """
        try:
            self.canvas.get_tk_widget().destroy()
            self.fig.clf() 
        except:
            pass
        if len(self.combobox_2.get()) ==0:
            tk.messagebox.showwarning("Module Attendance",
                                      "Select Week")
        else:
            self.fig = module_attendance(int(self.combobox_2.get()[1:]),
                                      self.ListBox_1.get(0))
            self.canvas = FigureCanvasTkAgg(self.fig, master = self.frm3)
            self.canvas.get_tk_widget().place(x = 50, y = 50)
        

        
    def delete(self):
        """
        Method is used to clear the contents of the ListBox, LineEdit,
        and Combobox widgets on the page
        """
        try:
            self.ListBox_1.delete(0,"end")
        except:
            pass
        try:
            self.LineEdit_1.delete(0,"end")
        except:
            pass
        try:
            self.LineEdit_2.delete(0,"end")
        except:
            pass
        try:
            self.ListBox_1.delete(0, tk.END)
        except:
            pass
        try:
            self.canvas.get_tk_widget().delete("all")
            self.canvas.get_tk_widget().destroy()
            self.fig.clf() #clear the figure
            self.canvas=None #or del self.canvas
        except:
            pass

class stud_att(tk.Frame):
    """
    This class creates a tkinter frame for student attendance monitoring.
    It has three child frames, a label, an entry widget, a combobox,
    a listbox, and two buttons. The layout of the frame is set up in the
    init method, which also sets up the functionality of the widgets.
    
    Attributes:
    modules:list
            list of modules in the database
    
    """
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent) 

        self.modules = sql_tables()[1]
        
        self.frm2 = tk.Frame(self,bg="#3d155b",width=1100,height=125)
        self.frm2.pack(side="top", anchor="n",fill = tk.X)
        self.frm1 = tk.Frame(self,bg="#ae9ff4",width=300,height=400)
        self.frm1.pack(side="left", anchor="w",fill = tk.Y)
        self.frm3 = tk.Frame(self,bg="#e7e5e6",width=800,height=450)
        self.frm3.pack(side="left", anchor="s",fill = tk.Y) 
        
        Styler.refresh_button(self,controller)
        Styler.home_button(self.frm2,controller)
        
                
        label_=tk.Label(self.frm2 ,text = "STUDENT ATTENDANCE MONITORING")
        Styler.label_style(label_, ft_size =20)
        label_.place(x=250,y=0,width=600,height=50)
        
        
        Label_1=tk.Label(self.frm1,text = "ENTER STUDENT ID")
        Styler.label_style(Label_1,bg ="#ae9ff4",fg = "#000000",ft_size=12)
        Label_1.place(x=80,y=30,width=150,height=30)

        
        self.LineEdit_1=tk.Entry(self.frm1)
        Styler.entry_box(self.LineEdit_1)
        self.LineEdit_1.place(x=80,y=60,width=150,height=30)
        # self.LineEdit_1["justify"] = "center"
        
        Label_2=tk.Label(self.frm1,text="SELECT MODULE")
        Styler.label_style(Label_2,bg ="#ae9ff4",fg = "#000000",ft_size=12)
        Label_2.place(x=80,y=90,width=150,height=30)
        
        self.all_modules = ["ALL MODULES"] + self.modules
        self.combobox = ttk.Combobox(self.frm1, state="readonly",
                                     values= self.all_modules,justify='center')
        self.combobox.place(x=80,y=120,width=150,height=30)
        self.combobox.bind("<<ComboboxSelected>>", self.update_listbox)
        
        
        self.Button_4=tk.Button(self.frm1,text="DISPLAY RESULTS",
                                command = self.plot_data)
        Styler.button_style(self.Button_4)
        self.Button_4.place(x=80,y=300,width=150,height=30)

        self.ListBox_1=tk.Listbox(self.frm1)
        Styler.list_box(self.ListBox_1)
        self. ListBox_1.place(x=80,y=180,width=150,height=100)

        Label_3=tk.Label(self.frm1,text="DATA SELECTED")
        Styler.label_style(Label_3,bg ="#ae9ff4",fg = "#000000",ft_size=12)
        Label_3.place(x=80,y=150,width=150,height=30)
        
    def update_listbox(self, *args):
        """
        Method to update the listbox with selected module
        """
        if self.combobox.get() in self.ListBox_1.get(0,tk.END):
            pass
        elif self.combobox.get() == "ALL MODULES" :
            self.ListBox_1.delete(0,tk.END)
            self.ListBox_1.insert(0, self.combobox.get())
        else:
            if self.ListBox_1.get(0) ==  "ALL MODULES":
                self.ListBox_1.delete(0)
                self.ListBox_1.insert(tk.END, self.combobox.get())
            else:
                self.ListBox_1.insert(tk.END, self.combobox.get())
    def plot_data(self):
        """
        Method to display the plot of Student attendance for the selected
        Student and module(optional)
        """
        try:
            self.canvas.get_tk_widget().destroy()
            self.fig.clf()
        except: 
            pass
        if "ALL MODULES" in self.ListBox_1.get(0,tk.END) or \
            len(self.ListBox_1.get(0,tk.END)) == 0:
            self.fig = student_attendance(self.LineEdit_1.get())
        else:
            self.fig = student_attendance(self.LineEdit_1.get(),
                                              list(self.ListBox_1.get(0,tk.END)))
        
        if type(self.fig) == str:
            tk.messagebox.showwarning("Student Attendance",
                                      self.fig)
        else:
            self.canvas = FigureCanvasTkAgg(self.fig, master = self.frm3)
            self.canvas.get_tk_widget().place(x = 50, y = 50)
        
    def delete(self):
        """
        Method is used to clear the contents of the ListBox, LineEdit,
        and Combobox widgets on the page
        """
        try:
            self.ListBox_1.delete(0,"end")
        except:
            pass
        try:
            self.LineEdit_1.delete(0,"end")
        except:
            pass
        try:
            self.LineEdit_2.delete(0,"end")
        except:
            pass
        try:
            self.canvas.get_tk_widget().delete("all")
            self.canvas.get_tk_widget().destroy()
            self.fig.clf() #clear the figure
            self.canvas=None #or del self.canvas
        except:
            pass
        
        
class poor_att(tk.Frame):
    """
    A class that creates a tkinter frame for monitoring student attendance. 
    It displays a table of student attendance data and a chart representation
    of the data. It also allows the user to select a module and a student
    to view their specific attendance data.
        
    Attributes:
    modules:list
            list of modules in the database
    """
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.modules = sql_tables()[1]
        
        label_=tk.Label(self,text = "STUDENT ATTENDANCE MONITORING")
        Styler.label_style(label_, ft_size =20)
        label_.place(x=250,y=0,width=600,height=50)
        
        self.frm2 = tk.Frame(self,bg="#3d155b",width=1100,height=125)
        self.frm2.pack(side="top", anchor="n",fill = tk.X)

        self.frm1 = tk.Frame(self,bg="#ae9ff4",width=300,height=400)
        self.frm1.pack(side="left", anchor="w",fill = tk.Y)
        
        self.notebook = ttk.Notebook(self,width=600,height=500)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)

        
        self.notebook.add(self.tab1, text='TABLE')
        self.notebook.add(self.tab2, text='CHART')
        self.notebook.pack(side="left", anchor="n",fill = tk.X)
        
        self.frm3 = tk.Frame(self,bg="#f0f0f0",width=200,height=453)
        self.frm3.pack(side="left", anchor="s")#,fill = tk.Y) 
        
        
        Label_1=tk.Label(self.frm3,text = "ENTER STUDENT ID")
        Styler.label_style(Label_1,bg ="#f0f0f0",fg = "#000000",ft_size=12)
        Label_1.place(x=20,y=20,width=150,height=30)
        
        Label_2=tk.Label(self,text="ENTER MODULE")
        Styler.label_style(Label_2,bg ="#ae9ff4",fg = "#000000",ft_size=12)
        Label_2.place(x=80,y=165,width=150,height=30)
        
        self.all_modules = ["ALL MODULES"] + self.modules
        self.combobox = ttk.Combobox(self, state="readonly",
                                     values= self.all_modules,
                                     justify = 'center')
        self.combobox.place(x=80,y=195,width=150,height=30)
        self.combobox.bind("<<ComboboxSelected>>", self.update_listbox)
        
        
        Label_3=tk.Label(self,text="MODULE SELECTED")
        Styler.label_style(Label_3,bg ="#ae9ff4",fg = "#000000",ft_size=12)
        Label_3.place(x=80,y=250,width=150,height=30)
        
        Label_4=tk.Label(self.frm3,text="STUDENT SELECTED")
        Styler.label_style(Label_4,bg ="#f0f0f0",fg = "#000000",ft_size=12)
        Label_4.place(x=20,y=105,width=150,height=30)
        
        self.ListBox_1=tk.Listbox(self,selectmode='multiple')
        Styler.list_box(self.ListBox_1)
        self.ListBox_1.place(x=80,y=290,width=150,height=100)
        
        self.combobox_2 = ttk.Combobox(self.frm3, state="normal",
                                     justify = 'center',)
        self.combobox_2.place(x=20,y=50,width=150,height=30)
        self.combobox_2.bind("<<ComboboxSelected>>", self.update_listbox_2)
        
        self.ListBox_2=tk.Listbox(self.frm3,selectmode='multiple')
        Styler.list_box(self.ListBox_2)
        self.ListBox_2.place(x=20,y=145,width=150,height=100)
    
        label_=tk.Label(self,text = "LOW ATTENDANCE MONITORING")
        Styler.label_style(label_, ft_size =20)
        label_.place(x=250,y=0,width=600,height=50)
        
        self.Button_4=tk.Button(self,text="DISPLAY TABLE",
                                command = lambda : 
                                          [self.plot_table(self.tab1,
                                          self.ListBox_1.get(0,tk.END)),
                                          self.show_tab_table()])
        Styler.button_style(self.Button_4)
        self.Button_4.place(x=80,y=420,width=150,height=30)
        
        self.Button_5=tk.Button(self.frm3,text="DISPLAY CHART",
                                command =lambda : [self.plot_chart(),
                                                   self.show_tab_chart()])
        Styler.button_style(self.Button_5)
        self.Button_5.place(x=20,y=275,width=150,height=30)
        
        self.canv = tk.Canvas(self.tab1, relief=tk.SUNKEN)
        self.canv.config(width=600, height=450, highlightthickness=0)
        self.sbar = tk.Scrollbar(self.tab1)
        self.sbar.config(command=self.canv.yview)
        self.canv.config(yscrollcommand=self.sbar.set)
        self.sbar.pack(side=tk.RIGHT,anchor="e",fill = "y")
        self.canv.pack(side= tk.TOP,fill = "y",anchor = "nw")
        self.canv.configure(scrollregion=self.canv.bbox("all"))
        
        self.label_frame = tk.Frame(self.canv)
        self.label_frame.bind("<Configure>", self.on_configure)
        self.canv.create_window((0, 0), window=self.label_frame, anchor='nw')
        self.label_frame.grid_rowconfigure(0, weight=1)

        Styler.refresh_button(self,controller)
        Styler.home_button(self,controller)

    
    def update_listbox_2(self,*args):
        """
        Method to update the listbox with selected student
        """
        if int(self.combobox_2.get()) in self.ListBox_2.get(0,tk.END):
            pass
        else:
            self.ListBox_2.insert(tk.END, int(self.combobox_2.get()))
    
    def update_listbox(self, *args):
        """
        Method to update the listbox with selected module
        """
        if self.combobox.get() in self.ListBox_1.get(0,tk.END):
            pass
        elif self.combobox.get() == "ALL MODULES" :
            self.ListBox_1.delete(0,tk.END)
            self.ListBox_1.insert(0, self.combobox.get())
        else:
            if self.ListBox_1.get(0) ==  "ALL MODULES":
                self.ListBox_1.delete(0)
                self.ListBox_1.insert(tk.END, self.combobox.get())
            else:
                self.ListBox_1.insert(tk.END, self.combobox.get())
    
    def on_configure(self, event):
        self.canv.configure(scrollregion=self.canv.bbox("all"))

    def plot_chart(self):
        """
        Method to call the poor attendance function and plot the graph
        of students with low attendance for the selected module. The function
        creates a canvas and packs the chart on to the canvas
        """
        try:
            self.canvas.get_tk_widget().destroy()
            self.fig.clf() 
        except:
            pass
        if self.ListBox_2.size()==0:
            if self.ListBox_1.get(0) == "ALL MODULES":
                self.mods = self.modules
            else:
                self.mods = list(self.ListBox_1.get(0,tk.END))
            self.df_final,self.fig = poor_attendance(sel_module =\
                                                         self.mods)
        else:
            self.df_final,self.fig = poor_attendance(list\
                                                        (self.ListBox_2.get\
                                                        (0,tk.END)),
                                              self.mods)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.tab2)
        self.canvas.get_tk_widget().pack(side="bottom",
                                         anchor="s",padx =0,
                                         pady=0)

    def plot_table(self,parent,mods):
        """
        Method displays the data of low attendance students and pack it onto a
        frame with labels.

        Parameters
        ----------
        parent : class
                 Parent widget for the table.
        mods :  list
                List of module names.

        Returns
        -------
        None.

        """
        if mods[0] == "ALL MODULES":
            self.mods = self.modules
        else:
            self.mods = list(mods) 
        self.df,plot = poor_attendance(sel_module = self.mods)
        self.combobox_2.config(values=list(self.df["Student_ID"][1:]))

        def create_button(df, x):
            """
            Creates a button with student ID as text display

            Parameters
            ----------
            df : Pandas dataframe
                Dataframe containing the students weekly attendance with
                poor average attendance.
            x : pandas dataseries
                dataseries of Student ID.

            Returns
            -------
            None.
            
            """
            def on_enter(e):
                "Method to change the color of button while hover"
                button.configure(bg = "#ae9ff4")
            def on_leave(e):
                "Method to change the color of button while hover"
                button.configure(bg = "#3d155b")
            button = tk.Button(self.label_frame, text=x,
                               command=lambda: on_button_click(self,x))
            button.grid(row=df[self.df["Student_ID"]==x].index[0]+1, column=0)
            button.configure(width=10, height=2,relief='raised',
                             bg="#3d155b", bd=1,fg="#ffffff",
                             justify = 'right')
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
            

        
        for i, row in enumerate(self.df.values):
            for j, value in enumerate(row):
                if j == 0:
                    continue
                self.label = tk.Label(self.label_frame, text=value)
                self.label.grid(row=i+1, column=j)
                self.label.configure(width=8, height=2,
                                     relief='ridge', bd=2,
                                     borderwidth=1)
                if isinstance(value, (int, float)):
                    if value > self.df.iloc[0,len(self.df.columns)-1]:
                        self.label.configure(bg="green")
                    else:
                        self.label.configure(bg='#e7e5e6')
                else:
                    self.label.configure(bg='#e7e5e6')
                    
        self.df["Student_ID"].apply(lambda x: create_button(self.df, x))
        

        for i, column_name in enumerate(self.df.columns):
            self.label = tk.Label(self.label_frame, text=column_name)
            self.label.grid(row=0, column=i,sticky = 'ew')
            self.label.configure(width=8, height=3,
                                 relief='flat', bd=1,
                                 bg="#3d155b", fg="#ffffff")
    
        def on_button_click(self, i):
            """
            

            Parameters
            ----------
            i : float
                Cell value which indicates the Student ID.

            Returns
            -------
            None.
            Updates the cell value to the listbox2
            """
            if i in self.ListBox_2.get(0,tk.END):
                pass
            else:
                self.ListBox_2.insert(tk.END,i)

        
    def show_tab_table(self):
        """
        Method to select the Chart tab upon clicking Display Chart button
        """
        self.notebook.select(0)
        
    def show_tab_chart(self):
        """
        Method to select the Chart tab upon clicking Display Chart button
        """
        self.notebook.select(1)
          
    def delete(self):
        """
        Method is used to clear the contents of the ListBox, LineEdit, and Combobox widgets on the page
        """
        try:
            self.ListBox_1.delete(0,"end")
        except:
            pass
        try:
            self.ListBox_2.delete(0,"end")
        except:
            pass
        try:
            self.LineEdit_1.delete(0,"end")
        except:
            pass
        try:
            self.LineEdit_2.delete(0,"end")
        except:
            pass

if __name__ == "__main__":
    app = tkinterApp() 
    app.mainloop()
    