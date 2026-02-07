import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from pymongo import MongoClient
from PIL import Image
import re
from datetime import datetime


    # Globalne połączenie z bazą danych MongoDB na localhost
client = MongoClient('mongodb://localhost:27017/')
db = client['przepisy'] 


# -----------------------------------------------------------------------------------------------------------------------------------------
    # customowy Entrybox który zezwala tylko na podawanie liczby całkowitych
class CustomEntry(ctk.CTkEntry):
    def __init__(self, master, **kwargs): 
        super().__init__(master, **kwargs)
        self.configure(validate="key")
        self.configure(validatecommand=(self.register(self.validate_input), '%P'))
        
    def validate_input(self, new_text):
        # Sprawdzanie dozwolonych wartości. Dozwolone są tylko cyfry dla objektów CustomEntry
        return re.match(r'^[0-9]*$', new_text) is not None
    


# -----------------------------------------------------------------------------------------------------------------------------------------
    # klasa wyświetlająca okno z formularzem do dodawania receptury
class AddRecipeWindow():
    def __init__(self, root):
        self.addRecipeWindow = ctk.CTkToplevel(root)
        self.addRecipeWindow.title("Add new recipe - wariacie")
        self.addRecipeWindow.iconbitmap('images/chef.ico')
        width = 450
        height = 680
        screen_width = self.addRecipeWindow.winfo_screenwidth()
        screen_height = self.addRecipeWindow.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2) - 50
        position_left = int(screen_width / 2 - width / 2)
        self.addRecipeWindow.geometry(f"{width}x{height}+{position_left}+{position_top}")
        self.addRecipeWindow.resizable(False, False)
        #addRecipeWindow.lift()
        #addRecipeWindow.focus_force()
        #addRecipeWindow.attributes("-topmost", 1)
        
        self.ingredientsList = []
        recipeName = tk.StringVar()
        mealCategory = tk.StringVar()
        kcal = tk.StringVar()
        prepTime = tk.StringVar()
        isVege = tk.BooleanVar()
        
        mealOptions = ["śniadania", "obiady", "kolacje", "przekąski", "desery"]

            # -------------------------------- addRecipeWindow COMPONENTS --------------------------------------
        self.addMealButton = ctk.CTkButton(self.addRecipeWindow, text="Dodaj przepis", command=lambda: self.addNewMeal(self.recipeNameEntry, self.mealCategoryCombobox, self.kcalEntry, self.prepTimeEntry, self.czyWegeCheckbox, self.ingredientsList, self.recipeEntry), corner_radius=50, fg_color='green', hover_color='#49cc49')
        self.addMealButton.grid(row=13, column=0, padx=20, pady=10, sticky='nsew')

        self.closeButton = ctk.CTkButton(self.addRecipeWindow, text="Wyjdź", command=self.close, corner_radius=50, fg_color='#d12634', hover_color='orange')
        self.closeButton.grid(row=13, column=1, padx=20, pady=10, sticky='nsew')

        self.recipeNameLabel = ctk.CTkLabel(self.addRecipeWindow, text="Nazwa przepisu *", font=("Helvetica", 14))
        self.recipeNameLabel.grid(row=0, column=0, padx=10, pady=2, sticky='w')

        self.recipeNameEntry = ctk.CTkEntry(self.addRecipeWindow, textvariable=recipeName, placeholder_text="Podaj nazwe przepisu", width=200, height=30) 
        self.recipeNameEntry.grid(row=1, column=0, padx=10, pady=2, sticky='w')

        self.mealCategoryLabel = ctk.CTkLabel(self.addRecipeWindow, text="Kategoria przepisu *", font=("Helvetica", 14))
        self.mealCategoryLabel.grid(row=2, column=0, padx=10, pady=2, sticky='w')

        self.mealCategoryCombobox = ctk.CTkComboBox(self.addRecipeWindow, variable=mealCategory, values=mealOptions, width=150, height=30, font=("Arial", 14), state="readonly")
        self.mealCategoryCombobox.grid(row=3, column=0, padx=10, pady=2, sticky='w')

        self.kcalLabel = ctk.CTkLabel(self.addRecipeWindow, text="Ilość kalori *", font=("Helvetica", 14))
        self.kcalLabel.grid(row=4, column=0, padx=10, pady=2, sticky='w')

        self.kcalEntry = CustomEntry(self.addRecipeWindow, textvariable=kcal, placeholder_text="Podaj ilość kalori dla posiłku", width=200, height=30)
        self.kcalEntry.grid(row=5, column=0, padx=10, pady=2, sticky='w')

        self.prepTimeLabel = ctk.CTkLabel(self.addRecipeWindow, text="Czas przygotowania [min] *", font=("Helvetica", 14))
        self.prepTimeLabel.grid(row=6, column=0, padx=10, pady=2, sticky='w')

        self.prepTimeEntry = CustomEntry(self.addRecipeWindow,  textvariable=prepTime, placeholder_text="Podaj czas przygotowania", width=200, height=30)
        self.prepTimeEntry.grid(row=7, column=0, padx=10, pady=2, sticky='w')
        
        self.czyWegeCheckbox = ctk.CTkCheckBox(self.addRecipeWindow, variable=isVege, text="Czy wege", width=100, height=35)  
        self.czyWegeCheckbox.grid(row=8, column=0, padx=10, pady=5, sticky='w')

        self.ingredientsLabel = ctk.CTkLabel(self.addRecipeWindow, text="Lista składników *", font=("Helvetica", 14))
        self.ingredientsLabel.grid(row=9, column=0, padx=10, pady=2, sticky='w')

        self.helpFrame = ctk.CTkFrame(self.addRecipeWindow, fg_color="#242424")
        self.helpFrame.grid(row=9, column=1, padx=10, pady=2, sticky='w')

        self.addIngredientsButton = ctk.CTkButton(self.helpFrame, text="+", command=self.openAddIngredientsWindow, corner_radius=100, fg_color='green', hover_color='#49cc49', width=40, font=("Helvetica", 18)) 
        self.addIngredientsButton.grid(row=9, column=0, padx=10, pady=2, sticky='w') 

        self.subtractIngredientsButton = ctk.CTkButton(self.helpFrame, text="-", command=self.subtractIngredient, corner_radius=100, fg_color='#d12634', hover_color='orange', width=40, font=("Helvetica", 18)) 
        self.subtractIngredientsButton.grid(row=9, column=1, padx=10, pady=2, sticky='w')

        self.ingredientsEntry = ctk.CTkTextbox(self.addRecipeWindow, width=420, height=100, state="disabled")  # state="disable"
        self.ingredientsEntry.grid(row=10, column=0, columnspan=2, padx=10, pady=2, sticky='w')

        self.recipeLabel = ctk.CTkLabel(self.addRecipeWindow, text="Przygotowanie *", font=("Helvetica", 14))
        self.recipeLabel.grid(row=11, column=0, padx=10, pady=2, sticky='w')

        self.recipeEntry = ctk.CTkTextbox(self.addRecipeWindow, width=420, height=150)
        self.recipeEntry.grid(row=12, column=0, columnspan=2, padx=10, pady=2, sticky='w')

        self.addRecipeWindow.bind('<Return>', lambda event: self.addNewMeal(self.recipeNameEntry, self.mealCategoryCombobox, self.kcalEntry, self.prepTimeEntry, self.czyWegeCheckbox, self.ingredientsList, self.recipeEntry))

        self.addRecipeWindow.grab_set()
        self.addRecipeWindow.wait_window(self.addRecipeWindow)


    def close(self):
        self.addRecipeWindow.destroy()

    def openAddIngredientsWindow(self):
        # opener okna do dodawania składników
        AddIngredientsWindow(self)

    def subtractIngredient(self):
        # funkcja odejmująca składnik z ingredientsList
        if len(self.ingredientsList) > 0:
            self.ingredientsList.pop()

            content = self.ingredientsEntry.get("1.0", ctk.END) 
            lines = content.strip().split("\n")  
            if lines:  
                lines.pop()  
                updated_content = "\n".join(lines) 

                if updated_content != "":
                    updated_content += "\n"

                self.ingredientsEntry.configure(state="normal")
                self.ingredientsEntry.delete("1.0", ctk.END) 
                self.ingredientsEntry.insert("1.0", updated_content)  
                self.ingredientsEntry.configure(state="disabled")



        # CREATE
    def addNewMeal(self,recipeNameEntry, mealCategoryEntry, kcalEntry, prepTimeEntry, czyWegeCheckbox, ingredientsList, recipeEntry):
        # funkcja dodająca przepis do bazy danych MongoDB
        recipeName = recipeNameEntry.get()
        mealCategory = mealCategoryEntry.get()
        kcal = kcalEntry.get()
        prepTime = prepTimeEntry.get()
        isVege = czyWegeCheckbox.get()
        recipe = recipeEntry.get("1.0", "end-1c") 

        if any(x == "" for x in [kcal, prepTime]):
            kcal = ""
            prepTimeEntry = ""
        else:
            kcal = int(kcalEntry.get())
            prepTime = int(prepTimeEntry.get())

        if any(field == "" for field in [recipeName, mealCategory, kcal, prepTime, isVege, recipe]) or len(ingredientsList) < 2 or len(recipe) < 10 or len(recipeName) < 5:
            if any(field == "" for field in [recipeName, mealCategory, kcal, prepTime, isVege, recipe]):
                messagebox.showerror("Error", "Nie poddano wszytkich wymaganych wartości - Każde pole musi być podane !")
            elif len(ingredientsList) < 2:
                messagebox.showerror("Error", "Wymagane podanie co najminiej dwóch składników !")
            elif len(recipeName) < 5:
                messagebox.showerror("Error", "Nazwa receptury musi mieć co najmniej 5 znaków !")
            elif len(recipe) < 10:
                messagebox.showerror("Error", "Wartość pola receptury jest za krótka - wymagane minimum 10 znaków !")

        elif kcal <= 100 or prepTime <= 1:
            if kcal <= 10:
                messagebox.showerror("Error", "Wartości kalori musi być większa niż 100 !")
            else:
                messagebox.showerror("Error", "Czas przygotowania nie może być mniejszy niż 1 minuta !")
        else:
            ingredientsObjects = []

            for i in range(len(ingredientsList)):
                ingredient = {}
                ingredient.update({"name": ingredientsList[i][0]})

                if len(ingredientsList[i]) == 1:
                    pass
                elif len(ingredientsList[i]) == 2:
                    if isinstance(ingredientsList[i][1], int):
                        ingredient.update({"quantity": ingredientsList[i][1]})

                    elif isinstance(ingredientsList[i][1], str):
                        ingredient.update({"unit": ingredientsList[i][1]})
                else: 
                    ingredient.update({"quantity": ingredientsList[i][1], "unit": ingredientsList[i][2]})
                
                ingredientsObjects.append(ingredient)

            collectionName = db[mealCategory] 

            queryID = [x for x in collectionName.find({},{"_id":1}).sort({"_id":-1}).limit(1)]
            currentID = queryID[0].get("_id") + 1

            dokument = {
                "_id": currentID,
                "name": recipeName,
                "ingredients": ingredientsObjects,
                "instructions": recipe,
                "meal_type": mealCategory,
                "prep_time": prepTime,
                "calories": kcal,
                "isVege": bool(isVege),
                "createdAt": datetime.now(),
                "updatedAt": datetime.now(),
            }

            collectionName.insert_one(dokument)
            self.close()

                # Sprawdzenie zmiennych
            # print("Nazwa przepisu:", recipeName)
            # print("Kategoria przepisu:", mealCategory)
            # print("Ilość kalori:", kcal)
            # print("Czas przygotowania:", prepTime)
            # print("Czy vege: ", isVege)
            # print("Przygotowanie:", recipe)
            # print(ingredientsObjects)
            # print(dokument)
            # print(currentID)


# -----------------------------------------------------------------------------------------------------------------------------------------
    # klasa wywoływana w klasie AddRecipeWindow, wyświetla okno z możliwością dodania składników 
class AddIngredientsWindow():
    def __init__(self, parentWindow):
        self.parentWindow = parentWindow
        self.addIngredientsWindow = ctk.CTkToplevel()
        self.addIngredientsWindow.title("Dodawanie składników")
        width = 220
        height = 300
        screen_width = self.addIngredientsWindow.winfo_screenwidth()
        screen_height = self.addIngredientsWindow.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2) - 50
        position_left = int(screen_width / 2 - width / 2)
        self.addIngredientsWindow.geometry(f"{width}x{height}+{position_left}+{position_top}")
        self.addIngredientsWindow.resizable(False, False)

        self.nameLabel = ctk.CTkLabel(self.addIngredientsWindow, text="Nazwa składnika *", font=("Helvetica", 14))
        self.nameLabel.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.nameEntry = ctk.CTkEntry(self.addIngredientsWindow, width=200, height=30)
        self.nameEntry.grid(row=1, column=0, sticky="w", padx=10, pady=3)

        self.quantityLabel = ctk.CTkLabel(self.addIngredientsWindow, text="Ilość", font=("Helvetica", 14))
        self.quantityLabel.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.quantityEntry = CustomEntry(self.addIngredientsWindow, width=200, height=30)
        self.quantityEntry.grid(row=3, column=0, sticky="w", padx=10, pady=3)

        self.unitLabel = ctk.CTkLabel(self.addIngredientsWindow, text="Jednostka", font=("Helvetica", 14))
        self.unitLabel.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        self.unitEntry = ctk.CTkEntry(self.addIngredientsWindow, width=200, height=30)
        self.unitEntry.grid(row=5, column=0, sticky="w", padx=10, pady=3)

        self.addIngredientsButton = ctk.CTkButton(self.addIngredientsWindow, text="Dodaj składnik",command=self.addToIngredientList, corner_radius=50, fg_color='green', hover_color='#49cc49', width=50)
        self.addIngredientsButton.grid(row=6, column=0, sticky="nesw", padx=50, pady=20)

        self.addIngredientsWindow.bind('<Return>', lambda event: self.addToIngredientList())
        
        self.addIngredientsWindow.grab_set()
        self.addIngredientsWindow.wait_window(self.addIngredientsWindow)


    def addToIngredientList(self):
        # funkcja dodajaca składnik do ingredientsList w celu przekazania listy do funkccji dodającej przepisy do bazy danych w klasie AddRecipeWindow
        ingredientName = self.nameEntry.get()
        
        if ingredientName:
            if len(ingredientName) >= 2:
                ingredientQuantity = self.quantityEntry.get()
                ingredientUnit = self.unitEntry.get()

                ingredient = [ingredientName]
                ingredientText = f"{ingredientName} " #Składnik: 

                if ingredientQuantity: 
                    ingredient.append(int(ingredientQuantity))
                    ingredientText += f" {ingredientQuantity} " #ilość: 

                if ingredientUnit:
                    ingredient.append(ingredientUnit)
                    ingredientText += f" {ingredientUnit}" #jednostka: 

                self.parentWindow.ingredientsList.append(ingredient)
                self.parentWindow.ingredientsEntry.configure(state="normal")
                self.parentWindow.ingredientsEntry.insert(ctk.END, ingredientText + "\n")
                self.parentWindow.ingredientsEntry.configure(state="disabled")
                self.nameEntry.delete(0, ctk.END)
                self.quantityEntry.delete(0, ctk.END)
                self.unitEntry.delete(0, ctk.END)
                # print(self.parentWindow.ingredientsList)  # sprawdzenie stanu listy po dodawaniu do niej

            else:
                self.showLenError()
        else: 
            self.showInputNameError()
            

    def clearPlaceholderText(self):
        # funkcja ustawiająca kolor napisów błędów
        self.nameEntry.configure(placeholder_text="", placeholder_text_color="white")

    def showInputNameError(self):
            # Błąd: Brak nazwy składnika
        self.nameEntry.delete(0, ctk.END)
        self.quantityEntry.delete(0, ctk.END)
        self.unitEntry.delete(0, ctk.END)
        self.nameEntry.configure(placeholder_text="Należy podać nazwę składnika!", placeholder_text_color="red")
        self.addIngredientsWindow.after(2000, self.clearPlaceholderText)
        
    def showLenError(self):
            # Błąd: Nazwa składnika musi mieć min. 2 znaki
        self.nameEntry.delete(0, ctk.END)
        self.quantityEntry.delete(0, ctk.END)
        self.unitEntry.delete(0, ctk.END)
        self.nameEntry.configure(placeholder_text="Nazwa musi mieć min. 2 znaki!", placeholder_text_color="red")
        self.addIngredientsWindow.after(2000, self.clearPlaceholderText)
    


# -----------------------------------------------------------------------------------------------------------------------------------------
    # klasa wywoływana w klasie AddRecipeWindow, wyświetla okno z możliwością dodania składników 
class UpdateRecipeWindow():
    def __init__(self, root):
        self.updateRecipeWindow = ctk.CTkToplevel(root)
        self.updateRecipeWindow.title("Aktualizacja przepisów")
        self.updateRecipeWindow.iconbitmap('images/chef.ico')
        width = 450
        height = 700
        screen_width = self.updateRecipeWindow.winfo_screenwidth()
        screen_height = self.updateRecipeWindow.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2) - 50
        position_left = int(screen_width / 2 - width / 2)
        self.updateRecipeWindow.geometry(f"{width}x{height}+{position_left}+{position_top}")
        self.updateRecipeWindow.resizable(False, False)

        self.ingredientsString = ""
        self.ingredientsList = []
        mealOptions = ["śniadania", "obiady", "kolacje", "przekąski", "desery"]
        self.recipeNames = []

        self.mealOptionLabel = ctk.CTkLabel(self.updateRecipeWindow, text="Kategoria przepisu", font=("Helvetica", 14))
        self.mealOptionLabel.grid(row=0, column=0, padx=10, pady=4, sticky='w')

        self.mealOptionsCombobox = ctk.CTkComboBox(self.updateRecipeWindow, values=mealOptions, width=170, height=35, font=("Arial", 16), state="readonly")
        self.mealOptionsCombobox.grid(row=1, column=0, padx=10, pady=2, sticky='w')

        self.mealOptionsCombobox.configure(command=self.mealOptionsBind)

        self.updateRecipeWindow.grab_set()
        self.updateRecipeWindow.wait_window(self.updateRecipeWindow)


    def close(self):
        # funkcja zamykająca okno updateRecipeWindow
        self.updateRecipeWindow.destroy()


        # UPDATE
    def updateRecipe(self): 
        # funkcja wkonująca update wybranej receptury
        selectedMealType = db[self.mealOptionsCombobox.get()]
        selectedRecipeName = self.recipeNamesCombobox.get()
        prepTime = self.prepTimeEntry.get()
        calories = self.kcalEntry.get()
        isVege = self.czyWegeCheckbox.get()
        instructions = self.instructionsEntry.get("1.0", "end-1c")
        ingredients = self.ingredientsEntry.get("1.0", "end-1c")

            # obsułga właściwosci wstawiania
        if len(instructions) < 10: 
            messagebox.showerror("Error", "Wartość pola receptury jest za krótka - wymagane minimum 10 znaków !")
        elif int(prepTime) < 1:
            messagebox.showerror("Error", "Czas przygotowania nie może być mniejszy niż 1 minuta !")
        elif int(calories) < 10:
            messagebox.showerror("Error", "Wartości kalori musi być większa niż 100 !")
        elif len(ingredients) == 0:
            messagebox.showerror("Error", "Wymagane podanie co najminiej dwóch składników !")
        else:
            ingredientsObjects = []

            for i in ingredients.splitlines():
                dictt = {}
                parts = i.split("  ")
                dictt.update({"name": i.split("  ")[0]})

                if len(parts) > 1:
                    try:
                        dictt.update({"quantity": int(parts[1])})
                        if len(parts) > 2:
                            dictt.update({"unit": parts[2]})
                    except ValueError:
                        dictt.update({"unit": parts[1]})

                ingredientsObjects.append(dictt)
        
            # print(ingredientsObjects)
            # print(selectedMealType)
            # print(selectedRecipeName)
            # print(prepTime)
            # print(calories)
            # print(isVege)
            # print(instructions)
            # print(ingredients)


                # wykoanie update
            selectedMealType.update_one(
                {"name": selectedRecipeName},
                {
                    "$set": {
                        "ingredients": ingredientsObjects,
                        "instructions": instructions,
                        "prep_time": int(prepTime),
                        "calories": int(calories),
                        "isVege": bool(isVege),
                        "updatedAt": datetime.now()
                    }
                }
            )
            self.close()


    def showDeleteConfirmWindow(self):
        # fukncja wyświetla okno z potwierdzeniem usunięcia
        selectedMealType = db[self.mealOptionsCombobox.get()]
        selectedRecipeName = self.recipeNamesCombobox.get()
        DeleteOrNotWindow(self, selectedMealType, selectedRecipeName)
    

        # DELETE
    def deleteRecipe(self, selectedMealType, selectedRecipeName): 
        # funkcja do usuwania receptur z bazy danych
        selectedMealType.delete_one({"name": selectedRecipeName})
        self.updateRecipeWindow.destroy()


    def openAddIngredientsWindowForUpdate(self):
        # opener okna do dodawania składników
        AddIngredientsWindow(self)

    
    def subtractIngredientString(self):
        # funkcja odejmująca składnik z ingredientsString
        if len(self.ingredientsList) > 0:
            self.ingredientsList.pop()

            content = self.ingredientsEntry.get("1.0", ctk.END) 
            lines = content.strip().split("\n")  
            if lines:  
                lines.pop()  
                updated_content = "\n".join(lines) 

                if updated_content != "":
                    updated_content += "\n"

                self.ingredientsEntry.configure(state="normal")
                self.ingredientsEntry.delete("1.0", ctk.END) 
                self.ingredientsEntry.insert("1.0", updated_content)  
                self.ingredientsEntry.configure(state="disabled")


    def mealOptionsBind(self, event):
        # funkcja która jest wywoływana po wyborze opcji z mealOptionsCombobox

        def SearchText(self, selectedMealType):
            # funkcja do wyszukiwania po wpisanym tekscie w self.recipeNamesCombobox
            regex_pattern = f"^{re.escape(self.recipeNamesCombobox.get())}"
            #print(self.recipeNamesCombobox.get())
            self.recipeNames = [x.get("name") for x in selectedMealType.find({"name": {"$regex": regex_pattern, "$options": "i"}},{"_id":0,"name":1})]

            if len(self.recipeNames) == 0:
                self.recipeNames = ["brak"]
            
            self.recipeNamesCombobox.configure(values=self.recipeNames)

        selectedMealType = db[self.mealOptionsCombobox.get()]

        self.recieNameLabel = ctk.CTkLabel(self.updateRecipeWindow, text="Nazwa przepisu", font=("Helvetica", 14))
        self.recieNameLabel.grid(row=2, column=0, padx=10, pady=2, sticky='w')

        self.recipeNamesCombobox = ctk.CTkComboBox(self.updateRecipeWindow, width=270, height=35, font=("Arial", 14), state="readonly") 
        self.recipeNamesCombobox.grid(row=3, column=0, padx=10, pady=2, sticky='w')

        self.recipeNames = [x.get("name") for x in selectedMealType.find({},{"_id":0,"name":1})]
       
        self.recipeNamesCombobox.configure(state="normal", values=self.recipeNames)
        self.recipeNamesCombobox.configure(command=lambda event: self.recipeOptionsBind(event, selectedMealType))
        self.recipeNamesCombobox.bind("<KeyRelease>", lambda event: SearchText(self, selectedMealType))
        # print(f"Wybrano posiłek: {self.recipeNames}")  # sprawdzenie wartości recipeNames


    def recipeOptionsBind(self, event, selectedMealType):
        # funckja oczekujaca na wartość z recipeNameComboboxa
        if hasattr(self, 'kcalEntry') and self.kcalEntry:
            self.kcalEntry.grid_forget()
            self.kcalLabel.grid_forget()
            self.prepTimeEntry.grid_forget()
            self.prepTimeLabel.grid_forget()
            self.czyWegeCheckbox.grid_forget()
            self.ingredientsEntry.grid_forget()
            self.ingredientsLabel.grid_forget()
            self.instructionsEntry.grid_forget()
            self.instructionsLabel.grid_forget()
            self.helpFrame.grid_forget()
            self.addIngredientsButton.place_forget()
            self.subtractIngredientsButton.place_forget()
            self.deleteButton.place_forget()
            

        myImage = ctk.CTkImage(light_image=Image.open("images/trashBin.png"), size=(30, 30))
        
        selectedRecipeName = self.recipeNamesCombobox.get()
        
        if selectedRecipeName != "brak":
            prepTime = selectedMealType.find_one({"name": selectedRecipeName}, {"_id": 0, "prep_time": 1}).get("prep_time")
            calories = selectedMealType.find_one({"name": selectedRecipeName}, {"_id": 0, "calories": 1}).get("calories")
            isVege = selectedMealType.find_one({"name": selectedRecipeName}, {"_id": 0, "isVege": 1}).get("isVege")
            instructions = selectedMealType.find_one({"name": selectedRecipeName}, {"_id": 0, "instructions": 1}).get("instructions")
            self.ingredientsList = selectedMealType.find_one({"name": selectedRecipeName}, {"_id": 0, "ingredients": 1}).get("ingredients")

            # print(self.ingredientsList)

            self.ingredientsString = ""

            for i in range(len(self.ingredientsList)):
                if len(self.ingredientsList[i]) == 3:
                    self.ingredientsString += f'{self.ingredientsList[i].get("name")}  {self.ingredientsList[i].get("quantity")}  {self.ingredientsList[i].get("unit")}\n'
                elif len(self.ingredientsList[i]) == 2:
                    if self.ingredientsList[i].get("qunatity"):
                        self.ingredientsString += f'{self.ingredientsList[i].get("name")}  {self.ingredientsList[i].get("quantity")}\n'
                    else:
                        self.ingredientsString += f'{self.ingredientsList[i].get("name")}  {self.ingredientsList[i].get("unit")}\n'
                else: 
                    self.ingredientsString += f'{self.ingredientsList[i].get("name")}\n'


            self.kcalLabel = ctk.CTkLabel(self.updateRecipeWindow, text="Ilość kalori", font=("Helvetica", 14))
            self.kcalLabel.grid(row=4, column=0, padx=10, pady=2, sticky='w')

            self.kcalEntry = CustomEntry(self.updateRecipeWindow, placeholder_text="Podaj ilość kalori dla posiłku", width=200, height=30)
            self.kcalEntry.grid(row=5, column=0, padx=10, pady=2, sticky='w')
    
            self.prepTimeLabel = ctk.CTkLabel(self.updateRecipeWindow, text="Czas przygotowania [min]", font=("Helvetica", 14))
            self.prepTimeLabel.grid(row=6, column=0, padx=10, pady=2, sticky='w')

            self.prepTimeEntry = CustomEntry(self.updateRecipeWindow, placeholder_text="Podaj czas przygotowania", width=200, height=30)
            self.prepTimeEntry.grid(row=7, column=0, padx=10, pady=2, sticky='w')
            
            self.czyWegeCheckbox = ctk.CTkCheckBox(self.updateRecipeWindow, text="Czy wege", width=100, height=35)  
            self.czyWegeCheckbox.grid(row=8, column=0, padx=10, pady=5, sticky='w')

            self.ingredientsLabel = ctk.CTkLabel(self.updateRecipeWindow, text="Lista składników", font=("Helvetica", 14))
            self.ingredientsLabel.grid(row=9, column=0, padx=10, pady=2, sticky='w')

            self.addIngredientsButton = ctk.CTkButton(self.updateRecipeWindow, text="+", command=self.openAddIngredientsWindowForUpdate, corner_radius=100, fg_color='green', hover_color='#49cc49', width=40, font=("Helvetica", 18)) 
            self.addIngredientsButton.place(relx=0.6, rely=0.46)

            self.subtractIngredientsButton = ctk.CTkButton(self.updateRecipeWindow, text="-", command=self.subtractIngredientString, corner_radius=100, fg_color='#d12634', hover_color='orange', width=40, font=("Helvetica", 18)) 
            self.subtractIngredientsButton.place(relx=0.75, rely=0.46)

            self.ingredientsEntry = ctk.CTkTextbox(self.updateRecipeWindow, width=420, height=100, state="disabled")  
            self.ingredientsEntry.grid(row=10, column=0, columnspan=2, padx=10, pady=2, sticky='w')

            self.instructionsLabel = ctk.CTkLabel(self.updateRecipeWindow, text="Przygotowanie", font=("Helvetica", 14))
            self.instructionsLabel.grid(row=11, column=0, padx=10, pady=2, sticky='w')

            self.instructionsEntry = ctk.CTkTextbox(self.updateRecipeWindow, width=420, height=150)
            self.instructionsEntry.grid(row=12, column=0, columnspan=2, padx=10, pady=2, sticky='w')

            self.helpFrame = ctk.CTkFrame(self.updateRecipeWindow, fg_color="#242424")
            self.helpFrame.grid(row=13, column=0, padx=10, pady=2, sticky='w')

            self.updateButton = ctk.CTkButton(self.helpFrame, text="Zmień", command=self.updateRecipe, corner_radius=50, fg_color='green', hover_color='#49cc49', width=180)
            self.updateButton.grid(row=13, column=0, padx=20, pady=10, sticky='nsew')

            self.closeButton = ctk.CTkButton(self.helpFrame, text="Wyjdź", command=self.close, corner_radius=50, fg_color='#d12634', hover_color='orange', width=180)
            self.closeButton.grid(row=13, column=1, padx=15, pady=10, sticky='nsew')

            self.deleteButton = ctk.CTkButton(self.updateRecipeWindow, text="", image=myImage, width=40, height=40, command=self.showDeleteConfirmWindow, corner_radius=50, fg_color='#d12634', hover_color='orange')
            self.deleteButton.place(relx=0.75, rely=0.05)

                # wprowadznie danych do odpowiednich pól
            self.kcalEntry.insert(0, str(calories)) 
            self.prepTimeEntry.insert(0, str(prepTime))  
            self.czyWegeCheckbox.select() if isVege else self.czyWegeCheckbox.deselect()  
            self.ingredientsEntry.configure(state="normal")
            self.ingredientsEntry.insert("1.0", self.ingredientsString)
            self.ingredientsEntry.configure(state="disabled")
            self.instructionsEntry.insert("1.0", instructions)



# -----------------------------------------------------------------------------------------------------------------------------------------
    # klasa okna potwierdzenia usunięcia
class DeleteOrNotWindow():
    def __init__(self, parentWindow, selectedMealType, selectedRecipeName):
        self.parentWindow = parentWindow
        self.selectedMealType = selectedMealType
        self.selectedRecipeName = selectedRecipeName
        self.deleteOrNotWindow = ctk.CTkToplevel()
        self.deleteOrNotWindow.title("Usuwanie przepisu")
        
        width = 300
        height = 120

        screen_width = self.deleteOrNotWindow.winfo_screenwidth()
        screen_height = self.deleteOrNotWindow.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2) - 50
        position_left = int(screen_width / 2 - width / 2)
        self.deleteOrNotWindow.geometry(f"{width}x{height}+{position_left}+{position_top}")
        self.deleteOrNotWindow.resizable(False, False)
    
        self.deleteQuestionLabel = ctk.CTkLabel(self.deleteOrNotWindow, text="Czy napewno chcesz usunąć wybrany przepis?", font=("Helvetica", 12))
        self.deleteQuestionLabel.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky='nsew')

        self.confirmDeleteButton = ctk.CTkButton(self.deleteOrNotWindow, text="Potwierdź", command=self.referenceToDeleteReciep, corner_radius=50, fg_color='green', hover_color='#49cc49')
        self.confirmDeleteButton.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.closeButton = ctk.CTkButton(self.deleteOrNotWindow, text="Anuluj", command=self.close, corner_radius=50, fg_color='#d12634', hover_color='orange')
        self.closeButton.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        self.deleteOrNotWindow.grid_columnconfigure(0, weight=1)
        self.deleteOrNotWindow.grid_columnconfigure(1, weight=1)

        self.deleteOrNotWindow.grab_set()
        self.deleteOrNotWindow.wait_window(self.deleteOrNotWindow)


    def referenceToDeleteReciep(self):
        self.deleteOrNotWindow.destroy()
        self.parentWindow.deleteRecipe(self.selectedMealType, self.selectedRecipeName)


    def close(self):
        self.deleteOrNotWindow.destroy()


# -----------------------------------------------------------------------------------------------------------------------------------------
    # klasa tworząca frame z przepisem
class RecipeFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, text_list, **kwargs):
        super().__init__(master, **kwargs)

        # Tworzenie etykiet w ramce
        for idx, text in enumerate(text_list):
            label = ctk.CTkLabel(self, text=text, wraplength=150, font=("Helvetica", 14))
            label.grid(row=idx, column=0, padx=25, pady=5, sticky="w") 
        
        


