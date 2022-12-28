import speech_recognition as sr
import pyttsx3 as tts
import threading
import sys

from neuralintents import GenericAssistant

class Assistant:
  
  def __init__(self):
    self.recognizer = sr.Recognizer()
    self.speaker = tts.init()
    self.speaker.setProperty("rate", 150)
    
    # dict to attribute every tag from json file to its method in class
    self.mapping = {"note": self.createNote}
    
    self.assistant = GenericAssistant("commands.json", intent_methods=self.mapping)
    
    ##################################################################################################
    #self.assistant.train_model()
    #self.assistant.save_model()
    self.assistant.load_model()
    
    # starts a thread
    threading.Thread(target=self.runAssistant).start()

  def createNote(self):
    # assistent asks what to write in note
    self.speaker.say("what do you want to write on your note?")
    self.speaker.runAndWait()
  
    done = False
    
    # check to verify if task is complete
    while not done:
      try:
        with sr.Microphone() as mic:
          # duration allowed for moment of silence
          self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
          # listening to audio
          audio = self.recognizer.listen(mic)
          
          # convert audio to text
          note = self.recognizer.recognize_google(audio)
          note = note.lower()
          
          self.speaker.say("what should i call the note?")
          self.speaker.runAndWait()
          
          self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
          audio = self.recognizer.listen(mic)
          
          filename = self.recognizer.recognize_google(audio)
          filename = filename.lower()
          
        # creates txt file with filename given and writes the note inside
        with open(filename+".txt", "w") as f:
          f.write(note)
          done = True
          self.speaker.say(f"i have successfully created the note {filename}")
          self.speaker.runAndWait()
          
      # if sr does not recognize the audio it will redo the while loop    
      except sr.UnknownValueError:
        self.recognizer
        self.speaker.say("i did not understand. please try again")
        self.speaker.runAndWait()

  def runAssistant(self):
    while True:
      
      try:
        with sr.Microphone() as mic:
          self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
          audio = self.recognizer.listen(mic)
          
          text = self.recognizer.recognize_google(audio)
          text = text.lower()
          
          # if hotword is found, assistent will start to listen to user
          if "orange" in text:
            print("listening...")
            audio = self.recognizer.listen(mic)
            text = self.recognizer.recognize_google(audio)
            text = text.lower()
            
            # if user says stop, assistent will terminate
            if text == "stop":
              self.speaker.say("bye")
              self.speaker.runAndWait()
              self.speaker.stop()
              sys.exit()
            
            # assistent will go through json file looking for the tag based on user's request
            # assistent will print or execute response
            else:
              if text is not None:
                response = self.assistant.request(text)
                if response is not None:
                  self.speaker.say(response)
                  self.speaker.runAndWait()
              print("stopped")
      except:
        print("stopped")
        continue

Assistant()