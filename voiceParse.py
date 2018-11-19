#Let's attempt to import the speech recgonition library.
try:
    import speech_recognition as sr
except:
    sys.exit("Error importing libraries. Install 'speech_recognition'")

#When it works, we can initialize the main objects for the recognition

try:
    recognize = sr.Recognizer()
    microphone = sr.Microphone()
except:
    sys.exit("Could not load objects required for speech recognition.")

#Listen timeout in seconds
TIMEOUT = 5

#A simple function that sets the ambient noise level to ease recognition.
def initSpeech():
    with microphone as source:
        recognize.adjust_for_ambient_noise(source)

#A function that parses the voice of the user.
def parseVoice():
    #This is where we stored the text
    parsedText = ""
    voice = ""
    try:
    #Now we can listen. We stored the resulting audio in the voice variable.
        with microphone as source:
            voice = recognize.listen(source, TIMEOUT, 10)
    #Now, let's attempt to parse the result using the Google speech recognition
    #API. The fall back for all cases is to just have the user input variable
    #keyboard what they want to say.
    except sr.WaitTimeoutError:
        print("listening error found")
    try:
        print("listening...")
        parsedText = recognize.recognize_google(voice)
    except sr.UnknownValueError:
        print("The Google Speech Recognition API could not recognize speech.(sr.UnknownValueError)")
        #parsedText = input("Please type message instead:")
        parsedText = parseVoice()
    except sr.RequestError as error:
        print("Could not contact Google Speech Recognition API. Error: {0}"\
        .format(error))
        #parsedText = input("Please type message instead: ")
        parsedText = parseVoice()
    except sr.WaitTimeoutError as error:
        print("The Google Speech Recognition API could not recognize speech.{0}".format(error))
        parsedText = parseVoice()
        #parsedText = input("Please type message instead:")
    #We return the recognized or inputted text.
    return parsedText