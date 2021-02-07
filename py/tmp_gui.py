import sys
import tkinter
from PIL import Image, ImageTk

def tmp_gui():
    root = tkinter.Tk()

    root.title("( * v * )")
    root.resizable(False, False)
    root.geometry("480x360")
    
    button = tkinter.Button(text = "Click and Quit", command = root.quit)
    button.pack(fill = 'x', padx=60, pady=30)
    
    root.mainloop()

# -------------------------------------------------

if __name__ == '__main__':
    tmp_gui()
    print('俺たちの旅はまだ始まったばかり…')
    #os.system('PAUSE')