import tkinter
from tkinter import END, filedialog
import customtkinter
from PIL import Image, ImageTk

from functions import *

customtkinter.set_appearance_mode("Dark")  
customtkinter.set_default_color_theme("dark-blue")

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Result Preview")
        self.geometry("1200x600")
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.image_preview_label = customtkinter.CTkLabel(self, text="")
        self.image_preview_label.grid(row = 0, column = 0, columnspan = 2, sticky="n")

        # reading Image from CV2 to PIL
        self.image = Image.fromarray(app.result_image)

        #WIDTH CHECK
        if self.image.size[0] > 448 :
            preview_img = resize_image_by_width(self.image, 448)
        else:
            preview_img = self.image

    
        img_aux = customtkinter.CTkImage(dark_image = preview_img, size = preview_img.size)
        self.image_preview_label.configure(image=img_aux, fg_color="transparent", text="")

        # BACK/ SAVE BUTTON

        self.back_button = customtkinter.CTkButton(self, text="Back",command=self.back_trigger)
        self.back_button.grid(row=1, column=0, padx=20, pady=10, sticky = "n")

        self.save_button = customtkinter.CTkButton(self, text="Save",command=self.save_trigger)
        self.save_button.grid(row=1, column=1, padx=20, pady=10, sticky = "n")
        
    def back_trigger(self):
        self.destroy()

    def save_trigger(self):
        # Saving sel.image (PIL)
        save_img_to_path(self.image, './images/result.png')
        self.image_preview_label.destroy()
        self.save_button.destroy()
        self.back_button.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky = "n")

        self.save_label = customtkinter.CTkLabel(self, text="The image was saved in the 'Images' folder. Thanks for using the app!")
        self.save_label.grid(row = 0, column = 0, columnspan = 2, sticky="nsew")

class MessageWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Now you can add a watermark simply \n by typing a text and hitting 'Apply text'. \nTry it yourself!")
        self.label.pack(padx=20, pady=20, side="top", fill="both", expand=True)

        self.back_button = customtkinter.CTkButton(self, text="Back",command=self.back_trigger)
        self.back_button.pack(padx=20, pady=20, side="bottom", fill=None, expand=False)
    
    def back_trigger(self):
            self.destroy()

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Rares's Watermarking App")
        self.geometry(f"{1100}x{900}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # IMAGES FRAME 
        def create_images_frame(self):
            
            self.images_frame = customtkinter.CTkFrame(self)
            self.images_frame.grid(row=0, column=1, rowspan=2, columnspan=4, sticky="nsew")
            self.images_frame.columnconfigure((0,1), weight=1)
            self.images_frame.rowconfigure(0,weight=1)

            self.image_frame = customtkinter.CTkFrame(self.images_frame)
            self.image_frame.grid(row=0, column=0, sticky="nsew")

            self.wm_frame = customtkinter.CTkFrame(self.images_frame)
            self.wm_frame.grid(row=0, column=1,sticky="nsew")

            self.image_preview_label = customtkinter.CTkLabel(self.image_frame, text="Load Image", cursor= "hand2")
            self.image_preview_label.pack(side="top", fill="both", expand = True)


            self.wm_preview_label = customtkinter.CTkLabel(self.wm_frame, text="Load Watermark",cursor= "hand2" )
            self.wm_preview_label.pack(side="top", fill="both", expand = True)

            # Bind the label with the URL to open in a new tab
            self.image_preview_label.bind("<Button-1>", self.load_img)
            self.wm_preview_label.bind("<Button-1>", self.load_wm)

        create_images_frame(self)

        # SIDEBAR FRAME
        def create_sidebar(self):
            self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
            self.sidebar_frame.grid_rowconfigure(4, weight=1)
            self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="WaterMarky", font=customtkinter.CTkFont(size=20, weight="bold"))
            self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
            self.sidebar_button_apply = customtkinter.CTkButton(self.sidebar_frame, text="Apply watermark", command=self.sidebar_apply_event, fg_color="#46AC5C")
            self.sidebar_button_apply.grid(row=1, column=0, padx=20, pady=10)
            self.sidebar_button_reset = customtkinter.CTkButton(self.sidebar_frame, text="Reset",command=self.sidebar_reset_event)
            self.sidebar_button_reset.grid(row=2, column=0, padx=20, pady=10)
            self.sidebar_button_quit = customtkinter.CTkButton(self.sidebar_frame, text="Quit",command=self.sidebar_quit_event, fg_color="#BE352C")
            self.sidebar_button_quit.grid(row=3, column=0, padx=20, pady=10)
            self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
            self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
            self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                        command=self.change_appearance_mode_event)
            self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
            self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
            self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
            self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                                command=self.change_scaling_event)
            self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        create_sidebar(self)
            
        # INPUT FRAME
        def create_input_frame(self):
            self.input_frame = customtkinter.CTkFrame(self)
            self.input_frame.grid(row=3, column=1, columnspan=3, sticky="nsew")

            self.input_frame.columnconfigure(0,weight=6)
            self.input_frame.columnconfigure(1,weight=2)
            self.input_frame.columnconfigure(2,weight=0)

            self.entry = customtkinter.CTkEntry(self.input_frame, placeholder_text="Type in your watermark!")
            self.entry.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")

            self.apply_text_button = customtkinter.CTkButton(master=self.input_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Apply text", command = self.apply_text_event)
            self.apply_text_button.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

            self.ask_button = customtkinter.CTkButton(master=self.input_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="?", command = self.open_message_window)
            self.ask_button.grid(row=0, column=2, padx=(5), pady=(20, 20), sticky="nsew")
        create_input_frame(self)

        # OPTIONS FRAME
        def create_options_frame(self):
            self.options_frame = customtkinter.CTkFrame(self, fg_color="transparent")
            self.options_frame.grid(row=2, column=1, padx=(0, 0), pady=(0, 0), sticky="w")
            self.options_frame.grid_columnconfigure(0, weight=2)
            self.options_frame.grid_columnconfigure(1, weight=3)

                # X/ Y POSITIONING
            self.x_pos_label = customtkinter.CTkLabel(master=self.options_frame, text="X Positioning:")
            self.x_pos_label.grid(row=0, column=0, padx=(5, 5), pady=(10, 10), sticky="e")
            self.x_pos_selector = customtkinter.CTkSegmentedButton(self.options_frame)
            self.x_pos_selector.grid(row=0, column=1, padx=(5, 5), pady=(10, 10), sticky="w")

            self.y_pos_label = customtkinter.CTkLabel(master=self.options_frame, text="Y Positioning:")
            self.y_pos_label.grid(row=1, column=0, padx=(5, 5), pady=(10, 10), sticky="e")
            self.y_pos_selector = customtkinter.CTkSegmentedButton(self.options_frame)
            self.y_pos_selector.grid(row=1, column=1, padx=(5, 5), pady=(10, 10), sticky="w")


                # TRANSPARENCY 
            self.transparency_label = customtkinter.CTkLabel(master=self.options_frame, text="Transparency:")
            self.transparency_label.grid(row=2, column=0, padx=(5, 5), pady=(10, 10), sticky="e")
            self.transparency_selector = customtkinter.CTkSlider(self.options_frame, from_=0, to=1, number_of_steps=10)
            self.transparency_selector.grid(row=2, column=1, padx=(5, 5), pady=(10, 10), sticky="w")

            self.transparency_number = customtkinter.CTkLabel(master=self.options_frame, text="0.0")
            self.transparency_number.grid(row=2, column=3, padx=(5, 5), pady=(10, 10), sticky="w")

        create_options_frame(self)

        

        # set default values
        def init_defaults(self):
            self.image_filename = ''
            self.wm_filename = ''

            self.toplevel_window = None

            load_img_button = Image.open('./images/load_img.jpg')
            img_aux = customtkinter.CTkImage(dark_image = load_img_button, size = load_img_button.size)
            self.image_preview_label.configure(image=img_aux, fg_color="transparent", text="")

            load_wm_button = Image.open('./images/load_wm.jpg')
            img_aux = customtkinter.CTkImage(dark_image = load_wm_button, size = load_wm_button.size)
            self.wm_preview_label.configure(image=img_aux, fg_color="transparent", text="")

            self.appearance_mode_optionemenu.set("Dark")
            self.scaling_optionemenu.set("100%")

            self.transparency = 0
            self.transparency_selector.configure(command=self.transparency_setter)
            self.transparency_selector.set(0)
            

            self.x_pos_selector.configure(values=["LEFT", "CENTER", "RIGHT"])
            self.x_pos_selector.set("CENTER")

            self.y_pos_selector.configure(values=["TOP", "CENTER", "BOTTOM"])
            self.y_pos_selector.set("CENTER")
        init_defaults(self)

    # SIDEBAR FNS

    def sidebar_apply_event(self):
        print(self.x_pos_selector.get(),self.y_pos_selector.get(), self.transparency)
        self.result_image = apply_watermark(self.image_filename, self.wm_filename, self.x_pos_selector.get(), self.y_pos_selector.get(), self.transparency)
        self.open_toplevel()
        print("apply")
    
    def sidebar_reset_event(self):
        print("reset")
        # RESETTING IMAGES
        preview_img = Image.open('./images/load_image.jpg')

        if preview_img.size[0] > 448 :
            preview_img = resize_image_by_width(preview_img, 448)

        img_aux = customtkinter.CTkImage(dark_image = preview_img, size = preview_img.size)
        self.image_preview_label.configure(image=img_aux, fg_color="transparent", text="")
        self.image_filename = ''
        

        preview_img = Image.open('./images/load_wm.jpg')

        if preview_img.size[0] > 448 :
            preview_img = resize_image_by_width(preview_img, 448)


        img_aux = customtkinter.CTkImage(dark_image = preview_img, size = preview_img.size)
        self.wm_preview_label.configure(image=img_aux, fg_color="transparent", text="")
        self.wm_filename = ''

        # RESETTIN OPTIONS
        self.x_pos_selector.set("CENTER")
        self.y_pos_selector.set("CENTER")

        self.transparency = 0
        self.transparency_selector.set(0)

        self.transparency_number.configure(text="0.0")

    def sidebar_quit_event(self):
            print("quit")
            app.quit()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    #OPTIONS FNS
    def transparency_setter(self,value):
        self.transparency = y = round(value, 2)
        self.transparency_number.configure(text=self.transparency)
        print(self.transparency)

   
    # IMAGES FNS
    def load_img(self,event):
        print("load img")
        self.image_filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetypes =
        (("jpeg files","*.jpg"),("all files","*.*"),("png file", "*.png"),("jpeg files","*.jpeg")))

        self.image = Image.open(self.image_filename)

        # WIDTH CHECK
        if self.image.size[0] > 448 :
            preview_img = resize_image_by_width(self.image, 448)
        else:
            preview_img = self.image

    
        img_aux = customtkinter.CTkImage(dark_image = preview_img, size = preview_img.size)
        self.image_preview_label.configure(image=img_aux, fg_color="transparent", text="")

    def load_wm(self,event):
        print("load wm")

        self.wm_filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetypes =
        (("jpeg files","*.jpg"),("all files","*.*"),("png files", "*.png"),("jpeg files","*.jpeg")))

        self.wm = Image.open(self.wm_filename)

        # WIDTH CHECK
        if self.wm.size[0] > 448 :
            preview_img = resize_image_by_width(self.wm, 448)
        else:
            preview_img = self.wm
      
        img_aux = customtkinter.CTkImage(dark_image = preview_img, size = preview_img.size)
        self.wm_preview_label.configure(image=img_aux, fg_color="transparent", text="")

    # TOPLEVEL WINDOWS OPENERS
    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)
        else:
            self.toplevel_window.focus() 

    def open_message_window(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = MessageWindow(self)
        else:
            self.toplevel_window.focus()
    
    

    # TEXT APPLY FN
    def apply_text_event(self):
        text = self.entry.get()
        self.result_image = apply_text(self.image_filename,text ,self.x_pos_selector.get(), self.y_pos_selector.get(), self.transparency)
        self.open_toplevel()
        print("apply")
        


if __name__ == "__main__":
    app = App()
    app.mainloop()