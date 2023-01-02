import speech_recognition as sr
import pyttsx3 as tts
import threading
import os

from neuralintents import GenericAssistant

def voiceRecognition():
  
  recognizer = sr.Recognizer()
  speaker = tts.init()
  speaker.setProperty("rate", 150)
  
  colours = {"red":(0, 0, 255), "orange":(0, 150, 255), "yellow":(0, 255, 255), "green":(0, 255, 0), "blue":(255, 0, 0), "purple":(255, 0, 200)}
  
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
          audio = recognizer.listen(mic, None)
          
          # convert audio to text
          text = recognizer.recognize_google(audio)
          text = text.lower()
          
          speaker.say("what color should the note be?")
          speaker.runAndWait()
          
          recognizer.adjust_for_ambient_noise(mic, duration=0.2)
          audio = recognizer.listen(mic, None, 2.5)
          
          colourText = recognizer.recognize_google(audio)
          colourText = colourText.lower()
          
          words = colourText.split(" ")
          
          for word in words:
            if word in colours.keys():
              colour = colours.get(word, "blue")
          
          writeString = "{}\n{},{},{}".format(text, colour[0], colour[1], colour[2])

        
        # creates txt file with filename given and writes the note inside
        with open("save/s.txt", "w") as f:
          f.write(writeString)
          done = True
          speaker.say(f"i have successfully created the note")
          speaker.runAndWait()
          
        os.rename("save/s.txt", "save/sticky.txt")
          
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
          audio = recognizer.listen(mic, None, 5)
          
          text = recognizer.recognize_google(audio)
          text = text.lower()
          
          # if hotword is found, assistent will start to listen to user
          if text == "virtual assistant":
            print("listening...")
            speaker.say("how can i help you")
            speaker.runAndWait()
            audio = recognizer.listen(mic, None, 5)
            text = recognizer.recognize_google(audio)
            text = text.lower()
            
            # if user says stop, assistent will terminate
            if "stop" in text:
              speaker.say("Have a good day")
              speaker.runAndWait()
              break
            
            # assistent will go through json file looking for the tag based on user's request
            # assistent will print or execute response
            else:
              if text is not None:
                response = assistantmodel.request(text)
                if response is not None:
                  speaker.say(response)
                  speaker.runAndWait()
              print("stopped")
      except:
        print("stopped")
        continue
  
  mapping = {"note": createNote}

  assistantmodel = GenericAssistant("commands.json", intent_methods=mapping)
  
  assistantmodel.load_model()
  
  threading.Thread(target=runAssistant()).start()


voiceRecognition()