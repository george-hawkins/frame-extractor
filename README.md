Frame extractor
===============

No additional Python libraries are needed, so a venv is not required.

Help:

```
$ ./unpack.py --help
...
$ ./repack.py --help
...
```

Unpacking
---------

Output frames 1 to 10 of `clip.mkv` to the directory `frames` (creating the directory if necessary):

```
$ ./unpack.py 1 10 clip.mkv frames
```

The interval is closed, i.e. the result will be frames 1 to 10 inclusive.

The resulting files will be named `frames/frame-0001.png` to `frames/frame-0010.png`.

It's convention whether the first frame in the video is called frame 1 or frame 0.

By default, numbering starts from 1. If you prefer to start from 0 - you can extract the same set of frames like so:

```
$ ./unpack.py --zero-based 0 9 clip.mkv frames
```

The resulting files will be named `frames/frame-0000.png` to `frames/frame-0009.png`.

If omitted, `start` defaults to the first frame and `end` defaults to the last frame.

Note: the output file name numbering always starts from 1 (or 0 if using `zero-based`), i.e. the original frame number is not used. 

Numbering
---------

If you want the frame number to be overlayed as text onto each output image:

```
$ ./unpack.py --numbered 10 20 clip.mkv frames
```

Note: the overlayed frame number will always starts from 1 (or 0 if using `zero-based`), i.e. the original frame number is not used. 


Repacking
---------

To repack the frames into a high quality H.264 video file:

```
$ ./repack.py --frame-rate=24 --output=repacked.mkv 'frames/*.png'
```

**Important:** the final argument in _not_ a glob to be expanded by the shell, it's a glob that will be passed to `ffmpeg`, so it must be enclosed in quotes.

`ffmpeg` requires that the glob contains a file extension - so it will accept e.g. `frames/*.png` but not `frames/*`.

If required, you can specify the frame rate as a fraction:

```
$ ./repack.py --frame-rate=24000/1001 --output=repacked.mkv 'frames/*.png'
```

Minor bug
---------

There seems to be a bug in Python's `argparse` help output (in Python 3.8.10 at least). It `-f` and `--foo` style arguments as optional even if you specified them as mandatory.

E.g. here it claims the `--frame-rate` and `--output` are optional:

```
$ ./repack.py --help
usage: repack.py [-h] --frame-rate FRAME_RATE --output OUTPUT frames_glob

positional arguments:
  frames_glob           glob for input frames, e.g. 'frames/*.png' (don't forget the quotes)

optional arguments:
  -h, --help            show this help message and exit
  --frame-rate FRAME_RATE
                        output frame rate, e.g. 25 or 24000/1001
  --output OUTPUT       the output video file name, e.g. video.mkv
```

But if you omit them, it complains (as expected):

```
$ ./repack.py 'frames/*.png'
usage: repack.py [-h] --frame-rate FRAME_RATE --output OUTPUT frames_glob
repack.py: error: the following arguments are required: --frame-rate, --output
```
