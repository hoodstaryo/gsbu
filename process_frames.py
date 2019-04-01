#!/usr/bin/python2

from multiprocessing import Pool, cpu_count
import glob
import re
import subprocess

CLIENT_X = 100
CLIENT_Y = 540
HOST_X = 1820
HOST_Y = 980


def process_frame(frame):
    # Get frame number.
    match = re.search(r"(\d+)", frame)
    frame_number = match.group(1)
    frame_number = int(frame_number)

    # Get colors at (CLIENT_X, CLIENT_Y) and (HOST_X, HOST_Y).
    proc = subprocess.Popen(
        [
            "convert",
            frame,
            "-format",
            "%[pixel:p{{{}, {}}}] %[pixel:p{{{}, {}}}]".format(
                CLIENT_X, CLIENT_Y, HOST_X, HOST_Y
            ),
            "info:-",
        ],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    (stdout, stderr) = proc.communicate()

    match = re.match(
        r"^(srgb\(\d{1,3},\d{1,3},\d{1,3}\)) (srgb\(\d{1,3},\d{1,3},\d{1,3}\))$", stdout
    )

    (client_color, host_color) = match.groups()

    #
    return (frame_number, client_color, host_color)


def main():
    frames = glob.iglob("frames/frame*.png")

    number_of_procs = cpu_count()
    pool = Pool(number_of_procs)

    results = pool.map(process_frame, frames)
    results.sort()

    for result in results:
        print("Frame: {} Client: {} Host: {}".format(*result))


main()
