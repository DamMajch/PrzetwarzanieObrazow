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
    
def adaptive_median_filter(img_path, label, max_window_size = 7):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    filtered_img = np.copy(img)

    def get_median(window):
        return np.median(window)

    for i in range(h):
        for j in range(w):
            window_size = 3  # Początkowy rozmiar okna
            while window_size <= max_window_size:
                half_size = window_size // 2

                # Ustalanie granic okna
                x1 = max(0, i - half_size)
                x2 = min(h, i + half_size + 1)
                y1 = max(0, j - half_size)
                y2 = min(w, j + half_size + 1)

                window = img[x1:x2, y1:y2]
                z_min, z_max, z_med = np.min(window), np.max(window), get_median(window)

                if z_min < z_med < z_max:
                    # Jeśli piksel nie jest szumem, pozostawiamy go
                    if z_min < img[i, j] < z_max:
                        filtered_img[i, j] = img[i, j]
                    else:
                        filtered_img[i, j] = z_med
                    break
                else:
                    window_size += 2  # Zwiększamy rozmiar okna

                # Jeśli osiągnięto maksymalny rozmiar okna, ustawiamy medianę
                if window_size > max_window_size:
                    filtered_img[i, j] = z_med

    # Przeskalowanie obrazu do wyświetlenia
    
    displayImg = Image.fromarray(filtered_img)
    displayImg = displayImg.resize((300, 300), Image.LANCZOS)
    
    # Wyświetlenie obrazu w Tkinterze
    
    img = ImageTk.PhotoImage(displayImg)
    label.config(image=img)
    label.image = img
    
    # Zapis obrazu do folderu
    
    saveImg(filtered_img, 'outputFolder', 'FilImg.png')
    
def adaptive_wiener_filter(img_path, label):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    filtered_img = cv2.medianBlur(img, 5)
    
    # Przeskalowanie obrazu do wyświetlenia
    
    displayImg = Image.fromarray(filtered_img)
    displayImg = displayImg.resize((300, 300), Image.LANCZOS)
    
    # Wyświetlenie obrazu w Tkinterze
    
    img = ImageTk.PhotoImage(displayImg)
    label.config(image=img)
    label.image = img
    
    # Zapis obrazu do folderu
    
    saveImg(filtered_img, 'outputFolder', 'FilImg.png')
    