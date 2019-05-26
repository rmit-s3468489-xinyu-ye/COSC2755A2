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
from MyError import InvalidOptionError
from dashboard_config import root_url

#root_folder = "dataset"
#detection_method = "hog"
#classifier = "haarcascade_frontalface_default.xml"

class AuthorizedFacialReconition:
    """
    This class is used for implementing the facial recognition login

    """
    def __init__(self,classifier="haarcascade_frontalface_default.xml",
    root_folder="dataset",encoding_file="encodings.pickle",resolution=240,
    detection_method="hog"):
        """
        Classifier used for recognizing the different state of face. 

        root_folder is the name of the folder used for storing photos. 

        encoding_file is the name of pickle file. 

        the default resolution is 240. 

        dectection_method can be hog or cnn.

        """

        self.root_folder = root_folder
        self.detection_method = detection_method
        self.classifier = classifier
        self.encoding_file = encoding_file
        self.resolution = resolution

    def record_user_face(self,username):
        """
        record a specific person's photo and store it by using his/her username.
        a person's photo cannot have more than 10 records, enter 'c' to continue and 'q' to exit

        """

        # Create a new folder for the specific user
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
                key = input("Press 'q' to quit or 'c' to continue: ")
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
        """
        Encode all photos of the user into a pickle file, in order to 
        not affecting the main thread, this task will add a work thread 
        to finish.

        """
        # Get the paths to the input images in our dataset
        imagePaths = list(paths.list_images(self.root_folder))
        # Initialize the list of known encodings and known names
        knownEncodings = []
        knownNames = []
        # Loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # Extract the person's name from the image path
            name = imagePath.split(os.path.sep)[-2]
            # Load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Detect the (x, y)-coordinates of the bounding boxes
            # for each corresponding face in the input image
            boxes = face_recognition.face_locations(rgb, model = self.detection_method)
            # Compute the facial encodings for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
            # Loop over the encodings
            for encoding in encodings:
                # Add each encoding + name to the set of known names and encodings
                knownEncodings.append(encoding)
                knownNames.append(name)
        # Dump the facial encodings + names to disk
        data = { "encodings": knownEncodings, "names": knownNames }
        with open(self.encoding_file, "wb") as f:
            f.write(pickle.dumps(data))

    def recognise_user_face(self):
        """
        Recognise the user face, if the face is found already exists in the folder, 
        return the corresponding user name, otherwise return None.

        """
        # Load the known faces and encodings
        data = pickle.loads(open(self.encoding_file, "rb").read())
        # Initialize the video stream and warm up the camera sensor
        print("[INFO] Starting video stream up...")
        vs = VideoStream(src = 0).start()
        time.sleep(2.0)
        # Set a counter to count the maximum record of a user's photos
        face_counter = 0
        # Loop over frames from the video file stream
        while face_counter < 10:
            # Get the frame from the threaded video stream
            frame = vs.read()
            # Convert the input frame from BGR to RGB then resize it to have
            # a width of 750px (to speed up processing)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(frame, width = self.resolution)

            # detect the (x, y)-coordinates of the bounding boxes
            # for each corresponding face in the input frame, then compute
            # the facial encodings for each face
            boxes = face_recognition.face_locations(rgb, model = self.detection_method)
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []

            # Loop over the facial encodings
            for encoding in encodings:
                # Attempt to match each face in the input image to the known encodings
                matches = face_recognition.compare_faces(data["encodings"], encoding)
                name = None

                # Check if a match is found
                if True in matches:
                    # Find the indices of all matched faces then initialize a
                    # dictionary to count the total number of times each face was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # Loop over the matched indices and maintain a counter for
                    # each recognized face
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    # Determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select the first entry in the dictionary)
                    name = max(counts, key = counts.get)

                # Update the list of names
                names.append(name)
            
             # Loop over the recognized faces
            for name in names:
                # Print to console, for an identified person
                if name is not None:
                    vs.stop()
                    return name
                # Sleep the cam
                time.sleep(3.0)

            face_counter += 1

        print("No matched user has been found!")
        vs.stop()
        return name
    




