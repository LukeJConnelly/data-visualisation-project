to_and_from_colour = [("#1a9641", "#d7191c"), ("#1b9e77", "#d95f02")]

colour_blind_mode = False

def get_colours():
    return to_and_from_colour[colour_blind_mode]

def set_colour_blind_mode(mode):
    global colour_blind_mode
    colour_blind_mode = mode

default_chart_height = "19vh"

default_bg_color = "#D4DADC"

get_neutral_colour = lambda: "#7570b3"