from imutils import paths
import cv2
from face_recognition import face_locations, face_encodings
from FaceSetBuilder.constants import *
from pickle import dumps
from os import mkdir
from os.path import join


def encode(app, dpath):
    try:
        mkdir(CROPPED_FACES_PATH)
    except FileExistsError:
        print("[ERROR] Delete the directory CroppedFaces first.")
        exit()

    imagePaths = list(paths.list_images(dpath))
    cascade = cv2.CascadeClassifier(CASCADE_PATH)

    counter = 0
    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # loading image to BGR
        image = cv2.imread(imagePath)

        # converting image to RGB format
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            crop_img = image[y:y + h, x:x + w]
            cv2.imwrite(join(CROPPED_FACES_PATH, f"{counter}.png"), crop_img)
            counter += 1

    imagePaths = list(paths.list_images(CROPPED_FACES_PATH))
    data = []

    num_op = len(imagePaths) + 4
    app.set_k(num_op)

    for (i, imagePath) in enumerate(imagePaths):
        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        app.update_text("Processing image {}/{}".format(i + 1, len(imagePaths)))
        app.draw()

        # loading image to BGR
        image = cv2.imread(imagePath)

        # ocnverting image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_locations(image, model="cnn")

        # compute the facial embedding for the face
        encodings = face_encodings(image, boxes)

        # build a dictionary of the image path, bounding box location,
        # and facial encodings for the current image
        d = [{"imagePath": imagePath, "loc": box, "encoding": enc} for (box, enc) in zip(boxes, encodings)]
        data.extend(d)

    # dump the facial encodings data to disk
    app.update_text("Serializing encodings...")
    app.draw()

    f = open(ENCODINGS_PATH, "wb")
    f.write(dumps(data))
    f.close()

    app.update_text("Encodings of images saved in {}".format(ENCODINGS_PATH))
    app.draw()
