import sys
import os
import getpass

# Obtenez le nom d'utilisateur actuel
current_user = getpass.getuser()
from CONTROLLER import cLogin as cl
from CONTROLLER import cSignup as cS
import customtkinter as ctk
from PIL import ImageTk, Image
import tkinter as tk
from MODEL import DatabaseSetup as db

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class Login:
    def __init__(self):    
        cl.historique('L\'utilisateur a ouvert l\'application')
        self.root = ctk.CTk()
        self.FRAME = None 
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "image1.png")
            # Load the background image
            bg=Image.open(resource_path("images\\image1.png"))
            self.bg1 = ImageTk.PhotoImage(bg)
         
            #self.bg1= ctk.CTkImage(light_image=Image.open("images/image1.png"))
            self.CANVA = ctk.CTkCanvas(self.root, width=700, height=400)
            self.CANVA.create_image(0, 0, image=self.bg1, anchor='nw')
            self.CANVA.pack(fill='both', expand=True)
            #self.CANVA.bind("<Configure>", self.resize_image)
        
            
        
            # Create the main frame with custom width and height
            self.FRAME = ctk.CTkFrame(master=self.CANVA, width=400, height=600,border_width=5,border_color="darkblue",corner_radius=5,bg_color="blue")
            self.FRAME.pack(pady=100, padx=6, anchor='nw')
            self.FRAME.pack_propagate(False) 
            self.FRAME.rowconfigure(0, weight=1)
            self.FRAME.columnconfigure(0, weight=1)
            self.FRAME.size()

            # Add labels, images, and buttons to the frame
            #add a logo image :
            """cript_dir = os.path.dirname(os.path.abspath(__file__))
            image_path1 = os.path.join(script_dir, "logo.png")"""
            self.LOGO=ctk.CTkImage(light_image=Image.open(resource_path("images\\logo.png")),size=(200,50))
            self.ctklabel=ctk.CTkLabel(master=self.FRAME,image=self.LOGO,text="")
            self.ctklabel.image=self.LOGO
            self.ctklabel.pack(padx=5,pady=10,anchor="nw")

            #set a username image
            self.image1= ctk.CTkImage(light_image=Image.open(resource_path("images\\profil2.png")),size=(70, 70))
            self.LABELimage1 = ctk.CTkLabel(master=self.FRAME,image=self.image1,text="")
            self.LABELimage1.image = self.image1
            self.LABELimage1.pack(padx=100,side=tk.TOP)
            # LABELimage1.place(x=85, y=172)
        except Exception as e:
          print("Error loading background image:", e)
        
        if cl.isRememeber()==True:
            result=cl.get_login_data()
            name=result[len(result)-1][1]
            password=result[len(result)-1][6]
            self.E1 = ctk.CTkEntry(master=self.FRAME)
            self.E1.pack(pady=5, padx=10)
            self.E = ctk.CTkEntry(master=self.FRAME ,show="*")
            self.E.pack(pady=10, padx=10)
            self.E1.insert(0,name)
            self.E.insert(0,password)
        else:
            self.E1 = ctk.CTkEntry(master=self.FRAME, placeholder_text="Username")
            self.E1.pack(pady=5, padx=10)
            self.E = ctk.CTkEntry(master=self.FRAME, placeholder_text="Password", show="*")
            self.E.pack(pady=10, padx=10)

        
        #set a password image
        self.image2= ctk.CTkImage(light_image=Image.open(resource_path("images\\image6.png")),size=(13, 13))
        self.LABELimage2 = ctk.CTkLabel(master=self.FRAME,image=self.image2,text="")
        self.LABELimage2.image = self.image2
        self.LABELimage2.place(x=250, y=186)

        self.button1 = ctk.CTkButton(master=self.FRAME, text="login",hover_color="darkblue",command=lambda:cl.Login(self.root,self.E1.get(),self.E.get()))
        self.button1.pack(pady=5, padx=10)

        self.button2 = ctk.CTkButton(master=self.FRAME, text="Sign up",hover_color="darkblue",command=lambda:self.Signup(self.root))
        self.button2.pack(pady=5, padx=10)
        
        # set a checkbox to remember the password
        self.ctklabel=ctk.CTkLabel(master=self.FRAME,text="Remember me",font=("Robot", 13))
        self.ctklabel.pack(pady=0,padx=0)
        self.checkbox1=ctk.CTkCheckBox(master=self.FRAME,checkmark_color="white",text="",width=70,height=18,checkbox_height=18,checkbox_width=18,hover_color="white",command=cl.Remember("oui",self.E1.get(),self.E.get()))
        self.checkbox1.place(x=250,y=302)
        
        # add an other image (company logo):
        self.logo=ctk.CTkImage(light_image=Image.open(resource_path("images\\image9.png")),size=(800,700))
        self.ctklabel=ctk.CTkLabel(master=self.CANVA,image=self.logo,text="")
        self.ctklabel.image=self.logo
        self.ctklabel.place(x=500, y=70)
        
        #add a frame 
        self.frame=ctk.CTkScrollableFrame(master=self.CANVA,width=400,height=300,bg_color="blue",corner_radius=5,border_color="darkblue",border_width=5)
        self.frame.place(x=640,y=220)
        
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        

        # add a window into frame
        self.label2=ctk.CTkLabel(master=self.frame,text_color="WHITE",text="Bienvenue au Gestionnaire de stock \n \n ABOUT:",font=('bold',15))
        self.label2.pack(padx=5,pady=10)

        self.button3=ctk.CTkButton(master=self.frame,hover_color="purple",text="Technical information",command=lambda:self.infos(self.frame,"A"))
        self.button3.pack( padx=10,pady=10,anchor='nw')

        self.button3=ctk.CTkButton(master=self.frame,hover_color="deeppink",text="Materials",command=lambda:self.infos(self.frame,"B"))
        self.button3.pack( padx=10,pady=10,anchor='nw')

        self.button3=ctk.CTkButton(master=self.frame,hover_color="green",text="Developer",command=lambda:self.infos(self.frame,"C"))
        self.button3.pack( padx=10,pady=10,anchor='nw')

        self.button3=ctk.CTkButton(master=self.frame,hover_color="red",text="Company",command=lambda:self.infos(self.frame,"D"))
        self.button3.pack( padx=10,pady=10,anchor='nw')
        
    def resize_image(self, event):
        # Resize the background image with the new width and height
        image = Image.open(resource_path("images\\image1.png"))
        resized = image.resize((event.width, event.height))
        # Update the image on the canvas
        self.CANVA.delete("all")  # Remove previous image
        image2 = ImageTk.PhotoImage(resized)
        self.CANVA.create_image(0, 0, anchor="nw", image=image2)
    def Signup(self,root):
        cl.historique('L\'utilisateur a crier un compte')
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
       
        button = ctk.CTkButton(master=FRAME, text="Soumettre et mémoriser",command=lambda:cS.Signup(FRAME,entry1,entry2,entry3,entry4,entry7,entry8,entry9))
        button.grid(padx=20, pady=50, row=36, column=0)
        button = ctk.CTkButton(master=FRAME, text="Retourner",command=lambda:self.returnToLogin(root))
        button.grid(padx=20, pady=50, row=36, column=1)
        
        # ADD sign up image
        
        
    
    def returnToLogin(self,root):
        cl.historique('BACK')
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

        button1 = ctk.CTkButton(master=FRAME, text="login",hover_color="darkblue",command=lambda:cl.Login(root,E1.get(),E.get()))
        button1.pack(pady=5, padx=10)

        button2 = ctk.CTkButton(master=FRAME, text="Sign up",hover_color="darkblue",command=lambda:self.Signup(root))
        button2.pack(pady=5, padx=10)
        
        # set a checkbox to remember the password
        ctklabel=ctk.CTkLabel(master=FRAME,text="Remember me",font=("Robot", 13))
        ctklabel.pack(pady=0,padx=0)
        checkbox1=ctk.CTkCheckBox(master=FRAME,checkmark_color="white",text="",width=70,height=18,checkbox_height=18,checkbox_width=18,hover_color="white")
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

        button3=ctk.CTkButton(master=frame,hover_color="purple",text="Technical information",command=lambda:self.infos(CANVA,frame,"A"))
        button3.pack( padx=5,pady=5,anchor='nw')

        button3=ctk.CTkButton(master=frame,hover_color="deeppink",text="Materials",command=lambda:self.infos(CANVA,frame,"B"))
        button3.pack( padx=5,pady=5,anchor='nw')

        button3=ctk.CTkButton(master=frame,hover_color="green",text="Developer",command=lambda:self.infos(CANVA,frame,"C"))
        button3.pack( padx=5,pady=5,anchor='nw')
        button3=ctk.CTkButton(master=frame,hover_color="red",text="Company",command=lambda:self.infos(CANVA,frame,"D"))
        button3.pack( padx=5,pady=5,anchor='nw')
    def infos(self,frame,letter):
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


if __name__ == "__main__":
     if db.verifier_installation()==True:
        obj = Login()
        obj.root.mainloop()
     else:
         db.create_database()
     
