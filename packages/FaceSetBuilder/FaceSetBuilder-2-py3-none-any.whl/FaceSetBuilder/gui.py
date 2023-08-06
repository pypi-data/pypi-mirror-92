from tkinter import *
from FaceSetBuilder.myTkinter import myButton


class Front(Frame):
    def __init__(self, master, w, h):
        super().__init__(master, bg='#295a75', width=w, height=h)

        self.info = None
        self.bar = None
        self.entry = None
        self.confirm = None

        self.set_layout()

    def set_layout(self):
        self.info = Label(self, background='#295a75', foreground="#defffc", anchor="w", text="Quantifiying images...")
        self.info.place(relx=0.045, rely=0.07, relwidth=0.91, relheight=0.19, anchor='nw')

        self.bar = Canvas(self, highlightthickness=0, bd=0, selectborderwidth=0, background='#557282')
        self.bar.place(relx=0.045, rely=0.323, relwidth=0.91, relheight=0.23, anchor='nw')

        self.entry = Entry(self, background='#557282', highlightthickness=0, foreground="#defffc",
                           justify="center", bd=0, selectborderwidth=0)

        self.confirm = myButton(self, text="Confirm")

    def show_entry(self):
        self.entry.place(relx=0.25, rely=0.675, relwidth=0.5, relheight=0.195, anchor='nw')

    def show_button(self):
        self.confirm.place(relx=0.789, rely=0.649, relwidth=0.165, relheight=0.243, anchor='nw')


class App(Frame):
    def __init__(self, master):
        super().__init__(master, bg='#295a75')
        self.master = master

        screen_w, screen_h = master.winfo_screenwidth(), master.winfo_screenheight()
        self.w, self.h, self.h2 = int(0.3177 * screen_w), int(0.1574 * screen_h), int(0.7222 * screen_h)
        self.x, self.y = int(0.375 * screen_w), int(0.0926 * screen_h)
        master.geometry(f"{self.w}x{self.h}+{self.x}+{self.y}")
        master.title("")

        self.top = None
        self.square = None
        self.master = master
        self.progress = -1
        self.k = 1

        self.set_layout()

    def set_layout(self):
        self.top = Front(self, self.w, self.h)
        self.top.pack(side=TOP)

        self.square = Canvas(self, background="#557282")
        self.square.pack(side=TOP, fill=BOTH, expand=1)

    def show_square(self):
        self.master.geometry(f"{self.w}x{self.h2}+{self.x}+{self.y}")

    def hide_square(self):
        self.master.geometry(f"{self.w}x{self.h}+{self.x}+{self.y}")

    def set_k(self, num_op):
        self.k = int(0.91 * self.w) // num_op

    def draw(self):
        if self.progress == -1:
            self.progress = self.k
        height = int(0.23 * self.h)
        self.top.bar.create_rectangle(0, 0, self.progress, height, fill="#defffc", outline="#defffc")
        self.master.update()
        self.progress += self.k

    def complete_draw(self):
        height = int(0.23 * self.h)
        self.top.bar.create_rectangle(0, 0, int(0.91 * self.w), height, fill="#defffc", outline="#defffc")

    def update_text(self, txt):
        self.top.info.configure(text=txt)


if __name__ == '__main__':
    root = Tk()

    a = App(root)
    a.place(relx=0, rely=0, relwidth=1, relheight=1)

    a.top.confirm.command = lambda *args: a.draw()
    a.set_k(10)
    a.top.show_button()

    root.mainloop()
