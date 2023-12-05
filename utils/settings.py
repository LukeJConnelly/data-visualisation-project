to_and_from_colour = [("#1a9641", "#d7191c"), ("#E66100", "#5D3A9B")]

colour_blind_mode = False

def get_colours():
    return to_and_from_colour[colour_blind_mode]

def set_colour_blind_mode(mode):
    global colour_blind_mode
    colour_blind_mode = mode