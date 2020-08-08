# importing face library
import face_recognition
import cv2
import numpy as np
# importing file manager
import re
import os
# Importation of PI Camera
# Importation of Door
#import Door
from time import sleep

PATH_FACE_IMAGES = "faces/"

# Load a sample picture and learn how to recognize it.

known_face_encodings = []
known_face_names = []
known_faces_filenames = []

for (dirpath, dirnames, filenames) in os.walk(PATH_FACE_IMAGES):
    known_faces_filenames.extend(filenames)
    break



for filename in known_faces_filenames:
    # Load all faces and learn how to recognize it.
    face = face_recognition.load_image_file(PATH_FACE_IMAGES + filename)
    known_face_names.append(re.sub("[0-9]", '', filename[:-4]))
    known_face_encodings.append(face_recognition.face_encodings(face)[0])



# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
video_capture = cv2.VideoCapture(0)

while True:
    verification_face = False

    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]
    # Only process every other frame of video to save time

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"


            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                for faceName in face_names:
                    if name == faceName and verification_face == False:
                        verification_face = True
                        Door.open()
                        print("Opening Door !")
                face_names.append(name)
    process_this_frame = not process_this_frame
    count_img = 0
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # cv2.contourArea()
        # count_img += 1
        # rec = frame[top:(top - right) * bottom, right:]
        # cv2.imwrite("Inconnue" + str(count_img) + ".png", rec)

    cv2.imshow('Domotic SmartDoor', frame)

    if verification_face == True:
        sleep(15)  # number seconds before locking the door
        cv2.putText(frame, "Closed Door !")
        Door.close()
        # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
