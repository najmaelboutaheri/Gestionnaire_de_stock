import tkinter as tk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
import sys
import os
import customtkinter as ctk
import getpass

# Obtenez le nom d'utilisateur actuel
current_user = getpass.getuser()

from MODEL import DatabaseSetup as db
from CONTROLLER import cLogin as cl
import sqlite3
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
    list_values=get_facture_data()
    print(list_values)
    for value_tuple in list_values[0:]:
        treeview.insert('', tk.END, values=value_tuple)
def get_facture_data():
    database=db.Database()
    factures=database.get_facture_details()
    return factures
def Delete_row_facture(frame, widgets_frame, treeview, treeFrame, treeScroll, style,cols):
    # Clear any existing widgets in the widgets_frame
    for widget in widgets_frame.winfo_children():
        widget.destroy()

    entry_label = ttk.Label(widgets_frame, text="id_facture")
    entry_label.grid(sticky="w", padx=5, pady=5)
    entry = ttk.Entry(widgets_frame)
    entry.grid(sticky="w", padx=5, pady=5)

    def delete():
        id_facture = entry.get()
        entry.delete(0,"end")
        database = db.Database()

        try:
            suppression = database.delete_facture(id_facture)
            if suppression:
               cl.historique(f'L\'utilisateur a supprime une facture numero {id_facture}')
               # Clear existing data in the treeview
               for item in treeview.get_children():
                   treeview.delete(item)
               # Refresh the treeview content
               load_data(treeview,cols)
            else:
               CTkMessagebox(title="Warning", message="L'opération a échoué")
        except sqlite3.IntegrityError as e:
            CTkMessagebox(title="Warning", message="Vous devez supprimer tout d'abord la vente associé à la facture")
    delete_button = ttk.Button(widgets_frame, text="Supprimer une facture",command=delete)
    delete_button.grid(row=3, column=2, padx=20, pady=10)

    back_button = ttk.Button(widgets_frame, text="Retourner", command=lambda: retourner( widgets_frame, treeview, treeFrame, treeScroll, frame, style))
    back_button.grid(row=4, column=2, padx=20, pady=10)
def search_row_facture(frame,widgets_frame,treeview,treeFrame,treeScroll,style):
    widgets_frame.destroy()
    widgets_frame = ttk.LabelFrame(frame, text="Vous pouvez rechercher une facture")
    widgets_frame.grid(row=0, column=2, padx=20, pady=10)
    entry_label = ttk.Label(widgets_frame, text="id_facture")
    entry_label.grid(sticky="w", padx=5, pady=5)
    entry = ttk.Entry(widgets_frame)
    entry.grid(sticky="w", padx=5, pady=5)
    
    delete_button = ttk.Button(widgets_frame, text="rechercher une facture",command=lambda: search_Row_facture(entry.get(),treeview,treeFrame,treeScroll,entry))#frame,widgets_frame ,treeview,path,mysheet
    delete_button.grid(row=3, column=2, padx=20, pady=10)
    back_button = ttk.Button(widgets_frame, text="Retourner",command=lambda:retourner(widgets_frame,treeview,treeFrame,treeScroll,frame,style))#frame,widgets_frame ,treeview,path,mysheet
    back_button.grid(row=4, column=2, padx=20, pady=10)

def search_Row_facture(id_facture, treeview, treeFrame, treeScroll, entry):
    # Connect to the database
    database = db.Database()
    
    # Get facture details from the database
    Recherche = database.get_facture(id_facture)
    entry.delete(0, "end")
    
    if Recherche!=[]:
        cl.historique(f'L\'utilisateur a chercher sur  une facture numero {id_facture}')
        # Clear the existing data in the treeview
        for item in treeview.get_children():
            treeview.delete(item)
        
        # Update the treeview with matching rows
        for row in Recherche:
            treeview.insert('', tk.END, values=row)
    else:
        CTkMessagebox(title="Warning", message="Aucune facture trouvée")

def retourner(widgets_frame,treeview,treeFrame,treeScroll,frame,style):
    for widget in widgets_frame.winfo_children():
        widget.destroy()
    treeview.destroy()
    widgets_frame.destroy()
    cols = ("id_facture","description_facture","date_facture")
    treeview = ttk.Treeview(treeFrame, show="headings",yscrollcommand=treeScroll.set, columns=cols, height=13)

    # Set column widths
    for col in cols:
        treeview.column(col, width=100)
    treeview.pack()
    treeScroll.config(command=treeview.yview)
    load_data(treeview,cols)
    widgets_frame = ttk.LabelFrame(frame, text="Vous pouvez supprimer, rechercher une facture ou afficher les ventes")
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
    delete_button = ttk.Button(widgets_frame, text="Supprimer", command=lambda: Delete_row_facture(frame,widgets_frame,treeview,treeFrame,treeScroll,style,cols))#frame,widgets_frame ,treeview,path,mysheet
    delete_button.grid(row=1, column=3, padx=20, pady=10)
    search_button = ttk.Button(widgets_frame, text="Rechercher", command=lambda: search_row_facture(frame,widgets_frame,treeview,treeFrame,treeScroll,style))
    search_button.grid(row=2, column=3, padx=20, pady=10)
    vente_button = ttk.Button(widgets_frame, text="Afficher les ventes", command=lambda: afficher_ventes(frame,widgets_frame,treeview,treeFrame,treeScroll,style))
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
   
    cols = ("id_facture","description_facture","date_facture")
    treeview = ttk.Treeview(treeFrame, show="headings",yscrollcommand=treeScroll.set, columns=cols, height=13)

    # Set column widths
    for col in cols:
        treeview.column(col, width=100)
   
    treeview.pack()
    treeScroll.config(command=treeview.yview)
    load_data(treeview,cols)
    widgets_frame = ttk.LabelFrame(frame, text="Vous pouvez supprimer, rechercher une facture ou afficher les ventes")
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

    delete_button = ttk.Button(widgets_frame, text="Supprimer", command=lambda: Delete_row_facture(frame,widgets_frame,treeview,treeFrame,treeScroll,style,cols))#frame,widgets_frame ,treeview,path,mysheet
    delete_button.grid(row=1, column=3, padx=20, pady=10)
    search_button = ttk.Button(widgets_frame, text="Rechercher", command=lambda: search_row_facture(frame,widgets_frame,treeview,treeFrame,treeScroll,style))
    search_button.grid(row=2, column=3, padx=20, pady=10)
    vente_button = ttk.Button(widgets_frame, text="Afficher les ventes", command=lambda: afficher_ventes(frame,widgets_frame,treeview,treeFrame,treeScroll,style))
    vente_button.grid(row=3, column=3, padx=20, pady=10)
    
    root.mainloop()
##############################################
def afficher_ventes(frame,widgets_frame,treeview,treeFrame,treeScroll,style):
    for widget in widgets_frame.winfo_children():
        widget.destroy()
    treeview.destroy()
    widgets_frame.destroy()
    cols = ("id_vente","quantite_vendue","Reference","id_facture")
    treeview = ttk.Treeview(treeFrame, show="headings",yscrollcommand=treeScroll.set, columns=cols, height=13)
    
    # Set column widths
    for col in cols:
        treeview.column(col, width=100)
    treeview.pack()
    treeScroll.config(command=treeview.yview)
    load_data_vente(treeview,cols)
    widgets_frame = ttk.LabelFrame(frame, text="Vous pouvez supprimer ou rechercher une vente ")
    widgets_frame.grid(row=0, column=2, padx=0, pady=0)

    delete_button = ttk.Button(widgets_frame, text="Supprimer", command=lambda: Delete_row_vente(frame,widgets_frame,treeview,treeFrame,treeScroll,style,cols))#frame,widgets_frame ,treeview,path,mysheet
    delete_button.grid(row=1, column=3, padx=20, pady=10)
    search_button = ttk.Button(widgets_frame, text="Rechercher", command=lambda: search_row_vente(frame,widgets_frame,treeview,treeFrame,treeScroll,style))
    search_button.grid(row=2, column=3, padx=20, pady=10)
    supprimer_button = ttk.Button(widgets_frame, text="Retourner",command=lambda:retourner(widgets_frame,treeview,treeFrame,treeScroll,frame,style))
    supprimer_button.grid(row=2, column=3, padx=20, pady=10)
def Delete_row_vente(frame,widgets_frame,treeview,treeFrame,treeScroll,style,cols):
     # Clear any existing widgets in the widgets_frame
    for widget in widgets_frame.winfo_children():
        widget.destroy()

    entry_label = ttk.Label(widgets_frame, text="id_vente")
    entry_label.grid(sticky="w", padx=5, pady=5)
    entry = ttk.Entry(widgets_frame)
    entry.grid(sticky="w", padx=5, pady=5)

    def delete():
        id_vente = entry.get()
        entry.delete(0,"end")
        database = db.Database()
        try:
            suppression = database.delete_vente(id_vente)
            if suppression:
              cl.historique(f'L\'utilisateur a supprime  une vente numero {id_vente}')
              # Clear existing data in the treeview
              for item in treeview.get_children():
                 treeview.delete(item)
              # Refresh the treeview content
              load_data_vente(treeview,cols)
            else:
               CTkMessagebox(title="Warning", message="L'opération a échoué")
        except sqlite3.IntegrityError as e:
             CTkMessagebox(title="Warning", message="Impossible  de supprimer ce produit")

           
    delete_button = ttk.Button(widgets_frame, text="Supprimer une vente",command=delete)
    delete_button.grid(row=3, column=2, padx=20, pady=10)
    back_button = ttk.Button(widgets_frame, text="Retourner",command=lambda:retourner(widgets_frame,treeview,treeFrame,treeScroll,frame,style))#frame,widgets_frame ,treeview,path,mysheet
    back_button.grid(row=4, column=2, padx=20, pady=10)
def search_row_vente(frame,widgets_frame,treeview,treeFrame,treeScroll,style):
    widgets_frame.destroy()
    widgets_frame = ttk.LabelFrame(frame, text="Vous pouvez rechercher une vente")
    widgets_frame.grid(row=0, column=2, padx=20, pady=10)
    entry_label = ttk.Label(widgets_frame, text="id_vente")
    entry_label.grid(sticky="w", padx=5, pady=5)
    entry = ttk.Entry(widgets_frame)
    entry.grid(sticky="w", padx=5, pady=5)
    
    delete_button = ttk.Button(widgets_frame, text="rechercher une vente",command=lambda: search_Row_vente(entry.get(),treeview,treeFrame,treeScroll,entry))#frame,widgets_frame ,treeview,path,mysheet
    delete_button.grid(row=3, column=2, padx=20, pady=10)
    back_button = ttk.Button(widgets_frame, text="Retourner",command=lambda:retourner(widgets_frame,treeview,treeFrame,treeScroll,frame,style))#frame,widgets_frame ,treeview,path,mysheet
    back_button.grid(row=4, column=2, padx=20, pady=10)
def search_Row_vente(id_vente, treeview, treeFrame, treeScroll, entry):
    # Connect to the database
    database = db.Database()
    
    # Get facture details from the database
    Recherche = database.get_vente_details(id_vente)
    entry.delete(0, "end")
    
    if Recherche!=[]:
        cl.historique(f'L\'utilisateur a cherche sur une vente numero {id_vente}')
        # Clear the existing data in the treeview
        for item in treeview.get_children():
            treeview.delete(item)
        
        # Update the treeview with matching rows
        for row in Recherche:
            treeview.insert('', tk.END, values=row)
    else:
        CTkMessagebox(title="Warning", message="Aucune vente trouvée")
def load_data_vente(treeview,cols):
    lists_values=cols
    for col_name in lists_values:
        treeview.heading(col_name, text=col_name)
    list_values=get_vente_data()
    print(list_values)
    for value_tuple in list_values[0:]:
        treeview.insert('', tk.END, values=value_tuple)
def get_vente_data():
    database = db.Database()
    achats=database.get_ventes_details()
    return achats