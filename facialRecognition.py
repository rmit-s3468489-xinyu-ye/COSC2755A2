# USAGE
# With default parameter of user/id
#       python3 01_capture.py -n default_user
# OR specifying the dataset and user/id
#       python3 02_capture.py -i dataset -n default_user

## Acknowledgement
## This code is adapted from:
## https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826

# import the necessary packages
from imutils.video import VideoStream
from imutils import paths
import imutils
import time
import face_recognition
import pickle
import cv2
import os, json, requests
from customisedError import InvalidOptionError
from dashboardConfig import root_url

#root_folder = "dataset"
#detection_method = "hog"
#classifier = "haarcascade_frontalface_default.xml"

class AuthorizedFacialReconition:
    def __init__(self,classifier="haarcascade_frontalface_default.xml",
    root_folder="dataset",encoding_file="encodings.pickle",resolution=240,
    detection_method="hog"):
        self.root_folder = root_folder
        self.detection_method = detection_method
        self.classifier = classifier
        self.encoding_file = encoding_file
        self.resolution = resolution
    def record_user_face(self,username):
        # Create a new folder for the new name
        folder = "./{}/{}".format(self.root_folder,username)
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Start the camera
        cam = cv2.VideoCapture(0)
        # Set video width
        cam.set(3, 640)
        # Set video height
        cam.set(4, 480)
        # Get the pre-built classifier that had been trained on 3 million faces
        face_detector = cv2.CascadeClassifier(self.classifier)

        img_counter = 0
        while img_counter < 10:
            try:
                key = input("Press q to quit or c to continue: ")
                if key == "q":
                    break
                if key == "c":
                    ret, frame = cam.read()
                    if not ret:
                        break
                    
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_detector.detectMultiScale(gray, 1.3, 5)

                    if(len(faces) == 0):
                        print("No face detected, please try again")
                        continue
                    
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        img_name = "{}/{:04}.jpg".format(folder, img_counter)
                        cv2.imwrite(img_name, frame[y : y + h, x : x + w])
                        print("{} written!".format(img_name))
                        img_counter += 1
                else:
                    raise InvalidOptionError()
            except InvalidOptionError as ioe:
                print(ioe)
        cam.release()

    def encode_user_face(self):
        # grab the paths to the input images in our dataset
        imagePaths = list(paths.list_images(self.root_folder))
        # initialize the list of known encodings and known names
        knownEncodings = []
        knownNames = []# loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            name = imagePath.split(os.path.sep)[-2]
            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb, model = self.detection_method)

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
            
            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and encodings
                knownEncodings.append(encoding)
                knownNames.append(name)
        # dump the facial encodings + names to disk
        data = { "encodings": knownEncodings, "names": knownNames }
        with open(self.encoding_file, "wb") as f:
            f.write(pickle.dumps(data))
    def recognise_user_face(self):

        # load the known faces and embeddings
        data = pickle.loads(open(self.encoding_file, "rb").read())

        # initialize the video stream and then allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        vs = VideoStream(src = 0).start()
        time.sleep(2.0)
        #set a counter to count the maximum time of the figuring
        face_counter = 0
        # loop over frames from the video file stream
        while face_counter < 10:
            # grab the frame from the threaded video stream
            frame = vs.read()

            # convert the input frame from BGR to RGB then resize it to have
            # a width of 750px (to speedup processing)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(frame, width = self.resolution)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input frame, then compute
            # the facial embeddings for each face
            boxes = face_recognition.face_locations(rgb, model = self.detection_method)
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"], encoding)
                name = "**__##"

                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key = counts.get)

                # update the list of names
                names.append(name)

        # loop over the recognized faces
            for name in names:
                # print to console, identified person
                if name != "**__##":
                    vs.stop()
                    return name
                # Set a flag to sleep the cam for fixed time
                time.sleep(3.0)
            
            face_counter += 1
        print("Person did not find!")
        # do a bit of cleanup
        vs.stop()
        return name
    




