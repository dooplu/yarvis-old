# yarvis

Yarvis is a python project in which we attempt to approximate the hologram tech from the [iron man movies](https://youtu.be/WNu6fRo_7fg)

![yarvis in action](https://github.com/dooplu/yarvis/blob/main/showcase.gif)
The showcase gif might take a while to load, for an immediate demonstration check out the [showcase.gif](https://github.com/dooplu/yarvis-old/blob/main/showcase.gif) on our GitHub repository

# Description

This project stems from my lack of a whiteboard, and the fragile and temporary nature of sticky notes. Also it's cheaper than a hololens :).
The main idea is that since we cannot stop and manipulate light midair as seen on film, the closest thing we can do (with what's available to us) is using gesture recognition and a projector.
Of course there are simpler ways to do this, such as microsoft's hololens or VR, but that is a little out of our price range. But more importantly, it defeats the purpose. We don't want it to get in the way of whatever else we're doing. The reason I came up with this in the first place was so I could plan projects and set up little reminders for myself as I'm working with my hands or programming. It should be completely unobtrusive.

To achieve all this we use [OpenCV](https://opencv.org/) and Google's [MediaPipe](https://google.github.io/mediapipe/), along with some gesture recognition software by [Kazuhito00](https://github.com/Kazuhito00), to do the gesture recognition. And then using OpenCV's built in GUI capabilites to do all the drawing.

The name comes from an inside joke: Yusuf in english is Joseph, in turn Jarvis with an arabic pronounciation would be Yarvis.

# Requirements
- [Python 3.9.13](https://www.python.org/downloads/release/python-3913/)
- A webcam
- Ideally a projector
- Patience

# Installation

First off clone the repository to anywhere on your computer using:
```
git clone https://github.com/dooplu/yarvis
```

Then, create a virtual environment using [python 3.9.13](https://www.python.org/downloads/release/python-3913/) and activate it.

Finally, `cd` into the repository and install the required packages with:
```
pip install -r requirements.txt
```

# Usage

Open two terminals, in each of them activate the virtual environment. 

`cd` into the src folder on both terminals and run `main.py` and `assistant.py`, you should see two windows, one with your webcam feed and the other with the output window, as well as a terminal output showing what you are saying. Drag the output window to your projector (if you have one set up).

To create a new sticky note, say out loud "virtual assistant" and wait for a response. After the virtual assistant responds with "How can I help you?", tell it "write a note", "write me a note", "make a note" or some variation of that sentence. You will be asked what do you want there to be written on the note, it will stop when you stop. Additionally, you can say "new line" to add a linebreak. You will then be prompted for a colour. You can repond with "the colour " plus any of the following colours: red, orange, yellow, green, blue, purple.

To manipulate objects on screen, move your hand to the desired location (a cursor will help you indicate where your hand is). When you are on an object that you wish to move, close your hand into a pinching gesture (see gif for reference) and drag the object while holding that motion. When you want to let go and leave the object there, open your hand completely and move the cursor away. We are aware that occasionally it may be janky, so be sure to make your hand gestures obvious. Additionally, the background and your hand have a good contrast.

Try not to let two widgets overlap, we have not implemented only grabbing one object at a time, so if you do this, they will become stuck ontop of each other, making it hard or even impossible to seperate them. 

To end the programs, simply press escape with either the camera feed or output window open. And for the virtual assistant, call it with "virtual assistant", and say some variation of "stop the program" (command should include the world stop).

We understand this is an odd way to operate, however, we found it impossible to get both programs to run from one file concurrently.

# Things to do / What we learned

- This was our biggest programming project so far. A lot of features we wanted to implement had to be scrapped just for the sake of finishing (such as drawing and displaying the weather). Additionally, it is not organized in the most elegant way possible. In the future, we should take alot of time to plan an adequate file hierarchy, but this isn't to say that we haven't learned immensively since we embarked on this endeavour.
- We plan on either revisiting and improving in the future, or making a version 2. Progress was heavily slowed down by the fact that alot of the UI systems had to be made from scratch as we thought OpenCV's graphics capabilities were sufficient for our needs (we were wrong), however this gave us alot of insight on how to build software systems from the ground up.
- Obtaining a projector

See our [Trello](https://trello.com/b/HLfzcOHO/yarvis)

# Credit
Getting the hand gestures is done with the help of Kazuhito00's [gesture recognition with mediapipe](https://github.com/Kazuhito00/hand-gesture-recognition-using-mediapipe)

# License



MIT License

Copyright (c) 2022 Adam Dia

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
