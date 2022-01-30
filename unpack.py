#!/usr/bin/env python3
import argparse
import os
import sys

from shared import run


def get_frame_rate(video_file):
    frame_rate = run(["ffprobe", "-v", "error", "-select_streams", "v", "-of", "default=noprint_wrappers=1:nokey=1", "-show_entries", "stream=r_frame_rate", video_file])
    num, denom = frame_rate.split("/")
    return int(num) / int(denom)


def get_drawtext(offset):
    font = "fontfile=Arial.ttf: fontsize=72: fontcolor=white"
    box = "box=1: boxcolor=0x00000099"
    pos = "x=(w-tw)/2: y=h-(2*lh)"
    # Applying an offset to the frame number is covered here: https://trac.ffmpeg.org/ticket/1949
    text = f"text=%{{eif\\\\:n+{offset}\\\\:d}}"

    return f"drawtext={font}: {box}: {pos}: {text}"


def main():
    # See https://docs.python.org/3/howto/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, help="start frame (inclusive)")
    parser.add_argument("--end", type=int, help="end frame (inclusive)")
    parser.add_argument("--numbered", action="store_true", help="include frame number as text in extracted frames")
    parser.add_argument("--zero-based", action="store_true", help="number frames from 0 rather than 1")
    parser.add_argument("video_file", help="the input video file")
    parser.add_argument("output_dir", help="output directory for extracted frames")
    args = parser.parse_args()

    video_file = args.video_file
    output_dir = args.output_dir
    start = args.start
    end = args.end

    if not os.path.isfile(video_file):
        sys.exit(f"{video_file} does not exist")

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
        print(f"created directory '{output_dir}' as it did not already exist")

    # By default, frame numbering starts from 0 but file numbering starts from 1.
    # So specify both explicitly to make them consistent.
    if args.zero_based:
        offset = 0
    else:
        offset = 1

    if start is None:
        start = offset

    # Sanity check that e.g. the 0th frame isn't requested when number is from 1.
    if start < offset:
        sys.exit(f"the start frame must be {offset} or greater")

    frame_rate = get_frame_rate(video_file)
    print(f"frame rate is {frame_rate:.3f}")

    start_time = (start - offset) / frame_rate
    print(f"start time is {start_time:.3f}s")

    extraction = ["ffmpeg", "-ss", start_time, "-i", video_file, "-start_number", offset]

    if end is not None:
        count = 1 + end - start
        print(f"frame count is {count}")
        extraction.extend(["-frames:v", count])

    if args.numbered:
        extraction.extend(["-vf", get_drawtext(offset)])

    extraction.append(f"{output_dir}/frame-%04d.png")

    print("extracting frames...")
    run(extraction)


if __name__ == "__main__":
    main()
