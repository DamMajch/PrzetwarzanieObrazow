import numpy as np
from tkinter import *
from PIL import Image, ImageTk
import cv2
from inne import saveImg
from scipy.signal import wiener

# Przykładowy filtr działanie:
# Filtruje zaszumiony obraz z scieżki: "outputFolder/NoisyImg.jpg"
# potem zapisuje ten obraz do outputFolder jako FilImg.png
# robi to żeby później można było go zapisać do folderu "ZapisaneObrazy" po kliknięciu Zapisz obraz
    
def adaptive_median_filter(img_path, label, max_window_size=7):
    """
    Optymalizacja filtra medianowego z wykorzystaniem wbudowanego cv2.medianBlur.
    """
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print("Nie udało się wczytać obrazu.")
        return

    # Zastosowanie wbudowanego filtra medianowego
    filtered_img = cv2.medianBlur(img, max_window_size)

    # Przeskalowanie obrazu do wyświetlenia
    displayImg = Image.fromarray(filtered_img)
    displayImg = displayImg.resize((300, 300), Image.LANCZOS)

    # Wyświetlenie obrazu w Tkinterze
    img_display = ImageTk.PhotoImage(displayImg)
    label.config(image=img_display)
    label.image = img_display

    # Zapis obrazu do folderu
    saveImg(filtered_img, 'outputFolder', 'FilImg.png')

    
def adaptive_wiener_filter(img_path, label):
    # Wczytanie obrazu w skali szarości
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    
    # Zastosowanie filtru Wienera
    filtered_img = wiener(img, mysize=(5, 5))  # Rozmiar okna można dostosować

    # Przekształcenie wyniku na typ uint8 (zakres 0-255)
    filtered_img = np.clip(filtered_img, 0, 255).astype(np.uint8)

    # Przeskalowanie obrazu do wyświetlenia w Tkinterze
    displayImg = Image.fromarray(filtered_img)
    displayImg = displayImg.resize((300, 300), Image.LANCZOS)

    # Wyświetlenie obrazu w Tkinterze
    img_display = ImageTk.PhotoImage(displayImg)
    label.config(image=img_display)
    label.image = img_display

    # Zapis obrazu do folderu
    saveImg(filtered_img, 'outputFolder', 'FilImg.png')


def adaptive_gaussian_filter(img_path, label, kernel_size=15, max_sigma=5.0):
    """
    Zoptymalizowana wersja adaptacyjnego filtra Gaussa.
    """
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print("Nie udało się wczytać obrazu.")
        return

    # Konwersja do float32
    img = img.astype(np.float32)

    # Obliczenie lokalnej wariancji
    mean = cv2.blur(img, (kernel_size, kernel_size))
    squared_mean = cv2.blur(img**2, (kernel_size, kernel_size))
    variance = squared_mean - mean**2

    # Mapowanie wariancji do zakresu sigma
    variance = np.clip(variance, 0, np.max(variance))
    sigma_map = max_sigma * variance / (np.max(variance) + 1e-5)  # Epsilon dla stabilności

    # Tworzenie filtrów Gaussa o różnym sigma
    output = np.zeros_like(img, dtype=np.float32)
    unique_sigmas = np.unique(np.round(sigma_map, 1))  # Wyodrębnienie unikalnych wartości sigma

    gaussian_kernels = {}
    for sigma in unique_sigmas:
        # Precompute Gaussian kernels dla każdej wartości sigma
        if sigma > 0:
            gaussian_kernels[sigma] = cv2.GaussianBlur(img, (kernel_size, kernel_size), sigma)

    # Mapowanie sigma do odpowiadających filtrowanych obrazów
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            sigma = np.round(sigma_map[i, j], 1)
            output[i, j] = gaussian_kernels[sigma][i, j]

    # Normalizacja wyniku
    output = np.clip(output, 0, 255).astype(np.uint8)

    # Wyświetlenie obrazu w Tkinterze
    displayImg = Image.fromarray(output)
    displayImg = displayImg.resize((300, 300), Image.LANCZOS)

    img_display = ImageTk.PhotoImage(displayImg)
    label.config(image=img_display)
    label.image = img_display

    # Zapis obrazu do pliku
    saveImg(output, 'outputFolder', 'FilImg.png')




def bilateral_filter(img_path, label, diameter=15, sigma_color=75, sigma_space=75):
    """
    Implementacja filtra bilateralnego z użyciem OpenCV.
    """
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    

    # Filtracja z użyciem OpenCV
    filtered_img = cv2.bilateralFilter(img, diameter, sigma_color, sigma_space)

    # Przeskalowanie obrazu do wyświetlenia
    displayImg = Image.fromarray(filtered_img)
    displayImg = displayImg.resize((300, 300), Image.LANCZOS)

    # Wyświetlenie obrazu w Tkinterze
    img_display = ImageTk.PhotoImage(displayImg)
    label.config(image=img_display)
    label.image = img_display

    # Zapis obrazu do folderu
    saveImg(filtered_img, 'outputFolder', 'FilImg.png')


    