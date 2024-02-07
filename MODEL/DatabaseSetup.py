# importing modules
import sqlite3
import os
import sys
import getpass

# Obtenez le nom d'utilisateur actuel
current_user = getpass.getuser()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
class Database():
    """ Connects to Database
        Foreign Key Check=ON
        Key Arguments : None
    """
    def __init__(self):
        # Create a db or connect to one
        self.conn = sqlite3.connect(resource_path("MODEL\\Database.db"))

        # Enabling foreign key constraints
        self.conn.execute("PRAGMA foreign_keys = 1")

        # Create cursor
        self.c = self.conn.cursor()
        
    ####=====================METHODS=========================####
            
    #==================== LOGIN ====================================#
        
    def create_login_table(self):
        with self.conn:
            self.c.execute("""CREATE TABLE login (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                PASSWORD TEXT NOT NULL
            )""")

    def insert_login_table(self,username,PASSWORD):
        with self.conn:
            self.c.execute("INSERT INTO login (username, password) VALUES (?, ?)",(username,PASSWORD))
    
    def change_password(self, new_password):
        """Changes Password value from the databse
        Key Arguments: new_password -- String
        """
        with self.conn:
            self.c.execute("UPDATE login SET password = ? WHERE id = 1", (new_password,)) 

    def get_login_data(self):
        with self.conn:
            self.c.execute("SELECT * FROM login")
            result = self.c.fetchone()
            return result   
    def searchLogin(self, username,password):
        with self.conn:
            self.c.execute("select * from login  where username=? and  password = ? ", (username,password))
            result=self.c.fetchall()
            return result
    #==================== SIGNUP ====================================#
        
    def create_signup_table(self):
        with self.conn:
            self.c.execute("""CREATE TABLE Sign_UP (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                NOM TEXT UNIQUE NOT NULL,
                PRENOM TEXT NOT NULL,
                EMAIL TEXT NOT NULL,
                CIN TEXT NOT NULL,
                NUMERO TEXT NOT NULL,
                PASSWORD TEXT NOT NULL
            )""")

    def insert_signup_table(self,NOM,PRENOM,EMAIL,CIN,NUMERO,PASSWORD):
        with self.conn:
            self.c.execute("INSERT INTO Sign_UP (NOM,PRENOM,EMAIL,CIN,NUMERO,PASSWORD) VALUES (?,?,?,?,?,?)",(NOM,PRENOM,EMAIL,CIN,NUMERO,PASSWORD))
    

    def get_signup_data(self):
        with self.conn:
            self.c.execute("SELECT * FROM Sign_UP")
            result = self.c.fetchall()
            return result 
    def delete_Signup(self):
        with self.conn:
            self.c.execute("DELETE FROM Sign_UP WHERE id= 2")
    def update_password(self,old_password,new_password):
        with self.conn:
            self.c.execute("UPDATE Sign_UP SET PASSWORD = ? WHERE PASSWORD = ?",(new_password,old_password))
    def searchSignup(self, username,password):
        with self.conn:
            self.c.execute("select * from Sign_UP  where NOM=? and  PASSWORD = ? ", (username,password))
            result=self.c.fetchall()
            return result
    #==================== Remember ====================================#
        
    def create_Remember_table(self):
        with self.conn:
            self.c.execute("""CREATE TABLE Remember (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                INDICE TEXT  NOT NULL,
                USERNAME TEXT NOT NULL,
                PASSWORD TEXT NOT NULL
            )""")

    def insert_Remember_table(self,INDICE,USERNAME,PASSWORD):
        with self.conn:
            self.c.execute("INSERT INTO Remember (INDICE,USERNAME,PASSWORD) VALUES (?,?,?)",(INDICE,USERNAME,PASSWORD))
    

    def get_Remember_data(self):
        with self.conn:
            self.c.execute("SELECT * FROM Remember")
            result = self.c.fetchall()
            return result  
    def delete_remember_data(self):
        with self.conn:
            self.c.execute("DELETE FROM Remember") 
    #======================== THEME =====================================#

    def create_theme_table(self):
        with self.conn:
            self.c.execute("""CREATE TABLE theme (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                theme_mode TEXT NOT NULL
            )""")
    
    def insert_theme_table(self):
        with self.conn:
            self.c.execute("INSERT INTO theme VALUES (1,'Light Mode')")
    
    def get_theme_value(self):
        with self.conn:
            self.c.execute("SELECT * FROM theme")
            result = self.c.fetchone()
            # print(result)
            return result
    
    def change_theme(self, theme_name):
        """Changes Theme value in Database
        Key Arguments: theme_name 
        theme_name allowed values = (1)Light Mode (2) Dark Mode
         """
        with self.conn:
            self.c.execute("UPDATE theme SET theme_mode = ? WHERE id = 1", (theme_name,))
    
    #======================== CATEGORY TABLE =====================================#

    def create_category_table(self):
        with self.conn:
            self.c.execute("""CREATE TABLE category (
                cat_name TEXT PRIMARY KEY  NOT NULL, 
                nom_classification TEXT  NOT NULL
            )""")
    def get_category_name(self,cat_name):
        """select Category name from Database
        Key Arguments: None
         """
        with self.conn:
            self.c.execute("SELECT cat_name FROM category WHERE cat_name=?",(cat_name,))
            result = self.c.fetchall()
            # print(result)
            return result
    def get_classification_name(self,nom_classification):
        """select the classification name from Database
        Key Arguments: nom_classification --String
         """
        with self.conn:
            self.c.execute("SELECT nom_classification FROM category WHERE nom_classification=?",(nom_classification,))
            result = self.c.fetchall()
            return result
    def insert_category(self, cat_name,nom_classification):
        """Insert Category value in Database
        Key Arguments: cat_name -- String
        nom_classification --- String
        """
        with self.conn:
            self.c.execute("INSERT INTO category (cat_name,nom_classification) VALUES (?,?)", (cat_name,nom_classification))
            return True
    def update_category(self, new_cat_name, old_cat_name):
        """Update Category name in Database
        Key Arguments: new_cat_name -- String
                       old_cat_name -- String
        """
        with self.conn:
            self.c.execute("UPDATE category SET cat_name = ? WHERE cat_name = ?", (new_cat_name, old_cat_name))

    def delete_category(self, cat_name):
        """Delete Category value in Database
        Key Arguments: cat_name -- String
         """
        with self.conn:
            self.c.execute("DELETE FROM category WHERE cat_name = ?", (cat_name,))
            return True
    def delete_category_and_classification(self,cat_name,nom_classification):
        """Delete Category and classification values from Database
        Key Arguments: cat_name -- String
        nom_classification -- String
         """
        with self.conn:
            self.c.execute("DELETE FROM category WHERE cat_name = ? and nom_classification=?", (cat_name,nom_classification))
            return True
    def get_category(self):
        """Fetches all Category name from Database
        Key Arguments: None
         """
        with self.conn:
            self.c.execute("SELECT * FROM category")
            result = self.c.fetchall()
            # print(result)
            return result
    def get_category_by_classification_name(self,nom_classification):
        """Fetches all Category name from Database using nom_classification
        Key Arguments: nom_classification ---String
         """
        with self.conn:
            self.c.execute("SELECT * FROM category WHERE nom_classification=?",(nom_classification,))
            result = self.c.fetchall()
            # print(result)
            return result
    def search_category(self,cat_name):
        """search for Category name from Database
        Key Arguments: None
         """
        with self.conn:
            self.c.execute("SELECT * FROM category WHERE cat_name = ?", (cat_name,))
            result = self.c.fetchall()
            # print(result)
            return result
    def category_count(self,classification_name):
        """returns the number of categories"""
        with self.conn:
            self.c.execute("SELECT count(*) FROM category WHERE nom_classification=? ",(classification_name,))
            result = self.c.fetchone()
            return result
    def delete_category_by_id(self):
        """Delete Category value in Database
        Key Arguments: cat_name -- String
         """
        with self.conn:
            self.c.execute("DELETE FROM category WHERE id IN (?,?,?,?) ", (1,2,3,4))
            return True
    def delete_all_category(self):
        """Delete ALL  Category values from Database
         """
        with self.conn:
            self.c.execute("DELETE  FROM category WHERE  cat_name <> ? ",("adiddass",))
            return True
    def add_classification_column(self):
        with self.conn:
        # Ajouter la colonne
             self.c.execute("""
          ALTER TABLE category ADD COLUMN nom_classification
        """)
    def update_category_classification(self, nom_classification,cat_name):
        """UPDATE classification value in Database
        Key Arguments: nom_classification -- String
        """
        with self.conn:
            self.c.execute("UPDATE category SET nom_classification = ? WHERE cat_name = ?", (nom_classification,cat_name))
            return True
    def get_categories_and_classifications(self):
        """Fetches all Categories from Database
        Key Arguments: None
        """
        with self.conn:
            self.c.execute("SELECT * FROM category")
            result = self.c.fetchall()
            # print(result)
            return result

    def get_classifications(self):
        """Fetches all nom_classification from Database
        Key Arguments: None
        """
        with self.conn:
            self.c.execute("SELECT DISTINCT nom_classification FROM category")
            result = self.c.fetchall()
            # print(result)
            return result
    def get_classifications_count(self):
        """Fetches all nom_classification from Database
        Key Arguments: None
        """
        with self.conn:
            self.c.execute("SELECT  count(DISTINCT nom_classification) FROM category")
            result = self.c.fetchall()
            # print(result)
            return result
    
    def delete_classification(self, nom_classification):
        """Delete nom_classification value in Database
        Key Arguments: nom_classification -- String
         """
        with self.conn:
            self.c.execute("DELETE FROM category WHERE nom_classification = ?", (nom_classification,))
            return True
    def search_classification(self, nom_classification):
        """search for Classification name from Database
        Key Arguments: None
         """
        with self.conn:
            self.c.execute("SELECT * FROM category WHERE nom_classification = ?", (nom_classification,))
            result = self.c.fetchone()
            #print(result)
            return result

    #======================== SUB-CATEGORY TABLE =====================================#

    def create_sub_category_table(self):
        with self.conn:
            self.c.execute("""CREATE TABLE sub_category (
                sub_cat_name TEXT PRIMARY KEY  NOT NULL,
                cat_name TEXT NOT NULL,
                FOREIGN KEY(cat_name) REFERENCES category(cat_name)
            )""")
    
    def insert_sub_category(self, sub_cat_name, cat_name):
        """Insert Sub-Category value in Database
        Key Arguments: sub_cat_name -- String
                    cat_name -- String
        """
        with self.conn:
            self.c.execute("INSERT INTO sub_category VALUES (?,?)", (sub_cat_name, cat_name,))
            return True 
    def update_sub_category(self, new_subcat_name, old_subcat_name):
        """Update Sub-Category name in Database
        Key Arguments: new_subcat_name -- String
                       old_subcat_name -- String
        """
        with self.conn:
            self.c.execute("UPDATE sub_category SET sub_cat_name = ? WHERE sub_cat_name = ?", (new_subcat_name, old_subcat_name))

    def delete_sub_category(self, cat_name):
        """Delete Category value in Database
        Key Arguments: cat_name -- String
         """
        with self.conn:
            self.c.execute("DELETE FROM sub_category WHERE cat_name = ?", (cat_name,))
            return True
    def delete_sub_categorie(self, sub_cat_name):
        """Delete sub_category value from Database
        Key Arguments: cat_name -- String
         """
        with self.conn:
            self.c.execute("DELETE FROM sub_category WHERE sub_cat_name = ?", (sub_cat_name,))
            return True
    def search_sub_category(self,sub_cat_name):
        """search for sub_category name from Database
        Key Arguments: None
         """
        with self.conn:
            self.c.execute("SELECT * FROM sub_category WHERE sub_cat_name = ?", (sub_cat_name,))
            result = self.c.fetchall()
            # print(result)
            return result
    def get_sub_category(self, category_name):
        """Fetches all Category name from Database
        Key Arguments: category_name -- String
         """
        with self.conn:
            self.c.execute("SELECT * FROM sub_category WHERE cat_name LIKE (?)",(category_name,))
            result = self.c.fetchall()
            # print(result)
            return result
    def get_sub_categorie(self, sub_cat_name):
        """Fetches all Category name from Database
        Key Arguments: category_name -- String
         """
        with self.conn:
            self.c.execute("SELECT * FROM sub_category WHERE sub_cat_name LIKE (?)",(sub_cat_name,))
            result = self.c.fetchall()
            # print(result)
            return result
    def sub_category_count(self,categorie):
        """returns the number of sub_categories"""
        with self.conn:
            self.c.execute("SELECT count(*) FROM sub_category WHERE cat_name=?",(categorie,))
            result = self.c.fetchone()
            return result
   #======================== PRODUCT TABLE =====================================#

    def create_product_table(self):
       with self.conn:
           self.c.execute("""CREATE TABLE product (
               Reference TEXT  PRIMARY KEY  NOT NULL,
               prod_name TEXT  NOT NULL,
               description TEXT NOT NULL,
               prod_quantity_STOCK INTEGER  NOT NULL,
               sub_cat_name TEXT  NOT NULL,
               cat_name TEXT NOT NULL,
               poids TEXT  NOT NULL,
               taille INTEGER  NOT NULL,
               nom_classification TEXT  NOT NULL,
               FOREIGN KEY(sub_cat_name) REFERENCES sub_category(sub_cat_name)
               FOREIGN KEY(cat_name) REFERENCES category(cat_name)
           )""")

    def insert_product(self, Reference,prod_name, description, prod_quantity_STOCK, sub_cat_name, cat_name,poids,taille,nom_classification):
        """Insert Product value in Database
        Key Arguments: prod_name -- String,
                       Reference -- String, prod_quantity_stock-- Int,
                       sub_cat_name--String, cat_name--String.
                       poids -- String , taille --float
        """
        with self.conn:
            self.c.execute("""INSERT INTO product (Reference,prod_name, description, prod_quantity_STOCK, sub_cat_name, cat_name,poids,taille,nom_classification)VALUES (?,?,?,?,?,?,?,?,?)""",(Reference,prod_name, description, prod_quantity_STOCK, sub_cat_name, cat_name,poids,taille,nom_classification))

   
    def update_product_quantity(self, prod_quantity_STOCK, Reference):
        """Update Product price in Database
        Key Arguments: prod_quantity_STOCK -- Int
                       Reference -- String
        """
        with self.conn:
            self.c.execute("UPDATE product SET prod_quantity_STOCK=? WHERE Reference=?", (prod_quantity_STOCK, Reference))

    # Add Amount from Backup Product Table
    def update_add_product_quantity(self, add_prod_quantity, Reference):
        """Add Product Quantity in Database
        Key Arguments: prod_quantity_stock -- Int
                       Reference -- String
        """
        with self.conn:
            self.c.execute("UPDATE product SET prod_quantity_STOCK = prod_quantity_STOCK + ? WHERE Reference=?", (add_prod_quantity, Reference))
            return True
    # Minus Amount from Backup Product Table
    def update_deduct_product_quantity(self, deduct_prod_quantity, Reference):
        """Deduct/Minus Product Quantity in Database
        Key Arguments: prod_quantity_stock-- Int
                       Reference -- String
        """
        with self.conn:
            self.c.execute("UPDATE product SET prod_quantity_STOCK = prod_quantity_STOCK - ? WHERE Reference=?", (deduct_prod_quantity, Reference))    

    # Delete product from Product table            
    def delete_product(self, Reference):
        """Delete Product value in Database
        Key Arguments: Reference -- String
        """
        with self.conn:
            self.c.execute("DELETE FROM product WHERE Reference = (?)",(Reference,))
            return True
    def get_products_by_sub_cat(self, sub_category_name):
        """Fetches set/group of Product values which has a common Sub-Category
        Key Arguments: sub_category_name -- String
        """
        with self.conn:
            self.c.execute("SELECT * FROM product WHERE sub_cat_name=(?)",(sub_category_name,))
            result = self.c.fetchall()
            return result
    
    def get_products_by_cat(self, category_name):
        """Fetches set/group of Product values which has a common Category
        Key Arguments: category_name -- String
        """
        with self.conn:
            self.c.execute("SELECT * FROM product WHERE cat_name=(?)",(category_name,))
            result = self.c.fetchall()
            return result
    
    def get_product_details(self, Reference):
        """Fetches all Product info/values of a single product.
        Key Arguments: Reference -- String
        """
        with self.conn:
            self.c.execute("SELECT * FROM product WHERE Reference LIKE (?)",(Reference,))
            result = self.c.fetchall()
            return result
    def show_products(self):
        """Fetches all Product info/values.
        """
        with self.conn:
            self.c.execute("SELECT * FROM product")
            result = self.c.fetchall()
            return result

    def get_products_details(self,sub_cat_name):
        """Fetches all Product info/values of a all products.
        Key Arguments: 
        """
        with self.conn:
            self.c.execute("SELECT * FROM product WHERE sub_cat_name=(?)",(sub_cat_name,))
            result = self.c.fetchall()
            return result
    def get_products(self):
        """Fetches all Product info/values of a all products.
        Key Arguments: 
        """
        with self.conn:
            self.c.execute("SELECT Reference,prod_quantity_stock FROM product ")
            result = self.c.fetchall()
            return result
    def get_poids(self,Reference):
        """returnns product poids
        Key Arguments: 
        Reference -- String
        """
        with self.conn:
            self.c.execute("SELECT poids FROM product where Reference=?",(Reference,))
            result = self.c.fetchone()
            return result

    def product_count(self):
        """returns the number of products"""
        with self.conn:
            self.c.execute("SELECT count(*) FROM product")
            result = self.c.fetchone()
            return result
    def product_quantity(self):
        """returns the global stock"""
        with self.conn:
            self.c.execute("SELECT sum(prod_quantity_STOCK) FROM product")
            result = self.c.fetchone()
            return result
    def add_classification_column_product(self):
        with self.conn:
        # Ajouter la colonne
             self.c.execute("""
          ALTER TABLE product ADD COLUMN nom_classification
        """)
    def get_product_references(self):
        """returns product references"""
        with self.conn:
            self.c.execute("SELECT Reference FROM product")
            result = self.c.fetchall()
            return result
    
    def get_product_quantity(self,Reference):
        """returns product references"""
        with self.conn:
            self.c.execute("SELECT prod_quantity_STOCK FROM product where Reference=?",(Reference,))
            result = self.c.fetchone()
            return result
    #============================= BACKUP REPLICA TABLE ==============================================#

    def create_replica(self):
        """Creates a duplicate/replica of local disk Database to temp Memory Database.
        Volatile Database.
        Implemented To prevent data loss when force close.
        Key Arguments: None
        """
        # Create a Backup db in memory and copying 
        self.bak_db = sqlite3.connect(':memory:')

        # Copying data to bak.db
        queries = "".join(line for line in self.conn.iterdump())
        # print(queries)
        self.bak_db.executescript(queries)
        # print(self.bak_db)
        
        # Create cursor for bakup db
        self.bak_c = self.bak_db.cursor()
    
    def get_bak_prod_details(self, Reference):
        """Fetches all Product info/values of a single product from the Temporary in Memory Db.
        Key Arguments: Reference -- String
        """
        with self.bak_db:
            self.bak_c.execute("SELECT * FROM product WHERE Reference LIKE (?)",(Reference,))
            result = self.bak_c.fetchall()
            # print(result)
            return result

    # Add Amount from Backup Product Table
    def update_add_bak_prod_quantity(self, add_prod_quantity, Reference):
        """Add Product Quantity in temporary in memory Database
        Key Arguments: prod_quantity_stock -- Int
                       Reference -- String
        """
        with self.bak_db:
            self.bak_c.execute("UPDATE product SET prod_quantity_stock = prod_quantity_stock + ? WHERE Reference=?", (add_prod_quantity, Reference))

    # Minus Amount from Backup Product Table
    def update_deduct_bak_prod_quantity(self, deduct_prod_quantity, Reference):
        """Deduct Product Quantity in temporary in memory Database
        Key Arguments: prod_quantity_stock -- Int
                       Reference -- String
        """
        with self.bak_db:
            self.bak_c.execute("UPDATE product SET prod_quantity_stock = prod_quantity_stock - ? WHERE Reference=?", (deduct_prod_quantity, Reference))
 
 #=============================  Table de facture  ==============================================#
    
    def create_facture_table(self):
       with self.conn:
           self.c.execute("""
                  CREATE TABLE facture (
                  id_facture INTEGER PRIMARY KEY AUTOINCREMENT,
                  description_facture TEXT,
                  date_facture TEXT
                          )""")

    def insert_facture(self, date_facture,description_facture):
        """Insert facture value in Database
        Key Arguments: id_facture -- int
                   date_facture -- String 
        """
        with self.conn:
           self.c.execute("INSERT INTO facture (description_facture,date_facture) VALUES (?,?)", (description_facture,date_facture))
        return self.c.lastrowid  # Récupère l'ID de la dernière facture insérée

   
    def update_date_facture(self,old_date_facture,new_date_facture):
        """Update facture quantity in Database
        Key Arguments: date_facture -- String
        id_facture -- int
        """
        with self.conn:
            self.c.execute("UPDATE facture SET date_facture=? WHERE date_facture=?", (new_date_facture,old_date_facture )) 

    # Delete from facture table            
    def delete_facture(self, id_facture):
        """Delete facture value in Database
        Key Arguments: id_facture -- int
        """
        with self.conn:
            self.c.execute("DELETE FROM facture WHERE id_facture = (?)",(id_facture,))    #id_facture doit etre determine a partir d'une fonction get_id_facture()
            return True
    # get facture details
    def get_facture_details(self):
        """Fetches all facture info/values.
        """
        with self.conn:
            self.c.execute("SELECT * FROM facture ") 
            result = self.c.fetchall()
            return result
    
    # get facture details
    def get_facture(self,id_facture):
        """Fetches all facture info/values.
        """
        with self.conn:
            self.c.execute("SELECT * FROM facture  WHERE  id_facture=?",(id_facture,)) 
            result = self.c.fetchall()
            return result
    def get_facture_dates(self):
        """fetches all facture dates"""
        with self.conn:
            self.c.execute("SELECT date_facture FROM facture ORDER BY date_facture DESC LIMIT 4 ") 
            result = self.c.fetchall()
            return result
    def facture_count(self):
        """fetches the number of factures"""
        with self.conn:
            self.c.execute("SELECT count(*) FROM facture ") 
            result = self.c.fetchone()
            return result

 #====================== classification =====================================#
    def create_classification_table(self):
       with self.conn:
           self.c.execute("""CREATE TABLE classification (
               id_classification INTEGER  PRIMARY KEY  AUTOINCREMENT,
               nom_classification TEXT NOT NULL
           )""")

    
    def insert_classification(self, nom_classification):
        """Insert classification value in Database
        Key Arguments: id_classification -- INT
                    nom_classification -- String
        """
        with self.conn:
            self.c.execute("INSERT INTO classification (nom_classification) VALUES (?)", (nom_classification,))
    
    def get_classification(self, nom_classification):
        """Fetches all classification name from Database
        Key Arguments: nom_classification -- String
         """
        with self.conn:
            self.c.execute("SELECT * FROM classification WHERE nom_classification LIKE (?)",(nom_classification,))
            result = self.c.fetchall()
            print(result)
            #return result
    def add_classification_reference(self):
        with self.conn:
        # Ajouter la colonne
             self.c.execute("""
          ALTER TABLE category DROP COLUMN nom_classification
        """)
        
       
    

 #=============================  Table de vente  ==============================================#
    
    def create_vente_table(self):
       with self.conn:
           self.c.execute("""CREATE TABLE vente (
               id_vente INTEGER  PRIMARY KEY  AUTOINCREMENT,
               quantite_vendue INTEGER NOT NULL,
               Reference TEXT NOT NULL,  
               id_facture INTEGER ,                                            
               FOREIGN KEY(Reference) REFERENCES product(Reference)
               FOREIGN KEY(id_facture) REFERENCES facture(id_facture)
           )""")

    def insert_vente(self, quantite_vendue, Reference, id_facture):
        """Insert vente value in Database
        Key Arguments: id_vente --int ,
                   quantite_vendue -- int,
                   Reference -- String,  
                   id_facture -- int ,
        """
        with self.conn:
            # Insérer la vente avec l'ID de la facture associée
            self.c.execute("INSERT INTO vente (quantite_vendue, Reference, id_facture) VALUES (?,?,?)",
                       (quantite_vendue, Reference, id_facture))
            self.c.execute("UPDATE product SET description=? WHERE Reference=?",("vendu",Reference,))

   
    def update_vente_quantity(self, quantite_vendue, id_vente):
        """Update vente quantity in Database
        Key Arguments: quantite_vendue -- int
        id_vente -- int
        """
        with self.conn:
            self.c.execute("UPDATE vente SET quantite_vendue=? WHERE id_vente=?", (quantite_vendue,id_vente )) #id_vente doit etre determine a partir d'une fonction get_id_vente()

    # Add Amount from Backup vente Table
    def update_add_vente_quantity(self, add_vente_quantity,id_vente ):
        """Add vente Quantity in Database
        Key Arguments: quantite_vendue -- Int
                       id_vente  -- String
        """
        with self.conn:
            self.c.execute("UPDATE vente SET quantite_vendue = quantite_vendue + ? WHERE id_vente=?", (add_vente_quantity, id_vente))

    # Minus Amount from Backup Product Table
    def update_deduct_vente_quantity(self, deduct_vente_quantity, id_vente):
        """Deduct/Minus vente Quantity in Database
        Key Arguments: quantite_vendue-- Int
                       id_vente -- int
        """
        with self.conn:
            self.c.execute("UPDATE vente SET quantite_vendue = quantite_vendue - ? WHERE id_vente=?", (deduct_vente_quantity, id_vente))    

    # Delete from vente table            
    def delete_vente(self, id_vente):
        """Delete vente value in Database
        Key Arguments: id_vente -- int
        """
        with self.conn:
            self.c.execute("DELETE FROM vente WHERE id_vente = (?)",(id_vente,))
            return True
    # get vente details
    def get_vente_details(self, id_vente):
        """Fetches all vente info/values.
        Key Arguments: id_vente -- int
        """
        with self.conn:
            self.c.execute("SELECT * FROM vente WHERE id_vente = (?) ",(id_vente,))
            result = self.c.fetchall()
            return result
    def get_ventes_details(self):
        """Fetches all vente info/values.
        Key Arguments: id_vente -- int
        """
        with self.conn:
            self.c.execute("SELECT * FROM vente ")
            result = self.c.fetchall()
            return result  
    def vente_count(self):
        """returns the number of vente.
        """
        with self.conn:
            self.c.execute("select count(*) from vente")
            result = self.c.fetchone()
            return result
    def get_products_vente(self):
        """returns the reference of products from vente.
        """
        with self.conn:
            self.c.execute("select Reference from vente")
            result = self.c.fetchall()
            return result
#=============================  Table de commande ==============================================#
    def create_commande_table(self):
        with self.conn:
            self.c.execute("""
                  CREATE TABLE commande(
                  id_commande INTEGER PRIMARY KEY AUTOINCREMENT,
                  description_commande TEXT,
                  date_commande TEXT
                           )""")

    def insert_commande(self, description_commande,date_commande):
        """Insert facture value in Database
        Key Arguments: id_commande -- int
                   date_commande -- String 
                   description_commande --String
        """
        with self.conn:
           self.c.execute("INSERT INTO commande (description_commande,date_commande) VALUES (?,?)", (description_commande,date_commande))
        return self.c.lastrowid  # Récupère l'ID de la dernière commande insérée

   
    def update_date_commande(self,old_date_commande,new_date_commande):
        """Update commande quantity in Database
        Key Arguments: date_commande -- String
        id_commande -- int
        """
        with self.conn:
            self.c.execute("UPDATE commande SET date_commande=? WHERE date_commande=?", (new_date_commande,old_date_commande )) 

    # Delete from commande table            
    def delete_commande(self, id_commande):
        """Delete commande value in Database
        Key Arguments: id_commande -- int
        """
        with self.conn:
            self.c.execute("DELETE FROM commande WHERE id_commande = (?)",(id_commande,))    #id_commande doit etre determine a partir d'une fonction get_id_commande()
            return True
    # get commande details
    def get_commande_details(self):
        """Fetches all commande info/values.
        """
        with self.conn:
            self.c.execute("SELECT * FROM commande ") 
            result = self.c.fetchall()
            return result

    def get_commande_dates(self):
        """get commandes dates details."""

        with self.conn:
            self.c.execute("SELECT date_commande FROM commande ORDER BY date_commande DESC LIMIT 4") 
            result = self.c.fetchall()
            return result
    def commande_count(self):
        """get commandes number """

        with self.conn:
            self.c.execute("SELECT count(*) FROM commande ") 
            result = self.c.fetchone()
            return result
    def get_commande(self,id_commande):
        """get commande """

        with self.conn:
            self.c.execute("SELECT * FROM commande WHERE id_commande=? ",(id_commande,)) 
            result = self.c.fetchall()
            return result

#=============================  Table d'achat  ==============================================#
    
    def create_achat_table(self):
       with self.conn:
           self.c.execute("""CREATE TABLE achat (
               id_achat INTEGER  PRIMARY KEY  AUTOINCREMENT,
               quantite_demandee INTEGER NOT NULL,
               Reference TEXT NOT NULL,  
               id_commande INTEGER ,                                            
               FOREIGN KEY(Reference) REFERENCES product(Reference)
               FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
           )""")

    def insert_achat(self, quantite_demandee, Reference,id_commande):
        """Insert vente value in Database
        Key Arguments: id_achat --int 
                       quantite_demandee -- int
                       Reference -- String,  
                       id_commande -- int
        """
        with self.conn:
            # Insérer l'achat avec l'ID de la commande associée
            self.c.execute("""INSERT INTO achat (quantite_demandee, Reference, id_commande)
                VALUES (?,?,?)""",(quantite_demandee, Reference, id_commande)) 

   
    def update_achat_quantity(self, quantite_demandee, id_achat):
        """Update achat quantity in Database
        Key Arguments: quantite_demandee -- int
        id_achat -- int
        """
        with self.conn:
            self.c.execute("UPDATE achat SET quantite_demandee=? WHERE id_achat=?", (quantite_demandee,id_achat )) #id_achat doit etre determine a partir d'une fonction get_id_achat()

    # Add Amount from Backup achat Table
    def update_add_achat_quantity(self, add_achat_quantity,id_achat ):
        """Add achat  Quantity in Database
        Key Arguments: quantite_demandee -- Int
                       id_achat  -- int
        """
        with self.conn:
            self.c.execute("UPDATE achat SET quantite_demandee = quantite_demandee + ? WHERE id_achat=?", (add_achat_quantity, id_achat)) # id_achat doit etre determine par une fonction get_id_achat()

    # Minus Amount from Backup achat Table
    def update_deduct_achat_quantity(self, deduct_achat_quantity, id_achat):
        """Deduct/Minus achat Quantity in Database
        Key Arguments: quantite_demandee-- Int
                       id_achat -- int
        """
        with self.conn:
            self.c.execute("UPDATE achat SET quantite_demandee = quantite_demandee - ? WHERE id_achat=?", (deduct_achat_quantity, id_achat))    

    # Delete from achat table            
    def delete_achat(self, id_achat):
        """Delete achat value in Database
        Key Arguments: id_achat -- int
        """
        with self.conn:
            self.c.execute("DELETE FROM achat WHERE id_achat = (?)",(id_achat,))
            return True
    # get achat details
    def get_achat_details(self, id_achat):
        """Fetches all achat info/values.
        Key Arguments: id_achat -- int
        """
        with self.conn:
            self.c.execute("SELECT * FROM achat WHERE id_achat = (?) ",(id_achat,))
            result = self.c.fetchall()
            return result
    def get_achats_details(self):
        """Fetches all achat info/values.
        Key Arguments: id_achat -- int
        """
        with self.conn:
            self.c.execute("SELECT * FROM achat")
            result = self.c.fetchall()
            return result
    def achat_count(self):
        """returns the number of achat.
        """
        with self.conn:
            self.c.execute("select count(*) from achat")
            result = self.c.fetchone()
            return result

    def get_products_achat(self):
        """returns the reference of products from achat.
        """
        with self.conn:
            self.c.execute("select Reference from achat")
            result = self.c.fetchall()
            return result


#=============================  Table de  stock  ==============================================#
    def create_stock_table(self):
       with self.conn:
           self.c.execute("""CREATE TABLE stock (
               id_stock INTEGER  PRIMARY KEY  AUTOINCREMENT,
            stock_minimal INTEGER NOT NULL,
            envoi TEXT NOT NULL
             
           )""")
    def insert_stock(self, stock_minimal):
        
        with self.conn:
            # Insérer le button
            self.c.execute("""INSERT INTO stock(stock_minimal)  VALUES (?)""",(stock_minimal,))
    def get_stock(self):
       
        with self.conn:
            self.c.execute("SELECT stock_minimal FROM stock WHERE id_stock=2")
            result = self.c.fetchone()
            return result
    def delete_stock(self):
       
        with self.conn:
            self.c.execute("DELETE FROM stock WHERE id_stock=2")
    def change_stock(self,stock_minimal):
        with self.conn:
            self.c.execute("UPDATE stock set envoi=? WHERE id_stock=2",(None,))
            self.c.execute("UPDATE stock set stock_minimal=? WHERE id_stock=2",(stock_minimal,))
            result = self.c.fetchone()
            return result
    def add_column_stock(self):
        with self.conn:
        # Ajouter la colonne
             self.c.execute("""
          ALTER TABLE stock ADD COLUMN envoi
        """)
    def update_envoi(self,envoi):
        with self.conn:
             self.c.execute("UPDATE stock set envoi=? WHERE id_stock=2",(envoi,))
    def get_envoi(self):
        with self.conn:
             self.c.execute("SELECT envoi FROM stock WHERE id_stock=2")
             result = self.c.fetchone()
             return result

#=============================  Table de  buttons  ==============================================#
    def create_button_table(self):
       with self.conn:
           self.c.execute("""CREATE TABLE button (
               id_button INTEGER  PRIMARY KEY  AUTOINCREMENT,
               row INTEGER NOT NULL
               
           )""")
    def insert_button(self, row):
        """Insert row value in Database
        Key Arguments: id_button --int 
                       row -- int             
        """
        with self.conn:
            # Insérer le button
            self.c.execute("""INSERT INTO button (row) VALUES (?)""",(row,)) 
    def get_button(self):
        """Fetches all button info/values.
        Key Arguments: id_button -- int
        """
        with self.conn:
            self.c.execute("SELECT * FROM button ORDER BY row DESC LIMIT 1")
            result = self.c.fetchone()
            return result

############################################################################################################################################

    def drop_table(self, table_name):
        """Drops given table from the Database.
        Key Arguments: table_name -- String
        """
        with self.conn:
            self.c.execute(f"DROP TABLE {table_name}")



def verifier_installation():
    if table_existe('login') and table_existe('Sign_UP') and table_existe('Remember') and table_existe('theme') and table_existe('category') and table_existe('sub_category') and table_existe('product') and table_existe('facture') and  table_existe('vente') and  table_existe('commande') and  table_existe('achat') and table_existe('stock'):
       return True
    else:
        return False
def create_database():
    db_obj = Database()
    db_obj.create_achat_table()
    db_obj.create_category_table()
    db_obj.create_commande_table()
    db_obj.create_facture_table()
    db_obj.create_login_table()
    db_obj.create_product_table()
    db_obj.create_Remember_table()
    db_obj.create_replica()
    db_obj.create_signup_table()
    db_obj.create_sub_category_table()
    db_obj.create_theme_table()
    db_obj.create_vente_table()
    db_obj.create_stock_table()
# Fonction pour vérifier si une table existe
def table_existe(table_name):
    # Connexion à la base de données
    conn = sqlite3.connect(resource_path("MODEL\\Database.db"))

    
    # Création d'un curseur
    cursor = conn.cursor()
    
    # Vérification de l'existence de la table
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    
    # Récupération du résultat
    table = cursor.fetchone()
    
    # Fermeture de la connexion
    conn.close()
    
    # Si la table existe, table contiendra le nom de la table, sinon il sera None
    return table is not None

# Exemple d'utilisation

if __name__ == "__main__":

    verifier_installation()
    db_obj = Database()
    #=================== LOGIN ===============================#
    # # Creating login table
    #db_obj.create_login_table()
    
    # # Inserting to login table
    #db_obj.insert_login_table("NAJMmA","TAHIRI")
    
    # # Changing Password
    # new_password = "ufxx|twi"
    """new_password = "password"
    db_obj.change_password(new_password)"""
    
    # # Fetch Login Data
    """result = db_obj.get_login_data()
    print(result)
    print("ID :", result[0])
    print("USERNAME :", result[1])
    print("PASSSWORD :", result[2])
    """
    #=================== SIGNUP ===============================#
    # # Creating SIGNUP table
    #db_obj.create_signup_table()
    #db_obj.insert_signup_table("ahmad","mohssin","ahmad@gmail.com","P123456","0623456789","sara")
    #print(db_obj.get_signup_data()[len(db_obj.get_signup_data())-1][1],(db_obj.get_signup_data()[len(db_obj.get_signup_data())-1][6]))
    #db_obj.delete_Signup()
    #print(db_obj.searchSignup("ahmad","momo"))
    #print(db_obj.get_signup_data())
    #=================== REMEMBER ===============================#
    # # Creating REMEMBER table
    #db_obj.create_Remember_table()
    #db_obj.insert_Remember_table()
    #print(db_obj.get_Remember_data())
    #db_obj.delete_remember_data()

    #====================== THEME =====================================#
    # # Creating theme table
    # db_obj.create_theme_table()
    
    # # Insert to theme table
    # db_obj.insert_theme_table()

    # # Fetching theme data
    # result = db_obj.get_theme_value()
    # print("Theme Value :", result[1])

    # # Changing theme
    # db_obj.change_theme("Light Mode")
    #====================== THEME =====================================#
    # # Creating button table
    #db_obj.create_button_table()
    #db_obj.insert_button(4)
    #print(db_obj.get_button()[1])
    #====================== classification =====================================#
    #db_obj.create_classification_table()
    #db_obj.insert_classification("Les chaussures")
    #db_obj.get_classification("Les chaussures")
    #db_obj.add_classification_reference()
    #====================== Category =====================================#
    # # Creating category table
    # db_obj.create_category_table()
    
    # # Insert to Category table
    #db_obj.insert_category("adiddass")
    # try:
    #     db_obj.insert_category(cat_name=None)
    # except sqlite3.Error as e:
    #     print(e," <= CATEGORY TABLE")
        # if e.args[0].startswith('UNIQUE constraint failed:'):
        #     print("yes")
        # else:
        #     print("No")

    # # Update Category item value
    #db_obj.update_category(new_cat_name="adiddass", old_cat_name="equipement de protection")

    # # Deleting from Category table
    #db_obj.delete_category("")
    
    # # Fetch from Category table
    #print(db_obj.get_category_by_classification_name("Les gants"))
    #print(db_obj.get_category()[1][0])
    #print(db_obj.category_count()[0])
    #db_obj.delete_category_by_id()
    ##################################
    #db_obj.insert_category("All flex","Les gants")
    #db_obj.insert_category("Sjntrile","Les gants")
    ##################################
    #db_obj.add_classification_column()
    #db_obj.insert_category_classification("Les chaussures","Cador")
    #db_obj.insert_category_classification("Les chaussures","Fitz")
    #db_obj.insert_category_classification("Les chaussures","Safety run")
    #db_obj.insert_category_classification("Les chaussures","Yukon")
    #db_obj.insert_category_classification("Les chaussures","Manager")
    #db_obj.insert_category_classification("Nike","Morris")
    #db_obj.insert_category_classification("Nikee","Morris")
    #db_obj.insert_category("momo","solo")
    #db_obj.insert_category("cat2","class2")
    #db_obj.insert_category("cat3","class3")
    #################################
    #db_obj.delete_category("A")
    #db_obj.delete_category("ADIDASS")
    #db_obj.delete_category("momo")
    #db_obj.delete_category("cat2")
    #db_obj.delete_category("")
    #db_obj.get_sub_category()
    #print(db_obj.sub_category_count("Cador"))
    """db_obj.delete_category("LA VESTES")
    db_obj.delete_category("LES CHAUSSETES")
    db_obj.delete_category("LES CHAUSSET")
    db_obj.delete_category("AAA")"""
    #print(db_obj.get_category_by_classification_name("Les chaussures"))
    """db_obj.delete_category("Fitz")
    db_obj.delete_category("Safety run")
    db_obj.delete_category("Yukon")
    db_obj.delete_category("Morris")
    db_obj.delete_category("All flex")
    db_obj.delete_category("Sjntrile")"""
    """db_obj.delete_category("cador")"""
    #print(db_obj.search_category("Cador"))
    #print(db_obj.get_category_by_classification_name("class3"))
    #db_obj.delete_all_category()
    #print(db_obj.get_classification_name(""))
    #====================== Sub-Category =====================================#
    # # Creating sub category table
    # db_obj.create_sub_category_table()

    # # Insert to Sub category table
    """try:
        db_obj.insert_sub_category(sub_cat_name="cador", cat_name="adiddass")
    except sqlite3.Error as er:
        print(er)"""

    # # Update Sub-Category item value
    #db_obj.update_sub_category(new_subcat_name="cadoor", old_subcat_name="cador")

    # # Deleting from Sub-Category table
    #db_obj.delete_sub_category(sub_cat_name="sss")
    #db_obj.delete_sub_category("")

    # # Fetching Sub cat values
    # print(db_obj.get_sub_category('%'))
    #print(db_obj.sub_category_count("Cador"))
   
    #====================== Products =====================================#
    # # Creating Products table
    #db_obj.create_product_table()

    # # Insert to products table
    #db_obj.insert_product("AbCxz2345", "Chaussure noir", "new_version", 200, "cador","adiddass","70 g",40) #Reference,prod_name, description, prod_quantity_STOCK, sub_cat_name, cat_name,poids,taille
    
    # # Updating product price
    # db_obj.update_product_price(prod_price=97, prod_name="Fair & Lovely Women, 50g")

    # # Updating product quantity 
    #db_obj.update_product_quantity(prod_quantity_STOCK=500,Reference="AbCxy2345") 

    # # Adding to the Backup product table quantity
    # db_obj.update_add_product_quantity(add_prod_quantity=60, Reference="AbCxy2345")

    # # Deduct from backup product table quantity
    # db_obj.update_deduct_product_quantity(deduct_prod_quantity=10, Reference="AbCxy2345")
    
    # # Delete a product from product table
    #db_obj.delete_product(Reference="")
    #db_obj.delete_product(Reference="produit3")

    #print(db_obj.delete_product(Reference="produit4"))
    
    # # Get all products list with help os sub cat name
    # print(db_obj.get_products('Hair'))
    
    # Get all products Details list
    #print(db_obj.get_products()[0][1]+1)
    #print(db_obj.get_products_details(""))
    #====================== FACTURE =====================================#
    # CREATING FACTURE TABLE
    #db_obj.create_facture_table()  
    #db_obj.drop_table("facture")

    # inserting in facture Table
    #db_obj.insert_facture("2024-01-01","facture1") 
    #db_obj.insert_facture("2024-01-02","facture12")
    #db_obj.insert_facture("2024-01-03","facture13") 
    #db_obj.insert_facture("2024-01-04","facture14")  
    
    #update date_facture in facture table
    #db_obj.update_date_facture("2024/01/01","2024/01/11")
    
    #delete facture
    #db_obj.delete_facture(13)
    #db_obj.delete_facture(14)
    #db_obj.delete_facture(15)
    #db_obj.delete_facture(16)
    
    #get facture details.
    #print(db_obj.get_facture_dates())
    #print(db_obj.get_commande_dates())
    
    #====================== vente =====================================#
    #create vente table
    #db_obj.create_vente_table()
    
    #insert vente data
    #db_obj.insert_vente(50,"AbCxy2345","2024/01/02","facture2") 
    
    #update vente
    #db_obj.update_vente_quantity(60,1)
    
    #get vente details
    #print(db_obj.get_vente_details(1))
    
    #delete vente
    #db_obj.delete_vente(6)
    #====================== stock =====================================#
    #db_obj.create_stock_table()
    #db_obj.insert_stock(20)
    #db_obj.change_stock(30)
    #db_obj.update_envoi("oui")
    #db_obj.change_stock(12)
    #====================== commande =====================================#
    #create commande table
    #db_obj.create_commande_table()

    #insert in commande table
    #db_obj.insert_commande("commande1","2024/02/01")
    
    #update date commande
    #db_obj.update_date_commande("2024/02/01","2024/03/02")
    
    #delete commande
    #db_obj.delete_commande(4)
    #db_obj.delete_commande(5)
    
 
    #get_commande_details
    #print(db_obj.get_commande_details())
    #====================== achat =====================================#
    #create achat table
    #db_obj.create_achat_table()
 
    #insert in achat table
    #db_obj.insert_achat(50,"AbCxy2345",2,"commande1")

    # update achat quantity
    #db_obj.update_achat_quantity(40,1)

    #delete  from achat
    #db_obj.delete_achat(2)
    #db_obj.delete_achat(3)
    #get achat details
    #print(db_obj.get_achat_details(1))

    #====================== BACKUP REPLICA TABLE =====================================#
    # # Getting backup product details
    #db_obj.create_replica()
    #print(db_obj.get_bak_prod_details('%'))

    # # Adding to the Backup product table quantity
    #db_obj.update_add_bak_prod_quantity(add_prod_quantity=10, Reference="AbCxy2345")
    #print(db_obj.get_bak_prod_details('AbCxy2345'))

    # # Deduct from backup product table quantity
    # db_obj.update_deduct_bak_prod_quantity(deduct_prod_quantity=10, Reference="AbCxy2345")
    # print(db_obj.get_bak_prod_details('AbCxy2345'))


    #===========================================================#
    # Drop a table
    #db_obj.drop_table("strock")
    
    # prod = "nprod"
    # scat = "cat2"
    # cat = "cat1"
    
    # db_obj.delete_product(prod)
    # db_obj.delete_sub_category(scat)
    # db_obj.delete_category(cat)
"""conn = sqlite3.connect("MODEL/Database.db")
def has_foreign_key(table_name, column_name, conn):
    c = conn.cursor()
    query = f"PRAGMA foreign_key_list({table_name})"
    c.execute(query)
    foreign_keys = c.fetchall()

    for fk in foreign_keys:
        if fk[3] == column_name:
            return True

    return False
if has_foreign_key("category", "nom_classification", conn):
    print("La table 'category' a une clé étrangère vers 'classification'")
else:
    print("La table 'category' n'a pas de clé étrangère vers 'classification'")"""
