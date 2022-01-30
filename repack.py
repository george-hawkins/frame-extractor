#!/usr/bin/env python3
import argparse
import os
import sys

from shared import run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--frame-rate", required=True, help="output frame rate, e.g. 25 or 24000/1001")
    parser.add_argument("--output", required=True, help="the output video file name, e.g. video.mkv")
    parser.add_argument("frames_glob", help="glob for input frames, e.g. 'frames/*.png' (don't forget the quotes)")
    args = parser.parse_args()

    glob = args.frames_glob
    output = args.output

    _, ext = os.path.splitext(glob)

    # For some reason, ffmpeg won't accept 'frames/*' but does accept 'frames/*.png'.
    if ext == "":
        sys.exit("the glob must include a file extension, eg. 'frames/*.png'")

    create_video = ["ffmpeg", "-y",
                    "-framerate", args.frame_rate,
                    "-pattern_type", "glob",
                    "-i", glob,
                    "-c:v", "libx264", "-preset", "slow", "-crf", "22",
                    "-pix_fmt", "yuv420p",  # Oddly, `vlc` chokes without this.
                    output
                    ]

    print(f"generating {output}...")
    run(create_video)


if __name__ == "__main__":
    main()
