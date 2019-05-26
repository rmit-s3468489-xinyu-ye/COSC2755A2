from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2
from dashboard_config import db, ma, app
from flask import Flask, request,jsonify
from gcloud_crud import *
import requests,json
from dashboard_config import root_url

class BarRecognition:
    """
    This class assembles the barcode recognition functions.
    """
    def add_barcode(self):
        """
        Return barcode data which has been recognized by the webcam, 
        attempt 10 times, if a correct barcode icon is not found, 
        it will return a None for barcodeData.
        """

        # Initialize the video stream and warm up the camera sensor
        print("[INFO] starting video stream...")
        vs = VideoStream(src = 0).start()
        time.sleep(2.0)
        barcodeData = None
        barcodeType = None
        temp_number = 0
        while temp_number < 10:
            # Get the frame from the threaded video stream and resize it to
	        # have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width = 400)
            # Find the barcodes in the frame and decode each of them
            barcodes = pyzbar.decode(frame)
            # Loop over the detected barcodes
            for barcode in barcodes:
                # The barcode data is a bytes object so convert it to a string
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type

                if barcodeData is not None and barcodeType is not None:
                    break
            if barcodeData is not None and barcodeType is not None:
                break
            # Wait a little while before scanning again
            time.sleep(1)
            temp_number += 1

        print("[INFO] Cleaning up...")
        vs.stop()
        return barcodeData

    def recognize_barcode(self,barcodedata):
        """
        determine which bookID this barcodedata belongs to, 
        if such a bookID is found, then return the bookID, otherwise 
        return -1

        """
        print(barcodedata)
        data = Book.query.filter(Book.BarcodeData==barcodedata).first()
        print(data)
        if data:
            return data.BookID
        else:
            return -1
    
    def add_to_database(self):
        """
        Use the Flask restful API to modify the barcode data in the table book, 
        actually, when inserting data to table book, the barcode field is empty, this 
        function can be regarded as adding a barcode to the book(that is already in the table book).
        """
        url = root_url + "/book/b/"
        barcode = self.add_barcode()
        book_title = input("Please enter book title: ")
        book_author = input("Please enter book author: ")
        book_published = input("Please enter book publish date: ")
        send_data = {"Title":book_title,"Author":book_author,"PublishedDate":book_published,"BarcodeData":barcode}
        requests.put(url,data=json.dumps(send_data),headers={'Content-Type': 'application/json'})
        print("Successfully added this book!")

if __name__ =="__main__":
    BarRecognition().add_to_database()
