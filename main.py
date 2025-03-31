import ASL as A
import RPSPRO as r
import tkinter as tk
root = tk.Tk()
root.title("Programming Project Using Python")
root.geometry("600x400")
label = tk.Label(root, text="""Welcome to our project!
 You Can choose one of the two below options.""")
label.pack(pady=10)
def ASL():
    A.mainASL()
    return 

def RPS():
    r.mainRPS()
    return
button_a = tk.Button(root, text="American Sign Detector", width= 50,command=ASL)
button_a.pack(pady=100)
button_b = tk.Button(root, text="Rock Paper Scissor Game", width= 50, command=RPS)
button_b.pack(pady=5)
root.mainloop()