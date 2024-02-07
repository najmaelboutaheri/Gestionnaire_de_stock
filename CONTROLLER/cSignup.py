import customtkinter as ctk
from customtkinter import END
import sys
import getpass

# Obtenez le nom d'utilisateur actuel
current_user = getpass.getuser()
from MODEL import DatabaseSetup as db
from CTkMessagebox import CTkMessagebox
import re
#methods to use
def Signup(Frame,nom,prenom,email,CIN,numero,mot_de_passe,mot_de_passe_confirme):
    #le button" Soumettre et mémoriser"<---------------------
    #cette fonction vas vérifier l'input de l'utilisateur ,et aprés vas l'insérer dans la base de données
    #declaration des varilables:
    Nom = nom.get()
    Prenom = prenom.get()
    Email = email.get()
    cIN = CIN.get()
    Numero = numero.get()
    Mot_de_passe = mot_de_passe.get()
    Mot_de_passe_confirme = mot_de_passe_confirme.get()
    
   
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    #ces dictionnaires sont déclarés pour optimiser le code 
    D={}
    B={}
    #le dictionnaire D contient la position exacte de la ligne d'instruction d'erreur qui sera nécessaire ci-dessous
    
    D[nom] = [8, 0]
    D[prenom] = [11, 0]
    D[email] = [14, 0]
    D[CIN] = [17, 0]
    D[numero] = [20, 0]
    D[mot_de_passe] = [23, 0]
    D[mot_de_passe_confirme] = [26, 0]
    # le dictionnaire B contient les variables ENTRY qui seront nécessaires ci-dessous
    B[nom] = nom
    B[prenom] = prenom
    B[email] = email
    B[CIN] = CIN
    B[numero] = numero
    B[mot_de_passe] = mot_de_passe
    B[mot_de_passe_confirme] = mot_de_passe_confirme
    # Verfication0: vérifier si les valeurs dans D sont numeric digits
    for i in D:
        if  i.get().isdigit() == True and i!=numero:
            B[i].delete(0, END)
            lab = ctk.CTkLabel(Frame, text="ne doit pas contenir seulement des chiffres", text_color="red")
            lab.grid(row=D[i][0], column=D[i][1])
    #verfication1: si le champ est vide.
    if Nom == "" or Prenom == "" or Email == "" or cIN == "" or Numero == "" or Mot_de_passe == "" or Mot_de_passe_confirme == "":
        label_erreur = ctk.CTkLabel(Frame, text="Erreur : Veuillez remplir tous les champs obligatoires*",fg_color="red")
        label_erreur.grid(row=3, column=0)
    #verfication2: si le numero est caractere
    elif Numero.isdigit() == False:
        numero.delete(0, END)
        lab = ctk.CTkLabel(Frame, text="ne doit pas contenir des caractères", text_color="red")
        lab.grid(row=20, column=0)
    #verification3 de mot de pass confirme
    elif Mot_de_passe_confirme!=Mot_de_passe:
         mot_de_passe_confirme.delete(0, END)
         lab = ctk.CTkLabel(Frame, text="vous devez taper le même Mot de passe", text_color="red")
         lab.grid(row=26, column=0)
    elif not (re.fullmatch(regex, Email)):
         email.delete(0, END)
         lab = ctk.CTkLabel(Frame, text="email invalid", text_color="red")
         lab.grid(row=14, column=0)
    else:
        # vérifier si le compte existe deja
        database=db.Database()
        database.searchLogin(Nom,Mot_de_passe)
        print("true")
        #fetching the result
        result= database.searchLogin(Nom,Mot_de_passe)
        if len(result)!=0 :
            CTkMessagebox(title="Warning ", message="vous avez deja un compte")
        else:
            # Exécuter le code pour insérer des informations dans la base de données
            database.insert_signup_table(Nom,Prenom,Email,cIN,Numero,Mot_de_passe)
            CTkMessagebox(title="Warning", message="l'opération est bien réussie")
            # créer une autre page pour  log in ou exit
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("green")
            
"""label=ctk.CTkLabel(master=first_frame,text="Entrez le nom des categories",text_color="blue",font=('bold',15))
    label.grid(row=4,column=0,pady=10,padx=10)
    try:
        num_categories = int(cat_number.get())
    except ValueError:
        label=ctk.CTkLabel(master=first_frame,text="Veuillez entrer un nombre",text_color="red",font=('bold',10))
        label.grid(row=3,column=0,pady=5,padx=5)
        
    for i in range(num_categories):
        cat_name= ctk.CTkEntry(master=first_frame,placeholder_text="categorie "+i+":")
        cat_name.grid(row=4+i+1,column=0,pady=10, padx=10)
        List_categories.append(cat_name.get())
    button=ctk.CTkButton(master=first_frame,text="Ajouter",command=lambda:add_classification(List_categories,classification_name.get(),first_frame,second_frame))
    button.grid(row=5,column=0,padx=5,pady=5)
    button=ctk.CTkButton(master=first_frame,text="Retourner",command=lambda:produits(first_frame,second_frame))
    button.grid(row=5,column=1,padx=5,pady=5)    


    

        """