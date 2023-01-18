import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb


class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        menubutton = ttk.Menubutton(text="Select Module", bootstyle="outline")
        menu = tk.Menu(menubutton, tearoff=False)
        menubutton.configure(menu=menu)
        menubutton.pack(padx=10, pady=10)

        self.choices = {}
        for choice in ("Iron Man", "Superman", "Batman"):
            self.choices[choice] = tk.IntVar(value=0)
            menu.add_checkbutton(label=choice, variable=self.choices[choice],
                                 onvalue=1, offvalue=0,
                                 command=self.printValues)
    def printValues(self):
        for name, var in self.choices.items():
            print("%s: %s" % (name, var.get()))


if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()