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
'''
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


'''

def sobel_canny_binary_gaussian_filter(img_path, label):
    """
    Delikatne filtrowanie obrazów za pomocą Sobela, Cannym, binaryzacji i Gaussa.
    
    Args:
        img_path (str): Ścieżka do obrazu wejściowego.
        label (tk.Label): Etykieta Tkintera do wyświetlenia obrazu.
    """
    # Załaduj obraz w odcieniach szarości
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)


   # Filtr Gaussa (delikatne wygładzenie szumów na wejściu)
    gaussian_blur = cv2.GaussianBlur(img, (3, 3), 0)

    # Filtr Sobela (zmniejszona intensywność gradientów)
    sobel_x = cv2.Sobel(gaussian_blur, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gaussian_blur, cv2.CV_64F, 0, 1, ksize=3)
    sobel_combined = np.sqrt(sobel_x**2 + sobel_y**2)
    sobel_combined = np.clip(sobel_combined, 0, 255).astype(np.uint8)

    # Binaryzacja adaptacyjna
    adaptive_binary = cv2.adaptiveThreshold(
        sobel_combined, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Delikatna filtracja Gaussa na końcu
    final_output = cv2.GaussianBlur(adaptive_binary, (3, 3), 0)

    # Przeskalowanie obrazu do wyświetlenia w Tkinterze
    displayImg = Image.fromarray(final_output)
    displayImg = displayImg.resize((300, 300), Image.LANCZOS)

    # Wyświetlenie obrazu w Tkinterze
    img_display = ImageTk.PhotoImage(displayImg)
    label.config(image=img_display)
    label.image = img_display

    # Zapis obrazu do folderu
    saveImg(final_output, 'outputFolder', 'FilImg.png')

    
def advanced_edge_preserving_filter(img_path, label):
    """
    Filtr zachowujący krawędzie:
    - Sobel do wykrycia krawędzi.
    - Canny do binaryzacji.
    - Filtr Gaussowski do punktów niebędących krawędziami.
    """
    # Załaduj obraz w odcieniach szarości
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
 

    # Krok 1: Sobel - Detekcja krawędzi
    sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    sobel_edges = cv2.magnitude(sobel_x, sobel_y)  # Kombinacja gradientów
    sobel_edges = cv2.convertScaleAbs(sobel_edges)  # Konwersja do zakresu 0-255

    # Krok 2: Canny - Binaryzacja krawędzi
    canny_edges = cv2.Canny(sobel_edges, 50, 150)

    # Krok 3: Maskowanie punktów krawędziowych
    # Tworzymy maskę punktów niebędących krawędziami
    mask_non_edges = cv2.bitwise_not(canny_edges)

    # Krok 4: Filtracja Gaussowska (dolnoprzepustowa) na reszcie punktów
    gaussian_blur = cv2.GaussianBlur(img, (3, 3), 0)

    # Krok 5: Łączenie krawędzi i filtrowanego tła
    # Krawędzie pozostają oryginalne, reszta punktów jest filtrowana
    result = cv2.bitwise_and(img, canny_edges) + cv2.bitwise_and(gaussian_blur, mask_non_edges)

    # Wyświetlenie wyniku w Tkinterze
    displayImg = Image.fromarray(result)
    displayImg = displayImg.resize((300, 300), Image.LANCZOS)

    img_display = ImageTk.PhotoImage(displayImg)
    label.config(image=img_display)
    label.image = img_display

    # Zapis przetworzonego obrazu do pliku
    saveImg(result, 'outputFolder', 'FilImg.png')


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


    