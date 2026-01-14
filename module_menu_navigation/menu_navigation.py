import tkinter as tk
from tkinter import messagebox

# ------------------------------
# Fonctions pour changer d'écran
# ------------------------------
def show_frame(frame):
    frame.tkraise()

def start_game():
    messagebox.showinfo("Jouer", "Lancer le jeu ici !")
    show_frame(game_frame)

def set_difficulty(level):
    print(f"Difficulté choisie : {level}")
    start_game()

def show_controls():
    messagebox.showinfo("Contrôles", "ZQSD / Flèches : se déplacer\nEspace : action\nÉchap : pause")

def pause_game():
    show_frame(pause_frame)

def resume_game():
    show_frame(game_frame)

def game_over():
    show_frame(gameover_frame)

def victory():
    show_frame(victory_frame)

def quit_game():
    root.destroy()

# ------------------------------
# Création de la fenêtre principale
# ------------------------------
root = tk.Tk()
root.title("Menu & Navigation - Jeu")
root.geometry("400x300")

# ------------------------------
# Création des frames (écrans)
# ------------------------------
menu_frame = tk.Frame(root)
difficulty_frame = tk.Frame(root)
game_frame = tk.Frame(root)
pause_frame = tk.Frame(root)
gameover_frame = tk.Frame(root)
victory_frame = tk.Frame(root)

for frame in (menu_frame, difficulty_frame, game_frame, pause_frame, gameover_frame, victory_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# ------------------------------
# MENU PRINCIPAL
# ------------------------------
tk.Label(menu_frame, text="Menu principal", font=("Arial", 18)).pack(pady=20)
tk.Button(menu_frame, text="Jouer", command=start_game).pack(pady=5)
tk.Button(menu_frame, text="Choisir difficulté", command=lambda: show_frame(difficulty_frame)).pack(pady=5)
tk.Button(menu_frame, text="Afficher contrôles", command=show_controls).pack(pady=5)
tk.Button(menu_frame, text="Quitter", command=quit_game).pack(pady=5)

# ------------------------------
# ÉCRAN DIFFICULTÉ
# ------------------------------
tk.Label(difficulty_frame, text="Choisir difficulté", font=("Arial", 18)).pack(pady=20)
tk.Button(difficulty_frame, text="Easy", command=lambda: set_difficulty("Easy")).pack(pady=5)
tk.Button(difficulty_frame, text="Normal", command=lambda: set_difficulty("Normal")).pack(pady=5)
tk.Button(difficulty_frame, text="Hard", command=lambda: set_difficulty("Hard")).pack(pady=5)
tk.Button(difficulty_frame, text="Retour", command=lambda: show_frame(menu_frame)).pack(pady=20)

# ------------------------------
# ÉCRAN DE JEU (placeholder)
# ------------------------------
tk.Label(game_frame, text="JEU EN COURS...", font=("Arial", 18)).pack(pady=20)
tk.Button(game_frame, text="Pause", command=pause_game).pack(pady=5)
tk.Button(game_frame, text="Victoire", command=victory).pack(pady=5)
tk.Button(game_frame, text="Game Over", command=game_over).pack(pady=5)

# ------------------------------
# ÉCRAN PAUSE
# ------------------------------
tk.Label(pause_frame, text="Pause", font=("Arial", 18)).pack(pady=20)
tk.Button(pause_frame, text="Reprendre", command=resume_game).pack(pady=5)
tk.Button(pause_frame, text="Quitter vers menu", command=lambda: show_frame(menu_frame)).pack(pady=5)

# ------------------------------
# GAME OVER
# ------------------------------
tk.Label(gameover_frame, text="Game Over", font=("Arial", 18)).pack(pady=20)
tk.Button(gameover_frame, text="Retour menu", command=lambda: show_frame(menu_frame)).pack(pady=5)

# ------------------------------
# VICTOIRE
# ------------------------------
tk.Label(victory_frame, text="Victoire !", font=("Arial", 18)).pack(pady=20)
tk.Button(victory_frame, text="Retour menu", command=lambda: show_frame(menu_frame)).pack(pady=5)

# ------------------------------
# Lancer le menu principal
# ------------------------------
show_frame(menu_frame)
root.mainloop()
