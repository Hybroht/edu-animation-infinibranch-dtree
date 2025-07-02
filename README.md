# Endless Growing Decision Tree Animation

This script generates a simple, ever-branching decision tree animation using Pygame. The decision tree will continuously grow, and once it reaches a certain level, the animation will slide to the bottom node on the right border before continuing to grow from that point.

![Decision Tree Animation](output.gif)

## Features
- Endless growth of the decision tree.
- Smooth animation transitions.

## How the Animation Works
1. The decision tree branches out indefinitely.
2. Upon reaching a specified level, the animation slides to the bottom node located at the right border.
3. The tree continues to grow from this position.

## How to use the code
1. infinibranch.py will generate the frames needed for the animation. Once enough frames are created, you have to end the animation.
2. frames_to_gif.py will concat the frames into a simple animation.

## Libraries Used
- pygame: For creating the animation.
- PIL (Pillow): For image processing.
- glob: For file handling.

## Reference
This animation was presented in the following article:

[Self-Similar Choices — Mandelbrot’s Angel of Fractals & Necessity](https://medium.com/@hybroht/self-similar-choices-mandelbrots-angel-of-fractals-necessity-5e7256414eb2)