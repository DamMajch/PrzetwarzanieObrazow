import tkinter as tk
from inne import delete_file, saveMultipleImg, save_image
from filters import adaptive_median_filter
from filters import adaptive_wiener_filter
from filters import adaptive_gaussian_filter
from filters import bilateral_filter
from tkinter import ttk

import numpy as np
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import cv2

delete_file("outputFolder")

button_clicked = False

isGaussian = False
isMinMax = False


def load_image(path, label):
    """Load an image from the given path and display it on the specified label."""
    try:
        global selectedImg
        selectedImg = path
        image = Image.open(path)
        image = image.resize((300, 300), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(image)
        label.config(image=img)
        label.image = img
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")

def add_noise(mean, std):
    global isGaussian 
    isGaussian = True
    if not button_clicked:
         messagebox.showwarning("Warning", "Choose image you want to noise")
    else:
        if selectedImg:
            image = cv2.imread(selectedImg, cv2.IMREAD_GRAYSCALE)
            noise = np.random.normal(mean, std, image.shape)
            noisy_img = np.clip(image + noise, 0, 255).astype(np.uint8)
            save_image(noisy_img, "outputFolder", "NoisyImg.jpg")
            try:
                img = Image.fromarray(noisy_img)
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                label2.config(image=img)
                label2.image = img
            except Exception as e:
                messagebox.showerror("Error", f"Failed to display noisy image: {e}") 

def add_min_max(nois_min, nois_max):
    global isGaussian 
    isGaussian = False
    if not button_clicked:
        messagebox.showwarning("Warning", "Choose image you want to noise")
    else:
        if selectedImg:
            image = cv2.imread(selectedImg, cv2.IMREAD_GRAYSCALE)
            noise = np.random.randint(nois_min, nois_max + 1, image.shape, dtype=np.int16)
            noisy_img = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            save_image(noisy_img, "outputFolder", "NoisyImg.jpg")
            try:
                img = Image.fromarray(noisy_img)
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                label2.config(image=img)
                label2.image = img
            except Exception as e:
                messagebox.showerror("Error", f"Failed to display noisy image: {e}") 


default_Folder = "images"
def choose_image(label):
    """Open file dialog to choose an image and load it."""
    global default_Folder
    global button_clicked
    button_clicked = True
    img_path = filedialog.askopenfilename(initialdir=default_Folder, title="Choose Image")
    if img_path:
        load_image(img_path, label)

def update_label(val):
    """Update the slider label and add noise with the current slider value."""
    sliderLabel.config(text=f"Value: {float(val):.2f}")
    if selectedImg:
        if isGaussian:
            add_noise(mean=0, std=float(val))
        else:
            add_min_max(nois_min=-50, nois_max=float(val))    

def on_hover(event, frame, label):
    button_x = event.widget.winfo_rootx()
    button_y = event.widget.winfo_rooty()
    button_width = event.widget.winfo_width()

    # Ustaw pozycję hover frame po prawej stronie przycisku
    frame.place(x=button_x + button_width - 250, y=button_y + 110)
    label.place(x = 10, y=10)

def off_hover(event, frame, label):
    frame.place_forget()
    label.place_forget()

root = tk.Tk()
root.title("Filtry adaptacyjne")

str1 = tk.StringVar(value="Filtry adaptacyjne") 
str2 = tk.StringVar(value="Adaptacyjny Filtr Medianowy") 
str3 = tk.StringVar(value="Adaptacyjny Filtr Wienerowski") 
str4 = tk.StringVar(value="Adaptacyjny Filtr Gaussowski") 
str5 = tk.StringVar(value="Filtr Bilateralny") 
str6 = tk.StringVar(value="Wybierz obraz") 
str7 = tk.StringVar(value="Dodaj Szum Gaussowski") 
str8 = tk.StringVar(value="Zapisz obraz") 
str9 = tk.StringVar(value="Próbny filtr") 
str10 = tk.StringVar(value="Adaptacyjny filtr medianowy działa poprzez iteracyjne stosowanie klasycznej metody mediany na obrazie, przy czym dynamicznie dopasowuje rozmiar okna (maski) w zależności od poziomu szumu")
str11 = tk.StringVar(value="Adaptacyjny filtr Wienerowski działa na zasadzie minimalizacji błędu rekonstrukcji obrazu, dopasowując swoje działanie do lokalnych statystyk obrazu \n Obraz jest przetwarzany w lokalnych obszarach (oknach/maskach) o określonym rozmiarze. \n")
str12 = tk.StringVar(value="Adaptacyjny filtr Gaussowski działa na zasadzie wygładzania obrazu, dopasowując rozmycie do lokalnych cech obrazu.")
str13 = tk.StringVar(value="Adaptacyjny filtr bilateralny działa na zasadzie wygładzania obrazu, zachowując krawędzie, dzięki wykorzystaniu zarówno różnic przestrzennych, jak i intensywności pikseli.")
str14 = tk.StringVar(value="Dodaj Szum Min-Max")

icon = "icons/iconsPoland.png"
ikona = tk.PhotoImage(file=icon)

def change_language():
    global ikona
    if str1.get() == "Filtry adaptacyjne":
        str1.set("Adaptive Filters")
        str2.set("Adaptive Median Filter")
        str3.set("Adaptive Wiener Filter")
        str4.set("Adaptive Gaussian Filter")
        str5.set("Bilateral Filter")
        str6.set("Choose Image")
        str7.set("Add Gaussian Noise")
        str8.set("Save Image")
        str9.set("Experimental Filter")
        str10.set("The adaptive median filter works by iteratively applying the classical median method to the image, while dynamically adjusting the window (mask) size depending on the noise level.")
        str11.set("The adaptive Wiener filter works on the principle of minimizing the image reconstruction error by adapting its performance to local image statistics. The image is processed in local areas (windows/masks) of a specified size.")
        str12.set("The adaptive Gaussian filter works on the principle of image smoothing by adjusting the blur to the local image characteristics")
        str13.set("The adaptive bilateral filter works by smoothing the image while preserving edges by using both spatial differences and pixel intensities")
        str14.set("Add Min-Max Noise")
        new_icon_path  = "icons/iconsBritish.png"
    else:
        str1.set("Filtry adaptacyjne") 
        str2.set("Adaptacyjny Filtr Medianowy")
        str3.set("Adaptacyjny Filtr Wienerowski")
        str4.set("Adaptacyjny Filtr Gaussowski")
        str5.set("Filtr Bilateralny")
        str6.set("Wybierz obraz")
        str7.set("Dodaj Szum Gaussowski")
        str8.set("Zapisz obraz")
        str9.set("Próbny filtr")
        str10.set("Adaptacyjny filtr medianowy działa poprzez iteracyjne stosowanie klasycznej metody mediany na obrazie, przy czym dynamicznie dopasowuje rozmiar okna (maski) w zależności od poziomu szumu")
        str11.set("Adaptacyjny filtr Wienerowski działa na zasadzie minimalizacji błędu rekonstrukcji obrazu, dopasowując swoje działanie do lokalnych statystyk obrazu \n Obraz jest przetwarzany w lokalnych obszarach (oknach/maskach) o określonym rozmiarze")
        str12.set("Adaptacyjny filtr Gaussowski działa na zasadzie wygładzania obrazu, dopasowując rozmycie do lokalnych cech obrazu")
        str13.set("Adaptacyjny filtr bilateralny działa na zasadzie wygładzania obrazu, zachowując krawędzie, dzięki wykorzystaniu zarówno różnic przestrzennych, jak i intensywności pikseli")
        str14.set("Dodaj Szum Min-Max")
        new_icon_path  = "icons/iconsPoland.png"

    ikona = tk.PhotoImage(file=new_icon_path)
    enPLButt.config(image=ikona)    

selectedImg = None

pitiPath = "outputFolder/FilImg.png"

img_path = ''

# Szary Frame dla wyświetlania przycisków oznaczających filtry

frameButtons = tk.Frame(root, bg="#505050")
frameButtons.place(relx=0, rely=0, relwidth=1, relheight=0.5)

titleLabel = tk.Label(frameButtons, bg="#505050", textvariable=str1, font=("Arial", 32), fg="white")
titleLabel.pack(pady=5)

# Trzy niebieskie tła

frame1 = tk.Frame(root, bg="#3256d5")
frame1.place(relx=0, rely=0.5, relwidth=0.33333, relheight=0.5) 

frame2 = tk.Frame(root, bg="#327fd5")
frame2.place(relx=0.33333, rely=0.5, relwidth=0.33333, relheight=0.5)

frame3 = tk.Frame(root, bg="#32bfd5")
frame3.place(relx=0.66666, rely=0.5, relwidth=0.33333, relheight=0.5)


# Zielony Frame na przyciski

buttonFrame = tk.Frame(frameButtons, bg='#326f39')
buttonFrame.pack(padx=0, pady=0)

butt1Fr =  tk.Frame(buttonFrame, bg='#326f39')
butt1Fr.pack(side=tk.LEFT, padx=10, pady=10)

butt2Fr =  tk.Frame(buttonFrame, bg='#326f39')
butt2Fr.pack(side=tk.LEFT, padx=10, pady=10)

butt3Fr =  tk.Frame(buttonFrame, bg='#326f39')
butt3Fr.pack(side=tk.LEFT, padx=10, pady=10)

butt4Fr =  tk.Frame(buttonFrame, bg='#326f39')
butt4Fr.pack(side=tk.LEFT, padx=10, pady=10)

butt5Fr =  tk.Frame(buttonFrame, bg='#326f39')
butt5Fr.pack(side=tk.LEFT, padx=10, pady=10)


# Frame dla wyświetlania obrazu

frameImg = tk.Frame(frame1, bg='blue')
frameImg.pack(side=tk.TOP, padx=10, pady=10)

# Frame dla wyświetlania zaszumionego obrazu

frameImgSzum = tk.Frame(frame2, bg='blue')
frameImgSzum.pack( padx=10, pady=10)

sliderFrame = ttk.Frame(frame2)
sliderFrame.pack(side=tk.RIGHT, padx=2, pady=2)

slider = ttk.Scale(sliderFrame, length=300 ,from_=0, to=100, orient="vertical", command=update_label)
slider.pack(pady=10)

sliderLabel = ttk.Label(sliderFrame, text="Value: 0")
sliderFrame.pack(pady=10)

# Frame dla wyświetlania przefiltrowanego obrazu i do zapisania go

frameImgZapisz = tk.Frame(frame3, bg='blue')
frameImgZapisz.pack(side=tk.TOP, padx=10, pady=10)

# Przycisk do zmiany języka na angielski i z powrotem

enPLButt = tk.Button(root, image=ikona, command=change_language)
enPLButt.pack(side="top", anchor="e")

# Przycisk do filtra medianowego (button1)

button1 = tk.Button(butt1Fr, textvariable=str2, width=24, height=4, cursor="hand2", font=("Arial", 15),
                    command=lambda: adaptive_median_filter("outputFolder/NoisyImg.jpg", label3))
button1.pack(side=tk.BOTTOM, padx=50, pady=0)

# Przycisk do filtra Wienerowskiego (button2)

button2 = tk.Button(butt2Fr, textvariable=str3, width=24, height=4, cursor="hand2", font=("Arial", 15),
                    command=lambda: adaptive_wiener_filter("outputFolder/NoisyImg.jpg", label3))
button2.pack(side=tk.BOTTOM, padx=50, pady=0)

# Przycisk do filtra Gaussa 

button3 = tk.Button(butt3Fr, textvariable=str4, width=24, height=4, cursor="hand2", font=("Arial", 15),
                    command=lambda: adaptive_gaussian_filter("outputFolder/NoisyImg.jpg", label3))
button3.pack(side=tk.BOTTOM, padx=50, pady=0)
# Przycisk do filtra bilateralnego


button4 = tk.Button(butt4Fr, textvariable=str5, width=24, height=4, cursor="hand2", font=("Arial", 15),
                    command=lambda: bilateral_filter("outputFolder/NoisyImg.jpg", label3))
button4.pack(side=tk.BOTTOM, padx=50, pady=0)


Sciezka = "outputFolder/NoisyImg.jpg"

# Przycisk do zaszumienia obrazu

szumFrame = tk.Frame(frame2, bg="#327fd5")
szumFrame.place(relx=0.1, rely=0, relheight=0.20)

open_button1 = tk.Button(frame1, textvariable=str6, width=12, command=lambda: choose_image(label1), cursor="hand2", font=("Arial", 11))
open_button1.pack(padx=10, pady=10)

open_button2 = tk.Button(szumFrame, textvariable=str7, width=18, command=lambda: add_noise(0, 50), cursor="hand2", font=("Arial", 11))
open_button2.pack(side=tk.LEFT, padx=10, pady=10)

open_button2_min_max = tk.Button(szumFrame, textvariable=str14, width=18, command=lambda: add_min_max(-50, 50), cursor="hand2", font=("Arial", 11))
open_button2_min_max.pack(side=tk.RIGHT ,padx=10, pady=10)

open_button3 = tk.Button(frame3, textvariable=str8, width=12, command=lambda: saveMultipleImg(cv2.imread("outputFolder/NoisyImg.jpg"), "SavedImages"), cursor="hand2", font=("Arial", 11))
open_button3.pack(padx=10, pady=10)


label2 = tk.Label(frame2, bg="#327fd5")
label2.pack(expand=True, padx=10, pady=(10, 75))  # 10 pikseli od góry, 50 pikseli od dołu




label1 = tk.Label(frame1)
label1.pack(padx=10, pady=10)

label3 = tk.Label(frame3)
label3.pack(padx=10, pady=10)


hovFrame1 = tk.Frame(root, bg="#111110", width=200, height=180)
hovFrame2 = tk.Frame(root, bg="#111110", width=200, height=180)
hovFrame3 = tk.Frame(root, bg="#111110", width=200, height=180)
hovFrame4 = tk.Frame(root, bg="#111110", width=200, height=180)

hovLabel1 = tk.Label(hovFrame1, textvariable=str10, bg="#111110", fg="white", wraplength=170)
hovLabel2 = tk.Label(hovFrame2, textvariable=str11, bg="#111110", fg="white", wraplength=170)
hovLabel3 = tk.Label(hovFrame3, textvariable=str12, bg="#111110", fg="white", wraplength=170)
hovLabel4 = tk.Label(hovFrame4, textvariable=str13, bg="#111110", fg="white", wraplength=170)

button1.bind("<Enter>", lambda e: on_hover(e,hovFrame1, hovLabel1))  
button1.bind("<Leave>", lambda e: off_hover(e, hovFrame1, hovLabel1))

button2.bind("<Enter>", lambda e: on_hover(e,hovFrame2, hovLabel2))  
button2.bind("<Leave>", lambda e: off_hover(e, hovFrame2, hovLabel2))

button3.bind("<Enter>", lambda e: on_hover(e,hovFrame3, hovLabel3))  
button3.bind("<Leave>", lambda e: off_hover(e, hovFrame3, hovLabel3))

button4.bind("<Enter>", lambda e: on_hover(e,hovFrame4, hovLabel4))  
button4.bind("<Leave>", lambda e: off_hover(e, hovFrame4, hovLabel4))

root.mainloop()

