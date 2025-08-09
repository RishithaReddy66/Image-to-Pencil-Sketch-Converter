import cv2
import pathlib
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import pyautogui

class SketchImage:
    def __init__(self, root):
        self.window = root
        self.window.geometry("940x580")
        self.window.title('Sketch Creator')
        self.window.resizable(width=False, height=False)

        self.width = 700
        self.height = 440

        self.Image_Path = ''
        self.SketchImg = None
        self.sketch_label = None

        # ==============================================
        # ================Menubar Section===============
        # ==============================================
        # Creating Menubar
        self.menubar = Menu(self.window)

        # Adding Edit Menu and its sub menus
        edit = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Open', menu=edit)
        edit.add_command(label='Open Image', command=self.Open_Image)
        
        sketch = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Sketch', menu=sketch)
        sketch.add_command(label='Create Sketch', command=self.CreateSketch)
    
        save = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Save', menu=save)
        save.add_command(label='Save Image', command=self.Save_Image)

        # Exit the Application
        exit = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Exit', menu=exit)
        exit.add_command(label='Exit', command=self.Exit)

        # Configuring the menubar
        self.window.config(menu=self.menubar)
        # ===================End=======================

        # Creating a Frame
        self.frame = Frame(self.window, width=self.width, height=self.height)
        self.frame.pack()
        self.frame.place(anchor='center', relx=0.5, rely=0.5)

        # The Scale widget to select the intensity of the sketch quality
        self.intensity = Scale(self.window, from_=5, to=155, resolution=2, orient=HORIZONTAL, length=300)
        self.intensity.set(37)
        self.intensity.place(x=320, y=520)

    # Open an Image through filedialog
    def Open_Image(self):
        self.Clear_Screen()
        self.Image_Path = filedialog.askopenfilename(title="Select an Image", filetypes=(("Image files", "*.jpg *.jpeg *.png"),))
        if len(self.Image_Path) != 0:
            self.Show_Image(self.Image_Path)
    
    # Display the Image
    def Show_Image(self, Img):
        # opening the image
        image = Image.open(Img)
        # resize the image, so that it fits to the screen
        resized_image = image.resize((self.width, self.height))

        # Create an object of tkinter ImageTk
        self.img = ImageTk.PhotoImage(resized_image)

        # A Label Widget for displaying the Image
        label = Label(self.frame, image=self.img)
        label.pack()

    def CreateSketch(self):
        # storing the image path to a variable
        self.ImgPath = self.Image_Path

        # If any image is not selected 
        if len(self.ImgPath) == 0:
            pass
        else:
            Img = cv2.imread(self.ImgPath)

            Img = cv2.resize(Img, (self.width, self.height))

            GrayImg = cv2.cvtColor(src=Img, code=cv2.COLOR_BGR2GRAY)

            InvertImg = cv2.bitwise_not(GrayImg)

            SmoothImg = cv2.medianBlur(src=InvertImg, ksize=self.intensity.get())

            IvtSmoothImg = cv2.bitwise_not(SmoothImg)

            self.SketchImg = cv2.divide(GrayImg, IvtSmoothImg, scale=250)

            self.Display_Sketch()

    def Display_Sketch(self):
        if self.sketch_label:
            self.sketch_label.destroy()

        # Convert the sketch image to PIL format and then to ImageTk format
        sketch_image = Image.fromarray(self.SketchImg)
        self.sketch_imgtk = ImageTk.PhotoImage(sketch_image)
        
        # A Label Widget for displaying the Sketch Image
        self.sketch_label = Label(self.frame, image=self.sketch_imgtk)
        self.sketch_label.pack()

    def Save_Image(self):
        if self.SketchImg is None:
            return

        # Open file dialog to save the image
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            # Saving the resulting file(self.SketchImg)
            cv2.imwrite(file_path, self.SketchImg)
            
            # Display a message box to confirm the image has been saved
            pyautogui.alert(f"Image saved as {file_path}")

    # Remove all widgets from the frame
    def Clear_Screen(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def Exit(self):
        self.window.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = SketchImage(root)
    root.mainloop()
