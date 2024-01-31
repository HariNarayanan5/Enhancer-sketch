import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image, ImageEnhance


class ImageEnhancer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing")

        self.label = tk.Label(root, text="Choose an Image Processing Option", font=("Arial", 12))
        self.label.pack()

        self.enhance_button = tk.Button(root, text="Image Enhancer", command=self.start_enhancer, width=20, height=2)
        self.enhance_button.pack(pady=10)

        self.sketch_button = tk.Button(root, text="Image Artist", command=self.start_sketch, width=20, height=2)
        self.sketch_button.pack(pady=10)

    def start_enhancer(self):
        self.root.destroy()
        enhancer_root = tk.Tk()
        enhancer_root.title("Enhance Image")
        enhancer = ImageEnhancerProgram(enhancer_root)
        enhancer_root.mainloop()

    def start_sketch(self):
        self.root.destroy()
        sketch_root = tk.Tk()
        sketch_root.title("Image to Sketch Converter")
        artist = ImageArtistProgram(sketch_root)
        sketch_root.mainloop()

class ImageEnhancerProgram:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhance Image")

        self.label = tk.Label(root, text="Click the button to upload an image.")
        self.label.pack()

        self.button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.button.pack()

        self.back_button = tk.Button(root, text="Back to Options", command=self.back_to_options)
        self.back_button.pack(pady=10)

    def enhance_image(self, image_path, quality):
        img = cv2.imread(image_path)
        if quality == "Normal":
            enhanced_image = img
        elif quality == "Advanced":
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            enhanced_image = cv2.filter2D(img, -1, kernel)
        elif quality == "Best":
            pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            enhancer = ImageEnhance.Contrast(pil_img)
            enhanced_img = enhancer.enhance(2.0)
            enhanced_image = cv2.cvtColor(np.array(enhanced_img), cv2.COLOR_RGB2BGR)

        cv2.imshow('Original Image', img)
        cv2.imshow('Enhanced Image', enhanced_image)

        self.save_button = tk.Button(self.root, text="Save Image", command=lambda: self.save_image(enhanced_image))
        self.save_button.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.quality = tk.StringVar()
            self.quality.set("Normal")
            options = ["Normal", "Advanced", "Best"]

            quality_label = tk.Label(self.root, text="Select Quality Level:")
            quality_label.pack()

            quality_menu = tk.OptionMenu(self.root, self.quality, *options)
            quality_menu.pack()

            enhance_image_button = tk.Button(self.root, text="Enhance Image",
                                             command=lambda: self.enhance_image(file_path, self.quality.get()))
            enhance_image_button.pack()

    def save_image(self, image):
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if save_path:
            cv2.imwrite(save_path, image)
            print("Image saved successfully.")
            self.save_button.destroy()

    def back_to_options(self):
        self.root.destroy()
        root = tk.Tk()
        app = ImageEnhancer(root)
        root.mainloop()

class ImageArtistProgram:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Sketch Converter")

        self.label = tk.Label(root, text="Click the button to select an image for conversion")
        self.label.pack()

        self.button = tk.Button(root, text="Select Image", command=self.upload_image)
        self.button.pack()

        self.back_button = tk.Button(root, text="Back to Options", command=self.back_to_options)
        self.back_button.pack(pady=10)

    def convert_to_sketch(self, file_path):
        if file_path:
            image = cv2.imread(file_path)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            inverted_image = 255 - gray_image
            blurred_image = cv2.GaussianBlur(inverted_image, (21, 21), 0)
            inverted_blurred = 255 - blurred_image
            sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
            cv2.imshow("Sketch Image", sketch)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        self.convert_to_sketch(file_path)

    def back_to_options(self):
        self.root.destroy()
        root = tk.Tk()
        app = ImageEnhancer(root)
        root.mainloop()

root = tk.Tk()
app = ImageEnhancer(root)
root.mainloop()
