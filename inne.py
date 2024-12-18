import numpy as np
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import cv2

# Funckcja do zapisywania obrazu

def saveImg(image, folderPath, filename):
    # Ścieżka do zapisu
    filePath = os.path.join(folderPath, filename)

    # Usunięcie istniejącego pliku
    if os.path.exists(filePath):
        os.remove(filePath)

    # Stworzenie folderu, jeśli nie istnieje
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    # Zapis obrazu
    cv2.imwrite(filePath, image)
    print(f"Obraz zapisany jako {filePath}")


def saveMultipleImg(image, folderPath, baseFilename = "SavedImg"):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    # Szukaj dostępnego numeru
    counter = 1
    while True:
        filename = f"{baseFilename}{counter}.png"
        filePath = os.path.join(folderPath, filename)
        if not os.path.exists(filePath):
            break
        counter += 1

    # Zapis obrazu
    cv2.imwrite(filePath, image)
    print(f"Obraz zapisany jako {filePath}") 

def getImg(path):
    return cv2.imread(path)

# Funkcja która jednocześnie wyświetla obraz i go zaszumia dzięki SomeNoise()

def load_imageWPath(path, label):
    global selectedImg
    try:
        selectedImg = path
        image = Image.open(path)
        image = image.resize((300, 300), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(image)
        label.config(image=img)
        label.image = img
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się załadować obrazu: {e}")
    SomeNoise(-100, 100)

def get_path(label):
    global img_path 
    img_path = filedialog.askopenfilename()
    if img_path:
        load_imageWPath(img_path, label) 

# Funkcja do usuwania obrazów     
# Niepotrzebna

def delete_file(folderPath):
    if os.path.exists(folderPath):
        for filename in os.listdir(folderPath):
            filepath = os.path.join(folderPath, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
    else:
        print(f"Folder {folderPath} nie istnieje")    




def Chosenimg(path, label):
    try:
        image = Image.open(path)
        image = image.resize((300, 300), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(image)
        label.config(image=img)
        label.image = img
    except Exception as e:
        messagebox.showerror("Błąd")    







def save_image(image, folder, filename):
    """Save the given image to the specified folder with the given filename."""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    try:
        cv2.imwrite(path, image)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {e}")







    