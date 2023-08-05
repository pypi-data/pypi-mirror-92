# animaty

## Description

animaty is a library for animating ASCII art inside the console. It is made
for both Windows and Linux.

## Installation

To install animaty just run the following command:

```bash
pip install animaty
```

After that, you can import animaty with

```py
from animaty import *
```

## Documentation

### animaty.helpers

```py
getFramesFromFile(file) -> Frame
```

getFramesFromFile lets you extract frames from a file
(The frames in the file must be seperated by a double-newline)

### animaty.animate.Frame

The Frame class is used to represent each frame in an animation. It implements getters and setters, I think those need no further explanation.

```py
Frame(content, time=1)
```

The content variable describes what the Frame displays, while the time variable sets how long the frame has to be displayed (in seconds).

### animaty.animate.Animator

The Animator class is responsible for animating the previously created frames

```py
Animator(frames, fps=None)
```

The frames variable is an array of Frame() instances which will be displayed. The fps variable represents the frames per seconds. If set, the Animator() instance will ignore any time set inside of the given Frame() instances.

```py
animate() -> None
```

animate starts an animation based on previously entered frames

```py
animationLoop() -> None
```

animationLoop starts an infinite animation based on previously entered frames

## Examples

```py
from animaty import *

frames = getFramesFromFile("test.txt")
animator = Animator(frames)
animator.animate()
```

First the animaty module gets imported. After that,a frames array is created the *getFramesFromFile* method, which is then passed into an Animator instance. Finally, the *animate* method is called, which starts an animation.

```py
from animaty import *

frames = [Frame("just", 0.2), Frame("some", 0.3), Frame("text", 0.4)]
animator = Animator(frames)
animator.animate()
```

This example is really similair to the previous one, the only difference is that we create a Frame array manually, which gives us some more control over the time the frames are displayed.

To achieve a similair amount of control in example one as in example two, you can use a syntax like this:

```py
frames[0].setFrametime(0.2)
```

## How to contribute

If you want to contribute to this Project, just request an issue on [my Github](https://github.com/GaiaHacking/).
