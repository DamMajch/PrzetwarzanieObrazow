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
    SomeNoise()

def get_path(label):
    global img_path 
    img_path = filedialog.askopenfilename()
    if img_path:
        load_imageWPath(img_path, label) 

# Funkcja do usuwania obrazów     
# Niepotrzebna
#
#def delete_file(filePath):
#    if os.path.exists(filePath):
#        os.remove(filePath)
#        print(f"Plik {filePath} został usunięty")
#    else:
#        print(f"Plik {filePath} nie istnieje")    

# Funkcja która dodaje szum

def SomeNoise():
    if selectedImg:  
        image = cv2.imread(selectedImg, cv2.IMREAD_GRAYSCALE)

        mean = 0
        std_dev = 25

        noise = np.random.normal(-100, 120, image.shape)

        noisy_img = image + noise

        saveImg(noisy_img, 'outputFolder', 'NoisyImg.jpg')
    else:
        print("No image selected!")


def Chosenimg(path, label):
    try:
        image = Image.open(path)
        image = image.resize((300, 300), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(image)
        label.config(image=img)
        label.image = img
    except Exception as e:
        messagebox.showerror("Błąd")    




    