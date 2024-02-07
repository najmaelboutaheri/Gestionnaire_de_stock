import tkinter as tk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
import sys
import os
import sqlite3
import getpass

# Obtenez le nom d'utilisateur actuel
current_user = getpass.getuser()

from MODEL import DatabaseSetup as db
from CONTROLLER import cLogin as cl
themes_loaded = False
create_root=False
def load_themes(root):
    global themes_loaded
    if not themes_loaded:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        light_theme_path = os.path.join(script_directory, "forest-light.tcl")
        dark_theme_path = os.path.join(script_directory, "forest-dark.tcl")

        root.tk.call("source", light_theme_path)
        root.tk.call("source", dark_theme_path)

        themes_loaded = True
def load_data(treeview,cols):
    lists_values=cols
    for col_name in lists_values:
        treeview.heading(col_name, text=col_name)
    list_values=get_commande_data()
    print(list_values)
    for value_tuple in list_values[0:]:
        treeview.insert('', tk.END, values=value_tuple)
def get_commande_data():
    database=db.Database()
    factures=database.get_commande_details()
    return factures
def Delete_row_commande(frame, widgets_frame, treeview, treeFrame, treeScroll, style,cols):
    # Clear any existing widgets in the widgets_frame
    for widget in widgets_frame.winfo_children():
        widget.destroy()

    entry_label = ttk.Label(widgets_frame, text="id_commande")
    entry_label.grid(sticky="w", padx=5, pady=5)
    entry = ttk.Entry(widgets_frame)
    entry.grid(sticky="w", padx=5, pady=5)

    def delete():
        id_commande = entry.get()
        entry.delete(0,"end")
        database = db.Database()
        try:
            suppression = database.delete_commande(id_commande)
            if suppression:
              cl.historique(f'L\'utilisateur a supprime  une commande numero {id_commande}')
              # Clear existing data in the treeview
              for item in treeview.get_children():
                 treeview.delete(item)
              # Refresh the treeview content
              load_data(treeview,cols)
            else:
               CTkMessagebox(title="Warning", message="L'opération a échoué")
        except sqlite3.IntegrityError as e:
            CTkMessagebox(title="Warning", message="Vous devez supprimer tout d'abord l'achat associé à la commande")

    delete_button = ttk.Button(widgets_frame, text="Supprimer une facture",command=delete)
    delete_button.grid(row=3, column=2, padx=20, pady=10)

    back_button = ttk.Button(widgets_frame, text="Retourner", command=lambda: retourner( widgets_frame, treeview, treeFrame, treeScroll, frame, style))
    back_button.grid(row=4, column=2, padx=20, pady=10)
def search_row_commande(frame,widgets_frame,treeview,treeFrame,treeScroll,style):
    widgets_frame.destroy()
    widgets_frame = ttk.LabelFrame(frame, text="Vous pouvez rechercher une commande")
    widgets_frame.grid(row=0, column=2, padx=20, pady=10)
    entry_label = ttk.Label(widgets_frame, text="id_commande")
    entry_label.grid(sticky="w", padx=5, pady=5)
    entry = ttk.Entry(widgets_frame)
    entry.grid(sticky="w", padx=5, pady=5)
    
    delete_button = ttk.Button(widgets_frame, text="rechercher une commande",command=lambda: search_Row_commande(entry.get(),treeview,treeFrame,treeScroll,entry))#frame,widgets_frame ,treeview,path,mysheet
    delete_button.grid(row=3, column=2, padx=20, pady=10)
    back_button = ttk.Button(widgets_frame, text="Retourner",command=lambda:retourner(widgets_frame,treeview,treeFrame,treeScroll,frame,style))#frame,widgets_frame ,treeview,path,mysheet
    back_button.grid(row=4, column=2, padx=20, pady=10)

def search_Row_commande(id_commande, treeview, treeFrame, treeScroll, entry):
    # Connect to the database
    database = db.Database()
    
    # Get facture details from the database
    Recherche = database.get_commande(id_commande)
    entry.delete(0, "end")
    
    if Recherche!=[]:
        cl.historique(f'L\'utilisateur a cherche sur une commande  numero {id_commande}')
        # Clear the existing data in the treeview
        for item in treeview.get_children():
            treeview.delete(item)
        
        # Update the treeview with matching rows
        for row in Recherche:
            treeview.insert('', tk.END, values=row)
    else:
        CTkMessagebox(title="Warning", message="Aucune commande trouvée")

def retourner(widgets_frame,treeview,treeFrame,treeScroll,frame,style):
    for widget in widgets_frame.winfo_children():
        widget.destroy()
    treeview.destroy()
    widgets_frame.destroy()
    cols = ("id_commande","description_commande","date_commande")
    treeview = ttk.Treeview(treeFrame, show="headings",yscrollcommand=treeScroll.set, columns=cols, height=13)

    # Set column widths
    for col in cols:
        treeview.column(col, width=100)
    treeview.pack()
    treeScroll.config(command=treeview.yview)
    load_data(treeview,cols)
    widgets_frame = ttk.LabelFrame(frame, text="Vous pouvez supprimer, rechercher une commande ou afficher les achats")
    widgets_frame.grid(row=0, column=2, padx=0, pady=0)
    #cols = ("Reference", "nom_produit", "description", "prod_quantity", "sub_category", "cat_name", "poids", "la_taille","nom_classification")
    """ entry_values = []
    for col in cols:
        entry_label = ttk.Label(widgets_frame, text=col)
        entry_label.grid(sticky="w", padx=5, pady=5)

        entry = ttk.Entry(widgets_frame)
        entry.grid(sticky="w", padx=5, pady=1)
        entry_values.append(entry)
    """
    delete_button = ttk.Button(widgets_frame, text="Supprimer", command=lambda: Delete_row_commande(frame,widgets_frame,treeview,treeFrame,treeScroll,style,cols))#frame,widgets_frame ,treeview,path,mysheet
    delete_button.grid(row=1, column=3, padx=20, pady=10)
    search_button = ttk.Button(widgets_frame, text="Rechercher", command=lambda: search_row_commande(frame,widgets_frame,treeview,treeFrame,treeScroll,style))
    search_button.grid(row=2, column=3, padx=20, pady=10)
    vente_button = ttk.Button(widgets_frame, text="Afficher les achats", command=lambda: afficher_achats(frame,widgets_frame,treeview,treeFrame,treeScroll,style))
    vente_button.grid(row=3, column=3, padx=20, pady=10)
def affichage_donnees():
    root=tk.Tk()
    script_directory = os.path.dirname(os.path.abspath(__file__))
    light_theme_path = os.path.join(script_directory, "forest-light.tcl")
    dark_theme_path = os.path.join(script_directory, "forest-dark.tcl")

    root.tk.call("source", light_theme_path)
    root.tk.call("source", dark_theme_path)
    style = ttk.Style(root)    
    style.theme_use("forest-dark")

    frame = ttk.Frame(root,width=1000,height=700)
    frame.pack()
    """separator = ttk.Separator(widgets_frame)
    separator.grid(row=5, column=0, padx=(20, 10), pady=10, sticky="ew")"""

    """ mode_switch = ttk.Checkbutton(widgets_frame, text="Mode", style="Switch", command=lambda:toggle_mode(mode_switch,style))
    mode_switch.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")"""

    treeFrame = ttk.Frame(frame)
    treeFrame.grid(row=0, column=1, pady=10)
    treeScroll = ttk.Scrollbar(treeFrame)
    treeScroll.pack(side="right", fill="y")
   
    cols = ("id_commande","description_commande","date_commande")
    treeview = ttk.Treeview(treeFrame, show="headings",yscrollcommand=treeScroll.set, columns=cols, height=13)

    # Set column widths
    for col in cols:
        treeview.column(col, width=100)
   
    treeview.pack()
    treeScroll.config(command=treeview.yview)
    load_data(treeview,cols)
    widgets_frame = ttk.LabelFrame(frame, text="Vous pouvez supprimer, rechercher une commande ou afficher les achats")
    widgets_frame.grid(row=0, column=2, padx=0, pady=0)
        
    """separator = ttk.Separator(widgets_frame)
    separator.grid(row=5, column=0, padx=(20, 10), pady=10, sticky="ew")"""

    """mode_switch = ttk.Checkbutton(widgets_frame, text="Mode", style="Switch", command=lambda:toggle_mode(mode_switch,style))
    mode_switch.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")"""
    """ entry_values = []
    for col in cols:
        entry_label = ttk.Label(widgets_frame, text=col)
        entry_label.grid(sticky="w", padx=5, pady=5)

        entry = ttk.Entry(widgets_frame)
        entry.grid(sticky="w", padx=5, pady=1)
        entry_values.append(entry)"""

    delete_button = ttk.Button(widgets_frame, text="Supprimer", command=lambda: Delete_row_commande(frame,widgets_frame,treeview,treeFrame,treeScroll,style,cols))#frame,widgets_frame ,treeview,path,mysheet
    delete_button.grid(row=1, column=3, padx=20, pady=10)
    search_button = ttk.Button(widgets_frame, text="Rechercher", command=lambda: search_row_commande(frame,widgets_frame,treeview,treeFrame,treeScroll,style))
    search_button.grid(row=2, column=3, padx=20, pady=10)
    achat_button = ttk.Button(widgets_frame, text="Afficher les achats", command=lambda: afficher_achats(frame,widgets_frame,treeview,treeFrame,treeScroll,style))
    achat_button.grid(row=3, column=3, padx=20, pady=10)
    
    root.mainloop()
##############################################
def afficher_achats(frame,widgets_frame,treeview,treeFrame,treeScroll,style):
    for widget in widgets_frame.winfo_children():
        widget.destroy()
    treeview.destroy()
    widgets_frame.destroy()
    cols = ("id_achat","quantite_demandee","Reference","id_commande")
    treeview = ttk.Treeview(treeFrame, show="headings",yscrollcommand=treeScroll.set, columns=cols, height=13)
    
    # Set column widths
    for col in cols:
        treeview.column(col, width=100)
    treeview.pack()
    treeScroll.config(command=treeview.yview)
    load_data_achat(treeview,cols)
    widgets_frame = ttk.LabelFrame(frame, text="Vous pouvez supprimer ou rechercher un achat ")
    widgets_frame.grid(row=0, column=2, padx=0, pady=0)

    delete_button = ttk.Button(widgets_frame, text="Supprimer", command=lambda: Delete_row_achat(frame,widgets_frame,treeview,treeFrame,treeScroll,style,cols))#frame,widgets_frame ,treeview,path,mysheet
    delete_button.grid(row=1, column=3, padx=20, pady=10)
    search_button = ttk.Button(widgets_frame, text="Rechercher", command=lambda: search_row_achat(frame,widgets_frame,treeview,treeFrame,treeScroll,style))
    search_button.grid(row=2, column=3, padx=20, pady=10)
    supprimer_button = ttk.Button(widgets_frame, text="Retourner",command=lambda:retourner(widgets_frame,treeview,treeFrame,treeScroll,frame,style))
    supprimer_button.grid(row=2, column=3, padx=20, pady=10)
def Delete_row_achat(frame,widgets_frame,treeview,treeFrame,treeScroll,style,cols):
     # Clear any existing widgets in the widgets_frame
    for widget in widgets_frame.winfo_children():
        widget.destroy()

    entry_label = ttk.Label(widgets_frame, text="id_achat")
    entry_label.grid(sticky="w", padx=5, pady=5)
    entry = ttk.Entry(widgets_frame)
    entry.grid(sticky="w", padx=5, pady=5)

    def delete():
        id_achat = entry.get()
        entry.delete(0,"end")
        database = db.Database()
        try:
            suppression = database.delete_achat(id_achat)
            if suppression:
                cl.historique(f'L\'utilisateur a supprime  un achat numero {id_achat}')
                # Clear existing data in the treeview
                for item in treeview.get_children():
                   treeview.delete(item)
                # Refresh the treeview content
                load_data_achat(treeview,cols)
            else:
               CTkMessagebox(title="Warning", message="L'opération a échoué")
        except sqlite3.IntegrityError as e:
            CTkMessagebox(title="Warning", message="Imposible de supprimer ce produit")
           
    delete_button = ttk.Button(widgets_frame, text="Supprimer un achat",command=delete)
    delete_button.grid(row=3, column=2, padx=20, pady=10)
    back_button = ttk.Button(widgets_frame, text="Retourner",command=lambda:retourner(widgets_frame,treeview,treeFrame,treeScroll,frame,style))#frame,widgets_frame ,treeview,path,mysheet
    back_button.grid(row=4, column=2, padx=20, pady=10)

def search_row_achat(frame,widgets_frame,treeview,treeFrame,treeScroll,style):
    widgets_frame.destroy()
    widgets_frame = ttk.LabelFrame(frame, text="Vous pouvez rechercher un achat")
    widgets_frame.grid(row=0, column=2, padx=20, pady=10)
    entry_label = ttk.Label(widgets_frame, text="id_achat")
    entry_label.grid(sticky="w", padx=5, pady=5)
    entry = ttk.Entry(widgets_frame)
    entry.grid(sticky="w", padx=5, pady=5)
    
    delete_button = ttk.Button(widgets_frame, text="rechercher un achat",command=lambda: search_Row_achat(entry.get(),treeview,treeFrame,treeScroll,entry))#frame,widgets_frame ,treeview,path,mysheet
    delete_button.grid(row=3, column=2, padx=20, pady=10)
    back_button = ttk.Button(widgets_frame, text="Retourner",command=lambda:retourner(widgets_frame,treeview,treeFrame,treeScroll,frame,style))#frame,widgets_frame ,treeview,path,mysheet
    back_button.grid(row=4, column=2, padx=20, pady=10)
    
def search_Row_achat(id_achat, treeview, treeFrame, treeScroll, entry):
    # Connect to the database
    database = db.Database()
    
    # Get facture details from the database
    Recherche = database.get_achat_details(id_achat)
    entry.delete(0, "end")
    
    if Recherche!=[]:
        cl.historique(f'L\'utilisateur a supprime  un achat numero {id_achat}')
        # Clear the existing data in the treeview
        for item in treeview.get_children():
            treeview.delete(item)
        
        # Update the treeview with matching rows
        for row in Recherche:
            treeview.insert('', tk.END, values=row)
    else:
        CTkMessagebox(title="Warning", message="Aucun achat trouvé")
def load_data_achat(treeview,cols):
    lists_values=cols
    for col_name in lists_values:
        treeview.heading(col_name, text=col_name)
    list_values=get_achats_details()
    print(list_values)
    for value_tuple in list_values[0:]:
        treeview.insert('', tk.END, values=value_tuple)
def get_achats_details():
    database = db.Database()
    achats=database.get_achats_details()
    return achats