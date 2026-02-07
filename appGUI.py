from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from classes import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from textwrap import wrap
import random
import os


def createMainWindow():
    ctk.set_appearance_mode("dark") 
    ctk.set_default_color_theme("green")
    ctk.deactivate_automatic_dpi_awareness()


    app = ctk.CTk()
    app.title("Random cook - ")
    app.iconbitmap('images/chef.ico')
    app.geometry("900x600")
    app.resizable(False, False)
    width = 900
    height = 600
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2) - 50
    position_left = int(screen_width / 2 - width / 2)
    app.geometry(f"{width}x{height}+{position_left}+{position_top}")


    numbers = ["1","2","3","4","5","6","7"]
    textForPDF = ""

    numbersOfDays = tk.StringVar()
    isVege = tk.BooleanVar()
    czyPrzekaski = tk.BooleanVar()


                            # -------------- COMPONENTS -----------------
    downloadImage = ctk.CTkImage(light_image=Image.open("images/downloadButton.png"), size=(25, 25))

    shaffleButton = ctk.CTkButton(app, text="Losuj dania", command=lambda: shuffleMealPlan(app, mainFrame, naIleDniCombobox,czyWegeCheckbox, czyPrzekaskiChecbox, czyDeseryCheckbox, downloadImage, textForPDF), corner_radius=50, fg_color='green', hover_color='#49cc49')
    shaffleButton.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    addMealButton = ctk.CTkButton(app,text="Dodaj potrawe", command=lambda: openAddRecipeWindow(app), corner_radius=50, fg_color='green', hover_color='#49cc49')
    addMealButton.place(relx=0.8, rely=0.9, anchor=tk.CENTER)

    updateRecipeButton = ctk.CTkButton(app, text="Zaaktualizuj przepis", command=lambda: openUpdateRecipeWindow(app), corner_radius=50, fg_color="green", hover_color='#49cc49')
    updateRecipeButton.place(relx=0.2, rely=0.9, anchor=tk.CENTER)

    mainLabel = ctk.CTkLabel(app,text="Nie myśl co by tu dziś ugotować",height=25, width=25, font=("Helvetica", 20))
    mainLabel.place(relx= 0.5, rely=0.05, anchor=tk.CENTER)

    textLabel = ctk.CTkLabel(app, text="wylosuj dania na cały tydzień spośród rekomendowanej bazy przepisów", height=25, width=250, font=("Helvetica", 16))
    textLabel.place(relx=0.23, rely=0.08)

    naIleDniLabel = ctk.CTkLabel(app, text="Na ile dni dieta", height=25, width=25, font=("Helvetica", 15))
    naIleDniLabel.place(relx=0.21, rely=0.19)

    naIleDniCombobox = ctk.CTkComboBox(app, values=numbers, variable=numbersOfDays, width=100, height=30, font=("Arial", 16), state="readonly")
    naIleDniCombobox.place(relx=0.08, rely=0.19)

    czyPrzekaskiChecbox = ctk.CTkCheckBox(app,text="Czy przękąski", variable=czyPrzekaski, width=100, height=35)
    czyPrzekaskiChecbox.place(relx=0.4, rely=0.19)

    czyWegeCheckbox = ctk.CTkCheckBox(app, text="Czy wege", variable=isVege, width=100, height=35)
    czyWegeCheckbox.place(relx=0.6, rely=0.19)

    czyDeseryCheckbox = ctk.CTkCheckBox(app, text="Czy desery", width=100, height=35) 
    czyDeseryCheckbox.place(relx=0.8, rely=0.19)

    mainFrame = ctk.CTkScrollableFrame(app, width=800, height=320, orientation="horizontal")
    mainFrame.place(relx=0.5, rely=0.55, anchor=tk.CENTER) 

    clearRecipeButton = ctk.CTkButton(app, text="Czyść", width=20, command=lambda: clearMainFrame(app, mainFrame), corner_radius=50, fg_color='red', hover_color='#49cc49')
    clearRecipeButton.place(relx=0.05, rely=0.9, anchor=tk.CENTER)

    app.mainloop()


# ---------------- OPENERY -----------------------------

def openAddRecipeWindow(app):
    newWindow = AddRecipeWindow(app)


def openUpdateRecipeWindow(app):
    newWindow = UpdateRecipeWindow(app)



# ---------------- RESZTA ------------------------------

def clearMainFrame(app, mainFrame):
    # funkcja do usuwania zawartości mainFrame jeśli była
    if mainFrame.winfo_children():
        for widget in mainFrame.winfo_children():
            widget.destroy()


def saveRecipeToPDF(textForPDF):
    # Funkcja do zapisu wylosowanych przepisów do pliku PDF
    folder = "przepisyPDFs"
    folder1 = "font"

    if not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(folder1):
        os.makedirs(folder1)

    sciezka1 = os.path.join(folder1, f"DejaVuSans.ttf")

    # Rejestracja czcionki DejaVu do obsługi polskich znaków
    pdfmetrics.registerFont(TTFont("DejaVuSans", sciezka1))
    
    pliki = [f for f in os.listdir(folder) if f.startswith("przepisy_") and f.endswith(".pdf")]
    numery = []
    
    for plik in pliki:
        numer = plik.split('_')[1].split('.')[0]
        numery.append(int(numer))
    
    # Jeśli są jakieś pliki, bierzemy najwyższy numer i zwiększamy o 1
    numer_pliku = max(numery, default=0) + 1
    
    sciezka = os.path.join(folder, f"przepisy_{numer_pliku}.pdf")
    
    # Tworzenie pliku PDF
    c = canvas.Canvas(sciezka, pagesize=letter)
    c.setFont("DejaVuSans", 12)

    # Parametry pozycji (wysokość, gdzie zaczynamy rysowanie)
    x = 50
    y = 750
    max_width = 500  

    lines = textForPDF.split("\n")
    
    for line in lines:
        # Zawijanie tekstu na podstawie maksymalnej szerokości
        wrapped_lines = wrap(line, width=int(max_width / 7))  # Dopasowanie szerokości (7 punktów na znak)
        
        for wrapped_line in wrapped_lines:
            c.drawString(x, y, wrapped_line)
            y -= 15  # Przesuwamy Y w dół dla następnej linii
            
            if y < 50:  #
                c.showPage()  
                c.setFont("DejaVuSans", 12)  
                y = 750  # Resetujemy pozycję Y na nowej stronie
    
    c.save()


def extractIngredientsPretty(tekst):
    # funkcja do ładnego przedstawienia składników w frame w oknie głównym
    składniki = ""
    
    for i in range(len(tekst[0]["ingredients"])):
        składniki += f'{tekst[0]["ingredients"][i]["name"]} '

        if len(tekst[0]["ingredients"][i]) > 1:
            try:
                składniki += f'{tekst[0]["ingredients"][i]["quantity"]} '
                if len(tekst[0]["ingredients"][i]) > 2:
                    składniki += f'{tekst[0]["ingredients"][i]["unit"]}\n'
                else:
                    składniki += "\n"
            except (ValueError, KeyError) as e:
                składniki += f'{tekst[0]["ingredients"][i]["unit"]}\n'
        else:
            składniki += "\n"

    return składniki


def checkIDLists(ListAllID, iloscDniDiety, isVege, mealType):
    # funkcja sprawdzająca czy jest odpowiednia ilość przepisów dla warunku isVege
    wylosowaneID = []

    if len(ListAllID) == 0:
        if isVege == True:
            messagebox.showerror("Error", f"Baza danych NIE zawiera przepisów w wersji wegetariańskiej dla {mealType}.")
        else:
            messagebox.showerror("Error", f"Baza danych NIE zawiera przepisów w wersji nie wegetariańskiej dla {mealType}.")
    else: 
        try:
            wylosowaneID = random.sample(ListAllID, k=int(iloscDniDiety))

        except ValueError:
            for i in range(int(iloscDniDiety)):
                try:
                    wylosowaneID = random.sample(ListAllID, k=int(iloscDniDiety) - (i+1))
                    break
                except ValueError:
                    continue

            print(wylosowaneID)

            if len(wylosowaneID) < int(iloscDniDiety):
                for i in range(int(iloscDniDiety) - len(wylosowaneID)):
                    x = random.choice(wylosowaneID)
                    wylosowaneID.append(x)

    return wylosowaneID
   

def shuffleMealPlan(app, mainFrame, naIleDniCombobox, czyWegeCheckbox, czyPrzekaskiChecbox, czyDeseryCheckbox, downloadImage, textForPDF):
    # funcja losująca na każdy wybrany dzień posiłki według kategorii
    iloscDniDiety = naIleDniCombobox.get()
    czyWege = bool(czyWegeCheckbox.get())
    czyPrzekaski = bool(czyPrzekaskiChecbox.get())
    czyDesery = bool(czyDeseryCheckbox.get())


    if iloscDniDiety == "":
        messagebox.showerror("Error", "Należy podać na ile dni rozpisać diete")
    else:
        clearMainFrame(app, mainFrame)

        if czyWege == True:
            AllSniadaniaID = [x.get("_id") for x in db.śniadania.find({"isVege": bool(True)},{"_id":1}).sort({"_id":1})]
            wylosowaneSniadaniaID = checkIDLists(AllSniadaniaID, int(iloscDniDiety), True, "śniadania")

            AllObiadyID = [x.get("_id") for x in db.obiady.find({"isVege": bool(True)},{"_id":1}).sort({"_id":1})]
            wylosowaneObiadyID = checkIDLists(AllObiadyID, int(iloscDniDiety), True, "obiady")

            AllKolacjeID = [x.get("_id") for x in db.kolacje.find({"isVege": bool(True)},{"_id":1}).sort({"_id":1})]
            wylosowaneKolacjeID = checkIDLists(AllKolacjeID, int(iloscDniDiety), True, "kolacje")

        else:
            AllSniadaniaID = [x.get("_id") for x in db.śniadania.find({"isVege": bool(False)},{"_id":1}).sort({"_id":1})]
            wylosowaneSniadaniaID = checkIDLists(AllSniadaniaID, int(iloscDniDiety), False, "śniadania")

            AllObiadyID = [x.get("_id") for x in db.obiady.find({"isVege": bool(False)},{"_id":1}).sort({"_id":1})]
            wylosowaneObiadyID = checkIDLists(AllObiadyID, int(iloscDniDiety), False, "obiady")

            AllKolacjeID = [x.get("_id") for x in db.kolacje.find({"isVege": bool(False)},{"_id":1}).sort({"_id":1})]
            wylosowaneKolacjeID = checkIDLists(AllKolacjeID, int(iloscDniDiety), False, "kolacje")


        wylosowaneSniadania = []
        wylosowaneObiady = []
        wylosowaneKolacje = []


        for i in range(int(iloscDniDiety)):
            tekstS = [x for x in db.śniadania.find({"_id": wylosowaneSniadaniaID[i]}, {"_id": 0, "createdAt":0, "updatedAt":0})]
            przepisS = f'{tekstS[0]["name"]}\n\nSkładniki:\n{extractIngredientsPretty(tekstS)}\n\nWykonanie:\n{tekstS[0]["instructions"]}\n\nCzas przygotowania:\n{tekstS[0]["prep_time"]} minut\nIlość Kalori:\n{tekstS[0]["calories"]} kcal\nCzy Wegetariańskie:\n{tekstS[0]["isVege"]}\n__________________'
            
            tekstO = [x for x in db.obiady.find({"_id": wylosowaneObiadyID[i]}, {"_id": 0, "createdAt":0, "updatedAt":0})]
            przepisO = f'{tekstO[0]["name"]}\n\nSkładniki:\n{extractIngredientsPretty(tekstO)}\n\nWykonanie:\n{tekstO[0]["instructions"]}\n\nCzas przygotowania:\n{tekstO[0]["prep_time"]} minut\nIlość Kalori:\n{tekstO[0]["calories"]} kcal\nCzy Wegetariańskie:\n{tekstO[0]["isVege"]}\n__________________'

            tekstK = [x for x in db.kolacje.find({"_id": wylosowaneKolacjeID[i]}, {"_id": 0, "createdAt":0, "updatedAt":0})]
            przepisK = f'{tekstK[0]["name"]}\n\nSkładniki:\n{extractIngredientsPretty(tekstK)}\n\nWykonanie:\n{tekstK[0]["instructions"]}\n\nCzas przygotowania:\n{tekstK[0]["prep_time"]} minut\nIlość Kalori:\n{tekstK[0]["calories"]} kcal\nCzy Wegetariańskie:\n{tekstK[0]["isVege"]}\n__________________'

            wylosowaneSniadania.append(przepisS)
            wylosowaneObiady.append(przepisO)
            wylosowaneKolacje.append(przepisK)


        if czyPrzekaski == True:
            if czyWege == True:
                AllPrzekaskiID = [x.get("_id") for x in db.przekąski.find({"isVege": bool(True)},{"_id":1}).sort({"_id":1})]
                wylosowanePrzekaskiID = checkIDLists(AllPrzekaskiID, int(iloscDniDiety), True, "przekąski")
            else:
                AllPrzekaskiID = [x.get("_id") for x in db.przekąski.find({"isVege": bool(False)},{"_id":1}).sort({"_id":1})]
                wylosowanePrzekaskiID = checkIDLists(AllPrzekaskiID, int(iloscDniDiety), False, "przekąski")

            wylosowanePrzekaski = []

            for i in range(int(iloscDniDiety)):
                tekst = [x for x in db.przekąski.find({"_id": wylosowanePrzekaskiID[i]}, {"_id": 0, "createdAt":0, "updatedAt":0})]
                przepis = f'{tekst[0]["name"]}\n\nSkładniki:\n{extractIngredientsPretty(tekst)}\n\nWykonanie:\n{tekst[0]["instructions"]}\n\nCzas przygotowania:\n{tekst[0]["prep_time"]} minut\nIlość Kalori:\n{tekst[0]["calories"]} kcal\nCzy Wegetariańskie:\n{tekst[0]["isVege"]}\n__________________'

                wylosowanePrzekaski.append(przepis)
            

        if czyDesery == True:
            if czyWege == True:
                AllDeseryID = [x.get("_id") for x in db.desery.find({"isVege": bool(True)},{"_id":1}).sort({"_id":1})]
                wylosowaneDeseryID = checkIDLists(AllDeseryID, int(iloscDniDiety), True, "desery")
            else:
                AllDeseryID = [x.get("_id") for x in db.desery.find({"isVege": bool(False)},{"_id":1}).sort({"_id":1})]
                wylosowaneDeseryID = checkIDLists(AllDeseryID, int(iloscDniDiety), False, "desery")

            wylosowaneDesery = []

            for i in range(int(iloscDniDiety)):
                tekst = [x for x in db.desery.find({"_id": wylosowaneDeseryID[i]}, {"_id": 0, "createdAt":0, "updatedAt":0})]
                przepis = f'{tekst[0]["name"]}\n\nSkładniki:\n{extractIngredientsPretty(tekst)}\n\nWykonanie:\n{tekst[0]["instructions"]}\n\nCzas przygotowania:\n{tekst[0]["prep_time"]} minut\nIlość Kalori:\n{tekst[0]["calories"]} kcal\nCzy Wegetariańskie:\n{tekst[0]["isVege"]}\n__________________'

                wylosowaneDesery.append(przepis)

        frameTextDict = {}

            # tworzenie słownika który zawiera nazwe jako klucz i liste jako wartość
        for i in range(int(iloscDniDiety)):
            frameTextDict[f'frameText{i+1}'] = [] 


            # pętla do wpisywania danych do list słowników
        for i in range(int(iloscDniDiety)):
            
            frame_text1 = [wylosowaneSniadania[i], wylosowaneObiady[i], wylosowaneKolacje[i]]

            frameTextDict[f'frameText{i+1}'] = frame_text1.copy()  

            if czyDesery == True:
                frameTextDict[f'frameText{i+1}'].append(wylosowaneDesery[i])

            if czyPrzekaski == True:
                frameTextDict[f'frameText{i+1}'].append(wylosowanePrzekaski[i])


            # wyświetlenie słownika z przepisami
        # for key, value in frameTextDict.items():
        #     print(f"{key}: {value}")
        
        # print(len(frameTextDict))

        numFrames = int(naIleDniCombobox.get())
        textForPDF = "Rozpisana dla ciebie dieta: \n\n"
        
        for i, texts in enumerate(frameTextDict.values()):
            frame = RecipeFrame(mainFrame, text_list=texts, scrollbar_button_color="#b51b3d", scrollbar_button_hover_color="orange", border_color="#b51b3d", fg_color="#3d3d3d")
            textForPDF += f"\n\nDzień {i+1}:  "
            
            for text in texts:
                textForPDF += f"{text}\n"

            frame.grid(row=0, column=i, sticky="nsew", padx=5)
        

        for i in range(numFrames):
            mainFrame.grid_columnconfigure(i, weight=1)

        mainFrame.grid_rowconfigure(0, weight=1)
        
        app.pobierzDieteButton = ctk.CTkButton(app, text="", height=35, width=35, image=downloadImage, command=lambda: saveRecipeToPDF(textForPDF), corner_radius=100, fg_color="#e07816", hover_color="orange") 
        app.pobierzDieteButton.place(relx=0.95, rely= 0.9, anchor=tk.CENTER)



