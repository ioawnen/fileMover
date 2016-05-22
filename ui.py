import Tkinter
from Tkconstants import *

def createUI():
	tk = Tkinter.Tk()
	frame = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
	frame.pack(fill=BOTH, expand=1, ipadx=5, ipady=5)

	title_label = Tkinter.Label(frame, text="fileMover UI")
	title_label.pack(fill=X, expand =1)

	list_canvas = Tkinter.Canvas(frame, background='WHITE', borderwidth=2)
	list_canvas.pack(fill=X, padx=5, pady=5)

	save_button = Tkinter.Button(frame, text="Save",command=tk.destroy)
	save_button.pack(side=BOTTOM)


	check_now_button = Tkinter.Button(frame, text="Check Now",command=tk.destroy)
	check_now_button.pack(side=BOTTOM)






	tk.mainloop()


def main():
	print "UI START"
	createUI()






main()