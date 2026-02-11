![Logo aplikacji Random Cook](images/Random_cook_logo_long.png)

**Random Cook** to prosta, ale praktyczna aplikacja napisana w Pythonie, która rozwiązuje jeden z największych codziennych problemów:  
👉 *„Co dziś zjeść?”*

Aplikacja losuje posiłki z Twojej własnej bazy ulubionych dań, planując jadłospis od **1 dnia do całego tygodnia**, **bez powtórzeń**. Zero myślenia, zero stresu – pełny porządek przez losowość w kuchni 😄

---

## 🚀 Funkcjonalności

- 🎲 **Losowanie posiłków** z bazy danych MongoDB
- 📅 **Planowanie od 1 do 7 dni**
- 🔁 **Brak powtórzeń** w wygenerowanym planie, bo po co jeść to samo kilka dni pod rząd
- ⚖️ **Możliwość wyboru od 3 - 5 posiłków na dzień**
- 🧠 **Decyzje bez wysiłku** – aplikacja myśli za Ciebie
- 🗂️ **Własna baza ulubionych posiłków**

---

## 🧩 Jak to działa?

1. Dodajesz swoje ulubione posiłki do bazy danych
2. Wybierasz, na ile dni chcesz zaplanować jedzenie  
3. Wybierasz ile posiłków dziennie i czy desery lub przekąska
4. Aplikacja losuje:
   - posiłki
   - ilości
   - bez powtórzeń  
5. Otrzymujesz gotowy plan posiłków do pobrania w PDF 🎉

---

## 🛠️ Stack technologiczny

- **Backend**: Python
- **Baza danych**: MongoDB
- **Layout**: customtkinter + tkinter
- python random
- pymongo

---

## 📦 Instalacja i uruchomienie

```bash
git clone https://github.com/twoj-login/random-cook.git
cd random-cook
python main.py
