import tkinter
import customtkinter

def tmp_gui():
    root = tkinter.Tk()

    root.title("( * v * )")
    root.resizable(False, False)
    root.geometry("480x360")
    
    button = tkinter.Button(text = "Click and Quit", command = root.quit)
    button.pack(fill = 'x', padx=60, pady=30)
    
    root.mainloop()

def test():
    
    customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
    #customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
    customtkinter.set_default_color_theme("./custom_theme.json")

    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.geometry("480x360")
    app.title("CustomTkinter simple_example.py")

    def button_function():
        print("button pressed")

    # Use CTkButton instead of tkinter Button
    button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
    button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    app.mainloop()

# -------------------------------------------------

if __name__ == '__main__':
    #tmp_gui()
    test()
    print('俺たちの旅はまだ始まったばかり…')
    #os.system('PAUSE')