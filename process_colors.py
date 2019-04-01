import re
import subprocess


def get_imagemagick_colors():
    # Sometimes ImageMagick returns names like "black", others it returns srgbs
    # like "srgb(0,0,0)". This function returns a dictionary that maps names to
    # srgbs.
    proc = subprocess.Popen(
        ["identify", "-list", "color"], stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )

    (stdout, stderr) = proc.communicate()

    #
    matches = re.finditer(
        r"""
    ([0-9A-Za-z]+)
    [ ]+
    (srgb\(\d{1,3},\d{1,3},\d{1,3}\))""",
        stdout,
        re.VERBOSE,
    )

    #
    colors = {}

    for match in matches:
        (color_name, color_srgb) = match.groups()
        colors[color_name] = color_srgb

    return colors


def parse_colors_file():
    colors = []
    imagemagick_colors = get_imagemagick_colors()

    with open("colors") as colors_file:
        for line in colors_file:
            [_, frame, _, client_color, _, host_color] = line.split()
            frame = int(frame)

            if client_color in imagemagick_colors:
                client_color = imagemagick_colors[client_color]

            client_color = parse_srgb(client_color)

            if host_color in imagemagick_colors:
                host_color = imagemagick_colors[host_color]

            host_color = parse_srgb(host_color)
            colors.append((frame, client_color, host_color))

    return colors


def parse_srgb(srgb):
    # Returns "red", "green", or "white" if the srgb is red-ish, green-ish,
    # or white-ish. We allow -ish colors because sometimes the colors are a
    # little off in recordings.
    match = re.match(r"^srgb\((\d{1,3}),(\d{1,3}),(\d{1,3})\)$", srgb)
    [r, g, b] = map(int, match.groups())

    if (245 <= r <= 255) and (0 <= g <= 10) and (0 <= b <= 10):
        return "red"

    elif (0 <= r <= 10) and (245 <= g <= 255) and (0 <= b <= 10):
        return "green"

    elif (245 <= r <= 255) and (245 <= g <= 255) and (245 <= b <= 255):
        return "white"

    raise Exception("Invalid srgb: " + srgb)


def main():
    colors = parse_colors_file()

    # Find input frames.
    #
    # An input frame is a frame that indicates that input was received. In our
    # case Masher and Mashee turn green on input so a frame is an input frame
    # if the previous frame is white and the current frame is green.
    client_input_frames = []
    host_input_frames = []
    prev_client_color = None
    prev_host_color = None

    for (frame, client_color, host_color) in colors:
        if prev_client_color == "white" and client_color == "green":
            client_input_frames.append(frame)

        if prev_host_color == "white" and host_color == "green":
            host_input_frames.append(frame)

        prev_client_color = client_color
        prev_host_color = host_color

    # Ensure that the host and client received the same number of inputs. This
    # is mostly to ensure that I didn't push a button while recording and send
    # the client an extra input but I imagine at some point a client will drop
    # an input.
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
