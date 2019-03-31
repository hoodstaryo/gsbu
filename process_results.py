#!/usr/bin/python2

import re
import sys


def get_color(red, green, blue):
    if (245 <= red <= 255) and (0 <= green <= 10) and (0 <= blue <= 10):
        return "red"

    elif (0 <= red <= 10) and (245 <= green <= 255) and (0 <= blue <= 10):
        return "green"

    elif (245 <= red <= 255) and (245 <= green <= 255) and (245 <= blue <= 255):
        return "white"

    else:
        raise Exception("Invalid color: srgb({}, {}, {})".format(red, green, blue))


def parse_result(result):
    match = re.match(
        r"^Frame: (\d+) Client: srgb\((\d{1,3}),(\d{1,3}),(\d{1,3})\) Host: srgb\((\d{1,3}),(\d{1,3}),(\d{1,3})\)\n$",
        result,
    )

    [
        frame,
        client_red,
        client_green,
        client_blue,
        host_red,
        host_green,
        host_blue,
    ] = map(int, match.groups())

    client_color = get_color(client_red, client_green, client_blue)
    host_color = get_color(host_red, host_green, host_blue)

    return (frame, client_color, host_color)


def main():
    results_file = open(sys.argv[1])
    results = map(parse_result, results_file)
    results_file.close()

    #
    client_input_frames = []
    host_input_frames = []
    last_client_color = None
    last_host_color = None

    for (frame, client_color, host_color) in results:
        if last_client_color == "white" and client_color == "green":
            client_input_frames.append(frame)

        if last_host_color == "white" and host_color == "green":
            host_input_frames.append(frame)

        last_client_color = client_color
        last_host_color = host_color

    #
    client_input_count = len(client_input_frames)
    host_input_count = len(host_input_frames)

    if client_input_count != host_input_count:
        raise Exception(
            "Invalid input count. Client inputs: {} Host Inputs: {}".format(
                client_input_count, host_input_count
            )
        )

    #
    input_frames = zip(client_input_frames, host_input_frames)

    for (client_input_frame, host_input_frame) in input_frames:
        print(client_input_frame - host_input_frame)


main()
