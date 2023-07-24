import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageFilter
import numpy as np
from skimage.util import random_noise


class ImageProcessor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image Processing Application")
        self.window.geometry("1700x800")
        # self.window.configure(bg="gray")

        self.original_image = None
        self.processed_image = None

        self.load_image_button = tk.Button(self.window, text="Load Image", command=self.load_image)
        self.load_image_button.pack(pady=10)

        self.filter_label = tk.Label(self.window, text="Filter Options:")
        self.filter_label.pack(pady=5)

        self.filter_options = tk.Frame(self.window)
        self.filter_options.pack(pady=5)

        self.filter_var = tk.StringVar()
        self.filter_var.set("")

        self.filter_var = tk.StringVar()
        self.filter_var.set("Original Image")  

        self.filter_dropdown = tk.OptionMenu(self.filter_options, self.filter_var,"Original Image", "High Pass", "Low Pass", "Laplacian",
                                            "Median", "Salt & Pepper")
        self.filter_dropdown.pack(side=tk.LEFT, padx=10)


        self.filter_button = tk.Button(self.filter_options, text="Apply Filter", command=self.apply_filter , bg="light blue")
        self.filter_button.pack(side=tk.LEFT, padx=10)

        self.save_image_button = tk.Button(self.window, text="Save Image", command=self.save_image)
        self.save_image_button.pack(pady=10)

        self.image_canvas = tk.Canvas(self.window, width=700, height=700)
        self.image_canvas.pack(side=tk.LEFT, padx=20, pady=20)

        self.hist_canvas = tk.Canvas(self.window, width=500, height=500)
        self.hist_canvas.pack(side=tk.LEFT, padx=20, pady=20)

        self.window.mainloop()

    def save_image(self):
        if self.processed_image:
            filename = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                    filetypes=[("JPEG", ".jpg"), ("PNG", ".png")])
            if filename:
                self.processed_image.save(filename)

    def load_image(self):
        filename = filedialog.askopenfilename(title="Select Image File",
                                              filetypes=[("Image Files", "*.jpg *.jpeg *.png")])

        if filename:
            self.original_image = Image.open(filename)
            if self.original_image.mode == "RGBA":
                self.original_image = self.original_image.convert("RGB")
            self.processed_image = self.original_image.copy()
            self.display_image(self.original_image)
            self.display_histogram(self.original_image)

    def display_image(self, image):
        self.image_canvas.delete("all")

        # Define the maximum width and height for the displayed image
        max_width = 700
        max_height = 700

        # Get the original image's dimensions
        original_width, original_height = image.size

        # Calculate the scaled width and height while maintaining aspect ratio
        if original_width > max_width or original_height > max_height:
            width_ratio = max_width / original_width
            height_ratio = max_height / original_height
            scale_factor = min(width_ratio, height_ratio)
            display_width = int(original_width * scale_factor)
            display_height = int(original_height * scale_factor)
        else:
            display_width = original_width
            display_height = original_height

        # Resize the image to the calculated dimensions
        resized_image = image.resize((display_width, display_height), Image.ANTIALIAS)

        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_canvas.config(width=display_width, height=display_height)
        self.image_canvas.create_image(display_width / 2, display_height / 2, image=self.image_tk)

    def display_histogram(self, image):
        self.hist_canvas.delete("all")
        histogram_values = self.calculate_histogram(image)
        max_count = max(histogram_values)
        scaling_factor = 300 / max_count

        bar_width = 1  
        bar_spacing = 1.5  

        # Draw background grid lines
        for i in range(0, 256, 16):
            x = i * (bar_width + bar_spacing)
            self.hist_canvas.create_line(x, 500, x, 0, fill="lightgray")

        for i, count in enumerate(histogram_values):
            x0 = i * (bar_width + bar_spacing) + 100 
            y0 = 500
            x1 = x0 + bar_width
            y1 = 500 - (count * scaling_factor)

            # Draw histogram bar
            self.hist_canvas.create_rectangle(x0, y0, x1, y1, fill="steelblue")

        #x,y axis
        self.hist_canvas.create_line(100, 500, 100, 0, fill="black")
       
        self.hist_canvas.create_text(40, 250, text="Frequency", fill="black", anchor=tk.NW, angle=90)

       
        self.hist_canvas.create_line(100, 500, self.hist_canvas.winfo_width(), 500, fill="black")
       
        self.hist_canvas.create_text((self.hist_canvas.winfo_width() + 100) / 2, 540, text="Grayscale Value",
                                     fill="black")

        # Draw numbers on y-axis
        y_values = list(range(0, max_count + 1, int(max_count / 5)))  # Adjust the increment as needed
        for y in y_values:
            y_pixel = 500 - (y * scaling_factor)
            self.hist_canvas.create_text(95, y_pixel, text=str(y), anchor=tk.E, fill="black")

        # Draw numbers on x-axis
        x_values = list(range(0, 256, 32))  
        for x in x_values:
            x_pixel = x * (bar_width + bar_spacing) + 100 
            self.hist_canvas.create_text(x_pixel, 510, text=str(x), anchor=tk.N, fill="black")

        # Set appropriate margins for the histogram
        hist_padding = 20  
        hist_margin = 30  
        hist_width = len(histogram_values) * (
                    bar_width + bar_spacing) + 100  
        hist_height = 550
        self.hist_canvas.config(width=hist_width + hist_padding + hist_margin,
                                height=hist_height, bd=0, highlightthickness=0)

        # Adjust the position of y-axis description
        self.hist_canvas.coords(1, 60, 250)

        # Adjust the position of x-axis description
        self.hist_canvas.coords(2, (hist_width + hist_padding + hist_margin) / 2, 540)
    def calculate_histogram(self, image):
        histogram = [0] * 256
        pixels = image.getdata()

        for pixel in pixels:  
            grayscale = int(sum(pixel) / 3)

            
            histogram[grayscale] += 1

        return histogram

    def apply_filter(self):
        if not self.original_image:
            return

        filter_name = self.filter_var.get()
        if filter_name == "Original Image":
            self.processed_image = self.original_image.copy()
        elif filter_name == "High Pass":
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            self.processed_image = self.original_image.filter(ImageFilter.Kernel((3, 3), kernel.flatten(), scale=1))
        elif filter_name == "Low Pass":
            kernel = np.ones((5, 5)) / 25
            self.processed_image = self.original_image.filter(ImageFilter.Kernel((5, 5), kernel.flatten(), scale=1))
        elif filter_name == "Laplacian":
            kernel = np.array([[-1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1],
                   [-1, -1, 24, -1, -1],
                   [-1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1]])
            self.processed_image = self.original_image.filter(ImageFilter.Kernel((5, 5), kernel.flatten(), scale=1))

        elif filter_name == "Median":
            self.processed_image = self.original_image.filter(ImageFilter.MedianFilter(size=5))
        elif filter_name == "Salt & Pepper":
            self.processed_image = random_noise(np.array(self.original_image), mode='s&p', amount=0.05)
            self.processed_image = (self.processed_image * 255).astype(np.uint8)
            self.processed_image = Image.fromarray(self.processed_image)

        self.display_image(self.processed_image)
        self.display_histogram(self.processed_image)


if __name__ == "__main__":
    app = ImageProcessor()
