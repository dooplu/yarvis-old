# yarvis

Yarvis is a python project in which we attempt to approximate the hologram tech from the [iron man movies](https://youtu.be/WNu6fRo_7fg)

(work in progress)

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

`cd` into the src folder and run `main.py`, you should see two windows, one with your webcam feed and the other with the output. Drag the output window to your projector (if you have one set up).

# Things to do

- Get Yusuf's audio assistant to interact with note taking. This was really one of the first things that even inspired me to do this project, I had so many stickynotes around my office at one point and they'd fall off, be hard to modify, so I asked myself, what if I had digital sticky notes? and you see where we are now. The problem is, this is very close to being done, but because as you'll see in later points, alot of work at to be done before this could even be attempted.
- Drawing in air. This is the other main reason I started this project. I do not own a white board, I would like one. But what if I could make a cooler one for free? (free up until I buy a projector...). This project is essentially a workflow tool, for jotting down ideas quickly along with some goodies. 
- Fix the requirements.txt file, currently it has all the dependencies of the main like 5 packages we initially used.
- Refactor alot of the code, this is the biggest project we've tackled so far and we learned so much, there's alot I (Adam) would like to move around and redo
- Ideally, make a version 2. Python is good for all the machine learning and gesture recognition stuff, but it's limited in the graphics aspect, a version 2 would entail sending all the hand information to something like unity, where time would not be wasted on making a lot of common functionality from scratch (like a lerp function)

See our [Trello](https://trello.com/b/HLfzcOHO/yarvis) for more.
# Credit:
Getting the hand gestures is done with the help of Kazuhito00's [gesture recognition with mediapipe](https://github.com/Kazuhito00/hand-gesture-recognition-using-mediapipe)

# License



MIT License

Copyright (c) 2022 Adam Dia

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
