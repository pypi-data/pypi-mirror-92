from os import getcwd
from os.path import split, join
from pathlib import Path


CLUSTERING_RESULT_PATH = split(Path(__file__))[0]
CWD = getcwd()

FACE_DATA_PATH = join(CLUSTERING_RESULT_PATH, 'face_cluster')
ENCODINGS_PATH = join(CLUSTERING_RESULT_PATH, 'encodings.pickle')
CASCADE_PATH = join(CLUSTERING_RESULT_PATH, 'haarcascade_frontalface_default.xml')
CROPPED_FACES_PATH = join(CWD, "CroppedFaces")
CURRENT_LABEL_PATH = join(CWD, "CurrentLabel")

