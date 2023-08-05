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
orange = (266, 165, 0)
dark_orange = (255, 69, 0)
golden = (218, 165, 32)
spring_green = (0, 250, 154)
dark_cyan = (0, 139, 139)
sky_blue = (0, 191, 255)
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
				self.rgb_list[i] = "0"+co

		if not hash:
			return self.rgb_list[0]+self.rgb_list[1]+self.rgb_list[2]
		
		return "#"+self.rgb_list[0]+self.rgb_list[1]+self.rgb_list[2]

	def hex2rgb(self, color):
		color_list = []
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
				if "0"+hex(i)[2:] == r:
					r = i
					color_list.append(r)

		for j in range(256):
			if len(hex(j)[2:]) > 1:
				if hex(j)[2:] == g:
					g = j
					color_list.append(g)
			else:
				if "0"+hex(j)[2:] == g:
					g = j
					color_list.append(g)

		for k in range(256):
			if len(hex(k)[2:]) > 1:
				if hex(k)[2:] == b:
					b = k
					color_list.append(b)
			else:
				if "0"+hex(k)[2:] == b:
					b = k
					color_list.append(b)

		new_color = (color_list[0], color_list[1], color_list[2])
		return new_color