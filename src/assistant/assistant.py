import speech_recognition as sr
import pyttsx3 as tts
import threading
import sys

from neuralintents import GenericAssistant

recognizer = sr.Recognizer()
speaker = tts.init()
speaker.setProperty("rate", 150)

def createNote():
  # assistent asks what to write in note
  speaker.say("what do you want to write on your note?")
  speaker.runAndWait()

  done = False
  
  # check to verify if task is complete
  while not done:
    try:
      with sr.Microphone() as mic:
        # duration allowed for moment of silence
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        # listening to audio
        audio = recognizer.listen(mic)
        
        # convert audio to text
        note = recognizer.recognize_google(audio)
        note = note.lower()
        
        speaker.say("what should i call the note?")
        speaker.runAndWait()
        
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)
        
        filename = recognizer.recognize_google(audio)
        filename = filename.lower()
        
      # creates txt file with filename given and writes the note inside
      with open(filename+".txt", "w") as f:
        f.write(note)
        done = True
        speaker.say(f"i have successfully created the note {filename}")
        speaker.runAndWait()
        
    # if sr does not recognize the audio it will redo the while loop    
    except sr.UnknownValueError:
      recognizer
      speaker.say("i did not understand. please try again")
      speaker.runAndWait()

def runAssistant():
  while True:
    
    try:
      with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)
        
        text = recognizer.recognize_google(audio)
        text = text.lower()
        
        # if hotword is found, assistent will start to listen to user
        if "orange" in text:
          print("listening...")
          audio = recognizer.listen(mic)
          text = recognizer.recognize_google(audio)
          text = text.lower()
          
          # if user says stop, assistent will terminate
          if text == "stop":
            speaker.say("bye")
            speaker.runAndWait()
            speaker.stop()
            sys.exit()
          
          # assistent will go through json file looking for the tag based on user's request
          # assistent will print or execute response
          else:
            if text is not None:
              response = assistant.request(text)
              if response is not None:
                speaker.say(response)
                speaker.runAndWait()
            print("stopped")
    except:
      print("stopped")
      continue


# dict to attribute every tag from json file to its method in class
mapping = {"note": createNote}

assistant = GenericAssistant("commands.json", intent_methods=mapping)

##################################################################################################
#assistant.train_model()
#assistant.save_model()
assistant.load_model()

# starts a thread
threading.Thread(target=runAssistant()).start()