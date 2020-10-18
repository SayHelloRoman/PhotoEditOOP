from tkinter import filedialog as fd, messagebox	
from tkinter import *
from PIL import Image, ImageTk, ImageFilter, ImageOps
from PIL.ImageFilter import (
	BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
	EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN, GaussianBlur, ModeFilter
	)
import os
import sys
import keyboard


class window:
	def __init__(self):

		#настройка окна
		self.root = Tk()
		self.root.title("PhotoEdit")
		self.root.minsize( width = 1600, height = 900 )
		self.root.maxsize( width = 2560, height = 1440 )
		self.root.geometry("1600x900+100+20")

		#Виджет menu

		self.mainmenu = Menu(self.root) 
		
		self.filemenu = Menu(self.mainmenu, tearoff=0)
		self.help_ = Menu(self.mainmenu, tearoff=0)

		self.filemenu.add_command(label="Open                      Ctrl + Y", command = self.open)
		self.filemenu.add_command(label="Save                        Ctrl + S", command = self.save, state= DISABLED)
		

		self.help_.add_command(label="Reload photo            Ctrl + R", command = self.reload_photo, state= DISABLED)

		self.mainmenu.add_cascade(label="File", menu=self.filemenu)
		self.mainmenu.add_cascade(label="Help", menu=self.help_)
		self.mainmenu.add_command(label="Program", command=self.program)

		self.root.config(menu=self.mainmenu)

		#Главный екран
		self.Image_main = Label(bd = 1, relief = "solid")

		self.information_label = Label(relief = "solid", bd = 2, font = "arial 20")

		
		self.filter()
		
		

		keyboard.add_hotkey('Ctrl + y', self.open)
		


		


	#функция mainloop
	def mainloop(self):
		self.root.mainloop()

	#функция открытия изображения
	def open(self, event = None):
		self.image_name = fd.askopenfilename(filetypes=(("Image Files", "*.png *.jpg *.jpeg *.TIFF *.bmp *.dib"),
		("All files", "*.*") ))

		if self.image_name == "":

			messagebox.showerror(title="Error", message="You have not selected a photo")

		else:
			self.img = Image.open(self.image_name)

			self.img_copy = self.img

			#Изменяем размер
			self.width, self.height = self.img.size

			if self.width >= 500:
				if self.width >= 1000:
					self.width_new = self.width / 2
				else:
					self.width_new = self.width / 1.5
				

			if self.height >= 500:
				if self.height >= 1000:
					self.height_new = self.height / 2
				else:
					self.height_new = self.height / 1.5

			self.img_copy = self.img_copy.resize((int(self.width_new), int(self.height_new)), Image.ANTIALIAS)
				
			

			self.imgTK = ImageTk.PhotoImage(self.img_copy)
			self.Image_main["image"] = self.imgTK
			self.Image_main.image = self.imgTK

			self.reset_buttons()

			self.Image_main.pack(expand=1)

			#bind
			self.blur_button.bind("<Button-1>", self.blur_)
			self.Drawn_button.bind("<Button-1>", self.Drawn_)
			self.Contour_button.bind("<Button-1>", self.Contour_)
			self.GrayScale_button.bind("<Button-1>", self.GrayScale_)
			self.SMOOTH_MORE_button.bind("<Button-1>", self.Smooth_)

			self.width_100 =self.width_new / 100
			self.height_100 = self.height_new / 100	

			self.init_clear()
			
			self.zoom()

			self.filemenu.entryconfigure(2, state= NORMAL)
			self.help_.entryconfigure(1, state= NORMAL)

			keyboard.add_hotkey('Ctrl + s', self.save)

			keyboard.add_hotkey('Ctrl + r', self.reload_photo)

	
			#self.save_c["state"] = NORMAL

			self.plus_b.bind("<Button-1>", self.plus)
			self.minus_b.bind("<Button-1>", self.minus)
			self.reload.bind("<Button-1>", self.update_photo)

	def reload_photo(self):

		self.img_copy = self.img

		#Изменяем размер
		self.width, self.height = self.img.size

		if self.width >= 500:
			if self.width >= 1000:
				self.width_new = self.width / 2
			else:
				self.width_new = self.width / 1.5
				

		if self.height >= 500:
			if self.height >= 1000:
				self.height_new = self.height / 2
			else:
				self.height_new = self.height / 1.5

		self.img_copy = self.img_copy.resize((int(self.width_new), int(self.height_new)), Image.ANTIALIAS)

		self.imgTK = ImageTk.PhotoImage(self.img_copy)
		self.Image_main["image"] = self.imgTK
		self.Image_main.image = self.imgTK
				

	def filter(self):
		#blur
		self.blur_button = Button(text = "BLUR", font = "Arial 12", bd = 1, relief = "solid", width = 12, bg = "#535057", fg = "white")
		self.blur_button.pack(anchor=NW)

		#Drawn
		self.Drawn_button = Button(text = "Drawn", font = "Arial 12", bd = 1, relief = "solid", width = 12, bg = "#535057", fg = "white")
		self.Drawn_button.pack(anchor=NW)

		#conrour
		self.Contour_button = Button(text = "Contour", font = "Arial 12", bd = 1, relief = "solid", width = 12, bg = "#535057", fg = "white")
		self.Contour_button.pack(anchor=NW)

		#Gray
		self.GrayScale_button = Button(text = "Gray", font = "Arial 12", bd = 1, relief = "solid", width = 12, bg = "#535057", fg = "white")
		self.GrayScale_button.pack(anchor=NW)

		#Smooth
		self.SMOOTH_MORE_button = Button(text = "Smooth", font = "Arial 12", bd = 1, relief = "solid", width = 12, bg = "#535057", fg = "white")
		self.SMOOTH_MORE_button.pack(anchor=NW)

	def save(self):
		self.img_copy = self.img_copy.resize((int(self.width), int(self.height)), Image.ANTIALIAS)

		save_name= fd.asksaveasfilename(initialfile = "File.png",filetypes=(("PNG", "*.png"),("JPEG", "*.jpeg"),("TIFF", "*.tiff"),("BMP", "*.bmp")), defaultextension='.png')

		self.img_copy.save(save_name, "png")	

		self.reset_buttons()

		self.img_copy = self.img

		self.img_copy = self.img_copy.resize((int(self.width_new), int(self.height_new)), Image.ANTIALIAS)

		self.imgTK = ImageTk.PhotoImage(self.img_copy)

		self.Image_main["image"] = self.imgTK
		self.Image_main.image = self.imgTK

	def program(self):
		window = Toplevel(self.root)
		window.title("Program")
		window.resizable(width = False, height = False)
		window.geometry("700x400")

		info_programm = Label(window, text = """The program was written in Python using the following modules: pillow, os, sys, Tkinter.
			 \nAuthor: SayHelloRoman. This program was written to replace PhotoEdit 1.2 using OOP only.
			 \nPhotoEdit was my program for one contest, I wrote it for 3 days.
			\nI hope this program will have good functionality and a good program will be published.
			\nThe one who read this thanks to you and good luck.""", justify = LEFT, font = "arial 13")

		info_programm.pack(side = LEFT, anchor = N)

	def blur_(self, event):
		self.img_copy = self.img_copy.filter(GaussianBlur(radius=10))

		imgTK = ImageTk.PhotoImage(self.img_copy)

		self.blur_button['bg'] = "black"

		self.Image_main["image"] = imgTK
		self.Image_main.image = imgTK


	def Drawn_(self, event):
		self.img_copy = self.img_copy.filter(ModeFilter(size=9))

		imgTK = ImageTk.PhotoImage(self.img_copy)

		self.Drawn_button['bg'] = "black"

		self.Image_main["image"] = imgTK
		self.Image_main.image = imgTK

	def Contour_(self, event):
		self.img_copy = self.img_copy.filter(CONTOUR())

		imgTK = ImageTk.PhotoImage(self.img_copy)

		self.Contour_button['bg'] = "black"

		self.Image_main["image"] = imgTK
		self.Image_main.image = imgTK

	def GrayScale_(self, event):
		self.img_copy = self.img_copy.convert('LA')

		imgTK = ImageTk.PhotoImage(self.img_copy)

		self.GrayScale_button['bg'] = "black"

		self.Image_main["image"] = imgTK
		self.Image_main.image = imgTK

	def Smooth_(self, event):
		self.img_copy = self.img_copy.filter(SMOOTH_MORE())

		imgTK = ImageTk.PhotoImage(self.img_copy)

		self.SMOOTH_MORE_button['bg'] = "black"

		self.Image_main["image"] = imgTK
		self.Image_main.image = imgTK

	def reset_buttons(self):
		self.blur_button["bg"] = "#535057"
		self.Drawn_button["bg"] = "#535057"
		self.Contour_button["bg"] = "#535057"
		self.GrayScale_button["bg"] = "#535057"
		self.SMOOTH_MORE_button['bg'] = "#535057"

	def zoom(self):

		self.plus_b = Button(text = "+", font = "arial 20", bd = 2, relief = "solid", width = 3, height = 1)
		self.plus_b.pack(anchor=S, side = RIGHT, padx = 2)

		self.minus_b = Button(text = "-", font = "arial 20", bd = 2, relief = "solid", width = 3, height = 1)
		self.minus_b.pack(anchor=S, side = RIGHT)

	def init_clear(self):
		self.reload = Button(text = "🔄", font = "arial 20", bd = 2, relief = "solid", width = 3, height = 1)
		self.reload.pack(anchor=S, side = RIGHT)


	def update_photo(self, event):

		self.img_copy = self.img

		self.img_copy = self.img_copy.resize((int(self.width_new), int(self.height_new)), Image.ANTIALIAS)

		self.imgTK = ImageTk.PhotoImage(self.img_copy)

		self.Image_main["image"] = self.imgTK
		self.Image_main.image = self.imgTK

		self.reset_buttons()

		

	def plus(self, event):

		self.width_new = self.width_new + self.width_100
		self.height_new = self.height_new + self.height_100

		self.img_copy = self.img_copy.resize((int(self.width_new), int(self.height_new)), Image.ANTIALIAS)

		self.imgTK = ImageTk.PhotoImage(self.img_copy)

		self.Image_main["image"] = self.imgTK
		self.Image_main.image = self.imgTK

	def minus(self, event):

		self.width_new = self.width_new - self.width_100
		self.height_new = self.height_new - self.height_100

		self.img_copy = self.img_copy.resize((int(self.width_new), int(self.height_new)), Image.ANTIALIAS)

		self.imgTK = ImageTk.PhotoImage(self.img_copy)

		self.Image_main["image"] = self.imgTK
		self.Image_main.image = self.imgTK

#за то работает	
	
win = window()
win.mainloop()