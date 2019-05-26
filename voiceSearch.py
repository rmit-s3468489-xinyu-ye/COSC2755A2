import speech_recognition
import subprocess, requests
from dashboardConfig import root_url


#MIC_NAME = "Sound Blaster Play! 3: USB Audio (hw:1,0)"
class VoiceRecognition:
    def __init__(self,mic_name):
        self.mic_name = mic_name
    
    def getSearchText(self,prompt):
        # To test searching without the microphone uncomment this line of code
        # return input("Enter the first name to search for: ")
        
        device_id = None
        # Set the device ID of the mic that we specifically want to use to avoid ambiguity
        for i, microphone_name in enumerate(speech_recognition.Microphone.list_microphone_names()):
            if(microphone_name == self.mic_name):
                device_id = i
                break

        # obtain audio from the microphone
        r = speech_recognition.Recognizer()
        with speech_recognition.Microphone(device_index = device_id) as source:
            # clear console of errors
            subprocess.run("clear")

            # wait for a second to let the recognizer adjust the
            # energy threshold based on the surrounding noise level
            r.adjust_for_ambient_noise(source)

            print(prompt)
            try:
                audio = r.listen(source, timeout = 1.5)
            except speech_recognition.WaitTimeoutError:
                return None

        # recognize speech using Google Speech Recognition
        SearchText = None
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            SearchText = r.recognize_google(audio)
        except(speech_recognition.UnknownValueError, speech_recognition.RequestError):
            pass
        finally:
            return SearchText
