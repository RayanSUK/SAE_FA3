import tkinter as tk

from src.controleur.controleur import ControleurApplication


def main():
    root = tk.Tk()
    root.title("SAE FA3 - Logiciel graphes ")
    root.geometry("1200x750")
    root.minsize(1000, 650)

    ControleurApplication(root)

    root.mainloop()


if __name__ == "__main__":
    main()
