import requests
from bs4 import BeautifulSoup
from tkinter import *




def msg1():
    url = 'https://api.kanye.rest'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    soup = str(soup)
    msg = soup[10:len(soup) - 2] + " - Kayne West"
    return msg

def change():
    global lbl
    lbl.config(text = msg1())

root = Tk()
root.title("Kayne Quotes")
root.geometry("720x450")
lbl = Label(root, text = msg1())
lbl.pack(side = "top", fill = "x", pady = 10)

B2 = Button(root, text = "New Quote", command = change)
B2.pack()

B1 = Button(root, text="Close", command = root.destroy)
B1.pack()

root.mainloop()



