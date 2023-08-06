from FaceSetBuilder.gui import *
from FaceSetBuilder.encode_faces import *
from FaceSetBuilder.cluster_faces import *


def start():
    dpath = input("Insert here the directory's path:\n").replace("\\ ", " ")
    if dpath[-1] == " ":
        dpath = dpath[:-1]

    root = Tk()

    app = App(root)
    app.place(relx=0, rely=0, relwidth=1, relheight=1)

    app.draw()

    encode(app, dpath)

    cluster(app)

    root.mainloop()


if __name__ == '__main__':
    start()
