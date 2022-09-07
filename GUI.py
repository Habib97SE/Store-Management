import tkinter as tk


class GUI:
    def __init__(self, title="GUI"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.mainloop()

    def create_label(self, text, row, column):
        label = tk.Label(self.root, text=text)
        label.grid(row=row, column=column)
        return label

    def create_entry(self, row, column):
        entry = tk.Entry(self.root)
        entry.grid(row=row, column=column)
        return entry
