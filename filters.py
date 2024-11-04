import numpy as np
from tkinter import *
from PIL import Image, ImageTk
import cv2
from inne import saveImg


# Przykładowy filtr działanie:
# Filtruje zaszumiony obraz z scieżki: "outputFolder/NoisyImg.jpg"
# potem zapisuje ten obraz do outputFolder jako FilImg.png
# robi to żeby później można było go zapisać do folderu "ZapisaneObrazy" po kliknięciu Zapisz obraz

def adaptFilter(path, label):
    x = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    X = cv2.randn(np.zeros_like(x), 0, 255)
    X = x + X

    Y = X.astype(np.float64)

    y = cv2.randn(np.zeros_like(Y), 0, 10) + Y

    U, V = 10, 10
    Z = np.pad(Y, ((U//2, U//2), (V//2, V//2)), 'constant', constant_values=0)

    lmean = np.zeros_like(Y)
    lvar = np.zeros_like(Y)

    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            temp = Z[i:i+U, j:j+V]
            lmean[i, j] = np.mean(temp)
            lvar[i, j] = np.var(temp)

    nvar = np.sum(lvar) / Y.size
    lvar = np.maximum(lvar, nvar)

    NewImg = Y - (nvar / lvar) * (Y - lmean)
    NewImg = np.clip(NewImg, 0, 255).astype(np.uint8)

    # Przeskalowanie obrazu do wyświetlenia
    displayImg = Image.fromarray(NewImg)
    displayImg = displayImg.resize((300, 300), Image.LANCZOS)

    # Wyświetlenie obrazu w Tkinterze
    img = ImageTk.PhotoImage(displayImg)
    label.config(image=img)
    label.image = img

    # Zapis obrazu do folderu
    saveImg(NewImg, 'outputFolder', 'FilImg.png')