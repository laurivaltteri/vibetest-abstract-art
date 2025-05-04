# Abstract Art Generator (v0.2.0)

This package generates abstract art images and animations by drawing random shapes.

## Getting Started

Install dependencies and create a virtual environment with Poetry:
```bash
poetry install
```

(Optional) Activate the virtual environment:
```bash
poetry shell
```

## Usage

Generate a single image:
```bash
art-gen --width 1024 --height 768 --num-shapes 200 --seed 42 --palette pastel \
  --distribution cluster --clusters 4 --cluster-radius 150 \
  --gradient --gradient-colors #ffdddd #ddddff \
  --noise --noise-scale 0.2 --fractal-trees 2 --output art.png
```

Create an animated GIF (e.g. 20 frames, 0.2s per frame):
```bash
art-gen --width 800 --height 600 --num-shapes 100 --seed 0 \
  --frames 20 --duration 0.2 --output art.gif
```

Available palettes: random, pastel, earth, duochrome, grayscale.  
Shape distributions: uniform, cluster, radial.  
Blend modes: normal, multiply, screen.

Run `art-gen --help` for full options.