from cansat_final import *
from tkinter import *
from PIL import ImageTk, Image

#splash_screen

splash = Tk()
splash.title("Astropeep Ground Station")
height = 400
width = 600
x = ((splash.winfo_screenwidth()//2)-(width)//2)
y = ((splash.winfo_screenheight()//2)-(height)//2)
splash.geometry('{}x{}+{}+{}'.format(width,height,x,y))

gif_img = "images\\splash.gif"
open_img = Image.open(gif_img)
frames = open_img.n_frames
imageObject = [PhotoImage(file = gif_img,format = f"gif -index {i}") for i in range(frames)]
count = 0
showAnimation = None


def animation(count):
    global showAnimation
    new_img = imageObject[count]
    gif_label.configure(image = new_img)
    count += 1
    if count == frames:
        count = 0
    showAnimation = splash.after(18,lambda: animation(count))
    
gif_label = Label(splash,image = "")
gif_label.place(x=0,y=0,width = 600,height = 400)



class LoginPage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1166x718')
        #self.window.resizable(0, 0)
        #self.window.state('zoomed')
        self.window.title('Login Page')


        self.bg_frame = Image.open('images\\background1.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
        
#login frame
  
        self.lgn_frame = Frame(self.window, bg='gray13', width=950, height=600)
        self.lgn_frame.place(x=200, y=70)


        self.txt = "ASTROPEEP GROUND STATION"
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="gray13",
                             fg='white',
                             bd=5,
                             relief=FLAT)
        self.heading.place(x=80, y=30, width=700, height=60)


        self.side_image = Image.open('images\\vector.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='gray13')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

#logos
 
#in_space

        self.sign_in_image = Image.open('images\\in_space.png')
        self.sign_in_image = self.sign_in_image.resize((120,75))
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='gray13')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=530, y=130)

#astro_logo

        self.sign_in_image2 = Image.open('images\\astro_logo.png')
        self.sign_in_image2 = self.sign_in_image2.resize((300,75))
        photo = ImageTk.PhotoImage(self.sign_in_image2)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='gray13')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=650, y=130)


#signin_label

        self.sign_in_label = Label(self.lgn_frame, text="Sign In", bg="gray13", fg="white",
                                    font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=240)

#username

        self.username_label = Label(self.lgn_frame, text="Username", bg="gray13", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="gray13", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"))
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        
#Username_icon
        
        self.username_icon = Image.open('images\\username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='gray13')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)

#Login_button

        self.lgn_button = Image.open('images\\btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='gray13')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)
        self.login = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.logon)
        self.login.place(x=20, y=10)



#Password

        self.password_label = Label(self.lgn_frame, text="Password", bg="gray13", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="gray13", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"), show="*")
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)
        
#Password icon
        
        self.password_icon = Image.open('images\\password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='gray13')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=414)
       
        
       
#Show/Hide Password

        self.show_image = ImageTk.PhotoImage \
            (file='images\\show.png')

        self.hide_image = ImageTk.PhotoImage \
            (file='images\\hide.png')

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="gray13"
                                  , borderwidth=0, background="gray13", cursor="hand2")
        self.show_button.place(x=860, y=420)

    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                  activebackground="gray13"
                                  , borderwidth=0, background="gray13", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="gray13"
                                  , borderwidth=0, background="gray13", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')
    def logon(self):
        if self.username_entry.get() == "Astropeep" and self.password_entry.get() == "ASI2022002":
            self.window.destroy()
            dashboard()
            
    


def page1():
    splash.destroy()
    window = Tk()
    LoginPage(window)
    window.mainloop()
splash.overrideredirect(1)
animation(count)
splash.after(8000,page1)
splash.mainloop()