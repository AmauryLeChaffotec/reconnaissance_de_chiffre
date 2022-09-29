import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import _flatten
from PIL import Image ,  ImageOps ,ImageChops
import os
import numpy as np
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from keras.models import load_model
import matplotlib.pyplot as plt
import random


def quitter():
    
    if messagebox.askokcancel("Quitter", "Voulez vous quitter?"):
      
                    
        root.destroy()
 
 
def tracer(event, canevas):
    
    # position du pointeur de la souris
    X = event.x
    Y = event.y
    id = canevas.create_line(X, Y, event.x, event.y, width=13 , fill='black')
    canevas.bind('<Control-Button1-Motion>', lambda event: deplacement(event, id, canevas))
    
 
 
def deplacement(event, id, canevas):
    
    coordonné = canevas.coords(id)
    coordonné.append(event.x+1)
    coordonné.append(event.y+1)
    canevas.coords(id, _flatten(coordonné))
    canevas.postscript(file="dessin.ps", height=400, width=400 )
    
    os.remove("./dessin.png")
    psimage=Image.open('dessin.ps')
    psimage.save('dessin.png')
 
 
def menu(ftop):
  
    menubar = tk.Menu(ftop)
    menu1 = tk.Menu(menubar, tearoff=0)
    menu1.add_command(label="Nouveau")
    menu1.add_command(label="Ouvrir")
    menu1.add_command(label='Sauver')
    menu1.add_separator()
    menu1.add_command(label="Quitter", command=quitter)
    menubar.add_cascade(label='Fichier', menu=menu1)
    ftop.config(menu=menubar)
    # creation du second menu
    menu2 = tk.Menu(menubar, tearoff=0)
    menu2.add_command(label="A propos")
    menubar.add_cascade(label="Aide", menu=menu2)
 
 
def canv(ftop,frame1):
    
    canevas = tk.Canvas(ftop, width=400, height=400, bg='white')
    canevas.bind('<Control-1>', lambda event: tracer(event, canevas))
    # Evévement clic gauche (press)
    boutoneffacer = tk.Button(frame1, text='Effacer',command=lambda:effacer(canevas) ).grid(column=1, row=2)
    canevas.pack()
 
    
    
    
def prediction(frame1):
    
    model = load_model('chiffre.h5')
    newsize = (28, 28)
    image_chiffre = Image.open('dessin.png').convert('L')
    image_chiffre = ImageChops.invert(image_chiffre)
    image_chiffre = image_chiffre.resize(newsize)
    image_chiffre = np.expand_dims(image_chiffre,axis = 0)
    image_chiffre = image_chiffre.astype("float32") / 255    
    image_chiffre = np.expand_dims(image_chiffre,-1)

    predict = model.predict(image_chiffre)
    chiffre_predict = np.argmax(predict)
    tk.Label(frame1, text="").grid(column=1, row=3)
    tk.Label(frame1, text=chiffre_predict,font=('Times 14')).grid(column=1, row=4)

    
    
def effacer(canevas):
    
    canevas.delete('all')
    
    

 
def app(window):
    

    window.title('LA POSTE')
    frame1 = tk.Frame(window)
   
    frame1.pack(side='bottom', fill=tk.Y, padx=200)
    tk.Label(frame1, text="").grid(column=0, row=1)
    bouton = tk.Button(frame1, text='Prédiction',command=lambda:prediction(frame1) ).grid(column=2, row=2)
    menu(window)
    canv(window,frame1)
    window.mainloop()
 
 
if __name__ == '__main__':
    window = tk.Tk()
    window.title("LA POSTE")
    app(window)