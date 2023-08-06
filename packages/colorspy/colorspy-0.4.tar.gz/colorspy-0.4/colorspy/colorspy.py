from tkinter import *
from tkinter import colorchooser
import math

# All the main colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
lime = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
silver = (192, 192, 192)
gray = (128, 128, 128)
maroon = (128, 0, 0)
olive = (128, 128, 0)
green = (0, 128, 0)
purple = (128, 0, 128)
teal = (0, 128, 128)
navy = (0, 0, 128)
orange = (255, 165, 0)
dark_orange = (255, 69, 0)
golden = (218, 165, 32)
spring_green = (0, 250, 154)
dark_cyan = (0, 139, 139)
deep_sky_blue = (0, 191, 255)
indigo = (75, 0, 130)
pink = (255, 108, 180)
dark_pink = (255, 20, 147)
baby_pink = (255, 192, 203)
off_white = (255, 228, 196)
brown = (139, 69, 19)
chocolate = (210, 105, 30)
peach = (244, 164, 96)
slate_gray = (112, 128, 144)
turquoise = (64, 224, 208)
dark_red = (139, 0, 0)
firebrick = (178, 34, 34)
crimson = (220, 20, 60)
tomato = (255, 91, 71)
coral = (255, 127, 80)
indian_red = (255, 92, 92)
light_coral = (240, 128, 128)
dark_salmon = (233, 150, 122)
salmon = (250, 128, 114)
light_salmon = (255, 160, 122)
gold = (255, 215, 0)
dark_golden_rod = (184, 134, 11)
golden_rod = (218, 165, 32)
pale_golden_rod = (238, 232, 170)
dark_khaki = (189, 183, 107)
khaki = (240, 230, 140)
yellow_green = (154, 205, 50)
dark_olive_green = (85, 107, 47)
olive_drab = (107, 142, 35)
lawn_green = (124, 252, 0)
green_yellow = (173, 255, 47)
dark_green = (0, 100, 0)
lime_green = (50, 205, 50)
light_green = (144, 238, 144)
pale_green = (151, 252, 151)
dark_sea_green = (143, 188, 143)
sea_green = (46, 139, 87)
medium_aqua_marine = (0, 250, 154)
medium_sea_green = (69, 173, 113)
light_sea_green = (32, 178, 170)
dark_slate_gray = (47, 79, 79)
light_cyan = (224, 255, 255)
dark_turquoise = (0, 206, 209)
medium_turquoise = (72, 209, 204)
pale_turquoise = (175, 238, 238)
aqua_marine = (127, 255, 212)
powder_blue = (176, 224, 230)
cadet_blue = (95, 158, 160)
steel_blue = (70, 130, 180)
corn_flower_blue = (100, 149, 237)
dodger_blue = (30, 144, 255)
sky_blue = (135, 206, 250)
midnight_blue = (25, 25, 112)
medium_blue = (0, 0, 205)
royal_blue = (65, 105, 225)
blue_violet = (138, 43, 226)
dark_slate_blue = (72, 61, 139)
slate_blue = (106, 90, 205)
medium_slate_blue = (123, 104, 238)
medium_purple = (147, 112, 119)
dark_magenta = (139, 0, 139)
dark_violet = (148, 0, 211)
dark_orchid = (153, 50, 204)
medium_orchid = (186, 85, 211)
thistle = (216, 191, 216)
plum = (221, 160, 221)
violet = (238, 130, 238)
orchid = (218, 112, 214)
medium_violet_red = (199, 21, 133)
pale_violet_red = (219, 112, 147)
hot_pink = (255, 105, 180)
light_pink = (255, 182, 193)
antique_white = (250, 235, 215)
beige = (245, 245, 220)
balanced_almond = (255, 235, 205)
wheat = (245, 222, 179)
corn_silk = (255, 248, 220)
lemon_chiffon = (255, 250, 205)
light_golden_yellow_rod = (250, 250, 210)
light_yellow = (255, 255, 224)
sienna = (160, 82, 45)
peru = (205, 133, 63)
sandy_brown = (244, 164, 96)
burly_wood = (224, 184, 135)
tan = (210, 180, 140)
rosy_brown = (188, 143, 143)
moccasin = (255, 228, 181)
navajo_white = (255, 222, 173)
peach_puff = (255, 218, 185)
misty_rose = (255, 228, 255)
lavender_brush = (255, 240, 245)
linen = (250, 240, 230)
old_lace = (253, 254, 230)
papaya_whip = (255, 239, 213)
sea_shell = (255, 245, 238)
mint_cream = (245, 255, 250)
light_slate_gray = (119, 136, 153)
light_steel_blue = (176, 196, 222)
lavender = (230, 230, 250)
floral_white = (255, 250, 240)
alice_blue = (240, 248, 255)
ghost_white = (248, 248, 255)
honeydew = (240, 255, 240)
ivory = (255, 255, 240)
azure = (240, 255, 255)
snow = (255, 250, 250)
dim_gray = (105, 105, 105)
dark_gray = (169, 169, 169)
light_gray = (211, 211, 211)
gainsboro = (220, 220, 220)
white_smoke = (245, 245, 245)


# Functions/Classes

class ColorConverter:
    def __init__(self):
        self.rgb_list = []
        self.hex_list = []

    def rgb2hex(self, color, hash=True):
        self.rgb_list = []
        r, g, b = color
        for c in color:
            self.rgb_list.append(hex(c)[2:])
        for i, co in enumerate(self.rgb_list):
            if len(co) <= 1:
                self.rgb_list[i] = "0" + co

        if not hash:
            return self.rgb_list[0] + self.rgb_list[1] + self.rgb_list[2]

        return "#" + self.rgb_list[0] + self.rgb_list[1] + self.rgb_list[2]

    def hex2rgb(self, color):
        self.hex_list.clear()
        color_list = self.hex_list
        if '#' not in color:
            r, g, b = color[0:2], color[2:4], color[4:6]
        else:
            r, g, b = color[1:3], color[3:5], color[5:7]

        for i in range(256):
            if len(hex(i)[2:]) > 1:
                if hex(i)[2:] == r:
                    r = i
                    color_list.append(r)
            else:
                if "0" + hex(i)[2:] == r:
                    r = i
                    color_list.append(r)

        for j in range(256):
            if len(hex(j)[2:]) > 1:
                if hex(j)[2:] == g:
                    g = j
                    color_list.append(g)
            else:
                if "0" + hex(j)[2:] == g:
                    g = j
                    color_list.append(g)

        for k in range(256):
            if len(hex(k)[2:]) > 1:
                if hex(k)[2:] == b:
                    b = k
                    color_list.append(b)
            else:
                if "0" + hex(k)[2:] == b:
                    b = k
                    color_list.append(b)

        new_color = (color_list[0], color_list[1], color_list[2])
        return new_color


def color_picker(hex_value=True):
    root = Tk()
    root.title("Color Picker")

    color = colorchooser.askcolor()
    color_list = []

    new_color = (math.floor(color[0][0]), math.floor(color[0][1]), math.floor(color[0][2]))

    color_list.append(new_color)

    if hex_value:
        color_list.append(color[1])

    root.mainloop()

    return color_list
