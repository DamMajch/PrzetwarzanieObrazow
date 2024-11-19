import tkinter as tk
from inne import getImg, get_path, Chosenimg, saveMultipleImg
from filters import adaptFilter
from filters import adaptive_median_filter
from filters import adaptive_wiener_filter
from filters import adaptive_gaussian_filter
from filters import bilateral_filter


root = tk.Tk()
root.title("Filtry adaptacyjne")

# Zmiana języka

str1 = tk.StringVar(value="Filtry adaptacyjne") 
str2 = tk.StringVar(value="Adaptacyjny Filtr Medianowy") 
str3 = tk.StringVar(value="Adaptacyjny Filtr Wienerowski") 
str4 = tk.StringVar(value="Adaptacyjny Filtr Gaussowski") 
str5 = tk.StringVar(value="Filtr Bilateralny") 
str6 = tk.StringVar(value="Wybierz obraz") 
str7 = tk.StringVar(value="Dodaj Szum") 
str8 = tk.StringVar(value="Zapisz obraz") 
str9 = tk.StringVar(value="Próbny filtr") 

def change_language():
    if str1.get() == "Filtry adaptacyjne":
        str1.set("Adaptive Filters")
        str2.set("Adaptive Median Filter")
        str3.set("Adaptive Wiener Filter")
        str4.set("Adaptive Gaussian Filter")
        str5.set("Bilateral Filter")
        str6.set("Choose Image")
        str7.set("Add Noise")
        str8.set("Save Image")
        str9.set("Experimental Filter")

    else:
        str1.set("Filtry adaptacyjne") 
        str2.set("Adaptacyjny Filtr Medianowy")
        str3.set("Adaptacyjny Filtr Wienerowski")
        str4.set("Adaptacyjny Filtr Gaussowski")
        str5.set("Filtr Bilateralny")
        str6.set("Wybierz obraz")
        str7.set("Dodaj Szum")
        str8.set("Zapisz obraz")
        str9.set("Próbny filtr")



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
buttonFrame.pack(padx=10, pady=80)

# Frame dla wyświetlania obrazu

frameImg = tk.Frame(frame1, bg='blue')
frameImg.pack(side=tk.TOP, padx=10, pady=10)

# Frame dla wyświetlania zaszumionego obrazu

frameImgSzum = tk.Frame(frame2, bg='blue')
frameImgSzum.pack(side=tk.TOP, padx=10, pady=10)

# Frame dla wyświetlania przefiltrowanego obrazu i do zapisania go

frameImgZapisz = tk.Frame(frame3, bg='blue')
frameImgZapisz.pack(side=tk.TOP, padx=10, pady=10)

# Przycisk do zmiany języka na angielski i z powrotem

enPLButt = tk.Button(frameButtons, text="En/Pl", command=change_language)
enPLButt.place(relx=0.975, rely=0)

# Przycisk do filtra medianowego (button1)
button1 = tk.Button(buttonFrame, textvariable=str2, width=25, height=5, cursor="hand2",
                    command=lambda: adaptive_median_filter("outputFolder/NoisyImg.jpg", label3))
button1.pack(side=tk.LEFT, padx=50, pady=40)

# Przycisk do filtra Wienerowskiego (button2)
button2 = tk.Button(buttonFrame, textvariable=str3, width=25, height=5, cursor="hand2",
                    command=lambda: adaptive_wiener_filter("outputFolder/NoisyImg.jpg", label3))
button2.pack(side=tk.LEFT, padx=50, pady=10)

# Przycisk do filtra Gaussa 
button3 = tk.Button(buttonFrame, textvariable=str4, width=25, height=5, cursor="hand2",
                    command=lambda: adaptive_gaussian_filter("outputFolder/NoisyImg.jpg", label3))
button3.pack(side=tk.LEFT, padx=50, pady=10)
# Przycisk do filtra bilateralnego
button4 = tk.Button(buttonFrame, textvariable=str5, width=25, height=5, cursor="hand2",
                    command=lambda: bilateral_filter("outputFolder/NoisyImg.jpg", label3))
button4.pack(side=tk.LEFT, padx=50, pady=10)


# Przycisk do wybierania i wyświetlania obrazów

open_button1 = tk.Button(frame1, textvariable=str6, width=12, command=lambda: get_path(label1), cursor="hand2")
open_button1.pack( padx=10, pady=10)

label1 = tk.Label(frame1)
label1.pack(padx=10, pady=10)


Sciezka = "outputFolder/NoisyImg.jpg"

# Przycisk do zaszumienia obrazu

open_button2 = tk.Button(frame2, textvariable=str7, width=12,command=lambda: Chosenimg(Sciezka, label2), cursor="hand2")
open_button2.pack( padx=10, pady=10)

label2 = tk.Label(frame2)
label2.pack(padx=10, pady=10)

# Przycisk do zapisywania obrazów

open_button3 = tk.Button(frame3, textvariable=str8, width=12, command=lambda: saveMultipleImg(getImg(pitiPath),"ZapisaneObrazy"), cursor="hand2")
open_button3.pack( padx=10, pady=10)

# próbny filtr. Żeby wypróbować jak działa filtrowanie

button5 = tk.Button(buttonFrame, textvariable=str9, width=25, height=5, command= lambda: adaptFilter("outputFolder/NoisyImg.jpg" , label3),cursor="hand2")
button5.pack(padx=50, pady=40)

label3 = tk.Label(frame3)
label3.pack(padx=10, pady=10)

root.mainloop()