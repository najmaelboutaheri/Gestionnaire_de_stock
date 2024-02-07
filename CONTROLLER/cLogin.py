import sys
import os
import getpass

# Obtenez le nom d'utilisateur actuel
current_user = getpass.getuser()

import customtkinter as ctk
from PIL import ImageTk, Image
import tkinter as tk
from customtkinter import filedialog
import pandas as pd
from MODEL import DatabaseSetup as db
from CONTROLLER import list_colisage 
from CTkMessagebox import CTkMessagebox
from excel import invoice_data_show as invoice_data
from excel import commande_data_show as commande_data
from excel import excel_data as ex
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import UnivariateSpline
import datetime
import tkinter.ttk as ttk
import tkinter.font as tkfont
from tkcalendar import Calendar
from tkcalendar import Calendar
from tkinter.filedialog import *
from tkinter.ttk import *
from tkinter import ttk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import *
from PIL import ImageTk, Image
import sqlite3
from CONTROLLER import cSignup as cS
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# methods to use 
def Login(root,nameEntry,passwordEntry):
    historique('L\'utilisateur a entre l\'application')
    database=db.Database()
    result=database.searchSignup(nameEntry,passwordEntry)
    if len(result) == 0:
        CTkMessagebox(title="Warning", message="Username ou Password incorrect")

    else: 
        historique('L\'utilisateur a entre l\'application')
        for widget in root.winfo_children():
            widget.destroy()
        bg=Image.open(resource_path("images\\image1.png"))
        bg1 = ImageTk.PhotoImage(bg)
        
        CANVA = ctk.CTkCanvas(root, width=700, height=400)
        CANVA.create_image(0, 0, image=bg1, anchor='nw')
        CANVA.image=bg1
        CANVA.pack(fill='both', expand=True)
        accueil(CANVA,root)

        
def Remember(oui,Username,password):
    database=db.Database()
    if isRememeber()==False:
       try:
           database.insert_Remember_table(oui,Username,password)
       except sqlite3.IntegrityError as e:
           CTkMessagebox(title="Warning", message="Erreur dans la base de donnees")
            
def isRememeber():
    database=db.Database()
    result=database.get_Remember_data()
    if len(result)!=0:
        return True
    else:
        return False
def get_login_data():
    database=db.Database()
    result=database.get_signup_data()
    return result



def create_sales_graph(root):
    facture_dates, _ = get_data()
    facture_counts = {date: facture_dates.count(date) for date in set(facture_dates)}

    unique_facture_dates = sorted(set(facture_dates))
    unique_facture_counts = [facture_counts[date] for date in unique_facture_dates]
    interp_facture = UnivariateSpline(range(len(unique_facture_dates)), unique_facture_counts, k=2)

    fig, ax = plt.subplots(figsize=(4, 4))
    fig.patch.set_facecolor('#1b2538')
    ax.set_facecolor('white')
    
    # Set the color of the x-axis and y-axis lines and ticks
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Set the color of the x-axis and y-axis labels
    ax.set_xlabel('X Axis Label', color='white')
    ax.set_ylabel('Y Axis Label', color='white')
    # Votre code pour personnaliser le graphique des ventes
    
    scatter1 = plt.scatter(unique_facture_dates, unique_facture_counts, edgecolors="green", color="green")
    plt.plot(unique_facture_dates, interp_facture(range(len(unique_facture_dates))), color="#1b2538", linestyle='solid')
    ax.text(0.85, 0.9, "Ventes", color="green", transform=ax.transAxes, fontsize=10)
    text = ax.text(0, 0, "", ha="center", va="center", backgroundcolor=(1, 1, 1, 0.7))

    plt.xlabel('La date')
    plt.ylabel('Le Nombre')
    plt.title("Ventes statistics", color="white", fontsize=16, fontweight='bold')
    
    def hover(event):
        vis1 = scatter1.contains(event)[0]
        if vis1:
            ind = scatter1.contains(event)[1]["ind"][0]
            text.set_text(f"{unique_facture_dates[ind]}\nNbr de ventes: {interp_facture(ind)}")
            text.set_position((unique_facture_dates[ind], interp_facture(ind)))
            text.set_visible(True)
        else:
            text.set_visible(False)
        
        fig.canvas.draw_idle()
    fig.canvas.mpl_connect("motion_notify_event", hover)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=0, pady=0)

def create_purchases_graph(root):
    _, commande_dates = get_data()
    commande_counts = {date: commande_dates.count(date) for date in set(commande_dates)}

    unique_commande_dates = sorted(set(commande_dates))
    unique_commande_counts = [commande_counts[date] for date in unique_commande_dates]
    interp_commande = UnivariateSpline(range(len(unique_commande_dates)), unique_commande_counts, k=2)

    fig, ax = plt.subplots(figsize=(4, 4))
    fig.patch.set_facecolor('#1b2538')
    ax.set_facecolor('white')
    
    # Set the color of the x-axis and y-axis lines and ticks
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Set the color of the x-axis and y-axis labels
    ax.set_xlabel('X Axis Label', color='white')
    ax.set_ylabel('Y Axis Label', color='white')
    # Votre code pour personnaliser le graphique des achats
    scatter2 = plt.scatter(unique_commande_dates, unique_commande_counts, edgecolors="red", color="red") 
    plt.plot(unique_commande_dates, interp_commande(range(len(unique_commande_dates))), color="#1b2538", linestyle='solid')
    ax.text(0.85, 0.85, "Achats", color="red", transform=ax.transAxes, fontsize=10)
    text = ax.text(0, 0, "", ha="center", va="center", backgroundcolor=(1, 1, 1, 0.7))

    plt.xlabel('La date')
    plt.ylabel('Le Nombre')
    plt.title("Achats statistics", color="white", fontsize=16, fontweight='bold')
    
    def hover(event):   
        vis2 = scatter2.contains(event)[0]
        if vis2:
            ind = scatter2.contains(event)[1]["ind"][0]
            text.set_text(f"{unique_commande_dates[ind]}\nNbr d'achats: {interp_commande(ind)}")
            text.set_position((unique_commande_dates[ind], interp_commande(ind)))
            text.set_visible(True)
        else:
            text.set_visible(False)
        
        fig.canvas.draw_idle()
    fig.canvas.mpl_connect("motion_notify_event", hover)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=1, padx=0, pady=0)


def show_sales_vs_purchases(root):
    import matplotlib.pyplot as plt
    facture_dates, commande_dates = get_data()
    # Triez les données par date
    unique_facture_dates = sorted(set(facture_dates))
    unique_commande_dates = sorted(set(commande_dates))

    facture_counts = [facture_dates.count(date) for date in set(facture_dates)]
    commande_counts = [commande_dates.count(date) for date in set(commande_dates)]
   
    # Créez les graphiques
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor('#1b2538')
    ax.set_facecolor('white')
    
    # Set the color of the x-axis and y-axis lines and ticks
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Set the color of the x-axis and y-axis labels
    ax.set_xlabel('X Axis Label', color='white')
    ax.set_ylabel('Y Axis Label', color='white')
    # Personnalisez le style de vos graphiques en utilisant les données extraites
    #scatter1 = plt.scatter(unique_facture_dates, facture_counts, edgecolors="darkblue", color="darkblue")
    #scatter2 = plt.scatter(unique_commande_dates, commande_counts, edgecolors="black", color="black")
    plt.xlabel('La date')
    plt.ylabel('Le Nombre')
    plt.title("Ventes & Achats statistics", color="white", fontsize=16, fontweight='bold')

    plt.plot(unique_facture_dates, facture_counts, label="Ventes", color="green", marker='o')
    plt.plot(unique_commande_dates, commande_counts, label="Achats", color="red", marker='o')
    
    
   
    ax.legend()
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0,column=0,padx=0, pady=0)

def show_graph(root):
       show_sales_vs_purchases(root)

def get_data():
    # Se connecter à la base de données
    database=db.Database()

    result1=database.get_facture_dates()
    facture_dates = [row[0] for row in result1]

    # Récupérer les données de commandes
    result2=database.get_commande_dates()
    commande_dates = [row[0] for row in result2]

    return facture_dates, commande_dates
def get_achats_data():
    database=db.Database()
    result=database.achat_count()
    return result
def get_vente_data():
    database=db.Database()
    result=database.vente_count()
    return result
def get_produits_data():
    database=db.Database()
    result=database.product_count()
    return result
def get_stock():
    database=db.Database()
    result=database.product_quantity()
    return result
def informations(first_frame,second_frame,root):

    # Clear the contents of first_frame
    for widget in first_frame.winfo_children():
        widget.destroy()

    #Clear the contents of second_frame
    for widget in second_frame.winfo_children():
        widget.destroy()
    
    #first frame:
    LOGO= ctk.CTkImage(light_image=Image.open(resource_path("images\\LOGO.png")),size=(1150, 320))
    LabelLogo = ctk.CTkLabel(master=first_frame, image=LOGO,text="")
    LabelLogo.image = LOGO
    LabelLogo.grid(row=0,column=1)
    
    #second frame:
    information=User_information()
    label_title= ctk.CTkImage(light_image=Image.open(resource_path("images\\image.png")),size=(150, 20))
    LabelLogo = ctk.CTkLabel(master=second_frame, image=label_title,text="")
    LabelLogo.image = label_title
    LabelLogo.grid(row=0,column=0)
    for row in information:
       button_nom = ctk.CTkButton(master=second_frame,text=("Le nom: " + row[1] +"\n\nLe pronom: " + row[2] +"\n\nL'email: " + row[3] +"\n\nLe CIN: " + row[4] +"\n\nLe numero: " + row[5] +"\n\nLe mot de passe: " + row[6]),hover=False,fg_color="white",text_color="black",corner_radius=15,width=500,height=300,font=('bold',20))
       button_nom.grid(row=2, column=0, padx=0, pady=0)
    button_modifier = ctk.CTkButton(master=second_frame,text="modifier",fg_color="blue",text_color="white",hover_color="skyblue",command=lambda:modifier(first_frame,second_frame,root))
    button_modifier.grid(row=4, column=0, padx=10, pady=10)
    button_exit= ctk.CTkButton(master=second_frame,text="quitter",fg_color="blue",text_color="white",hover_color="skyblue",command=lambda:quitter(root))
    button_exit.grid(row=4, column=1, padx=10, pady=10)
      
     
def User_information():
    database=db.Database()
    result=database.get_signup_data()
    return result

def quitter(root):
    historique('L\'utilisateur a quitté l\'application')
    root.destroy()
def modifier(first_frame,second_frame,root):
    #Clear the contents of second_frame
    for widget in second_frame.winfo_children():
        widget.destroy()
    label=ctk.CTkLabel(master=second_frame,text="Modifier votre mot de passe",text_color="blue",font=('bold',15))
    label.grid(row=0,column=0,pady=10,padx=10)
    old_password= ctk.CTkEntry(master=second_frame,placeholder_text="old Password")
    old_password.grid(row=1,column=0,pady=10, padx=10)
    new_password = ctk.CTkEntry(master=second_frame,placeholder_text="new Password")
    new_password.grid(row=2,column=0,pady=10, padx=10)
    button_modifier=ctk.CTkButton(master=second_frame,text="modifier",command=lambda:update(old_password.get(),new_password.get()))
    button_modifier.grid(row=3,column=0,padx=5,pady=5)
    button_modifier=ctk.CTkButton(master=second_frame,text="retourner",command=lambda:informations(first_frame,second_frame,root))
    button_modifier.grid(row=3,column=1,padx=5,pady=5)

def update(old_password,new_password):
    historique('L\'utilisateur a modifie le mot de passe ')
    database=db.Database()
    database.update_password(old_password,new_password)
    CTkMessagebox(title="succee", message="l'operation est valide")
def historique(action):
    # Cette fonction enregistre l'action et la date/heure correspondantes dans un fichier journal
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open('historique.txt', 'a') as file:
        file.write(f'{timestamp}: {action}\n')
def fichier_historique():
    import subprocess
    import platform
    
    system = platform.system()
    file_path = "historique.txt" 

    if system == "Windows":
       print("Le système d'exploitation est Windows.")
       subprocess.Popen(["start", "", file_path], shell=True)

    elif system == "Linux":
       print("Le système d'exploitation est Linux.")
       subprocess.Popen(["xdg-open", file_path])

    else:
       print("Le système d'exploitation n'est pas reconnu.")

def retourner_Login(root):
    for widget in root.winfo_children():
        widget.destroy()
    try:
        # Load the background image
        bg=Image.open(resource_path("images\\image1.png"))
        bg1 = ImageTk.PhotoImage(bg)
         
        CANVA = ctk.CTkCanvas(root, width=700, height=400)
        CANVA.pack(fill='both', expand=True)
        CANVA.create_image(0, 0, image=bg1, anchor='nw')
            
        #self.CANVA.bind("<Configure>", self.resize_image)
    except Exception as e:
        print("Error loading background image:", e) 

    # Create the main frame with custom width and height
    FRAME = ctk.CTkFrame(master=CANVA, width=400, height=600,border_width=5,border_color="darkblue",corner_radius=5,bg_color="blue")
    FRAME.pack(pady=100, padx=6, anchor='nw')
    FRAME.pack_propagate(False) 
    FRAME.rowconfigure(0, weight=1)
    FRAME.columnconfigure(0, weight=1)
    FRAME.size()

    # Add labels, images, and buttons to the frame
    #add a logo image :
    LOGO=ctk.CTkImage(light_image=Image.open(resource_path("images\\logo.png")),size=(200,50))
    ctklabel=ctk.CTkLabel(master=FRAME,text="",image=LOGO,)
    ctklabel.image=LOGO
    ctklabel.pack(padx=5,pady=10,anchor="nw")
    #set a username image
    image1= ctk.CTkImage(light_image=Image.open(resource_path("images\\profil2.png")),size=(70, 70))
    LABELimage1 = ctk.CTkLabel(master=FRAME,image=image1,text="")
    LABELimage1.image = image1
    LABELimage1.pack(padx=100,side=tk.TOP)
    # LABELimage1.place(x=85, y=172)

    E1 = ctk.CTkEntry(master=FRAME, placeholder_text="Username")
    E1.pack(pady=5, padx=10)
    E = ctk.CTkEntry(master=FRAME, placeholder_text="Password", show="*")
    E.pack(pady=10, padx=10)
        
    #set a password image
    image2= ctk.CTkImage(light_image=Image.open(resource_path("images\\image6.png")),size=(13, 13))
    LABELimage2 = ctk.CTkLabel(master=FRAME, image=image2,text="")
    LABELimage2.image = image2
    LABELimage2.place(x=250, y=186)

    button1 = ctk.CTkButton(master=FRAME, text="login",hover_color="darkblue",command=lambda:Login(root,E1.get(),E.get()))
    button1.pack(pady=5, padx=10)

    button2 = ctk.CTkButton(master=FRAME, text="Sign up",hover_color="darkblue",command=lambda:Signup(root))
    button2.pack(pady=5, padx=10)
        
    # set a checkbox to remember the password
    ctklabel=ctk.CTkLabel(master=FRAME,text="Remember me",font=("Robot", 13))
    ctklabel.pack(pady=0,padx=0)
    checkbox1=ctk.CTkCheckBox(master=FRAME,checkmark_color="white",text="",width=70,height=18,checkbox_height=18,checkbox_width=18,hover_color="white",command=lambda:Remember("oui",E1.get(),E.get()))
    checkbox1.place(x=250,y=302)
        
    # add an other image (company logo):
    """logo=ctk.CTkImage(light_image=Image.open("images/image9.png"),size=(800,700))
    ctklabel=ctk.CTkLabel(master=CANVA,text="",image=logo,)
    ctklabel.image=logo
    ctklabel.place(x=500, y=70)"""
         
    #add a frame 
    frame=ctk.CTkScrollableFrame(master=CANVA,width=500,height=400,bg_color="blue",corner_radius=5,border_color="darkblue",border_width=5)
    frame.place(x=500,y=150)
        
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
     
    # add a window into frame
    label2=ctk.CTkLabel(master=frame,text_color="WHITE",text="Bienvenue au Gestionnaire de stock \n \n ABOUT:",font=('bold',15))
    label2.pack(padx=5,pady=10)

    button3=ctk.CTkButton(master=frame,hover_color="purple",text="Technical information",command=lambda:infos(frame,"A"))
    button3.pack( padx=5,pady=5,anchor='nw')

    button3=ctk.CTkButton(master=frame,hover_color="deeppink",text="Materials",command=lambda:infos(frame,"B"))
    button3.pack( padx=5,pady=5,anchor='nw')

    button3=ctk.CTkButton(master=frame,hover_color="green",text="Developer",command=lambda:infos(frame,"C"))
    button3.pack( padx=5,pady=5,anchor='nw')
    button3=ctk.CTkButton(master=frame,hover_color="red",text="Company",command=lambda:infos(frame,"D"))
    button3.pack( padx=5,pady=5,anchor='nw')
def Signup(root):
    historique('L\'utilisateur a crier un compte')
    for widget in root.winfo_children():
            widget.destroy()
    bg=Image.open(resource_path("images\\image1.png"))
    bg1 = ImageTk.PhotoImage(bg)
    CANVA = ctk.CTkCanvas(root, width=700, height=400)
    CANVA.pack(fill='both', expand=True)
    CANVA.create_image(0, 0, image=bg1, anchor='nw')
    # ADD sign up image
    signImage=ctk.CTkImage(light_image=Image.open(resource_path("images\\design4.png")),size=(728,700))
    ctklabel=ctk.CTkLabel(master=CANVA,text="",image=signImage,)
    ctklabel.pack(pady=0,padx=0,side=tk.RIGHT)

    #set first frame
    FRAME = ctk.CTkScrollableFrame(master=CANVA, width=1350, height=900,corner_radius=5,border_color="darkblue",border_width=10,bg_color="blue")
    FRAME.pack(padx=0,pady=0,anchor="nw",expand=True)
        
    FRAME.rowconfigure(0, weight=1)
    FRAME.columnconfigure(0, weight=1)

    #add a logo image :
        
    LOGO=ctk.CTkImage(light_image=Image.open(resource_path("images\\logo.png")),size=(200,50))
    ctklabel=ctk.CTkLabel(master=FRAME,text="",image=LOGO,)
    ctklabel.grid(row=0, column=0,padx=10,pady=10)
        
    labell = ctk.CTkLabel(master=FRAME, text="Obtenez votre compte gratuit dès maintenant", text_color="darkblue",font=("Robot", 14))
    labell.grid(row=2, column=0,padx=20,pady=20)
    label_text = ctk.CTkLabel(FRAME, text="Veuillez remplir tous les champs obligatoires*", text_color="blue",font=("String var",13))
    label_text.grid(row=3, column=0,padx=10,pady=10)
        
        
        
    #add entrys
    label = ctk.CTkLabel(FRAME, text="Nom *")#<----------------------------
    label.grid(row=6, column=0,padx=10,pady=0)
    entry1 = ctk.CTkEntry(master=FRAME)
    entry1.grid(row=7, column=0,padx=0,pady=0)
    label1 = ctk.CTkLabel(FRAME, text="Prenom *")
    label1.grid(row=9, column=0,padx=0,pady=0)
    entry2 = ctk.CTkEntry(master=FRAME)
    entry2.grid(row=10, column=0,padx=0,pady=0)
    label2 = ctk.CTkLabel(FRAME, text="Email *")
    label2.grid(row=12, column=0,padx=0,pady=0)
    entry3 = ctk.CTkEntry(master=FRAME)
    entry3.grid(row=13, column=0,padx=0,pady=0)
    label3 = ctk.CTkLabel(FRAME, text="CIN *")
    label3.grid(row=15, column=0,padx=0,pady=0)
    entry4 = ctk.CTkEntry(master=FRAME)
    entry4.grid(row=16, column=0,padx=0,pady=0)
    label6 = ctk.CTkLabel(FRAME, text="Numero*")
    label6.grid(row=18, column=0,padx=0,pady=0)
    entry7 = ctk.CTkEntry(master=FRAME)
    entry7.grid(row=19, column=0,padx=0,pady=0)
    label7 = ctk.CTkLabel(FRAME, text="Mot de passe  *")#Mot de passe 
    label7.grid(row=21, column=0,padx=10,pady=0)
    entry8 = ctk.CTkEntry(master=FRAME,show='*')
    entry8.grid(row=22, column=0,padx=0,pady=0)
    label8 = ctk.CTkLabel(FRAME, text="le mot de passe confirmè *")#le mot de passe confirmè
    label8.grid(row=24, column=0,padx=0,pady=0)
    entry9 = ctk.CTkEntry(master=FRAME,show='*')
    entry9.grid(row=25, column=0,padx=0,pady=0)
       
    button = ctk.CTkButton(master=FRAME, text="Soumettre ",command=lambda:cS.Signup(FRAME,entry1,entry2,entry3,entry4,entry7,entry8,entry9))
    button.grid(padx=20, pady=50, row=36, column=0)
    button = ctk.CTkButton(master=FRAME, text="Retourner",command=lambda:retourner_Login(root))
    button.grid(padx=20, pady=50, row=36, column=1)
        
def infos(frame,letter):
    if letter=="A":
        label=ctk.CTkLabel(master=frame,text="Technical Information",font=('bold',15),text_color="yellow")
        label.pack(padx=5,pady=10)
        label=ctk.CTkLabel(master=frame,text_color="WHITE",text="G_STOCK C'est une application de gestion de stock\n sert a gerer le stockage des produits\n et le nombre de ventes et d'achats effectue\n par la societe ISSMaroc.",font=('bold',12))
        label.pack()
    if letter=="B":
        label=ctk.CTkLabel(master=frame,text="Materials",font=('bold',15),text_color="yellow")
        label.pack(padx=5,pady=10)
        label=ctk.CTkLabel(master=frame,text_color="WHITE",text="les utiles de developement d'application sont:\n Vscode,python 3.10.6 et\n une base de donnes embarquee sqLite3. ",font=('bold',12))
        label.pack()
    if letter=="C":
        label=ctk.CTkLabel(master=frame,text="Developer",font=('bold',15),text_color="yellow")
        label.pack(padx=5,pady=10)
        label=ctk.CTkLabel(master=frame,text_color="WHITE",text="Najma El boutaheri\n E_mail: najmaelboutaheri@gmail.com",font=('bold',12))
        label.pack()
    if letter=="D":
        label=ctk.CTkLabel(master=frame,text="Company",font=('bold',15),text_color="yellow")
        label.pack(padx=5,pady=10)
        label=ctk.CTkLabel(master=frame,text_color="WHITE",text="ISSMaroc c'est une societe de fabrication\n et comercialisation des equipements de protection",font=('bold',12))
        label.pack()


#concernant la fonction historique qui enregistre tous les entres et les sorties dans l'application
"""
# ... Votre code existant ...

# Exemples d'appels à la fonction historique pour enregistrer des entrées et des sorties importantes :

# Enregistrement de l'ouverture de l'application
historique('L\'utilisateur a ouvert l\'application')

# Enregistrement d'une entrée de produit
produit = "Produit A"
historique(f'L\'utilisateur a entré le produit "{produit}" dans le système')

# Enregistrement d'une vente
vente = "Vente B"
historique(f'L\'utilisateur a enregistré la vente du produit "{vente}"')

# Enregistrement d'une modification
modification = "Produit C"
historique(f'L\'utilisateur a modifié les détails du produit "{modification}"')

# Enregistrement d'une sortie de l'application
historique('L\'utilisateur a quitté l\'application')
"""
def accueil(CANVA,root):
        
        #add a frame:
        FRAME = ctk.CTkFrame(master=CANVA, width=450, height=2000,border_width=5,border_color="darkblue",corner_radius=5,bg_color="blue")
        FRAME.grid(pady=5, padx=10, row=0, column=0, rowspan=2)
        FRAME.rowconfigure(0, weight=1)
       
        

        #add  the first scrollable frame:
        frame = ctk.CTkScrollableFrame(master=CANVA,border_width=5,border_color="darkblue",corner_radius=5,bg_color="blue",width=1150,height=250)
        frame.grid(row=0, column=1,padx=10,pady=0) 
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.size()
        #add  the second scrollable frame:
        frame1 = ctk.CTkScrollableFrame(master=CANVA, border_width=5,border_color="darkblue",corner_radius=5,bg_color="blue",width=1150,height=400)
        frame1.grid(row=1, column=1,padx=10,pady=0)
        frame1.rowconfigure(0, weight=1)
        frame1.columnconfigure(0, weight=1)
        frame1.size()
        """TO DO: le button Accueil est implimente dans une fonction
        """
        # add buttons to the first frame:
        button3=ctk.CTkButton(master=FRAME,hover_color="#274472",text="Accueil",height=120,fg_color="#02084b",command=lambda:accueil(CANVA,root))
        button3.grid( padx=10,pady=2,row=0,column=0)
        """TO DO: le button produits est implimente dans une fonction
        """
        button3=ctk.CTkButton(master=FRAME,hover_color="#155ac1",text="Produits",height=120,fg_color="#1025a1",command=lambda:produits(frame,frame1))
        button3.grid( padx=10,pady=2,row=1,column=0)
        """TO DO: le button Ventes  est implimente dans une fonction
        """
        button3=ctk.CTkButton(master=FRAME,hover_color="#a4d8ef",text="Ventes",text_color="#427898",height=120,fg_color="#5ba3f8",command=lambda:ventes(frame,frame1))
        button3.grid( padx=10,pady=2,row=2,column=0)
        """TO DO: le button Achats  est implimente dans une fonction
        """
        button3=ctk.CTkButton(master=FRAME,hover_color="#a2c4e0",text="Achats",text_color="#427898",height=120,fg_color="#f8f9f9",command=lambda:achats(frame,frame1))
        button3.grid( padx=10,pady=2,row=3,column=0)
        """TO DO: le button listes de collisage  est implimente dans une fonction
        
        button3=ctk.CTkButton(master=FRAME,hover_color="#a2c6e0",text="colisage",text_color="#427898",height=120,fg_color="#f8f9f9",command=lambda:crier_colisage())
        button3.grid( padx=10,pady=2,row=4,column=0)"""
        """TO DO: le button Retourner  est implimente dans une fonction
        """
        button3=ctk.CTkButton(master=FRAME,hover_color="#a2c6e9",text="Retourner",text_color="white",height=100,fg_color="blue",command=lambda:retourner_Login(root))
        button3.grid( padx=10,pady=2,row=5,column=0)
        
        
        # add gestion logo the second frame:
        logo= ctk.CTkImage(light_image=Image.open(resource_path("images\\logo.png")),size=(200, 50))
        LabelLogo = ctk.CTkLabel(master=frame, image=logo,text="")
        LabelLogo.image = logo
        LabelLogo.grid(padx=1,pady=1,row=0,column=2)
        """To do: L'historique a determine par une fonction"""
        image_historique= ctk.CTkImage(light_image=Image.open(resource_path("images\\historique1.png")),size=(100,100))
        button3=ctk.CTkButton(master=frame,text="Historique",height=100,width=200,image=image_historique,text_color="white",font=('bold',15),fg_color="#5e17eb",hover_color="#d9d9d9",command=lambda:fichier_historique())
        button3.grid(row=1, column=0, padx=5, pady=5)
        Nombre_dachats=get_achats_data()
        """To do: Le nombre d'achats a determine par une fonction"""
        image_achat=ctk.CTkImage(light_image=Image.open(resource_path("images\\achat1.png")),size=(120,100))
        button3=ctk.CTkButton(master=frame,text="Le nombre \nd'achats:\n"+str(Nombre_dachats[0])+" achats",height=100,width=200,image=image_achat,hover=False,text_color="white",font=('bold',15),fg_color="#5e17eb")
        button3.grid(row=1, column=1, padx=5, pady=5)
        Nombre_ventes=get_vente_data()
        """To do: Le nombre de ventes a determine par une fonction"""
        image_vente= ctk.CTkImage(light_image=Image.open(resource_path("images\\ventes.png")),size=(100,100))
        button=ctk.CTkButton(master=frame,text="Le nombre de\n ventes:\n"+str(Nombre_ventes[0])+" ventes",height=100,width=140,image=image_vente,hover=False,text_color="white",font=('bold',15),fg_color="#5e17eb")
        button.grid(row=1, column=2, padx=10, pady=5)
        """To do: Les informations a determine par une fonction"""
        image_informations= ctk.CTkImage(light_image=Image.open(resource_path("images\\informations1.png")),size=(100,100))
        button=ctk.CTkButton(master=frame,text="Informations",height=100,width=200,image=image_informations,text_color="white",font=('bold',15),fg_color="#5e17eb",hover_color="#d9d9d9",command=lambda:informations(frame,frame1,root))
        button.grid(row=1, column=3, padx=10, pady=5)
        """To do: La liste de colisage a determine par une fonction"""
        image_informations= ctk.CTkImage(light_image=Image.open(resource_path("images\\colisage.png")),size=(100,100))
        button=ctk.CTkButton(master=frame,text="Liste de colisage",height=100,width=200,image=image_informations,text_color="white",font=('bold',15),fg_color="#5e17eb",hover_color="#d9d9d9",command=lambda:crier_colisage(root))
        button.grid(row=1, column=4, padx=10, pady=5)
        Nombre_produits=get_produits_data()
        stock=get_stock()
        """To do: Le nombre de produits a determine par une fonction"""
        image_produits= ctk.CTkImage(light_image=Image.open(resource_path("images\\produits1.png")),size=(100,100))
        button=ctk.CTkButton(master=frame1,text="Nombre de produits:\n "+str(Nombre_produits[0])+" produits\n Le stock global: "+str(stock[0]),height=200,width=200,image=image_produits,hover=False,text_color="white",font=('bold',15),fg_color="#5e17eb")
        button.grid(row=0,column=2,padx=10,pady=10) 
        show_graph(frame1)
        

###########################################################Gestion de produits###############################################

def produits(first_frame, second_frame):
    email=get_email()
    # Clear previous content
    for widget in first_frame.winfo_children():
        widget.destroy()
    for widget in second_frame.winfo_children():
        widget.destroy()
    
    image_category= ctk.CTkImage(light_image=Image.open(resource_path("images\\category.png")),size=(100,100))
    # add a gategory image :
   
    nombre_de_classification=get_classification_count()
    button=ctk.CTkButton(master=first_frame,text="Nombre de classifications:\n"+str(nombre_de_classification)+" classifications",height=200,width=200,image=image_category,hover=False,text_color="white",font=('bold',15),fg_color="#145da0")
    button.grid(row=0,column=0,rowspan=2,padx=10,pady=10) 
    button=ctk.CTkButton(master=first_frame,text="Ajouter",text_color="white",fg_color="blue",height=100,hover_color="#061bb0",command=lambda:ajouter_classification(first_frame,second_frame))
    button.grid(row=0,column=1,padx=5,pady=5) 
    button=ctk.CTkButton(master=first_frame,text="Supprimer",text_color="white",fg_color="blue",height=100,hover_color="#061bb0",command=lambda:supprimer_classification(first_frame,second_frame))
    button.grid(row=0,column=2,padx=5,pady=5) 
    button=ctk.CTkButton(master=first_frame,text="Rechercher",text_color="white",fg_color="blue",height=100,hover_color="#061bb0",command=lambda:rechercher_classification(first_frame,second_frame))
    button.grid(row=1,column=1,padx=5,pady=5)
    button=ctk.CTkButton(master=first_frame,text=" Definir le stock minimal",text_color="white",fg_color="blue",height=100,hover_color="#061bb0",command=lambda:definir_stock_minimal(first_frame,second_frame))
    button.grid(row=1,column=2,padx=5,pady=5)
    button=ctk.CTkButton(master=first_frame,text=" Afficher produits",text_color="white",fg_color="blue",height=100,hover_color="#061bb0",command=afficher_produits)
    button.grid(row=1,column=3,padx=5,pady=5)
    logo= ctk.CTkImage(light_image=Image.open(resource_path("images\\logo.png")),size=(200, 50))
    LabelLogo = ctk.CTkLabel(master=first_frame, image=logo,text="")
    LabelLogo.image = logo
    LabelLogo.grid(row=0,column=3,padx=0,pady=5)
   

    label=ctk.CTkLabel(master=second_frame,text="Les classification des produits:",text_color="yellow",font=('bold',15))
    label.grid(row=0,column=0,padx=5,pady=5)
   
    afficher_classification(second_frame,first_frame)
    envoi_alerte(email)
def afficher_produits():
    ex.show_products()
def definir_stock_minimal(first_frame,second_frame):
     # Clear previous content
    for widget in first_frame.winfo_children():
        widget.destroy()
    label=ctk.CTkLabel(master=first_frame,text="Definir le stock minimal des produits ",text_color="blue",font=('bold',15))
    label.grid(row=0,column=0,pady=10,padx=10)
    stock= ctk.CTkEntry(master=first_frame,placeholder_text=f"Le stock minimal:{get_Stock()[0]}")
    stock.grid(row=1,column=0,pady=10, padx=10)
    button=ctk.CTkButton(master=first_frame,text="entrer",command=lambda:definir_stock(int(stock.get())))
    button.grid(row=3,column=0,padx=5,pady=5)
    button=ctk.CTkButton(master=first_frame,text="Retourner",command=lambda:produits(first_frame,second_frame))
    button.grid(row=3,column=1,padx=5,pady=5)
def definir_stock(stock):
    database=db.Database()
    database.change_stock(stock)
    CTkMessagebox(title="Succes", message="l'operation est valide")
def get_Stock():
    database=db.Database()
    stock_minimal=database.get_stock()
    return stock_minimal
def envoi_alerte(email):
    stock=get_Stock()[0]
    refrences=" "
    database = db.Database()
    list_products=database.get_products()
    list=[]
    for product in list_products:   
        try:
           
           if int(product[1])<=stock:
              list.append(product[0])
        except ValueError: 
            CTkMessagebox(title="Warning", message="Vous avez insere un produit avec le reference '' ")
    if len(list)!=0 and verification_email()==None:
        insert_envoi()
        CTkMessagebox(title="Warning", message=f"Un email est envoiye automatiquement a votre boite d'email\n concernant le stock minimal des produits.")
        for i in range(len(list)):
           refrences= refrences+list[i]+","
        import smtplib
        from email.mime.text import MIMEText

        subject = "Le stock minimal des produits"
        body = f"Salut nous esperons que vous allez bien.\n Nous vous informons que les produits de references suivants: {refrences} sont inferieur a la valeur minimal de stock {stock}"
        sender = "najmatahiri200@gmail.com"
        recipients = [email]
        password = "qtwiocilmorjkpuz"
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
            print("Message sent!")


    
    
def ajouter_classification(first_frame,second_frame):
    # Clear previous content
    for widget in first_frame.winfo_children():
        widget.destroy()
    label=ctk.CTkLabel(master=first_frame,text="ajouter une classification",text_color="blue",font=('bold',15))
    label.grid(row=0,column=0,pady=10,padx=10)
    classification_name= ctk.CTkEntry(master=first_frame,placeholder_text="Nom de classification")
    classification_name.grid(row=1,column=0,pady=10, padx=10)
    cat_number= ctk.CTkEntry(master=first_frame,placeholder_text="Nombre de categories")
    cat_number.grid(row=2,column=0,pady=10, padx=10)
    #Verification si une categorie est deja existe ou non 
    button_entrer=ctk.CTkButton(master=first_frame,text="Entrer",command=lambda:entrer(cat_number.get(),classification_name.get(),second_frame,first_frame,button_entrer))
    button_entrer.grid(row=4,column=0,padx=5,pady=5)
def crier_colisage(root):
    historique('L\'utilisateur a crier une liste de colisage')
    list_colisage.insert_data(root)

# add function entrer() for  ajouter_classification
def entrer(nombre, nom_classification, second_frame, first_frame, button_entrer):
    #Verification si une classification est deja existe ou non 
    if nom_classification=="":
        CTkMessagebox(title="Warning", message="l'operation est echoue")
    if  verification_classification_name(nom_classification):
        CTkMessagebox(title="Warning", message="Cette classification est deja existe ")
    else:
        button_entrer.destroy()
        label = ctk.CTkLabel(master=first_frame, text="Entrez le nom des categories", text_color="blue", font=('bold', 15))
        label.grid(row=4, column=0, pady=10, padx=10)
        List_categories = []
     
        def collect_categories():
            for i in range(number):
                cat_name = entry_list[i].get()
                if verification_cat_name(cat_name):
                   label_verification = ctk.CTkLabel(master=first_frame, text="Cette categorie existe déjà et elle appartient à une autre classification", text_color="blue")
                   label_verification.grid(row=4 + i + 1 + 1, column=0, padx=5, pady=5)
                else:
                   List_categories.append(cat_name)
                   add_classification(List_categories, nom_classification, first_frame, second_frame)

        if nombre.isdigit() == False:
           label = ctk.CTkLabel(master=first_frame, text="Veuillez entrer un nombre", text_color="red", font=('bold', 10))
           label.grid(row=3, column=0, pady=5, padx=5)
        else:
           number = int(nombre)
           entry_list = []
           for i in range(number):
               cat_name = ctk.CTkEntry(master=first_frame, placeholder_text="categorie " + str(i) + ":")
               cat_name.grid(row=4 + i + 1, column=0, pady=10, padx=10)
               entry_list.append(cat_name)
    
            
        button = ctk.CTkButton(master=first_frame, text="Ajouter", command=collect_categories)
        button.grid(row=4 + 1 + number + 1, column=0, padx=5, pady=5)
        button = ctk.CTkButton(master=first_frame, text="Retourner", command=lambda: produits(first_frame, second_frame))
        button.grid(row=4 + 1 + number + 1, column=1, padx=5, pady=5)

def add_classification(List_categories, nom_classification, first_frame, second_frame):
    database = db.Database()
    for cat_name in List_categories:
        print(cat_name, nom_classification)
        historique(f'L\'utilisateur a ajoute {nom_classification}')
        try:
            database.insert_category(cat_name, nom_classification)
        except sqlite3.IntegrityError as e:
           print("Erreur dans la base de donnees")
        CTkMessagebox(title="succe", message="l'operation est valide")
    afficher_classification(second_frame, first_frame)
def get_email():
    database = db.Database()
    data=database.get_signup_data()[len(database.get_signup_data())-1]
    email=data[3]
    return email
def supprimer_classification(first_frame,second_frame):
    # Clear previous content
    for widget in first_frame.winfo_children():
        widget.destroy()
    label=ctk.CTkLabel(master=first_frame,text="supprimer une classification",text_color="blue",font=('bold',15))
    label.grid(row=0,column=0,pady=10,padx=10)
    classification_name= ctk.CTkEntry(master=first_frame,placeholder_text="Nom de classification")
    classification_name.grid(row=1,column=0,pady=10, padx=10)
    button=ctk.CTkButton(master=first_frame,text="Supprimer",command=lambda:remove_classification(classification_name.get(),first_frame,second_frame))
    button.grid(row=5,column=0,padx=5,pady=5)
    button=ctk.CTkButton(master=first_frame,text="Retourner",command=lambda:produits(first_frame,second_frame))
    button.grid(row=5,column=1,padx=5,pady=5)
def remove_classification(nom_classification,first_frame,second_frame):
    
    database=db.Database()
    if nom_classification=="": 
       CTkMessagebox(title="warning", message="l'operation est echoue")
    else:
        suppression=database.delete_classification(nom_classification)
        if suppression==True:
           historique(f"L\'utilisateur a supprime une {nom_classification}")
           CTkMessagebox(title="succe", message="l'operation est valide")
           afficher_classification(second_frame,first_frame)

def rechercher_classification(first_frame,second_frame):
    # Clear previous content
    for widget in first_frame.winfo_children():
        widget.destroy()
    label=ctk.CTkLabel(master=first_frame,text="rechercher une classification",text_color="blue",font=('bold',15))
    label.grid(row=0,column=0,pady=10,padx=10)
    classification_name= ctk.CTkEntry(master=first_frame,placeholder_text="Nom de classification")
    classification_name.grid(row=1,column=0,pady=10, padx=10)
    button=ctk.CTkButton(master=first_frame,text="rechercher",command=lambda:search_classification(classification_name.get(),first_frame,second_frame))
    button.grid(row=3,column=0,padx=5,pady=5)
    button=ctk.CTkButton(master=first_frame,text="Retourner",command=lambda:produits(first_frame,second_frame))
    button.grid(row=3,column=1,padx=5,pady=5)
def search_classification(nom_classification,first_frame,second_frame):
    
    database=db.Database()
    if nom_classification=="": 
       CTkMessagebox(title="warning", message="l'operation est echoue")
    recherche=database.search_classification(nom_classification)
    if recherche==None:
       CTkMessagebox(title="warning", message="Aucune classification trouve")
    else:
        historique(f"L\'utilisateur a recherche sur {nom_classification}")
        for widget in second_frame.winfo_children():
            widget.destroy()
        image_sous_category=ctk.CTkImage(light_image=Image.open(resource_path("images\\souscategory.png")),size=(100,100))
        button=ctk.CTkButton(master=second_frame,text=recherche[1],height=200,width=270,image=image_sous_category,text_color="white",font=('bold',15),fg_color="#ffbd59", hover_color="#ffde59",command=lambda:category(recherche[1],first_frame,second_frame))
        button.grid(row=1,column=1,padx=10,pady=10) 


def afficher_classification(second_frame,first_frame):
    image_category = ctk.CTkImage(light_image=Image.open(resource_path("images\\category.png")), size=(100, 100))
    database=db.Database()
    classifications = database.get_classifications()
    label=ctk.CTkLabel(master=second_frame,text="Les classification des produits:",text_color="white",font=('bold',15))
    label.grid(row=0,column=0,padx=5,pady=5)
    for idx, classification in enumerate(classifications):
        row = 2 + idx//2  # Calculate the row based on the index
        column = 0 + idx % 2  # Calculate the column based on the index
        classification_name = classification[0]
        print(classification,idx)
        button = ctk.CTkButton(master=second_frame, text=classification_name, height=200, width=270,
                              image=image_category, text_color="white", font=('bold', 15),
                              fg_color="#145da0", hover_color="#6257e3",command=lambda name=classification_name: category(name,first_frame,second_frame))
        button.grid(row=row, column=column, padx=10, pady=10)
#afficher_classification() 


########################################################################################3
def category(classification_name,first_frame,second_frame):
   
    # Clear previous content
    for widget in first_frame.winfo_children():
        widget.destroy()
    for widget in second_frame.winfo_children():
        widget.destroy()
    nombre_categories=get_category_count(classification_name)
    image_sous_category=ctk.CTkImage(light_image=Image.open(resource_path("images\\souscategory.png")),size=(100,100))
    button=ctk.CTkButton(master=first_frame,text="Nombre de catgories:\n "+str(nombre_categories)+" categories",height=200,width=200,image=image_sous_category,hover=False,text_color="white",font=('bold',15),fg_color="#56aeff")
    button.grid(row=0,column=0,rowspan=2,padx=10,pady=10) 
    button=ctk.CTkButton(master=first_frame,text="Ajouter",text_color="white",fg_color="blue",height=100,hover_color="#061bb0",command=lambda:ajouter_categorie(first_frame,second_frame,classification_name))
    button.grid(row=0,column=1,padx=5,pady=5) 
    button=ctk.CTkButton(master=first_frame,text="Supprimer",text_color="white",fg_color="blue",height=100,hover_color="#061bb0",command=lambda:supprimer_categorie(first_frame,second_frame,classification_name))
    button.grid(row=0,column=2,padx=5,pady=5) 
    button=ctk.CTkButton(master=first_frame,text="Rechercher",text_color="white",fg_color="blue",height=100,hover_color="#061bb0",command=lambda:rechercher_categorie(first_frame,second_frame,classification_name))
    button.grid(row=1,column=1,padx=5,pady=5) 
    afficher_categories(classification_name,first_frame,second_frame)


def ajouter_categorie(first_frame,second_frame,classification_name):
    # Clear previous content
    for widget in first_frame.winfo_children():
        widget.destroy()
    label=ctk.CTkLabel(master=first_frame,text="Ajouter une categorie",text_color="blue",font=('bold',15))
    label.grid(row=0,column=0,pady=10,padx=10)
    cat_name= ctk.CTkEntry(master=first_frame,placeholder_text="Nom de categorie")
    cat_name.grid(row=1,column=0,pady=10, padx=10)
    nom_classification = ctk.CTkEntry(master=first_frame,placeholder_text="Nom de classification")
    nom_classification.grid(row=3,column=0,pady=10, padx=10)
    button=ctk.CTkButton(master=first_frame,text="Soumettre",command=lambda:add_category(cat_name.get(),nom_classification.get(),first_frame,second_frame))
    button.grid(row=4,column=0,padx=5,pady=5)
    button=ctk.CTkButton(master=first_frame,text="Retourner",command=lambda: category(classification_name,first_frame,second_frame))
    button.grid(row=4,column=1,padx=5,pady=5)
def add_category(cat_name,nom_classification,first_frame,second_frame):
    database=db.Database()
    if cat_name== "" or nom_classification== "": 
       CTkMessagebox(title="Warning", message="l'operation est echoue")
    else:
        if verification_cat_name(cat_name):
            label_verification = ctk.CTkLabel(master=first_frame, text="Cette categorie existe déjà ou elle appartient à une autre classification", text_color="blue")
            label_verification.grid(row=2, column=0, padx=5, pady=5)
        else:
            historique(f"L\'utilisateur a recherche sur {cat_name} de classification{nom_classification}")
            try:
                insertion=database.insert_category(cat_name,nom_classification)
            except sqlite3.IntegrityError as e:
                    print("Erreur dans la base de donnees")
            if insertion==True:
                   CTkMessagebox(title="Succe", message="l'operation est valide")
                   afficher_categories(nom_classification,first_frame,second_frame)
def supprimer_categorie(first_frame,second_frame,classification_name):
    # Clear previous content
    for widget in first_frame.winfo_children():
        widget.destroy()
    label=ctk.CTkLabel(master=first_frame,text="supprimer une categorie",text_color="blue",font=('bold',15))
    label.grid(row=0,column=0,pady=10,padx=10)
    cat_name= ctk.CTkEntry(master=first_frame,placeholder_text="Nom de categorie")
    cat_name.grid(row=1,column=0,pady=10, padx=10)
    nom_classification= ctk.CTkEntry(master=first_frame,placeholder_text="Nom de classification")
    nom_classification.grid(row=2,column=0,pady=10, padx=10)
    button=ctk.CTkButton(master=first_frame,text="supprimer",command=lambda:remove_category(cat_name.get(),nom_classification.get(),second_frame,first_frame))
    button.grid(row=3,column=0,padx=5,pady=5)
    button=ctk.CTkButton(master=first_frame,text="Retourner",command=lambda:category(classification_name,first_frame,second_frame))
    button.grid(row=3,column=1,padx=5,pady=5)
def remove_category(cat_name,classification_name,second_frame,first_frame):
    database=db.Database()
    if cat_name=="" or classification_name=="": 
       CTkMessagebox(title="Warning", message="l'operation est echoue")
    elif  verification_cat_name(cat_name)==False or verification_classification_name(classification_name)==False:
        CTkMessagebox(title="Warning", message="le nom de classification ou le nom de la categorie n'existe pas")
    else:
        historique(f"L\'utilisateur a supprime sur {cat_name} de classification {classification_name}")
        suppression=database.delete_category_and_classification(cat_name,classification_name)
        if suppression==True:
           CTkMessagebox(title="succe", message="l'operation est valide")
           afficher_categories(classification_name,first_frame,second_frame)

def rechercher_categorie(first_frame,second_frame,classification_name):
    # Clear previous content
    for widget in first_frame.winfo_children():
        widget.destroy()
    label=ctk.CTkLabel(master=first_frame,text="rechercher une categorie",text_color="blue",font=('bold',15))
    label.grid(row=0,column=0,pady=10,padx=10)
    cat_name= ctk.CTkEntry(master=first_frame,placeholder_text="Nom de categorie")
    cat_name.grid(row=1,column=0,pady=10, padx=10)
    button=ctk.CTkButton(master=first_frame,text="rechercher",command=lambda:search_category(cat_name.get(),first_frame,second_frame,classification_name))
    button.grid(row=3,column=0,padx=5,pady=5)
    button=ctk.CTkButton(master=first_frame,text="Retourner",command=lambda:category(classification_name,first_frame,second_frame))
    button.grid(row=3,column=1,padx=5,pady=5)
def search_category(cat_name,first_frame,second_frame,nom_classification):
    database=db.Database()
    if cat_name=="": 
       CTkMessagebox(title="Warning", message="l'operation est echoue")
    elif verification_cat_name(cat_name)==False:
       CTkMessagebox(title="Warning", message="Aucune categorie trouve")
    else:
        historique(f"L\'utilisateur a cherche sur {cat_name} de classification {nom_classification}")
        recherche=database.search_category(cat_name)
        if recherche!= []:
           CTkMessagebox(title="Succes", message="l'operation est valide")
           for widget in second_frame.winfo_children():
               widget.destroy()
           for i in range(len(recherche)):
               image_sous_category=ctk.CTkImage(light_image=Image.open(resource_path("images\\souscategory.png")),size=(100,100))
               button=ctk.CTkButton(master=second_frame,text=recherche[i][0]+" de classification: "+recherche[i][1],height=200,width=310,image=image_sous_category,text_color="white",font=('bold',15),fg_color="#56aeff",hover_color="#76b9f0",command=lambda:sous_category(recherche[i][0],first_frame,second_frame,nom_classification))
               button.grid(row=i,column=1,padx=10,pady=10)
     



def afficher_categories(nom_classification,first_frame,second_frame):#,
    image_category = ctk.CTkImage(light_image=Image.open(resource_path("images\\souscategory.png")), size=(100, 100))
    database=db.Database()
    list_categories=database.get_category_by_classification_name(nom_classification)
    label=ctk.CTkLabel(master=second_frame,text="Les categories de produits de classification :"+nom_classification,text_color="white",font=('bold',15))
    label.grid(row=0,column=0,padx=5,pady=5)
    for idx, cat in enumerate(list_categories):
        row = 2 + idx//2  # Calculate the row based on the index
        column = 0 + idx % 2  # Calculate the column based on the index
        cat_name = cat[0]
        print(cat_name)
        print(idx)
        print(row)
        print(column)
        button = ctk.CTkButton(master=second_frame, text=cat_name, height=200, width=270,
                               image=image_category, text_color="white", font=('bold', 15),
                               fg_color="#56aeff", hover_color="#76b9f0",command=lambda name=cat_name:sous_category(name,first_frame,second_frame,nom_classification))
        button.grid(row=row, column=column, padx=10, pady=10)
#afficher_categories("Les chaussures")



########################################################################################################
def sous_category(categorie,first_frame,second_frame,classification_name):

    # Clear previous content
    for widget in first_frame.winfo_children():
        widget.destroy()
    for widget in second_frame.winfo_children():
        widget.destroy()
    nombre_sous_categories=get_sub_category_count(categorie)
    image_sous_category=ctk.CTkImage(light_image=Image.open(resource_path("images\\souscategorie.png")),size=(100,100))
    button=ctk.CTkButton(master=first_frame,text="Nombre de sous catgories:\n "+str(nombre_sous_categories)+" sous categories",height=200,width=200,image=image_sous_category,hover=False,text_color="white",font=('bold',15),fg_color="#b1d4e0")
    button.grid(row=0,column=0,rowspan=2,padx=10,pady=10) 
    button=ctk.CTkButton(master=first_frame,text="Ajouter",text_color="white",fg_color="blue",height=100,hover_color="#061bb0" ,command=lambda:ajouter_sous_categorie(first_frame,second_frame,categorie,classification_name))
    button.grid(row=0,column=1,padx=5,pady=5) 
    button=ctk.CTkButton(master=first_frame,text="Supprimer",text_color="white",fg_color="blue",height=100,hover_color="#061bb0",command=lambda:supprimer_sous_categorie(first_frame,second_frame,categorie,classification_name))
    button.grid(row=0,column=2,padx=5,pady=5) 
    button=ctk.CTkButton(master=first_frame,text="Rechercher",text_color="white",fg_color="blue",height=100,hover_color="#061bb0",command=lambda:rechercher_sous_categorie(first_frame,second_frame,categorie,classification_name))
    button.grid(row=1,column=1,padx=5,pady=5)
    button=ctk.CTkButton(master=first_frame,text="Retourner",text_color="white",fg_color="blue",height=100,hover_color="#061bb0",command=lambda:category(classification_name,first_frame,second_frame))
    button.grid(row=1,column=2,padx=5,pady=5) 
    afficher_sous_categories(categorie,first_frame,second_frame,classification_name)

def afficher_sous_categories(cat_name,first_frame,second_frame,classification_name):
    image_category = ctk.CTkImage(light_image=Image.open(resource_path("images\\souscategorie.png")), size=(100, 100))
    database=db.Database()
    List_sous_categories=database.get_sub_category(cat_name)
    label=ctk.CTkLabel(master=second_frame,text="Les sous categories des produits de categorie:"+cat_name,text_color="white",font=('bold',15))
    label.grid(row=0,column=0,padx=5,pady=5)
    for idx, sub_cat in enumerate(List_sous_categories):
        row = 2 + idx//2  # Calculate the row based on the index
        column = 0 + idx % 2  # Calculate the column based on the index
        sub_cat_name = sub_cat[0]
        print(sub_cat_name)
        #add a function excel  
        button = ctk.CTkButton(master=second_frame, text=sub_cat_name, height=200, width=270,image=image_category, text_color="white", font=('bold', 15),fg_color="#b1d4e0", hover_color="#c0f0f7",command=lambda name=sub_cat_name:inserer_produit(cat_name,first_frame,second_frame,classification_name,name))
        button.grid(row=row, column=column, padx=10, pady=10)




def ajouter_sous_categorie(first_frame,second_frame,categorie,classification_name):
      # Clear previous content
    for widget in first_frame.winfo_children():
        widget.destroy()
    label=ctk.CTkLabel(master=first_frame,text="Ajouter une sous  categorie",text_color="blue",font=('bold',15))
    label.grid(row=0,column=0,pady=10,padx=10)
    sub_cat_name= ctk.CTkEntry(master=first_frame,placeholder_text="Nom de sous categorie")
    sub_cat_name.grid(row=1,column=0,pady=10, padx=10)
    cat_name = ctk.CTkEntry(master=first_frame,placeholder_text="Nom de categorie")
    cat_name.grid(row=2,column=0,pady=10, padx=10)
    button=ctk.CTkButton(master=first_frame,text="Soumettre",command=lambda:add_sub_category(sub_cat_name.get(),cat_name.get(),first_frame,second_frame,classification_name))
    button.grid(row=4,column=0,padx=5,pady=5)
    button=ctk.CTkButton(master=first_frame,text="Retourner",command=lambda:sous_category(categorie,first_frame,second_frame,classification_name))
    button.grid(row=4,column=1,padx=5,pady=5)
def add_sub_category(sub_cat_name,cat_name,first_frame,second_frame,classification_name):
    database=db.Database()
    if sub_cat_name== "" or cat_name== "": 
       CTkMessagebox(title="Warning", message="l'operation est echoue")
    else:
        if verification_cat_name(cat_name)==False:
            label_verification = ctk.CTkLabel(master=first_frame, text="Il n'existe aucune categorie avec ce nom", text_color="blue")
            label_verification.grid(row=3, column=0, padx=5, pady=5)
        else:
            historique(f"L\'utilisateur a ajoute  {sub_cat_name} de categorie {cat_name} de classification {classification_name}")
            try:
                insertion=database.insert_sub_category(sub_cat_name,cat_name)
            except sqlite3.IntegrityError as e:
                   print("Erreur dans la base de donnees")

            if insertion==True:
                   CTkMessagebox(title="Succes", message="l'operation est valide")
                   afficher_sous_categories(cat_name,first_frame,second_frame,classification_name)
def supprimer_sous_categorie(first_frame,second_frame,categorie,classification_name):
     # Clear previous content
    for widget in first_frame.winfo_children():
        widget.destroy()  
    label=ctk.CTkLabel(master=first_frame,text="supprimer une sous categorie",text_color="blue",font=('bold',15))
    label.grid(row=0,column=0,pady=10,padx=10)
    sub_cat_name= ctk.CTkEntry(master=first_frame,placeholder_text="Nom de sous categorie")
    sub_cat_name.grid(row=1,column=0,pady=10, padx=10)
    cat_name= ctk.CTkEntry(master=first_frame,placeholder_text="Nom de categorie")
    cat_name.grid(row=2,column=0,pady=10, padx=10)
    button=ctk.CTkButton(master=first_frame,text="Supprimer",command=lambda:remove_sub_category(sub_cat_name.get(),cat_name.get(),first_frame,second_frame,classification_name))
    button.grid(row=3,column=0,padx=5,pady=5)
    button=ctk.CTkButton(master=first_frame,text="Retourner",command=lambda:sous_category(categorie,first_frame,second_frame,classification_name))
    button.grid(row=3,column=1,padx=5,pady=5)
def remove_sub_category(sub_cat_name,cat_name,first_frame,second_frame,classification_name):
    database=db.Database()
    if sub_cat_name=="" or cat_name=="":
       CTkMessagebox(title="Warning", message="l'operation est echoue")
    elif  verification_cat_name(cat_name)==False or verification_subcategory_name(sub_cat_name)==False:
        CTkMessagebox(title="Warning", message="Le nom de sous categorie ou le nom de la categorie n'existe pas")
    else:
        suppression=database.delete_sub_categorie(sub_cat_name)
        historique(f"L\'utilisateur a supprime  {sub_cat_name} de categorie {cat_name} de classification {classification_name}")
        if suppression==True:
           CTkMessagebox(title="Succe", message="l'operation est valide")
           afficher_sous_categories(cat_name,first_frame,second_frame,classification_name)


def rechercher_sous_categorie(first_frame,second_frame,categorie,classification_name):
    # Clear previous content
    for widget in first_frame.winfo_children():
        widget.destroy()
    label=ctk.CTkLabel(master=first_frame,text="rechercher une sous  categorie",text_color="blue",font=('bold',15))
    label.grid(row=0,column=0,pady=10,padx=10)
    sub_cat_name= ctk.CTkEntry(master=first_frame,placeholder_text="Nom de sous categorie")
    sub_cat_name.grid(row=1,column=0,pady=10, padx=10)
    button=ctk.CTkButton(master=first_frame,text="rechercher",command=lambda:search_sub_category(sub_cat_name.get(),categorie,first_frame,second_frame,classification_name))
    button.grid(row=3,column=0,padx=5,pady=5)
    button=ctk.CTkButton(master=first_frame,text="Retourner",command=lambda:sous_category(categorie,first_frame,second_frame,classification_name))
    button.grid(row=3,column=1,padx=5,pady=5)
def search_sub_category(sub_cat_name,categorie,first_frame,second_frame,classification_name):
    database=db.Database()
    if sub_cat_name=="": 
       CTkMessagebox(title="Warning", message="l'operation est echoue")
    elif verification_subcategory_name(sub_cat_name)==False:
       CTkMessagebox(title="Warning", message="Aucune sous categorie trouve")
    else:
        recherche=database.search_sub_category(sub_cat_name)
        if recherche!= []:
           historique(f"L\'utilisateur a cherche sur  {sub_cat_name} de categorie {categorie} de classification {classification_name}")
           CTkMessagebox(title="Succes", message="l'operation est valide")
           for widget in second_frame.winfo_children():
               widget.destroy()
           for i in range(len(recherche)):
               image_sous_category=ctk.CTkImage(light_image=Image.open(resource_path("images\\souscategorie.png")),size=(100,100))
               button=ctk.CTkButton(master=second_frame,text=recherche[i][0],height=200,width=310,image=image_sous_category,text_color="white",font=('bold',15),fg_color="#b1d4e0", hover_color="#c0f0f7",command=lambda name=sub_cat_name:inserer_produit(categorie,first_frame,second_frame,classification_name,name))
               button.grid(row=i,column=1,padx=10,pady=10) 
     


def inserer_produit(categorie,first_frame,second_frame,classification_name,sub_cat):
    
    for widget in second_frame.winfo_children():
        widget.destroy()   
    print(sub_cat)
    ex.product_data(sub_cat)
    """path = filedialog.askopenfilename(filetypes=[("Fichiers Excel", "*.xlsx *.xls")])
    label=ctk.CTkLabel(master=second_frame,text="Le nom de la fenetre de fichier excel",text_color="blue",font=('bold',15))
    label.grid(row=0,column=0,pady=10,padx=10)
    sheet_name= ctk.CTkEntry(master=second_frame,placeholder_text="Nom de fenetre")
    sheet_name.grid(row=1,column=0,pady=10, padx=10)"""
    """button=ctk.CTkButton(master=second_frame,text="Entrer",command=lambda:ex.excel_data())#path,sheet_name.get()))
    button.grid(row=3,column=0,padx=5,pady=5)
    button=ctk.CTkButton(master=second_frame,text="Retourner",command=lambda:sous_category(categorie,first_frame,second_frame,classification_name))
    button.grid(row=3,column=1,padx=5,pady=5)"""
 


# add ajouter function:




def get_classification_count():
    database=db.Database()
    classification_count=database.get_classifications_count()
    return classification_count[0][0]

def get_sub_category_count(categorie):
    database=db.Database()
    sub_category_count=database.sub_category_count(categorie)
    return sub_category_count[0]

def get_category_count(classification_name):
    database=db.Database()
    category_count=database.category_count(classification_name)
    return category_count[0]

def verification_email():
    database=db.Database()
    envoi=database.get_envoi()
    return envoi[0]

def insert_envoi():
    database=db.Database()
    database.update_envoi("oui")
    




def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def import_excel_and_display(frame):
    excel_file = resource_path(filedialog.askopenfilename(filetypes=[("Fichiers Excel", "*.xlsx *.xls")]))

    if excel_file:
        data = pd.read_excel(excel_file)

        for widget in frame.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(frame)
        tree["columns"] = list(data.columns)
        for col in data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for i, row in data.iterrows():
            tree.insert("", i, values=[str(cell) for cell in row])  # Convert all values to strings

        tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)

        font = tkfont.Font()
        for col in data.columns:
            col_width = max(font.measure(str(data[col].max())), font.measure(col))
            tree.column(col, width=col_width)

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)



#verifier si une categorie est deja existe dans la base de donnees et appartient a une autre classification
def verification_cat_name(cat_name):
    # selectionner cat_name from database
    database=db.Database()
    verification=database.get_category_name(cat_name)
    if verification!=[]:
        return True
    else:
        return False
#verifier si une classification est deja existe dans la base de donnees
def verification_classification_name(classification_name):
    # selectionner classification_name from database
    database=db.Database()
    verification=database.get_classification_name(classification_name)
    if verification!=[]:
        return True
    else:
        return False
#verifier si une sous categorie est deja existe dans la base de donnees
def verification_subcategory_name(sub_cat_name):
    # selectionner sub_cat_name from database
    database=db.Database()
    verification=database.get_sub_categorie(sub_cat_name)
    if verification!=[]:
        return True
    else:
        return False
#---------------------------------------------------------Gestion de Ventes----------------------------------------------------------------------
def ventes(first_frame,second_frame):
    for widget in first_frame.winfo_children():
        widget.destroy() 
    for widget in second_frame.winfo_children():
        widget.destroy() 
    nombre_ventes=get_vente_data()
    nombre_factures=get_facture_data()
    image_vente=ctk.CTkImage(light_image=Image.open(resource_path("images\\ventes.png")),size=(100,100))
    image_facture=ctk.CTkImage(light_image=Image.open(resource_path("images\\facture.png")),size=(100,100))
    button=ctk.CTkButton(master=first_frame,text="Nombre de ventes:\n "+str(nombre_ventes[0])+" ventes",height=200,width=200,image=image_vente,hover=False,text_color="white",font=('bold',15),fg_color="#b1d4e0")
    button.grid(row=0,column=0,rowspan=2,padx=10,pady=10) 
    button=ctk.CTkButton(master=first_frame,text="Nombre de factures:\n "+str(nombre_factures[0])+" factures",height=200,width=200,image=image_facture,hover=False,text_color="white",font=('bold',15),fg_color="#b1d4e0")
    button.grid(row=0,column=1,rowspan=2,padx=10,pady=10)
    button=ctk.CTkButton(master=first_frame,text="Afficher les factures ",text_color="white",fg_color="blue",height=100,hover_color="#061bb0",command=lambda:afficher_facture())
    button.grid(row=0,column=3,padx=5,pady=5) 
   
    def afficher_facture():
        invoice_data.affichage_donnees()
    #add a facture
    label_facture=ctk.CTkLabel(master=second_frame,text="Effectuer une facture",text_color="blue",font=('bold',20))
    label_facture.grid(row=0,column=0,padx=5,pady=5)
    facture_entry= ctk.CTkEntry(master=second_frame,placeholder_text="Description de la facture")
    facture_entry.grid(row=1,column=0,padx=5,pady=5)
    date_facture_entry= ctk.CTkEntry(master=second_frame,placeholder_text="Date facture")
    date_facture_entry.grid(row=2,column=0,padx=5,pady=5)
    date_facture_entry.insert(0, "yyyy-mm-dd")
   

    def pick_date_vente(event):
        date_window = Toplevel()
        date_window .wait_visibility()  
        date_window.grab_set()
        date_window.title('chosir une date')
        date_window.geometry('250x220+590+370')
        cal =Calendar(date_window,selectmode="day", date_pattern="yyyy-mm-dd")
        cal.place(x=0, y=0)
        submit_btn = Button(date_window, text="Soumettre", command=lambda:grab_date(cal,date_facture_entry,date_window))
        submit_btn.place(x=80, y=190)

    def grab_date(cal,date_facture_entry,date_window):
        date_facture_entry.delete(0, END)
        date_facture_entry.insert(0, cal.get_date())
        date_window.destroy()
    date_facture_entry.bind("<1>",  pick_date_vente)

    nombre_factures= ctk.CTkEntry(master=second_frame,placeholder_text="nombre de produits")
    nombre_factures.grid(row=3,column=0,padx=5,pady=5)
    button=ctk.CTkButton(master=second_frame,text="Entrer",text_color="white",fg_color="blue",hover_color="#061bb0",command=lambda:entrer_facture(nombre_factures.get(),button,second_frame,facture_entry.get(),date_facture_entry.get()))
    button.grid(row=5,column=0,padx=5,pady=5)
def entrer_facture(nombre_factures, button, second_frame,desription,date_facture):
    id_facture=insert_facture(date_facture,desription)

    button.destroy()
    label = ctk.CTkLabel(master=second_frame, text="Saisissez les references et les quantitees vendues", text_color="blue", font=('bold', 15))
    label.grid(row=5, column=0, pady=10, padx=10)

    if nombre_factures.isdigit() == False:
        label = ctk.CTkLabel(master=second_frame, text="Veuillez entrer un nombre", text_color="red", font=('bold', 10))
        label.grid(row=4, column=0, pady=5, padx=5)
    else:
        number = int(nombre_factures)
        entry_list = []

        for i in range(1, number + 1):
            # Create combo box for references
            les_choix_reference = ctk.CTkComboBox(master=second_frame, font=("Arial", 10), values=get_product_reference())
            les_choix_reference.grid(row=5 + i, column=0, pady=10, padx=10)

            # Create entry field for quantity
            quantite_vendue = ctk.CTkEntry(master=second_frame, placeholder_text="la quantite vendue:")
            quantite_vendue.grid(row=5 + i, column=1, pady=10, padx=10)

            entry_list.append((les_choix_reference, quantite_vendue))

        def soumettre():
            for reference, quantity_entry in entry_list:
                reference_value = reference.get()
                quantity_value = quantity_entry.get()
                print("Reference:", reference_value)
                print("Quantity:", quantity_value)
                calculate_stock_vente(quantity_value,reference_value)
                inserer_vente(reference_value,quantity_value,id_facture)
        button = ctk.CTkButton(master=second_frame, text="Soumettre", command=soumettre)
        button.grid(row=5 + number * 2, column=0, padx=5, pady=5)

#une fonction pour inserer les ventes:
def inserer_vente(Reference,quantite_vendue,id_facture):
    database=db.Database()
    try:
        database.insert_vente(quantite_vendue, Reference, id_facture)
    except sqlite3.IntegrityError as e:
           print("Erreur dans la base de donnees")
    historique(f'L\'utilisateur a effectue une vente associe a la facture numero {id_facture}')
#une fonction pour traiter les quantites vendues des produits choisis:
def calculate_stock_vente(quantite_vendue,Reference):
    database=db.Database()
    if database.get_product_quantity(Reference)[0]-int(quantite_vendue)>=0:
       database.update_deduct_product_quantity(quantite_vendue,Reference)
       CTkMessagebox(title="Succes", message="L'operation est valide")

    else:
        CTkMessagebox(title="Warning", message="Impossible d'effectuer cette facture, la quantite vendue \n depasse le stock de produit de reference"+Reference)
def insert_facture(date_facture,description):
    database=db.Database()
    try:
       id_facture=database.insert_facture(date_facture,description)
    except sqlite3.IntegrityError as e:
           print("Erreur dans la base de donnees")
    historique(f'L\'utilisateur a saisi une facture numero {id_facture}')
    return id_facture
def get_product_reference():
    database=db.Database()
    List_references=[]
    list_reference=database.get_product_references()
    for i in  range(len(list_reference)):
        List_references.append(list_reference[i][0]) 
    return List_references
def get_facture_data():
    database=db.Database()
    nombre_factures=database.facture_count()
    return nombre_factures

#---------------------------------------------------------Gestion d'achats----------------------------------------------------------------------
def achats(first_frame,second_frame):
    for widget in first_frame.winfo_children():
        widget.destroy() 
    for widget in second_frame.winfo_children():
        widget.destroy() 

    nombre_achats=get_achats_data()
    nombre_commandes=get_commandes_data()
    image_vente=ctk.CTkImage(light_image=Image.open(resource_path("images\\achat1.png")),size=(100,100))
    image_commande=ctk.CTkImage(light_image=Image.open(resource_path("images\\commande.png")),size=(100,100))
    button=ctk.CTkButton(master=first_frame,text="Nombre d'achats:\n "+str(nombre_achats[0])+" achats",height=200,width=200,image=image_vente,hover=False,text_color="white",font=('bold',15),fg_color="#b1d4e0")
    button.grid(row=0,column=0,rowspan=2,padx=10,pady=10)
    button=ctk.CTkButton(master=first_frame,text="Nombre de commandes:\n "+str(nombre_commandes[0])+" commandes",height=200,width=200,image=image_commande,hover=False,text_color="white",font=('bold',15),fg_color="#b1d4e0")
    button.grid(row=0,column=1,rowspan=2,padx=10,pady=10)  
    button=ctk.CTkButton(master=first_frame,text="Afficher les commandes",text_color="white",fg_color="blue",height=100,hover_color="#061bb0",command=lambda:afficher_commande())
    button.grid(row=0,column=2,padx=5,pady=5) 
    
    
#add a commande label
    label_facture=ctk.CTkLabel(master=second_frame,text="Effectuer une commande",text_color="blue",font=('bold',20))
    label_facture.grid(row=0,column=0,padx=5,pady=5)
    commande_entry= ctk.CTkEntry(master=second_frame,placeholder_text="Description de la commande")
    commande_entry.grid(row=1,column=0,padx=5,pady=5)
    date_commande_entry= ctk.CTkEntry(master=second_frame,placeholder_text="Date de commande")
    date_commande_entry.grid(row=2,column=0,padx=5,pady=5)
    date_commande_entry.insert(0, "yyyy-mm-dd")

    def pick_date_achat(event):
        date_window = Toplevel()
        date_window .wait_visibility()  
        date_window.grab_set()
        date_window.title('chosir une date')
        date_window.geometry('250x220+590+370')
        cal =Calendar(date_window,selectmode="day", date_pattern="yyyy-mm-dd")
        cal.place(x=0, y=0)
        submit_btn = Button(date_window, text="Soumettre", command=lambda:grab_date(cal,date_commande_entry,date_window))
        submit_btn.place(x=80, y=190)

    def grab_date(cal,date_commande_entry,date_window):
        date_commande_entry.delete(0, END)
        date_commande_entry.insert(0, cal.get_date())
        date_window.destroy()

    date_commande_entry.bind("<1>", pick_date_achat)
    nombre_commandes= ctk.CTkEntry(master=second_frame,placeholder_text="nombre de produits")
    nombre_commandes.grid(row=3,column=0,padx=5,pady=5)
    button=ctk.CTkButton(master=second_frame,text="Entrer",text_color="white",fg_color="blue",hover_color="#061bb0",command=lambda:entrer_commande(nombre_commandes.get(),button,second_frame,commande_entry.get(),date_commande_entry.get()))
    button.grid(row=5,column=0,padx=5,pady=5)
def entrer_commande(nombre_commandes, button, second_frame,desription,date_commande):
    id_commande=insert_commande(desription,date_commande)
    button.destroy()
    label = ctk.CTkLabel(master=second_frame, text="Saisissez les references et les quantitees achetees", text_color="blue", font=('bold', 15))
    label.grid(row=5, column=0, pady=10, padx=10)

    if nombre_commandes.isdigit() == False:
        label = ctk.CTkLabel(master=second_frame, text="Veuillez entrer un nombre", text_color="red", font=('bold', 10))
        label.grid(row=4, column=0, pady=5, padx=5)
    else:
        number = int(nombre_commandes)
        entry_list = []

        for i in range(1, number + 1):
            # Create combo box for references
            les_choix_reference = ctk.CTkComboBox(master=second_frame, font=("Arial", 10), values=get_product_reference())
            les_choix_reference.grid(row=5 + i, column=0, pady=10, padx=10)

            # Create entry field for quantity
            quantite_achetee = ctk.CTkEntry(master=second_frame, placeholder_text="la quantite achetee:")
            quantite_achetee.grid(row=5 + i, column=1, pady=10, padx=10)

            entry_list.append((les_choix_reference, quantite_achetee))

        def soumettre():
            for reference, quantity_entry in entry_list:
                reference_value = reference.get()
                quantity_value = quantity_entry.get()
                print("Reference:", reference_value)
                print("Quantity:", quantity_value)
                calculate_stock_achat(quantity_value,reference_value)
                inserer_achat(quantity_value,reference_value,id_commande)
        button = ctk.CTkButton(master=second_frame, text="Soumettre", command=soumettre)
        button.grid(row=5 + number * 2, column=0, padx=5, pady=5)
#une fonction pour afficher les commandes
def afficher_commande():
    commande_data.affichage_donnees()
#une fonction pour traiter les quantites achetees des produits choisis:
def calculate_stock_achat(quantite_achetee,Reference):
    database=db.Database()
    ajout=database.update_add_product_quantity(quantite_achetee,Reference)
    if ajout:
       CTkMessagebox(title="Succes", message="L'operation est valide")

    
def insert_commande(date_commande,description):
    database=db.Database()
    try:
        id_commande=database.insert_commande(date_commande,description)
    except sqlite3.IntegrityError as e:
           print("Erreur dans la base de donnees")
    historique(f'L\'utilisateur a saisi une commande numero {id_commande}')
    return id_commande
def inserer_achat(quantite_demandee,Reference,id_commande):
    database=db.Database()
    try:
        database.insert_achat(quantite_demandee,Reference,id_commande)
    except sqlite3.IntegrityError as e:
           print("Erreur dans la base de donnees")
    historique(f'L\'utilisateur a effectue un achat associe a la  commande numero {id_commande}')
def get_product_reference():
    database=db.Database()
    List_references=[]
    list_reference=database.get_product_references()
    for i in  range(len(list_reference)):
        List_references.append(list_reference[i][0]) 
    return List_references


def get_commandes_data():
    database=db.Database()
    nombre_commandes=database.commande_count()
    return nombre_commandes




