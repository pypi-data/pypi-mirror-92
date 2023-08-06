from sklearn.cluster import DBSCAN
from imutils import build_montages
import numpy as np
import pickle
import cv2
from os import mkdir, rename
from os.path import join
from FaceSetBuilder.constants import *
from PIL.Image import open as open_
from PIL.Image import ANTIALIAS
from PIL.ImageTk import PhotoImage
from tkinter import IntVar


def save(app, var):
    name = app.top.entry.get()
    app.top.entry.delete(0, "end")
    rename(CURRENT_LABEL_PATH, join(CWD, name))
    var.set(1)


def cluster(app):
    app.update_text("Loading encodings...")
    app.draw()

    data = pickle.loads(open(ENCODINGS_PATH, "rb").read())
    data = np.array(data)
    encodings = [d["encoding"] for d in data]

    app.update_text("Clustering...")
    app.draw()

    clt = DBSCAN(n_jobs=-1)
    clt.fit(encodings)

    labelIDs = np.unique(clt.labels_)

    numUniqueFaces = len(np.where(labelIDs > -1)[0])
    app.update_text("Number of unique faces: {}".format(numUniqueFaces))
    app.complete_draw()
    app.top.show_entry()
    app.top.show_button()
    app.master.update()

    # loop over the unique face integers
    for labelID in labelIDs:
        # find all indexes into the `data` array that belong to the
        # current label ID, then randomly sample a maximum of 25 indexes
        # from the set

        if labelID == -1:
            continue

        idxs = np.where(clt.labels_ == labelID)[0]

        # initialize the list of faces to include in the montage
        faces = []

        mkdir(CURRENT_LABEL_PATH)
        var = IntVar()

        # loop over the sampled indexes
        for i in idxs:
            # load the input image and extract the face ROI
            image = cv2.imread(data[i]["imagePath"])
            (top, right, bottom, left) = data[i]["loc"]
            face = image[top:bottom, left:right]

            # putting the image in the clustered folder
            filename = str(i) + '.jpg'
            cv2.imwrite(join(CURRENT_LABEL_PATH, filename), image)

            # force resize the face ROI to 96x96 and then add it to the
            # faces montage list
            face = cv2.resize(face, (96, 96), interpolation=cv2.INTER_AREA)
            faces.append(face)

        # create a montage using 96x96 "tiles" with 5 rows and 5 columns
        if len(faces) > 25:
            faces = faces[:25]

        montage = build_montages(faces, (96, 96), (5, 5))[0]
        path_montage = join(CURRENT_LABEL_PATH, "montage.jpg")
        cv2.imwrite(path_montage, montage)

        # show the montage and ask for the subject's name
        app.show_square()

        raw_img = open_(path_montage)
        img = raw_img.resize((app.w, app.w), ANTIALIAS)
        img_tk = PhotoImage(img)

        app.master.img_tk = img_tk
        app.square.create_image(0, 0, anchor="nw", image=img_tk)

        app.top.entry.insert(0, "Name this subject here and confirm.")

        app.top.confirm.command = lambda *args: save(app, var)

        app.master.wait_variable(var)

    print("You labelled every unique face I've found.\n")
    exit()
