import datetime
from tkcalendar import Calendar
from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk
from tkinter import messagebox, ttk
import tkinter as tk
from time import strftime
from datetime import date
import sqlite3
import io

f=('Arial', 14)


#inti logo
def inti_logo(self):
    image=Image.open('INTI_Logo.png')
    img=image.resize((220,50))
    my_img=ImageTk.PhotoImage(img)
    intilogo = tk.Label(self, image=my_img)
    intilogo.place(x=0, y=10)
    intilogo.image = my_img

#clock
def clock(self): 
        def time():
            string = strftime('%H:%M:%S %p')
            lbl.config(text = string)
            lbl.after(1000, time)

        lbl = Label(self, font = ('calibri', 20, 'bold'),background= 'antique white',foreground = 'black')
        lbl.pack()
        lbl.place(x=935, y=80)
        time()

#Today's date
def today_date(self):
        today=date.today()
        f_today = today.strftime("%A %d/%m/%Y")
        today_label = Label(self, text=f_today, font= ('Calibri', 20, 'bold'),background= 'antique white',foreground = 'black')
        today_label.pack()
        today_label.place(x=40, y=80)

#adminpage clock
def adminclock(self):
    
    def my_time():
        time_string = strftime('%H:%M:%S %p \n %A \n %d/%m/%Y') # time format 
        l1.config(text=time_string)
        l1.after(1000,my_time) # time delay of 1000 milliseconds 

    l1=tk.Label(self,font=('calibri', 26, 'bold'),bg='AntiqueWhite1', foreground='black')
    l1.place(x=900, y=5)
    my_time()


#top buttons
def top_buttons(self, controller):
    button1=tk.Button(self, height=1, width= 12, text="Homepage", font=f,command= lambda:controller.show_frame(Homepage))
    button1.place(x=230, y=12)

    button2=tk.Button(self, height=1, width=12, text="Announcements", font=f, command= lambda:controller.show_frame(Announcements))
    button2.place(x=230*1.75, y=12)

    button3=tk.Button(self, height=1, width=12, text="Events", font=f,command= lambda:controller.show_frame(Events))
    button3.place(x=230*2.5, y=12)

    button4=tk.Button(self, height=1, width=12, text="Competitions", font=f,command= lambda:controller.show_frame(Competitions))
    button4.place(x=230*3.25, y=12)

    button5=tk.Button(self, height=1, width=12, text="Profile", font=f, command=lambda: controller.show_frame(Profile))
    button5.place(x=230*4, y=12)




class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #create frame and assign it to container
        container = tk.Frame(self)

        container.pack(fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #create dictionary of frames
        self.frames={}

        for F in (Loginpage, RegisterPage, Adminpage,Homepage, Announcements, Events, Competitions, Profile):
            frame= F(container, self)
            #windows class act as root window for frames
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        #using a method to switch frames
        self.show_frame(Loginpage)

    #method to switch view frames
    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

    def updateAdmin(self, login_details):
        frame= self.frames[Adminpage]
        frame.adminwelcome_lbl.config(text='Welcome Admin, '+login_details[0])
        frame.tkraise()

    def updateHomepage(self, login_details):
        frame = self.frames[Homepage]
        frame.lbl_welcome.config(text='Welcome, '+ login_details[0])
        frame.tkraise() 

    def updateProfile(self, login_details):
        frame = self.frames[Profile]
        frame.lbl_welcome.config(text='Welcome, '+ login_details[0])
        frame.lbl_name.config(text=login_details[0])
        frame.lbl_email.config(text=login_details[2])
        frame.lbl_contact.config(text=str(login_details[3]))
        frame.lbl_gender.config(text=login_details[5])
        frame.tkraise()


class Loginpage(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        #loginpage bg
        raw_image=Image.open("IICP4.png")
        background_image=ImageTk.PhotoImage(raw_image)
        background_label = tk.Label(self, image=background_image)
        background_label.place(x=-560,y=-350)
        background_label.image = background_image


        #direct to register page for new users
        def go_to_register():
            controller.show_frame(RegisterPage)
        register_link_btn = Button(self, text= "New user? Go to Register Page", cursor= "hand2", font= ('Arial', 18), command=go_to_register)
        register_link_btn.place(x=330,y=500)
        
                
        def login_response():
            global login_details
            try:
                uname = email_tf.get()
                upwd = pwd_tf.get()
                con = sqlite3.connect('eventsystem.db')
                c = con.cursor()
                c.execute("Select * from UserDetails where email=? AND password=?",(uname,upwd))
                
            except Exception as ep:
                messagebox.showerror('Error', ep)

            check_counter=0
            if uname == '':
                warn ='Please enter username.'
            else: 
                check_counter += 1
            if upwd == "":
                warn = "Please enter password."
            else:
                check_counter += 1
            if check_counter == 2:
                login_details=c.fetchone()
                if login_details is not None:
                    messagebox.showinfo('Login Status', 'Logged in Successfully!')
                    controller.updateProfile( login_details)
                    controller.updateHomepage(login_details)
                    controller.updateAdmin(login_details)
                    if login_details[4]== 'admin':
                        controller.show_frame(Adminpage)
                    else:
                        controller.show_frame(Homepage)
                
                else:
                    messagebox.showerror('Login Status', 'invalid username or password')
            else:
                messagebox.showerror('Error', warn)

            

        page_title =  Label(self, text ='Welcome to INTI Event System', font = ('Arial', 25), bg='grey')
        page_title.pack()
        page_title.place(x=290, y=250)

        # widgets
        left_frame = Frame(
        self, 
        bd=2, 
        bg='salmon',   
        relief=SOLID, 
        padx=10, 
        pady=-1000
        )

        Label(
        left_frame, 
        text="Enter Email", 
        bg='salmon2',
        font=f).grid(row=0, column=0, sticky=W, pady=10)

        Label(
        left_frame, 
        text="Enter Password", 
        bg='salmon2',
        font=f
        ).grid(row=1, column=0, pady=10)

        email_tf = Entry(
        left_frame, 
        font=f
        )

        #show/hide password
        def toggle_password():
            if pwd_tf.cget('show') == '':
                pwd_tf.config(show='*')
                pwd_btn.config(text='Show')
            else:
                pwd_tf.config(show='')
                pwd_btn.config(text='Hide')

        pwd_tf = Entry(left_frame, font=f, show='*')
        pwd_btn=Button(self, text='Show', width=4, font=('Arial', 9), command=toggle_password)
        pwd_btn.place(x=659, y=382)
        

        login_btn = Button(
            left_frame, 
            width=15, 
            text='Login', 
            font=f, 
            relief=SOLID,
            cursor='hand2',
            command=login_response
            )




        # widgets placement
        email_tf.grid(row=0, column=1, pady=10, padx=20)
        pwd_tf.grid(row=1, column=1, pady=10, padx=20)
        login_btn.grid(row=2, column=1, pady=10, padx=20)
        left_frame.place(x=300, y=320)
   

class RegisterPage(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        #registerpage bg
        raw_image=Image.open("IICP4.png")
        background_image=ImageTk.PhotoImage(raw_image)
        background_label = tk.Label(self, image=background_image)
        background_label.place(x=-560,y=-350)
        background_label.image = background_image

        #direct to register page for new users
        def go_to_login():
            controller.show_frame(Loginpage)

        login_link_btn = Button(self, text= "Go to Login Page", cursor= "hand2", font= ('Arial', 18), command=go_to_login)
        login_link_btn.place(x=410,y=645)
        


        #connect to database
        con = sqlite3.connect('eventsystem.db')
        cur=con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS UserDetails( name text PRIMARY KEY NOT NULL,
                                                            user_id number NOT NULL, 
                                                            email text NOT NULL, 
                                                            contact number NOT NULL, 
                                                            usertype text NOT NULL, 
                                                            gender text NOT NULL, 
                                                            password text NOT NULL)''')
        con.commit()

        var1=StringVar()
        var1.set(None)
        var2=StringVar()
        var2.set(None)


        def insert_record():
            check_counter=0
            warn = " "
            if register_name.get() == "":
                warn = 'Please enter a name.'
            else:
                check_counter += 1
            
            if register_userid.get() == "":
                warn='Please enter student ID.'
            else:
                check_counter += 1

            if register_email.get() == "":
                warn = 'Please enter an email.'
            else:
                check_counter += 1

            if register_mobile.get() == "":
                warn = 'Please enter contact number.'
            else:
                check_counter += 1

            if var1.get() == 'None':
                warn = 'Select User Type'
            else:
                check_counter += 1

            if var2.get() == 'None':
                warn = 'Select Gender'
            else:
                check_counter += 1

            if register_pwd.get() == "":
                warn = 'Please enter a password.'
            else:
                check_counter += 1

            if pwd_again.get() == "":
                warn = 'Please re-enter your password.'
            else:
                check_counter += 1

            if register_pwd.get() != pwd_again.get():
                warn = 'Your passwords do not match!'
            else:
                check_counter += 1

            if check_counter == 9:
                try:
                    con = sqlite3.connect('eventsystem.db')
                    cur = con.cursor()
                    cur.execute("INSERT INTO UserDetails VALUES (:name, :user_id, :email, :contact, :usertype, :gender, :password)", {
                                'name': register_name.get(),
                                'user_id': register_userid.get(),
                                'email': register_email.get(),
                                'contact': register_mobile.get(),
                                'usertype': var1.get(),
                                'gender': var2.get(),
                                'password': register_pwd.get()              
                    })
                    con.commit()
                    messagebox.showinfo('confirmation', 'Record Saved')
                    controller.show_frame(Loginpage)

                except Exception as ep:
                    messagebox.showerror('', ep)
            else:
                messagebox.showerror('Error', warn)

        #page title
        page_title =  Label(self, text ='Welcome to INTI Event System', font = ('Arial', 25), bg='grey')
        page_title.pack()
        page_title.place(x=303, y=65)


        #register frame
        right_frame = Frame(
            self, 
            bd=2, 
            bg='salmon',
            relief=SOLID, 
            padx=10, 
            pady=-1000
            )

        Label(
            right_frame, 
            text="Enter Name", 
            bg='salmon2',
            font=f
            ).grid(row=0, column=0, sticky=W, pady=10)

        Label(
            right_frame, 
            text="Enter ID", 
            bg='salmon2',
            font=f
            ).grid(row=1, column=0, sticky=W, pady=10)

        Label(
            right_frame, 
            text="Enter Email", 
            bg='salmon2',
            font=f
            ).grid(row=2, column=0, sticky=W, pady=10)

        Label(
            right_frame, 
            text="Contact Number", 
            bg='salmon2',
            font=f
            ).grid(row=3, column=0, sticky=W, pady=10)

        Label(
            right_frame,
            text="Select User Type",
            bg='salmon2',
            font=f
            ).grid(row=4, column=0, sticky =W, pady=10)

        Label(
            right_frame, 
            text="Select Gender", 
            bg='salmon2',
            font=f
            ).grid(row=5, column=0, sticky=W, pady=10)

        Label(
            right_frame, 
            text="Enter Password", 
            bg='salmon2',
            font=f
            ).grid(row=6, column=0, sticky=W, pady=10)

        
        #show/hide password
        def toggle_password2():
            if register_pwd.cget('show') == '':
                register_pwd.config(show='*')
                pwd_btn2.config(text='Show')
            else:
                register_pwd.config(show='')
                pwd_btn2.config(text='Hide')

        register_pwd = Entry(right_frame, font=f, show='*')
        pwd_btn2=Button(self, text='Show', width=4, font=('Arial', 9), command=toggle_password2)
        pwd_btn2.place(x=690, y=475)

        def toggle_password3():
            if pwd_again.cget('show') == '':
                pwd_again.config(show='*')
                pwd_btn3.config(text='Show')
            else:
                pwd_again.config(show='')
                pwd_btn3.config(text='Hide')

        pwd_again = Entry(right_frame, font=f, show='*')
        pwd_btn3=Button(self, text='Show', width=4, font=('Arial', 9), command=toggle_password3)
        pwd_btn3.place(x=690, y=523)

        Label(
            right_frame, 
            text="Re-Enter Password", 
            bg='salmon2',
            font=f
            ).grid(row=7, column=0, sticky=W, pady=10)

        usertype_frame = LabelFrame(
            right_frame,
            bg='#CCCCCC',
            padx=10, 
            pady=10,
            )


        gender_frame = LabelFrame(
            right_frame,
            bg='#CCCCCC',
            padx=10, 
            pady=10,
            )


        register_name = Entry(
            right_frame, 
            font=f
            )

        register_userid = Entry(
            right_frame,
            font=f
            )

        register_email = Entry(
            right_frame, 
            font=f
            )

        register_mobile = Entry(
            right_frame, 
            font=f
            )

        user_rb = Radiobutton(
            usertype_frame,
            text='User',
            bg='#CCCCCC',
            variable=var1,
            value='user',
            font=('Arial',10)
        )

        admin_rb = Radiobutton(
            usertype_frame,
            text='Admin',
            bg='#CCCCCC',
            variable=var1,
            value='admin',
            font=('Arial',10)
        )

        male_rb = Radiobutton(
            gender_frame, 
            text='Male',
            bg='#CCCCCC',
            variable=var2,
            value='male',
            font=('Arial', 10),
            
        )

        female_rb = Radiobutton(
            gender_frame,
            text='Female',
            bg='#CCCCCC',
            variable=var2,
            value='female',
            font=('Arial', 10),
        
        )

        others_rb = Radiobutton(
            gender_frame,
            text='Others',
            bg='#CCCCCC',
            variable=var2,
            value='others',
            font=('Arial', 10)
        
        )

        register_pwd = Entry(
            right_frame, 
            font=f,
            show='*'

        )
        pwd_again = Entry(
            right_frame, 
            font=f,
            show='*'
        )

        register_btn = Button(
            right_frame, 
            width=15, 
            text='Register', 
            font=f, 
            relief=SOLID,
            cursor='hand2',
            command= insert_record,
        )

        #widgets placement
        register_name.grid(row=0, column=1, pady=10, padx=20)
        register_userid.grid(row=1, column=1, pady=10, padx=20)
        register_email.grid(row=2, column=1, pady=10, padx=20) 
        register_mobile.grid(row=3, column=1, pady=10, padx=20)
        register_pwd.grid(row=6, column=1, pady=10, padx=20)
        pwd_again.grid(row=7, column=1, pady=10, padx=20)
        register_btn.grid(row=8, column=1, pady=10, padx=20)
        right_frame.place(x=300, y=130)

        usertype_frame.grid(row=4, column=1, pady=10, padx=20)
        user_rb.pack(expand=True, side=LEFT)
        admin_rb.pack(expand=True, side=LEFT)

        gender_frame.grid(row=5, column=1, pady=10, padx=20)
        male_rb.pack(expand=True, side=LEFT)
        female_rb.pack(expand=True, side=LEFT)
        others_rb.pack(expand=True, side=LEFT)

        
class Adminpage(tk.Frame):
    def __init__(self,parent, controller):
        global login_details
        tk.Frame.__init__(self,parent,bg='AntiqueWhite1')
    
        #inti logo
        inti_logo(self)

        #show admin date and clock
        adminclock(self)

        #Welcome to Admin page title
        self.adminwelcome_lbl = Label(self, text ='', font = ('Arial', 28) , bg='AntiqueWhite1')
        self.adminwelcome_lbl.pack()
        self.adminwelcome_lbl.place(x=390, y=20)


        #add events
        def add_event_popup():
            top = Toplevel(ws)
            top.geometry('600x500')
            top.title("Admin Event Registration Form")
            top.resizable(False,False)

            def filedialogs():
                global get_image
                get_image = filedialog.askopenfilenames(title='Select Image', filetypes=( ("png", "*.png"), ("jpg", "*.jpg"), ("Allfile", "*.*")))

            def covert_image_into_binary(filename):
                with open(filename, 'rb') as file:
                    photo_image = file.read()
                return photo_image
            
            #connect to database
            conn = sqlite3.connect('eventsystem.db')
            cursor=conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS EventRegistrationAdmin (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                                AdminName text NOT NULL,
                                                                                AdminID number NOT NULL,
                                                                                Email text NOT NULL,
                                                                                ContactNo text NOT NULL,
                                                                                EventName text NOT NULL,
                                                                                EventDescription text NOT NULL, 
                                                                                EventType text NOT NULL,
                                                                                Date text NOT NULL, 
                                                                                Time text NOT NULL,
                                                                                Location text NOT NULL,
                                                                                Requirements text NOT NULL, 
                                                                                EventImage BLOB,
                                                                                FOREIGN KEY (AdminName)
                                                                                REFERENCES UserDetails (name))''')
            conn.commit()


            EventT=StringVar()
            EventT.set('Select')

            #warning if missing information
            def insert_record():
                for image in get_image:
                    itemimage = covert_image_into_binary(image)
                global insert_record
                check_counter=0
                warn = " "
                if name1.get() == "":
                    warn = 'Please enter Admin Name.'
                else:
                    check_counter += 1

                if AdminId.get() == "":
                    warn = 'Please enter Admin ID.'
                else:
                    check_counter += 1
                            
                if email.get() == "":
                    warn='Please enter Email.'
                else:
                    check_counter += 1

                if cNO.get() == "":
                    warn = 'Please enter Contact Number.'
                else:
                    check_counter += 1

                if date.get() == "":
                    warn = 'Enter Date.'
                else:
                    check_counter += 1

                if loc.get() == "":
                    warn = 'Enter Location.'
                else:
                    check_counter += 1

                if EventN.get() == "":
                    warn = 'Enter Event Name.'
                else:
                    check_counter += 1

                if EventT.get() == "Select":
                    warn = 'Select Event Type'
                else:
                    check_counter += 1

                #1.0 reads the first character, end: reads til the end of txtbox that it adds a new line, so -1c(minus one character)
                if EventDes.get('1.0', "end-1c") == "":
                    warn = 'Enter Event Description'
                else:
                    check_counter += 1

                if Req.get() == "":
                    warn = 'Enter Event Requirements'
                else:
                    check_counter += 1

                if time.get() == "":
                    warn = 'Please insert time.'
                else:
                    check_counter += 1

                if check_counter == 11:
                    try:
                        conn=sqlite3.connect('eventsystem.db')
                        cursor=conn.cursor()
                        cursor.execute('INSERT INTO EventRegistrationAdmin VALUES (:id,:AdminName, :AdminID, :Email, :ContactNo, :EventName, :EventDescription, :EventType, :Date, :Time, :Location, :Requirements,:EventImage)',{
                            'id':None,
                            'AdminName':name1.get(), 
                            'AdminID':AdminId.get(), 
                            'Email':email.get(), 
                            'ContactNo':cNO.get(), 
                            'EventName': EventN.get(), 
                            'EventDescription' :EventDes.get('1.0', "end-1c"), 
                            'EventType': EventT.get(), 
                            'Date':date.get(), 
                            'Time':time.get(),
                            'Location':loc.get(), 
                            'Requirements': Req.get(),
                            'EventImage':itemimage})
                        conn.commit()
                        messagebox.showinfo('Confirmation', 'Event Registered')
                        top.destroy()
                    
                    except Exception as ep:
                        messagebox.showerror('', ep)

                else: 
                    messagebox.showerror('Error', warn)

            
            #registration form buttons and widgets
            label_0 = Label(top, text="Admin Event Registration Form",width=30,font=("bold", 18))
            label_0.place(x=90,y=30)
            
            label_1 = Label(top, text="Admin Name",width=15,font=("bold", 10))
            label_1.place(x=0,y=85)
            
            name1 = Entry(top,width=15)
            name1.place(x=120,y=85)

            label_2 = Label(top, text="Admin ID",width=15,font=("bold", 10))
            label_2.place(x=0,y=125)
            
            AdminId = Entry(top,width=15)
            AdminId.place(x=120,y=125)
            
            label_3 = Label(top, text="Email",width=15,font=("bold", 10))
            label_3.place(x=0,y=165)
            
            email = Entry(top)
            email.place(x=120,y=165)
            
            label_4 = Label(top, text="Contact Number",width=15,font=("bold", 10))
            label_4.place(x=0,y=205)

            cNO = Entry(top)
            cNO.place(x=120,y=205)

            label_6 = Label(top, text="Event Name",width=15,font=("bold", 10))
            label_6.place(x=250,y=85)

            EventN = Entry(top)
            EventN.place(x=400,y=85)
            
            label_7 = Label(top, text="Date",width=15,font=("bold",10))
            label_7.place(x=250,y=125)

            date = Entry(top)
            date.place(x=400,y=125)
            
            label_8 = Label(top,text="Time",width=15,font=("bold",10))
            label_8.place(x=250,y=165)

            time = Entry(top)
            time.place(x=400,y=165)

            label_9 = Label(top, text="Location",width=15,font=("bold",10))
            label_9.place(x=250,y=205)

            loc = Entry(top)
            loc.place(x=400,y=205)

            label_10 = Label(top,text="Event Type",width=15,font=("bold",10))
            label_10.place(x=250,y=245)

            list2 = ['Seminar','Sports','Educational','Gathering'];

            droplist=OptionMenu(top,EventT, *list2)
            droplist.config(width=15)
            droplist.place(x=395,y=245)

            label_11 = Label(top,text="Requirements",width=15,font=("bold",10))
            label_11.place(x=250,y=285)

            Req = Entry(top)
            Req.place(x=400,y=285)

            label_12 = Label(top,text="Event Description",width=15,font=("bold",10))
            label_12.place(x=250,y=325)

            EventDes = Text(top, height=5, width=23, font=("bold",10), wrap=WORD )
            EventDes.place(x=400,y=325)

            label_13 = Label(top, text="Event Image",width=20,font=("bold", 10))
            label_13.place(x=250,y=420)


            itemimage = Button(top, width=15, text='Upload Image',cursor='hand2', command=filedialogs)
            itemimage.place(x=420,y=420)

            #submit button
            Button(top, text='Submit',width=18,bg='red',fg='white',command=insert_record).place(x=250,y=455)

        #edit events
        def edit_event_popup():
            top = Toplevel(ws)
            top.geometry('1240x450')
            top.title("Edit Events")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Edit Events', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=420, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            my_tree['columns'] = ('ID', 'Event Name', 'Date', 'Time', 'Location', 'Event Type', 'Event Description')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Event Name', width=300, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
            my_tree.column('Location', width=160, anchor=CENTER, stretch=NO)
            my_tree.column('Event Type', anchor=CENTER, stretch=NO)
            my_tree.column('Event Description', width=200, anchor=CENTER, stretch=NO)

            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Event Name', text='Event Name', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Location', text='Location', anchor=CENTER)
            my_tree.heading('Event Type', text='Event Type', anchor=CENTER)
            my_tree.heading('Event Description', text='Event Description', anchor=CENTER)

            #show events from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, EventName, Date, Time, Location, EventType, EventDescription from EventRegistrationAdmin ''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #entry boxes for editing db
            id_lbl = Label(top, text='ID', font=f)
            id_lbl.place(x=35, y=320)
            id_entry = Entry(top, width=5, font=f)
            id_entry.place(x=150, y=320)

            eventname_lbl = Label(top, text="Event Name", font=f)
            eventname_lbl.place(x=35, y=360)
            eventname_entry = Entry(top, width=16, font=f)
            eventname_entry.place(x=150,y=360)

            date_lbl = Label(top, text="Date", font=f)
            date_lbl.place(x=35, y=400)
            date_entry = Entry(top, width=16, font=f)
            date_entry.place(x=150,y=400)

            time_lbl = Label(top, text="Time", font=f)
            time_lbl.place(x=360, y=320)
            time_entry = Entry(top, width=16, font=f)
            time_entry.place(x=475,y=320)

            loc_lbl = Label(top, text="Location", font=f)
            loc_lbl.place(x=360, y=360)
            loc_entry = Entry(top, width=16, font=f)
            loc_entry.place(x=475,y=360)
            
            eventtype_lbl = Label(top, text="Event Type", font=f)
            eventtype_lbl.place(x=360, y=400)
            eventtype_entry = Entry(top, width=16, font=f)
            eventtype_entry.place(x=475,y=400)

            eventdes_lbl = Label(top, text="Event Description", font=f)
            eventdes_lbl.place(x=690, y=320)
            eventdes_entry = Text(top, width=25, height=5, wrap=WORD, font=f)
            eventdes_entry.place(x=845,y=320)

            #Show record
            def show_record(e):
                # Clear entry boxes
                id_entry.delete(0,END)
                eventname_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0, END)
                loc_entry.delete(0, END)
                eventtype_entry.delete(0, END)
                eventdes_entry.delete('1.0', 'end')
                

                # Grab the record number
                selected = my_tree.focus()
                # Grab record values
                values= my_tree.item(selected, 'values')

                # outputs to entry boxes
                id_entry.insert(0, values[0])
                eventname_entry.insert(0, values[1])
                date_entry.insert(0, values[2])
                time_entry.insert(0, values[3])
                loc_entry.insert(0, values[4])
                eventtype_entry.insert(0, values[5])
                eventdes_entry.insert('1.0', values[6])
                

            # Update record
            def update_record():
                # Grab the record number
                selected = my_tree.focus()
                # Update record
                my_tree.item(selected, text="", values=(id_entry.get(), eventname_entry.get(), date_entry.get(), time_entry.get(), loc_entry.get(), eventtype_entry.get(), eventdes_entry.get('1.0', "end-1c")))
                conn = sqlite3.connect('eventsystem.db')
                c = conn.cursor()

                # Update the database

                c.execute("""UPDATE EventRegistrationAdmin SET
                    EventName = :name,
                    Date = :date,
                    Time = :time,
                    Location = :loc,
                    EventType = :type,
                    EventDescription = :des

                    WHERE id = :id""",
                    {
                        'id' : id_entry.get(),
                        'name': eventname_entry.get(),
                        'date': date_entry.get(),
                        'time': time_entry.get(),
                        'loc': loc_entry.get(),
                        'type': eventtype_entry.get(),
                        'des': eventdes_entry.get('1.0', "end-1c")
                        
                    })

                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear entry boxes
                id_entry.delete(0,END)
                eventname_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0, END)
                loc_entry.delete(0, END)
                eventtype_entry.delete(0, END)
                eventdes_entry.delete('1.0', 'end')
                

            #Edit button
            edit_btn=tk.Button(top,height=1, width=6, font=f, command=update_record, text='Edit')
            edit_btn.place(x=1140, y=360)

            my_tree.bind('<ButtonRelease-1>', show_record)
        
        #delete events
        def del_event_popup():
            top = Toplevel(ws)
            top.geometry('1240x450')
            top.title("Delete Events")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Delete Events', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=420, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            # my_tree.tag_configure('odd', background='grey82')
            # my_tree.tag_configure('even', background='grey79')

            my_tree['columns'] = ('ID', 'Event Name', 'Date', 'Time', 'Location', 'Event Type', 'Event Description')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Event Name', width=300, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
            my_tree.column('Location', width=160, anchor=CENTER, stretch=NO)
            my_tree.column('Event Type', anchor=CENTER, stretch=NO)
            my_tree.column('Event Description', width=200, anchor=CENTER, stretch=NO)

            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Event Name', text='Event Name', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Location', text='Location', anchor=CENTER)
            my_tree.heading('Event Type', text='Event Type', anchor=CENTER)
            my_tree.heading('Event Description', text='Event Description', anchor=CENTER)

            #show events from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, EventName, Date, Time, Location, EventType, EventDescription from EventRegistrationAdmin ''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #entry boxes for editing db
            id_lbl = Label(top, text='ID', font=f)
            id_lbl.place(x=35, y=320)
            id_entry = Entry(top, width=5, font=f)
            id_entry.place(x=150, y=320)

            eventname_lbl = Label(top, text="Event Name", font=f)
            eventname_lbl.place(x=35, y=360)
            eventname_entry = Entry(top, width=16, font=f)
            eventname_entry.place(x=150,y=360)

            date_lbl = Label(top, text="Date", font=f)
            date_lbl.place(x=35, y=400)
            date_entry = Entry(top, width=16, font=f)
            date_entry.place(x=150,y=400)

            time_lbl = Label(top, text="Time", font=f)
            time_lbl.place(x=360, y=320)
            time_entry = Entry(top, width=16, font=f)
            time_entry.place(x=475,y=320)

            loc_lbl = Label(top, text="Location", font=f)
            loc_lbl.place(x=360, y=360)
            loc_entry = Entry(top, width=16, font=f)
            loc_entry.place(x=475,y=360)
            
            eventtype_lbl = Label(top, text="Event Type", font=f)
            eventtype_lbl.place(x=360, y=400)
            eventtype_entry = Entry(top, width=16, font=f)
            eventtype_entry.place(x=475,y=400)

            eventdes_lbl = Label(top, text="Event Description", font=f)
            eventdes_lbl.place(x=690, y=320)
            eventdes_entry = Text(top, width=25, height=5, wrap=WORD, font=f)
            eventdes_entry.place(x=845,y=320)

            #Show record
            def show_record(e):
                # Clear entry boxes
                id_entry.delete(0,END)
                eventname_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0, END)
                loc_entry.delete(0, END)
                eventtype_entry.delete(0, END)
                eventdes_entry.delete('1.0', 'end')
                

                # Grab the record number
                selected = my_tree.focus()
                # Grab record values
                values= my_tree.item(selected, 'values')

                # outputs to entry boxes
                id_entry.insert(0, values[0])
                eventname_entry.insert(0, values[1])
                date_entry.insert(0, values[2])
                time_entry.insert(0, values[3])
                loc_entry.insert(0, values[4])
                eventtype_entry.insert(0, values[5])
                eventdes_entry.insert('1.0', values[6])
                

            # Update record
            def del_record():
                x = my_tree.selection()[0]
                my_tree.delete(x)

                conn = sqlite3.connect('eventsystem.db')
                c = conn.cursor()

                # Delete From Database
                c.execute("DELETE from EventRegistrationAdmin WHERE oid=" + id_entry.get())

                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear entry boxes
                id_entry.delete(0,END)
                eventname_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0, END)
                loc_entry.delete(0, END)
                eventtype_entry.delete(0, END)
                eventdes_entry.delete('1.0', 'end')

                # Add a little message box for fun
                messagebox.showinfo("Alert", "Event Deleted.")
                

            #Delete button
            del_btn=tk.Button(top,height=1, width=6, font=f, command=del_record, text='Delete')
            del_btn.place(x=1140, y=360)

            my_tree.bind('<ButtonRelease-1>', show_record)

        #add competitions
        def add_comp_popup():
                        top = Toplevel(ws)
                        top.geometry('600x500')
                        top.title("Admin Competition Registration Form")
                        top.resizable(False,False)

                        def filedialogs():
                            global get_image
                            get_image = filedialog.askopenfilenames(title='Select Image', filetypes=( ("png", "*.png"), ("jpg", "*.jpg"), ("Allfile", "*.*")))

                        def covert_image_into_binary(filename):
                            with open(filename, 'rb') as file:
                                photo_image = file.read()
                            return photo_image

                        #connect to database
                        conn = sqlite3.connect('eventsystem.db')
                        cursor=conn.cursor()
                        cursor.execute('''CREATE TABLE IF NOT EXISTS CompRegistrationAdmin (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                                        AdminName text NOT NULL,
                                                                                        AdminID number NOT NULL,
                                                                                        Email text NOT NULL,
                                                                                        ContactNo number NOT NULL, 
                                                                                        CompetitionName text NOT NULL, 
                                                                                        CompetitionDescription text NOT NULL, 
                                                                                        CompetitionType text NOT NULL, 
                                                                                        Date text NOT NULL, 
                                                                                        Time text NOT NULL,
                                                                                        Location text NOT NULL,
                                                                                        Requirements text NOT NULL, 
                                                                                        CompImage BLOB,
                                                                                        FOREIGN KEY (AdminName)
                                                                                        REFERENCES UserDetails (name))''')
                        conn.commit()

                        CompT=StringVar()
                        CompT.set('Select')

                        #warning if missing information
                        def insert_record():
                            for image in get_image:
                                itemimage = covert_image_into_binary(image)
                            global insert_record
                            check_counter=0
                            warn = " "
                            if name1.get() == "":
                                warn = 'Please enter Admin Name.'
                            else:
                                check_counter += 1

                            if AdminId.get() == "":
                                warn = 'Please enter Admin ID.'
                            else:
                                check_counter += 1
                                                    
                            if email.get() == "":
                                warn='Please enter Email.'
                            else:
                                check_counter += 1

                            if cNO.get() == "":
                                warn = 'Please enter Contact Number.'
                            else:
                                check_counter += 1

                            if date.get() == "":
                                warn = 'Enter Date.'
                            else:
                                check_counter += 1

                            if loc.get() == "":
                                warn = 'Enter Location.'
                            else:
                                check_counter += 1

                            if CompN.get() == "":
                                warn = 'Enter Competition Name.'
                            else:
                                check_counter += 1

                            if CompT.get() == "Select":
                                warn = 'Select Competition Type'
                            else:
                                check_counter += 1

                            #1.0 reads the first character, end: reads til the end of txtbox that it adds a new line, so -1c(minus one character)
                            if CompDes.get('1.0', "end-1c") == "":
                                warn = 'Enter Competition Description'
                            else:
                                check_counter += 1

                            if Req.get() == "":
                                warn = 'Enter Competition Requirements'
                            else:
                                check_counter += 1

                            if time.get() == "":
                                warn = 'Please insert time.'
                            else:
                                check_counter += 1
                            

                            if check_counter == 11:
                                try:
                                    conn=sqlite3.connect('eventsystem.db')
                                    cursor=conn.cursor()
                                    cursor.execute('INSERT INTO CompRegistrationAdmin VALUES (:id, :AdminName, :AdminID, :Email, :ContactNo, :CompetitionName, :CompetitionDescription, :CompetitionType, :Date, :Time, :Location, :Requirements, :CompImage)',{
                                                    'id': None,
                                                    'AdminName':name1.get(), 
                                                    'AdminID':AdminId.get(), 
                                                    'Email':email.get(), 
                                                    'ContactNo':cNO.get(), 
                                                    'CompetitionName': CompN.get(), 
                                                    'CompetitionDescription' :CompDes.get('1.0', "end-1c"), 
                                                    'CompetitionType': CompT.get(), 
                                                    'Date':date.get(), 
                                                    'Time':time.get(),
                                                    'Location':loc.get(), 
                                                    'Requirements': Req.get(),
                                                    'CompImage':itemimage})
                                    conn.commit()
                                    messagebox.showinfo('Confirmation', 'Competition Registered')
                                    top.destroy()
                                            
                                except Exception as ep:
                                    messagebox.showerror('', ep)

                            else: 
                                messagebox.showerror('Error', warn)

                        #registration form buttons and widgets
                        label_0 = Label(top, text="Admin Competition Registration Form",width=30,font=("bold", 18))
                        label_0.place(x=90,y=30)
                                    
                        label_1 = Label(top, text="Admin Name",width=15,font=("bold", 10))
                        label_1.place(x=0,y=85)
                                    
                        name1 = Entry(top,width=15)
                        name1.place(x=120,y=85)

                        label_2 = Label(top, text="Admin ID",width=15,font=("bold", 10))
                        label_2.place(x=0,y=125)
                                    
                        AdminId = Entry(top,width=15)
                        AdminId.place(x=120,y=125)
                                    
                        label_3 = Label(top, text="Email",width=15,font=("bold", 10))
                        label_3.place(x=0,y=165)
                                    
                        email = Entry(top)
                        email.place(x=120,y=165)
                                    
                        label_4 = Label(top, text="Contact Number",width=15,font=("bold", 10))
                        label_4.place(x=0,y=205)

                        cNO = Entry(top)
                        cNO.place(x=120,y=205)

                        label_6 = Label(top, text="Competition Name",width=15,font=("bold", 10))
                        label_6.place(x=250,y=85)

                        CompN = Entry(top)
                        CompN.place(x=400,y=85)
                                    
                        label_7 = Label(top, text="Date",width=15,font=("bold",10))
                        label_7.place(x=250,y=125)

                        date = Entry(top)
                        date.place(x=400,y=125)
                                    
                        label_8 = Label(top,text="Time",width=15,font=("bold",10))
                        label_8.place(x=250,y=165)

                        time = Entry(top)
                        time.place(x=400,y=165)

                        label_9 = Label(top, text="Location",width=15,font=("bold",10))
                        label_9.place(x=250,y=205)

                        loc = Entry(top)
                        loc.place(x=400,y=205)

                        label_10 = Label(top,text="Competition Type",width=15,font=("bold",10))
                        label_10.place(x=250,y=245)

                        list2 = ['Mathematics','Business','Science','Others'];

                        droplist=OptionMenu(top,CompT, *list2)
                        droplist.config(width=15)
                        droplist.place(x=395,y=245)

                        label_11 = Label(top,text="Requirements",width=15,font=("bold",10))
                        label_11.place(x=250,y=285)

                        Req = Entry(top)
                        Req.place(x=400,y=285)

                        label_12 = Label(top,text="Competition\n Description",width=15,font=("bold",10))
                        label_12.place(x=250,y=325)

                        CompDes = Text(top, height=5, width=23, font=("bold",10), wrap=WORD )
                        CompDes.place(x=400,y=325)

                        label_13 = Label(top, text="Competition Image",width=20,font=("bold", 10))
                        label_13.place(x=250,y=420)


                        itemimage = Button(top, width=15, text='Upload Image',cursor='hand2', command=filedialogs)
                        itemimage.place(x=400,y=420)

                        #submit button
                        Button(top, text='Submit',width=18,bg='red',fg='white',command=insert_record).place(x=250,y=460)

        #edit competitions
        def edit_comp_popup():
            
            top = Toplevel(ws)
            top.geometry('1240x450')
            top.title("Edit Competitions")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Edit Competitions', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=420, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            # my_tree.tag_configure('odd', background='grey82')
            # my_tree.tag_configure('even', background='grey79')

            my_tree['columns'] = ('ID', 'Comp Name', 'Date', 'Time', 'Location', 'Comp Type', 'Comp Description')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Comp Name', width=300, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
            my_tree.column('Location', width=160, anchor=CENTER, stretch=NO)
            my_tree.column('Comp Type', anchor=CENTER, stretch=NO)
            my_tree.column('Comp Description', width=200, anchor=CENTER, stretch=NO)

            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Comp Name', text='Comp Name', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Location', text='Location', anchor=CENTER)
            my_tree.heading('Comp Type', text='Comp Type', anchor=CENTER)
            my_tree.heading('Comp Description', text='Comp Description', anchor=CENTER)

            #show events from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, CompetitionName, Date, Time, Location, CompetitionType, CompetitionDescription from CompRegistrationAdmin ''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #entry boxes for editing db
            id_lbl = Label(top, text='ID', font=f)
            id_lbl.place(x=35, y=320)
            id_entry = Entry(top, width=5, font=f)
            id_entry.place(x=150, y=320)

            compname_lbl = Label(top, text="Comp Name", font=f)
            compname_lbl.place(x=35, y=360)
            compname_entry = Entry(top, width=16, font=f)
            compname_entry.place(x=150,y=360)

            date_lbl = Label(top, text="Date", font=f)
            date_lbl.place(x=35, y=400)
            date_entry = Entry(top, width=16, font=f)
            date_entry.place(x=150,y=400)

            time_lbl = Label(top, text="Time", font=f)
            time_lbl.place(x=360, y=320)
            time_entry = Entry(top, width=16, font=f)
            time_entry.place(x=475,y=320)

            loc_lbl = Label(top, text="Location", font=f)
            loc_lbl.place(x=360, y=360)
            loc_entry = Entry(top, width=16, font=f)
            loc_entry.place(x=475,y=360)
            
            comptype_lbl = Label(top, text="Comp Type", font=f)
            comptype_lbl.place(x=360, y=400)
            comptype_entry = Entry(top, width=16, font=f)
            comptype_entry.place(x=475,y=400)

            compdes_lbl = Label(top, text="Comp Description", font=f)
            compdes_lbl.place(x=690, y=320)
            compdes_entry = Text(top, width=25, height=5, wrap=WORD, font=f)
            compdes_entry.place(x=845,y=320)

            #Show record
            def show_record(e):
                # Clear entry boxes
                id_entry.delete(0,END)
                compname_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0, END)
                loc_entry.delete(0, END)
                comptype_entry.delete(0, END)
                compdes_entry.delete('1.0', 'end')
                

                # Grab the record number
                selected = my_tree.focus()
                # Grab record values
                values= my_tree.item(selected, 'values')

                # outputs to entry boxes
                id_entry.insert(0, values[0])
                compname_entry.insert(0, values[1])
                date_entry.insert(0, values[2])
                time_entry.insert(0, values[3])
                loc_entry.insert(0, values[4])
                comptype_entry.insert(0, values[5])
                compdes_entry.insert('1.0', values[6])
                

            # Update record
            def update_record():
                # Grab the record number
                selected = my_tree.focus()
                # Update record
                my_tree.item(selected, text="", values=(id_entry.get(), compname_entry.get(), date_entry.get(), time_entry.get(), loc_entry.get(), comptype_entry.get(), compdes_entry.get('1.0', "end-1c")))
                conn = sqlite3.connect('eventsystem.db')
                c = conn.cursor()

                # Update the database

                c.execute("""UPDATE CompRegistrationAdmin SET
                    CompetitionName = :name,
                    Date = :date,
                    Time = :time,
                    Location = :loc,
                    CompetitionType = :type,
                    CompetitionDescription = :des

                    WHERE id = :id""",
                    {
                        'id' : id_entry.get(),
                        'name': compname_entry.get(),
                        'date': date_entry.get(),
                        'time': time_entry.get(),
                        'loc': loc_entry.get(),
                        'type': comptype_entry.get(),
                        'des': compdes_entry.get('1.0', "end-1c")
                        
                    })

                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear entry boxes
                id_entry.delete(0,END)
                compname_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0, END)
                loc_entry.delete(0, END)
                comptype_entry.delete(0, END)
                compdes_entry.delete('1.0', 'end')
                

            #Edit button
            edit_btn=tk.Button(top,height=1, width=6, font=f, command=update_record, text='Edit')
            edit_btn.place(x=1140, y=360)

            my_tree.bind('<ButtonRelease-1>', show_record)
        
        #delete competiitons
        def del_comp_popup():
            top = Toplevel(ws)
            top.geometry('1240x450')
            top.title("Delete Competitions")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Delete Competitions', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=420, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            # my_tree.tag_configure('odd', background='grey82')
            # my_tree.tag_configure('even', background='grey79')

            my_tree['columns'] = ('ID', 'Comp Name', 'Date', 'Time', 'Location', 'Comp Type', 'Comp Description')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Comp Name', width=300, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
            my_tree.column('Location', width=160, anchor=CENTER, stretch=NO)
            my_tree.column('Comp Type', anchor=CENTER, stretch=NO)
            my_tree.column('Comp Description', width=200, anchor=CENTER, stretch=NO)

            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Comp Name', text='Comp Name', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Location', text='Location', anchor=CENTER)
            my_tree.heading('Comp Type', text='Comp Type', anchor=CENTER)
            my_tree.heading('Comp Description', text='Comp Description', anchor=CENTER)

            #show competitions from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, CompetitionName, Date, Time, Location, CompetitionType, CompetitionDescription from CompRegistrationAdmin ''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #entry boxes for editing db
            id_lbl = Label(top, text='ID', font=f)
            id_lbl.place(x=35, y=320)
            id_entry = Entry(top, width=5, font=f)
            id_entry.place(x=150, y=320)

            compname_lbl = Label(top, text="Comp Name", font=f)
            compname_lbl.place(x=35, y=360)
            compname_entry = Entry(top, width=16, font=f)
            compname_entry.place(x=150,y=360)

            date_lbl = Label(top, text="Date", font=f)
            date_lbl.place(x=35, y=400)
            date_entry = Entry(top, width=16, font=f)
            date_entry.place(x=150,y=400)

            time_lbl = Label(top, text="Time", font=f)
            time_lbl.place(x=360, y=320)
            time_entry = Entry(top, width=16, font=f)
            time_entry.place(x=475,y=320)

            loc_lbl = Label(top, text="Location", font=f)
            loc_lbl.place(x=360, y=360)
            loc_entry = Entry(top, width=16, font=f)
            loc_entry.place(x=475,y=360)
            
            comptype_lbl = Label(top, text="Comp Type", font=f)
            comptype_lbl.place(x=360, y=400)
            comptype_entry = Entry(top, width=16, font=f)
            comptype_entry.place(x=475,y=400)

            compdes_lbl = Label(top, text="Comp Description", font=f)
            compdes_lbl.place(x=690, y=320)
            compdes_entry = Text(top, width=25, height=5, wrap=WORD, font=f)
            compdes_entry.place(x=845,y=320)

            #Show record
            def show_record(e):
                # Clear entry boxes
                id_entry.delete(0,END)
                compname_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0, END)
                loc_entry.delete(0, END)
                comptype_entry.delete(0, END)
                compdes_entry.delete('1.0', 'end')
                

                # Grab the record number
                selected = my_tree.focus()
                # Grab record values
                values= my_tree.item(selected, 'values')

                # outputs to entry boxes
                id_entry.insert(0, values[0])
                compname_entry.insert(0, values[1])
                date_entry.insert(0, values[2])
                time_entry.insert(0, values[3])
                loc_entry.insert(0, values[4])
                comptype_entry.insert(0, values[5])
                compdes_entry.insert('1.0', values[6])
                

            # Update record
            def del_record():
                x = my_tree.selection()[0]
                my_tree.delete(x)

                conn = sqlite3.connect('eventsystem.db')
                c = conn.cursor()

                # Delete From Database
                c.execute("DELETE from CompRegistrationAdmin WHERE oid=" + id_entry.get())

                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear entry boxes
                id_entry.delete(0,END)
                compname_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0, END)
                loc_entry.delete(0, END)
                comptype_entry.delete(0, END)
                compdes_entry.delete('1.0', 'end')

                # Add a little message box for fun
                messagebox.showinfo("Alert", "Competition Deleted.")
                

            #Delete button
            del_btn=tk.Button(top,height=1, width=6, font=f, command=del_record, text='Delete')
            del_btn.place(x=1140, y=360)

            my_tree.bind('<ButtonRelease-1>', show_record)

        #events and competition frame
        eventtable_frame = Frame(self, bd=2, bg='AntiqueWhite1', relief=SOLID)
        comptable_frame = Frame(self, bd=2, bg='AntiqueWhite1', relief=SOLID)

        #show events frame
        def show_event():
            eventtable_frame.pack(side=TOP, pady=70, anchor=W)
            comptable_frame.forget()

            #EVENTS Title
            adminevents_lbl = Label(eventtable_frame, text ='Events', font = ('Arial', 25), bg='AntiqueWhite1' )
            adminevents_lbl.grid(row=0, column=2, sticky=W, pady=5, padx=10, columnspan=5)

            #columnnames
            eventname_lbl = Label(eventtable_frame, text ='Event Name', font = ('Arial', 14,'bold'),  bg='AntiqueWhite1', fg= 'brown4' )
            eventname_lbl.grid(row=1, column=0, sticky=W, pady=5, padx=17 )

            date_lbl= Label(eventtable_frame, text ='Date', font = ('Arial', 14,'bold'),bg='AntiqueWhite1', fg= 'brown4')
            date_lbl.grid(row=1, column=1, sticky=W, pady=5, padx=50 )

            time_lbl= Label(eventtable_frame, text ='Time', font = ('Arial', 14,'bold'), bg='AntiqueWhite1', fg= 'brown4')
            time_lbl.grid(row=1, column=2, sticky=W, pady=5, padx=35 )

            loc_lbl= Label(eventtable_frame, text ='Location', font = ('Arial', 14,'bold'), bg='AntiqueWhite1', fg= 'brown4')
            loc_lbl.grid(row=1, column=3, sticky=W, pady=5, padx=35 )

            eventtype_lbl= Label(eventtable_frame, text ='Event Type', font = ('Arial', 14,'bold'), bg='AntiqueWhite1', fg= 'brown4')
            eventtype_lbl.grid(row=1, column=4, sticky=W, pady=5, padx=28 )

            # #show event from db
            conn = sqlite3.connect('eventsystem.db')
            r_set=conn.execute('''SELECT EventName, Date, Time, Location, EventType from EventRegistrationAdmin LIMIT 0,5''');
            i=0 # row value inside the loop 
            for EventRegistrationAdmin in r_set: 
                for j in range(len(EventRegistrationAdmin)):
                    e = tk.Label(eventtable_frame, width=18, height=1, font=('Arial', 11),text=EventRegistrationAdmin[j], pady=5, relief='solid', wraplength=180, justify=CENTER) 
                    e.grid(row=i+2, column=j) 
                i=i+1

            #view all events popup
            def view_events():
                top = Toplevel()
                top.geometry('1040x450')
                top.title("View All Events")
                top.resizable(False, False)

                style=ttk.Style()
                style.theme_use('clam')
                style.configure('Treeview.Heading', font=f)
                style.configure('Treeview', font=('Arial', 13))

                #view all compertitions label
                allcomp_lbl = Label(top, text ='View All Events', font = ('Arial', 25,'bold'))
                allcomp_lbl.place(x=375, y=10)

                tree_frame = Frame(top)
                tree_frame.pack(pady=70)

                tree_scroll = Scrollbar(tree_frame)
                tree_scroll.pack(side=RIGHT, fill=Y)

                my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
                my_tree.pack()

                tree_scroll.config(command=my_tree.yview)

                # my_tree.tag_configure('odd', background='grey82')
                # my_tree.tag_configure('even', background='grey79')

                my_tree['columns'] = ('ID', 'Event Name', 'Date', 'Time', 'Location', 'Event Type')

                #format columns
                my_tree.column('#0', width=0, stretch=NO)
                my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
                my_tree.column('Event Name', width=300, anchor=CENTER, stretch=NO)
                my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
                my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
                my_tree.column('Location', width=160, anchor=CENTER, stretch=NO)
                my_tree.column('Event Type', anchor=CENTER, stretch=NO)

                #column headings
                my_tree.heading('#0', text='', anchor=W)
                my_tree.heading('ID', text='ID', anchor=CENTER)
                my_tree.heading('Event Name', text='Event Name', anchor=CENTER)
                my_tree.heading('Date', text='Date', anchor=CENTER)
                my_tree.heading('Time', text='Time', anchor=CENTER)
                my_tree.heading('Location', text='Location', anchor=CENTER)
                my_tree.heading('Event Type', text='Event Type', anchor=CENTER)

                #show events from db
                conn = sqlite3.connect('eventsystem.db')
                c=conn.cursor()
                r_set=c.execute('''SELECT id, EventName, Date, Time, Location, EventType from EventRegistrationAdmin ''')
                r_set=c.fetchall()
                for row in r_set:
                    my_tree.insert("", tk.END, values=row)

            
            



            #show all events button
            showevents_btn=tk.Button(eventtable_frame,height=1, width=10, font=('Arial', 15), text='View All', command=view_events)
            showevents_btn.grid(row=11, column=0, sticky=W, pady=5, padx=10, columnspan=5)

            #add,edit,delete events btn
            #add events button
            add_event_btn=tk.Button(eventtable_frame,height=1, width=10, font=('Arial', 15), command=add_event_popup, text='Add Events')
            add_event_btn.grid(row=11, column=1, sticky=W, pady=5, padx=10, columnspan=5)

            #edit evnts btn
            edt_event_btn=tk.Button(eventtable_frame,height=1, width=10, font=('Arial', 15), command=edit_event_popup, text='Edit Events')
            edt_event_btn.grid(row=11, column=2, sticky=W, pady=5, padx=10, columnspan=5)

            dlt_event_btn=tk.Button(eventtable_frame,height=1, width=11, font=('Arial', 15), command=del_event_popup, text='Delete Events')
            dlt_event_btn.grid(row=11, column=3, sticky=W, pady=5, padx=10, columnspan=5)

            #show competitions frame button
            showcomp_btn=tk.Button(eventtable_frame,height=1, width=15, font=('Arial', 13), text='Show Competitions', command=show_competitions)
            showcomp_btn.grid(row=11, column=4, sticky=W, pady=5, padx=10, columnspan=5)



        #show competitions frame
        def show_competitions():
            comptable_frame.pack(side=TOP,pady=70, anchor=W)
            eventtable_frame.forget()

            #competitions title
            admincomp_lbl = Label(comptable_frame, text ='Competitions', font = ('Arial', 25) , bg='AntiqueWhite1')
            admincomp_lbl.grid(row=0, column=2, sticky=W, pady=5, padx=10, columnspan=5)

            #columnnames
            compname_lbl = Label(comptable_frame, text ='Comp Name', font = ('Arial', 14,'bold'),  bg='AntiqueWhite1', fg= 'brown4' )
            compname_lbl.grid(row=1, column=0, sticky=W, pady=5, padx=17 )

            date_lbl= Label(comptable_frame, text ='Date', font = ('Arial', 14,'bold'),bg='AntiqueWhite1', fg= 'brown4')
            date_lbl.grid(row=1, column=1, sticky=W, pady=5, padx=50 )

            time_lbl= Label(comptable_frame, text ='Time', font = ('Arial', 14,'bold'), bg='AntiqueWhite1', fg= 'brown4')
            time_lbl.grid(row=1, column=2, sticky=W, pady=5, padx=35 )

            loc_lbl= Label(comptable_frame, text ='Location', font = ('Arial', 14,'bold'), bg='AntiqueWhite1', fg= 'brown4')
            loc_lbl.grid(row=1, column=3, sticky=W, pady=5, padx=35 )

            comptype_lbl= Label(comptable_frame, text ='Comp Type', font = ('Arial', 14,'bold'), bg='AntiqueWhite1', fg= 'brown4')
            comptype_lbl.grid(row=1, column=4, sticky=W, pady=5, padx=28 )

            # #show competitions from database
            conn = sqlite3.connect('eventsystem.db')
            r_set=conn.execute('''SELECT CompetitionName, Date, Time, Location, CompetitionType from CompRegistrationAdmin LIMIT 0,5''');
            i=0 # row value inside the loop 
            for CompRegistrationAdmin in r_set: 
                for j in range(len(CompRegistrationAdmin)):
                    e = tk.Label(comptable_frame, width=18, height=1, font=('Arial', 11),text=CompRegistrationAdmin[j], pady=5, relief='solid', wraplength=180, justify=CENTER) 
                    e.grid(row=i+2, column=j) 
                i=i+1


            #view all competitions popup
            def view_comp():
                top = Toplevel()
                top.title('View All Competitions')
                top.geometry('1040x450')
                top.resizable(False,False)

                style=ttk.Style()
                style.theme_use('clam')
                style.configure('Treeview.Heading', font=f)
                style.configure('Treeview', font=('Arial', 13))

                #view all compertitions label
                allcomp_lbl = Label(top, text ='View All Competitions', font = ('Arial', 25,'bold'))
                allcomp_lbl.place(x=375, y=10)

                tree_frame = Frame(top)
                tree_frame.pack(pady=70)

                tree_scroll = Scrollbar(tree_frame)
                tree_scroll.pack(side=RIGHT, fill=Y)

                my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
                my_tree.pack()

                tree_scroll.config(command=my_tree.yview)

                # my_tree.tag_configure('odd', background='grey82')
                # my_tree.tag_configure('even', background='grey79')

                my_tree['columns'] = ('ID', 'Comp Name', 'Date', 'Time', 'Location', 'Comp Type')

                #format columns
                my_tree.column('#0', width=0, stretch=NO)
                my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
                my_tree.column('Comp Name', width=300, anchor=CENTER, stretch=NO)
                my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
                my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
                my_tree.column('Location', width=160, anchor=CENTER, stretch=NO)
                my_tree.column('Comp Type', anchor=CENTER, stretch=NO)

                #column headings
                my_tree.heading('#0', text='', anchor=W)
                my_tree.heading('ID', text='ID', anchor=CENTER)
                my_tree.heading('Comp Name', text='Comp Name', anchor=CENTER)
                my_tree.heading('Date', text='Date', anchor=CENTER)
                my_tree.heading('Time', text='Time', anchor=CENTER)
                my_tree.heading('Location', text='Location', anchor=CENTER)
                my_tree.heading('Comp Type', text='Comp Type', anchor=CENTER)

                #show competition from db
                conn = sqlite3.connect('eventsystem.db')
                c=conn.cursor()
                r_set=c.execute('''SELECT id, CompetitionName, Date, Time, Location, CompetitionType from CompRegistrationAdmin ''')
                r_set=c.fetchall()
                for row in r_set:
                    my_tree.insert("", tk.END, values=row)

            #view all competitions
            all_comp_btn=tk.Button(comptable_frame,height=1, width=10, font=('Arial', 15), text='View All', command=view_comp)
            all_comp_btn.grid(row=11, column=0, sticky=W, pady=5, padx=10, columnspan=5)

            #add,edit,delete competition btns
            #add comp button
            add_comp_btn=tk.Button(comptable_frame,height=1, width=10, font=('Arial', 15), command=add_comp_popup, text='Add Comp')
            add_comp_btn.grid(row=11, column=1, sticky=W, pady=5, padx=10, columnspan=5)

            #edit comp btn
            edt_comp_btn=tk.Button(comptable_frame,height=1, width=10, font=('Arial', 15), command=edit_comp_popup, text='Edit Comp')
            edt_comp_btn.grid(row=11, column=2, sticky=W, pady=5, padx=10, columnspan=5)

            dlt_comp_btn=tk.Button(comptable_frame,height=1, width=11, font=('Arial', 15), command=del_comp_popup, text='Delete Comp')
            dlt_comp_btn.grid(row=11, column=3, sticky=W, pady=5, padx=10, columnspan=5)

            #show events frame
            show_event_btn=tk.Button(comptable_frame,height=1, width=10, font=('Arial', 15), text='Show Events', command=show_event)
            show_event_btn.grid(row=11, column=4, sticky=W, pady=5, padx=10, columnspan=5)

        #show events frame first
        show_event()    

        #refresh events button
        def refresh_evnt():
            show_event()

        #refresh competitions button
        def refresh_comp():
            show_competitions()

        re_evnt_btn = Button(eventtable_frame, text='Refresh', width=8, height=1, font=f, command=refresh_evnt)
        re_evnt_btn.grid(row=0,column=4)

        re_comp_btn = Button(comptable_frame, text='Refresh', width=8, height=1, font=f, command=refresh_comp)
        re_comp_btn.grid(row=0,column=4)

        #lf_frame for admin to add,delete
        lf_frame = Frame(self, bd=2, bg='AntiqueWhite1', relief=SOLID)
        lf_frame.place(x=90, y=375)

        #add lost and found item
        def add_lf():
            top = Toplevel()
            top.geometry('500x550')
            top.title("Lost and Found Items Form")
            top.resizable(False, False)
            
            def filedialogs():
                global get_image
                get_image = filedialog.askopenfilenames(title='Select Image', filetypes=( ("png", "*.png"), ("jpg", "*.jpg"), ("Allfile", "*.*")))

            def covert_image_into_binary(filename):
                with open(filename, 'rb') as file:
                    photo_image = file.read()
                return photo_image

            conn = sqlite3.connect('eventsystem.db')
            cursor=conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS LostFound (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                                AdminName TEXT NOT NULL,
                                                                AdminID NUMBER NOT NULL,
                                                                ItemName TEXT NOT NULL,
                                                                LocationFound TEXT NOT NULL, 
                                                                Description TEXT NOT NULL, 
                                                                Image BLOB,
                                                                FOREIGN KEY (AdminName)
                                                                REFERENCES UserDetails (name))''')
            conn.commit()

            def insert_record():
                    for image in get_image:
                        itemimage = covert_image_into_binary(image)

                    check_counter=0
                    warn = " "
                    if name.get() == "":
                        warn = 'Please enter admin name.'
                    else:
                        check_counter += 1
                        
                    if adminID.get() == "":
                        warn='Please enter admin ID.'
                    else:
                        check_counter += 1

                    if itemname.get() == "":
                        warn = 'Please enter item name.'
                    else:
                        check_counter += 1

                    if location.get() == "":
                        warn = 'Please enter location.'
                    else:
                        check_counter += 1

                    if des.get('1.0', "end-1c") == "":
                        warn = 'Enter Item Description.'
                    else:
                        check_counter += 1


                    if check_counter == 5:
                        try:
                            conn= sqlite3.connect('eventsystem.db')
                            cursor=conn.cursor()
                            cursor.execute("INSERT INTO LostFound VALUES (:id, :AdminName, :AdminID, :ItemName, :LocationFound, :Description, :Image)", {
                            'id':None,
                            'AdminName':name.get(),
                            'AdminID':adminID.get(),
                            'ItemName':itemname.get(),
                            'LocationFound':location.get(),
                            'Description': des.get('1.0', "end-1c"),
                            'Image':itemimage
                            })
                            conn.commit()
                            messagebox.showinfo('Confirmation', 'Lost & Found Item added')
                            top.destroy()

                        except Exception as ep:
                            messagebox.showerror('', ep)

                    else:
                        messagebox.showerror('Error', warn)

            label_0 = Label(top, text="Lost & Found Items Admin Page",font=("bold", 22))
            label_0.place(x=45,y=30)
            
            label_1 = Label(top, text="Admin Name",width=20,font=("bold", 10))
            label_1.place(x=75,y=100)
            
            name = Entry(top, width=30)
            name.place(x=240,y=100)

            label_2 = Label(top, text="Admin ID",width=20,font=("bold", 10))
            label_2.place(x=75,y=150)
            
            adminID = Entry(top, width=30)
            adminID.place(x=240,y=150)
            
            label_3 = Label(top, text="Item Name",width=20,font=("bold", 10))
            label_3.place(x=71,y=200)
            
            itemname = Entry(top, width=30)
            itemname.place(x=240,y=200)

            label_4 = Label(top, text="Location Found",width=20,font=("bold", 10))
            label_4.place(x=70,y=250)

            location = Entry(top, width=30)
            location.place(x=240,y=250)
            
            label_5 = Label(top, text="Item Description",width=20,font=("bold", 10))
            label_5.place(x=70,y=300)

            des = Text(top, height=5, width=30, font=("bold",10), wrap=WORD )
            des.place(x=240,y=300)

            label_6 = Label(top, text="Item Image",width=20,font=("bold", 10))
            label_6.place(x=70,y=400)


            itemimage = Button(top, width=15, text='Upload Image',cursor='hand2', command=filedialogs)
            itemimage.place(x=240,y=400)
            
            
            Button(top, text='Submit',width=13,bg='red',fg='white', cursor='hand2', command=insert_record).place(x=180,y=500)       

        #delete lost and found item
        def del_lf():
            top = Toplevel(ws)
            top.geometry('890x450')
            top.title("Delete Lost and Found Items")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Delete Lost and Found Items', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=230, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            # my_tree.tag_configure('odd', background='grey82')
            # my_tree.tag_configure('even', background='grey79')

            my_tree['columns'] = ('ID', 'Item Name', 'Location Found', 'Description')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Item Name', width=180, anchor=CENTER, stretch=NO)
            my_tree.column('Location Found', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Description', width=300, anchor=CENTER, stretch=NO)

            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Item Name', text='Item Name', anchor=CENTER)
            my_tree.heading('Location Found', text='Location Found', anchor=CENTER)
            my_tree.heading('Description', text='Description', anchor=CENTER)

            #show lost found items from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, ItemName, LocationFound, Description from LostFound ''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #entry boxes for editing db
            id_lbl = Label(top, text='ID', font=f)
            id_lbl.place(x=35, y=320)
            id_entry = Entry(top, width=5, font=f)
            id_entry.place(x=150, y=320)

            itemname_lbl = Label(top, text="Item Name", font=f)
            itemname_lbl.place(x=35, y=360)
            itemname_entry = Entry(top, width=16, font=f)
            itemname_entry.place(x=150,y=360)

            loc_lbl = Label(top, text="Location Found", font=f)
            loc_lbl.place(x=35, y=400)
            loc_entry = Entry(top, width=16, font=f)
            loc_entry.place(x=175,y=400)

            des_lbl = Label(top, text="Description", font=f)
            des_lbl.place(x=360, y=320)
            des_entry = Text(top, width=27, height=5, wrap=WORD, font=f)
            des_entry.place(x=475,y=320)

            #Show record
            def show_record(e):
                # Clear entry boxes
                id_entry.delete(0,END)
                itemname_entry.delete(0, END)
                loc_entry.delete(0, END)
                des_entry.delete('1.0', 'end')
                

                # Grab the record number
                selected = my_tree.focus()
                # Grab record values
                values= my_tree.item(selected, 'values')

                # outputs to entry boxes
                id_entry.insert(0, values[0])
                itemname_entry.insert(0, values[1])
                loc_entry.insert(0, values[2])
                des_entry.insert('1.0', values[3])
                

            # Update record
            def del_record():
                x = my_tree.selection()[0]
                my_tree.delete(x)

                conn = sqlite3.connect('eventsystem.db')
                c = conn.cursor()

                # Delete From Database
                c.execute("DELETE from LostFound WHERE oid=" + id_entry.get())

                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear entry boxes
                id_entry.delete(0,END)
                itemname_entry.delete(0, END)
                loc_entry.delete(0, END)
                des_entry.delete('1.0', 'end')

                # Add a little message box for fun
                messagebox.showinfo("Alert", "Lost and Found Item Deleted.")
                

            #Delete button
            del_btn=tk.Button(top,height=1, width=6, font=f, command=del_record, text='Delete')
            del_btn.place(x=790, y=360)

            my_tree.bind('<ButtonRelease-1>', show_record)

        #lf_frame title
        lf_frame_lbl = Label(lf_frame, text ='Lost & Found Items', font = ('Arial', 25) , bg='AntiqueWhite1')
        lf_frame_lbl.grid(row=0, column=0, sticky=W, pady=5, padx=10, columnspan=3)

        #show lost and found images in admin lf_frame
        #connect to database for lost and found
        #show image from database
        conn = sqlite3.connect('eventsystem.db')
        cursor=conn.cursor()
        l_set=cursor.execute('''SELECT id, Image, Description FROM LostFound''')
        l_set=cursor.fetchall()
        # def lf_details(i):
        
        # def lf_display(LostFound):
        global rec_no
        rec_no=0
        img2= Image.open(io.BytesIO(l_set[rec_no][1]))
        img2 = img2.resize((300,220))
        img2 = ImageTk.PhotoImage(img2)
        lf_image=tk.Label(lf_frame, image=img2)
        lf_image.grid(row=2, column=0, columnspan=2, sticky=W, pady=5)
        lf_image.image=img2

        lf_details=Label(lf_frame, text= "Description: "+ l_set[rec_no][2], wraplength=225, font=f)
        lf_details.grid(row=2, column=2, columnspan=2, sticky=W, pady=5)


        #lf_frame add items, edit, view btns
        add_lf_btn=tk.Button(lf_frame,height=1, width=10, font=f, command=add_lf, text='Add Items')
        add_lf_btn.grid(row=3, column=1, sticky=W, pady=5, padx=10)

        del_lf_btn=tk.Button(lf_frame,height=1, width=10, font=f, command=del_lf, text='Delete Items')
        del_lf_btn.grid(row=3, column=2, sticky=W, pady=5, padx=10)

        def previous():
            global lf_image
            global rec_no
            if rec_no>0:
                rec_no=rec_no-1

            if rec_no==0:
                prev_btn.config(state=DISABLED)
            else:
                prev_btn.config(state=NORMAL)
                next_btn.config(state=NORMAL)

            img2= Image.open(io.BytesIO(l_set[rec_no][1]))
            img2 = img2.resize((300,220))
            img2 = ImageTk.PhotoImage(img2)
            lf_image=tk.Label(lf_frame, image=img2)
            lf_image.grid(row=2, column=0, columnspan=2, sticky=W, pady=5)
            lf_image.image=img2
            
            lf_details.config(text="Description: "+ l_set[rec_no][2])

        def next():
            global lf_image
            global rec_no
            if rec_no < (len(l_set)-1):
                rec_no=rec_no+1
            if rec_no == (len(l_set)-1):
                next_btn.config(state=DISABLED)
            else:
                next_btn.config(state=NORMAL)
                prev_btn.config(state=NORMAL)
                
            img2= Image.open(io.BytesIO(l_set[rec_no][1]))
            img2 = img2.resize((300,220))
            img2 = ImageTk.PhotoImage(img2)
            lf_image=tk.Label(lf_frame, image=img2)
            lf_image.grid(row=2, column=0, columnspan=2, sticky=W, pady=5)
            lf_image.image=img2


            lf_details.config(text="Description: "+ l_set[rec_no][2])

        # #Previous image button
        prev_btn=tk.Button(lf_frame, height=1, width=4, text="<<",  command=previous, font=f)
        prev_btn.grid(row=3, column=0, sticky=W, pady=5, padx=5)
        # #Next image button
        next_btn=tk.Button(lf_frame, height=1, width=4, text=">>", command=next, font=f)
        next_btn.grid(row=3, column=3, sticky=W, pady=5, padx=5)



        #Admin Key in What's New 
        #What's new frame
        whatnew_frame = Frame(self, bd=2, bg='AntiqueWhite1', relief=SOLID)
        whatnew_frame.place(x=630, y=375)

        whatnew_lbl = Label(whatnew_frame, text ='What\'s New', font = ('Arial', 25), bg='AntiqueWhite1' )
        whatnew_lbl.grid(row=0, column=1, sticky=W, pady=5, padx=10, columnspan=3)

        #events take from database(done i think)
        #cancellation of class notice

        #add cancellation of class popup
        def add_classcancel():
            root = Tk()
            root.geometry('400x290')
            root.title("Class Cancellation")
            root.resizable(False, False)

            #database
            conn = sqlite3.connect('eventsystem.db')
            cursor=conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS ClassCancel (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                    Subject TEXT NOT NULL,
                                                                    Date Text NOT NULL,
                                                                    Time Text NOT NULL, 
                                                                    Venue Text NOT NULL, 
                                                                    Replacement Text NOT NULL)''')
            conn.commit()

            def insert_record():
                check_counter=0
                warn = " "
                if subj.get() == "":
                    warn = 'Please enter subject.'
                else:
                    check_counter += 1
                        
                if date.get() == "":
                    warn='Please enter date.'
                else:
                    check_counter += 1

                if time.get() == "":
                    warn = 'Please enter time.'
                else:
                    check_counter += 1

                if venue.get() == "":
                    warn = 'Please enter venue.'
                else:
                    check_counter += 1

                if replacement.get() == "":
                    warn = 'Enter replacement (If not, type \'to be announced\').'
                else:
                    check_counter += 1


                if check_counter == 5:
                    try:
                        conn= sqlite3.connect('eventsystem.db')
                        cursor=conn.cursor()
                        cursor.execute("INSERT INTO ClassCancel VALUES (:id,:Subject, :Date, :Time, :Venue, :Replacement)", {
                        'id':None,
                        'Subject':subj.get(),
                        'Date':date.get(),
                        'Time':time.get(),
                        'Venue':venue.get(),
                        'Replacement':replacement.get()
                        })
                        conn.commit()
                        messagebox.showinfo('Confirmation', 'Class cancellation added')
                        root.destroy()

                    except Exception as ep:
                        messagebox.showerror('', ep)

                else:
                    messagebox.showerror('Error', warn)

            #Add to countdown title, widgets, entries
            classcancel_title= Label(root, text='Class Cancellation Page', font=("Arial", 18))
            classcancel_title.grid(row=0, column=0, sticky=W, pady=5, columnspan=2)

            subjname_lbl= Label(root, text='Subject', font=f)
            subjname_lbl.grid(row=1, column=0, sticky=W, pady=5)

            subj = Entry(root, font=f, width=15)
            subj.grid(row=1, column=1, sticky=W, pady=5)

            date_lbl= Label(root, text='Date', font=f)
            date_lbl.grid(row=2, column=0, sticky=W, pady=5)

            date=Entry(root, font=f, width=15)
            date.grid(row=2, column=1, sticky=W, pady=5)

            time_lbl= Label(root, text='Time', font=f)
            time_lbl.grid(row=3, column=0, sticky=W, pady=5)

            time =Entry(root, font=f, width=15)
            time.grid(row=3, column=1, sticky=W, pady=5)

            venue_lbl=Label(root, text='Venue', font=f)
            venue_lbl.grid(row=4, column=0, sticky=W, pady=5)

            venue =Entry(root, font=f, width=15)
            venue.grid(row=4, column=1, sticky=W, pady=5)

            replacement_lbl=Label(root, text='Class Replacement', font=f)
            replacement_lbl.grid(row=5, column=0, sticky=W, pady=5)

            replacement =Entry(root, font=f, width=15)
            replacement.grid(row=5, column=1, sticky=W, pady=5)


            add_event_btn=Button(root,height=1,width=5, command=insert_record, text='Add', font=f)
            add_event_btn.grid(row=6, column=1,sticky=W, pady=5, columnspan=2)
        
        #edit cancellation of class
        def edit_classcancel():
            top = Toplevel(ws)
            top.geometry('855x450')
            top.title("Edit Class Cancellation")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Edit Class Cancellation', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=300, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            # my_tree.tag_configure('odd', background='grey82')
            # my_tree.tag_configure('even', background='grey79')

            my_tree['columns'] = ('ID', 'Subject', 'Date', 'Time', 'Venue', 'Replacement')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Subject', width=180, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
            my_tree.column('Venue', width=160, anchor=CENTER, stretch=NO)
            my_tree.column('Replacement', anchor=CENTER, stretch=NO)

            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Subject', text='Subject', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Venue', text='Venue', anchor=CENTER)
            my_tree.heading('Replacement', text='Replacement', anchor=CENTER)

            #show events from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, Subject, Date, Time, Venue, Replacement from ClassCancel ''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #entry boxes for editing db
            id_lbl = Label(top, text='ID', font=f)
            id_lbl.place(x=35, y=320)
            id_entry = Entry(top, width=5, font=f)
            id_entry.place(x=150, y=320)

            subjname_lbl = Label(top, text="Subject", font=f)
            subjname_lbl.place(x=35, y=360)
            subjname_entry = Entry(top, width=16, font=f)
            subjname_entry.place(x=150,y=360)

            date_lbl = Label(top, text="Date", font=f)
            date_lbl.place(x=35, y=400)
            date_entry = Entry(top, width=16, font=f)
            date_entry.place(x=150,y=400)

            time_lbl = Label(top, text="Time", font=f)
            time_lbl.place(x=360, y=320)
            time_entry = Entry(top, width=16, font=f)
            time_entry.place(x=475,y=320)

            venue_lbl = Label(top, text="Venue", font=f)
            venue_lbl.place(x=360, y=360)
            venue_entry = Entry(top, width=16, font=f)
            venue_entry.place(x=475,y=360)
            
            replace_lbl = Label(top, text="Replacement", font=f)
            replace_lbl.place(x=360, y=400)
            replace_entry = Entry(top, width=16, font=f)
            replace_entry.place(x=475,y=400)

            #Show record
            def show_record(e):
                # Clear entry boxes
                id_entry.delete(0,END)
                subjname_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0, END)
                venue_entry.delete(0, END)
                replace_entry.delete(0, END)                

                # Grab the record number
                selected = my_tree.focus()
                # Grab record values
                values= my_tree.item(selected, 'values')

                # outputs to entry boxes
                id_entry.insert(0, values[0])
                subjname_entry.insert(0, values[1])
                date_entry.insert(0, values[2])
                time_entry.insert(0, values[3])
                venue_entry.insert(0, values[4])
                replace_entry.insert(0, values[5])                

            # Update record
            def update_record():
                # Grab the record number
                selected = my_tree.focus()
                # Update record
                my_tree.item(selected, text="", values=(id_entry.get(), subjname_entry.get(), date_entry.get(), time_entry.get(), venue_entry.get(), replace_entry.get()))
                conn = sqlite3.connect('eventsystem.db')
                c = conn.cursor()

                # Update the database

                c.execute("""UPDATE ClassCancel SET
                    Subject = :subj,
                    Date = :date,
                    Time = :time,
                    Venue = :venue,
                    Replacement = :replace

                    WHERE id = :id""",
                    {
                        'id' : id_entry.get(),
                        'subj': subjname_entry.get(),
                        'date': date_entry.get(),
                        'time': time_entry.get(),
                        'venue': venue_entry.get(),
                        'replace': replace_entry.get()                        
                    })

                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear entry boxes
                id_entry.delete(0,END)
                subjname_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0, END)
                venue_entry.delete(0, END)
                replace_entry.delete(0, END)                

            #Edit button
            edit_btn=tk.Button(top,height=1, width=6, font=f, command=update_record, text='Edit')
            edit_btn.place(x=700, y=360)

            my_tree.bind('<ButtonRelease-1>', show_record)

        #delete cancellation of class
        def del_classcancel():
            top = Toplevel(ws)
            top.geometry('890x450')
            top.title("Delete Class Cancellation")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Delete Class Cancellation', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=230, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            # my_tree.tag_configure('odd', background='grey82')
            # my_tree.tag_configure('even', background='grey79')

            my_tree['columns'] = ('ID', 'Subject', 'Date', 'Time', 'Replacement')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Subject', width=220, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Replacement', width=180, anchor=CENTER, stretch=NO)


            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Subject', text='Subject', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Replacement', text='Replacement', anchor=CENTER)


            #show class cancellation from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, Subject, Date, Time, Replacement from ClassCancel ''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #entry boxes for editing db
            id_lbl = Label(top, text='ID', font=f)
            id_lbl.place(x=35, y=320)
            id_entry = Entry(top, width=5, font=f)
            id_entry.place(x=150, y=320)

            subj_lbl = Label(top, text="Subject", font=f)
            subj_lbl.place(x=35, y=360)
            subj_entry = Entry(top, width=16, font=f)
            subj_entry.place(x=150,y=360)

            date_lbl = Label(top, text="Date", font=f)
            date_lbl.place(x=35, y=400)
            date_entry = Entry(top, width=16, font=f)
            date_entry.place(x=150,y=400)

            time_lbl = Label(top, text="Time", font=f)
            time_lbl.place(x=360, y=320)
            time_entry = Entry(top, width=16, font=f)
            time_entry.place(x=475,y=320)

            replace_lbl = Label(top, text="Replacement", font=f)
            replace_lbl.place(x=360, y=360)
            replace_entry = Entry(top, width=16, font=f)
            replace_entry.place(x=480,y=360)

            #Show record
            def show_record(e):
                # Clear entry boxes
                id_entry.delete(0,END)
                subj_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0,END)
                replace_entry.delete(0,END)
                

                # Grab the record number
                selected = my_tree.focus()
                # Grab record values
                values= my_tree.item(selected, 'values')

                # outputs to entry boxes
                id_entry.insert(0, values[0])
                subj_entry.insert(0, values[1])
                date_entry.insert(0, values[2])
                time_entry.insert(0, values[3])
                replace_entry.insert(0, values[4])
                

            # Update record
            def del_record():
                x = my_tree.selection()[0]
                my_tree.delete(x)

                conn = sqlite3.connect('eventsystem.db')
                c = conn.cursor()

                # Delete From Database
                c.execute("DELETE from ClassCancel WHERE oid=" + id_entry.get())

                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear entry boxes
                id_entry.delete(0,END)
                subj_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0,END)
                replace_entry.delete(0,END)

                # Add a little message box for fun
                messagebox.showinfo("Alert", "Class Cancellation Deleted.")
                

            #Delete button
            del_btn=tk.Button(top,height=1, width=6, font=f, command=del_record, text='Delete')
            del_btn.place(x=790, y=360)

            my_tree.bind('<ButtonRelease-1>', show_record)

        #add replacement of class 
        def add_classreplace():
            root = Tk()
            root.geometry('400x290')
            root.title("Class Replacement")
            root.resizable(False, False)

            #database
            conn = sqlite3.connect('eventsystem.db')
            cursor=conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS ClassReplace (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                                    Subject TEXT NOT NULL,
                                                                                    Date Text NOT NULL,
                                                                                    Time Text NOT NULL, 
                                                                                    Venue Text NOT NULL)''')
            conn.commit()

            def insert_record():
                check_counter=0
                warn = " "
                if subj.get() == "":
                    warn = 'Please enter subject.'
                else:
                    check_counter += 1
                        
                if date.get() == "":
                    warn='Please enter date.'
                else:
                    check_counter += 1

                if time.get() == "":
                    warn = 'Please enter time.'
                else:
                    check_counter += 1

                if venue.get() == "":
                    warn = 'Please enter venue.'
                else:
                    check_counter += 1



                if check_counter == 4:
                    try:
                        conn= sqlite3.connect('eventsystem.db')
                        cursor=conn.cursor()
                        cursor.execute("INSERT INTO ClassReplace VALUES (:id, :Subject, :Date, :Time, :Venue)", {
                        'id':None,
                        'Subject':subj.get(),
                        'Date':date.get(),
                        'Time':time.get(),
                        'Venue':venue.get()
                        })
                        conn.commit()
                        messagebox.showinfo('Confirmation', 'Class replacement added')
                        root.destroy()

                    except Exception as ep:
                        messagebox.showerror('', ep)

                else:
                    messagebox.showerror('Error', warn)

            #Add to countdown title, widgets, entries
            classcancel_title= Label(root, text='Class Replacement Page', font=("Arial", 18))
            classcancel_title.grid(row=0, column=0, sticky=W, pady=5, columnspan=2)

            subjname_lbl= Label(root, text='Subject', font=f)
            subjname_lbl.grid(row=1, column=0, sticky=W, pady=5)

            subj = Entry(root, font=f, width=15)
            subj.grid(row=1, column=1, sticky=W, pady=5)

            date_lbl= Label(root, text='Date', font=f)
            date_lbl.grid(row=2, column=0, sticky=W, pady=5)

            date=Entry(root, font=f, width=15)
            date.grid(row=2, column=1, sticky=W, pady=5)

            time_lbl= Label(root, text='Time', font=f)
            time_lbl.grid(row=3, column=0, sticky=W, pady=5)

            time =Entry(root, font=f, width=15)
            time.grid(row=3, column=1, sticky=W, pady=5)

            venue_lbl=Label(root, text='Venue', font=f)
            venue_lbl.grid(row=4, column=0, sticky=W, pady=5)

            venue =Entry(root, font=f, width=15)
            venue.grid(row=4, column=1, sticky=W, pady=5)


            add_event_btn=Button(root,height=1,width=5, command=insert_record, text='Add', font=f)
            add_event_btn.grid(row=6, column=1,sticky=W, pady=5, columnspan=2)

        #edit replacement of class
        def edit_classreplace():
            top = Toplevel(ws)
            top.geometry('855x450')
            top.title("Edit Class Replacement")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Edit Class Replacement', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=300, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            # my_tree.tag_configure('odd', background='grey82')
            # my_tree.tag_configure('even', background='grey79')

            my_tree['columns'] = ('ID', 'Subject', 'Date', 'Time', 'Venue')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Subject', width=180, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
            my_tree.column('Venue', width=160, anchor=CENTER, stretch=NO)

            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Subject', text='Subject', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Venue', text='Venue', anchor=CENTER)

            #show events from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, Subject, Date, Time, Venue from ClassReplace ''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #entry boxes for editing db
            id_lbl = Label(top, text='ID', font=f)
            id_lbl.place(x=35, y=320)
            id_entry = Entry(top, width=5, font=f)
            id_entry.place(x=150, y=320)

            subjname_lbl = Label(top, text="Subject", font=f)
            subjname_lbl.place(x=35, y=360)
            subjname_entry = Entry(top, width=16, font=f)
            subjname_entry.place(x=150,y=360)

            date_lbl = Label(top, text="Date", font=f)
            date_lbl.place(x=35, y=400)
            date_entry = Entry(top, width=16, font=f)
            date_entry.place(x=150,y=400)

            time_lbl = Label(top, text="Time", font=f)
            time_lbl.place(x=360, y=320)
            time_entry = Entry(top, width=16, font=f)
            time_entry.place(x=475,y=320)

            venue_lbl = Label(top, text="Venue", font=f)
            venue_lbl.place(x=360, y=360)
            venue_entry = Entry(top, width=16, font=f)
            venue_entry.place(x=475,y=360)
            

            #Show record
            def show_record(e):
                # Clear entry boxes
                id_entry.delete(0,END)
                subjname_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0, END)
                venue_entry.delete(0, END)             

                # Grab the record number
                selected = my_tree.focus()
                # Grab record values
                values= my_tree.item(selected, 'values')

                # outputs to entry boxes
                id_entry.insert(0, values[0])
                subjname_entry.insert(0, values[1])
                date_entry.insert(0, values[2])
                time_entry.insert(0, values[3])
                venue_entry.insert(0, values[4])

            # Update record
            def update_record():
                # Grab the record number
                selected = my_tree.focus()
                # Update record
                my_tree.item(selected, text="", values=(id_entry.get(), subjname_entry.get(), date_entry.get(), time_entry.get(), venue_entry.get()))
                conn = sqlite3.connect('eventsystem.db')
                c = conn.cursor()

                # Update the database

                c.execute("""UPDATE ClassReplace SET
                    Subject = :subj,
                    Date = :date,
                    Time = :time,
                    Venue = :venue

                    WHERE id = :id""",
                    {
                        'id' : id_entry.get(),
                        'subj': subjname_entry.get(),
                        'date': date_entry.get(),
                        'time': time_entry.get(),
                        'venue': venue_entry.get()
                    })

                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear entry boxes
                id_entry.delete(0,END)
                subjname_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0, END)
                venue_entry.delete(0, END)

            #Edit button
            edit_btn=tk.Button(top,height=1, width=6, font=f, command=update_record, text='Edit')
            edit_btn.place(x=700, y=360)

            my_tree.bind('<ButtonRelease-1>', show_record)

        #delete replacement of class
        def del_classreplace():
            top = Toplevel(ws)
            top.geometry('890x450')
            top.title("Delete Class Replacement")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Delete Class Replacement', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=230, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            # my_tree.tag_configure('odd', background='grey82')
            # my_tree.tag_configure('even', background='grey79')

            my_tree['columns'] = ('ID', 'Subject', 'Date', 'Time', 'Venue')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Subject', width=220, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Venue', width=230, anchor=CENTER, stretch=NO)


            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Subject', text='Subject', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Venue', text='Venue', anchor=CENTER)


            #show class cancellation from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, Subject, Date, Time, Venue from ClassReplace ''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #entry boxes for editing db
            id_lbl = Label(top, text='ID', font=f)
            id_lbl.place(x=35, y=320)
            id_entry = Entry(top, width=5, font=f)
            id_entry.place(x=150, y=320)

            subj_lbl = Label(top, text="Subject", font=f)
            subj_lbl.place(x=35, y=360)
            subj_entry = Entry(top, width=16, font=f)
            subj_entry.place(x=150,y=360)

            date_lbl = Label(top, text="Date", font=f)
            date_lbl.place(x=35, y=400)
            date_entry = Entry(top, width=16, font=f)
            date_entry.place(x=150,y=400)

            time_lbl = Label(top, text="Time", font=f)
            time_lbl.place(x=360, y=320)
            time_entry = Entry(top, width=16, font=f)
            time_entry.place(x=475,y=320)

            venue_lbl = Label(top, text="Venue", font=f)
            venue_lbl.place(x=360, y=360)
            venue_entry = Entry(top, width=16, font=f)
            venue_entry.place(x=475,y=360)

            #Show record
            def show_record(e):
                # Clear entry boxes
                id_entry.delete(0,END)
                subj_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0,END)
                venue_entry.delete(0,END)
                

                # Grab the record number
                selected = my_tree.focus()
                # Grab record values
                values= my_tree.item(selected, 'values')

                # outputs to entry boxes
                id_entry.insert(0, values[0])
                subj_entry.insert(0, values[1])
                date_entry.insert(0, values[2])
                time_entry.insert(0, values[3])
                venue_entry.insert(0, values[4])
                

            # Update record
            def del_record():
                x = my_tree.selection()[0]
                my_tree.delete(x)

                conn = sqlite3.connect('eventsystem.db')
                c = conn.cursor()

                # Delete From Database
                c.execute("DELETE from ClassReplace WHERE oid=" + id_entry.get())

                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear entry boxes
                id_entry.delete(0,END)
                subj_entry.delete(0, END)
                date_entry.delete(0, END)
                time_entry.delete(0,END)
                venue_entry.delete(0,END)

                # Add a little message box for fun
                messagebox.showinfo("Alert", "Class Replacement Deleted.")
                

            #Delete button
            del_btn=tk.Button(top,height=1, width=6, font=f, command=del_record, text='Delete')
            del_btn.place(x=790, y=360)

            my_tree.bind('<ButtonRelease-1>', show_record)

        #class cancel add, edit, delete btns
        classcancel_lbl = Label(whatnew_frame, text ='Class Cancellation notice', font = f )
        classcancel_lbl.grid(row=1, column=1, sticky=W, pady=5, padx=10, columnspan=3)

        add_classcancel_btn = tk.Button(whatnew_frame,height=1, width=7, font=f, text='Add', command=add_classcancel)
        add_classcancel_btn.grid(row=2, column=1, sticky=W, pady=5, padx=10)

        edit_classcancel_btn = tk.Button(whatnew_frame,height=1, width=7, font=f, text='Edit', command=edit_classcancel)
        edit_classcancel_btn.grid(row=2, column=2, sticky=W, pady=5, padx=10)

        delete_classcancel_btn = tk.Button(whatnew_frame,height=1, width=7, font=f, text='Delete', command=del_classcancel)
        delete_classcancel_btn.grid(row=2, column=3, sticky=W, pady=5, padx=10)

        #add, edit, delete class replacement btns
        classreplace_lbl = Label(whatnew_frame, text ='Class Replacement notice', font = f )
        classreplace_lbl.grid(row=3, column=1, sticky=W, pady=5, padx=10, columnspan=3)

        add_classreplace_btn = tk.Button(whatnew_frame,height=1, width=7, font=f, text='Add', command=add_classreplace)
        add_classreplace_btn.grid(row=4, column=1, sticky=W, pady=5, padx=10)

        edit_classreplace_btn = tk.Button(whatnew_frame,height=1, width=7, font=f, text='Edit', command=edit_classreplace)
        edit_classreplace_btn.grid(row=4, column=2, sticky=W, pady=5, padx=10)

        delete_classreplace_btn = tk.Button(whatnew_frame,height=1, width=7, font=f, text='Delete', command=del_classreplace)
        delete_classreplace_btn.grid(row=4, column=3, sticky=W, pady=5, padx=10)

        #show users registered events

        #admin view as normal user
        def view_user():
            controller.show_frame(Homepage)
        viewuser_btn=tk.Button(self,height=1, width=10, font=f, command=view_user, text='View as User')
        viewuser_btn.place(x=945, y=135)

        #Logout
        def log_out():
            controller.show_frame(Loginpage)
            messagebox.showinfo('Logout Status', 'Logged out successfully!')
        logout_btn=tk.Button(self, height=1, width=9, font=f, command=log_out, text='Logout')
        logout_btn.place(x=950 ,y=180)
        

class Homepage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='antique white')
        self.controller=controller 
        global login_details

        #inti logo
        inti_logo(self)
        #top buttons
        top_buttons(self,controller)
        #show date and clock
        clock(self)
        today_date(self)

        #Homepage
        #Homepage title
        w = Label(self, text ='Homepage', font = ('Arial', 28) , bg='antique white')
        w.pack()
        w.place(x=480, y=80)
        
        #Welcome name title
        self.lbl_welcome = Label(self, text ='', font = ('Arial', 20), bg='antique white' )
        self.lbl_welcome.pack()
        self.lbl_welcome.place(x=40, y=115)

        #Activity frame filled with registered events and comp
        self.activity_frame = Frame(self, height=8, width=100, bg='antique white')
        self.activity_frame.place(x=40, y=200)

        #Registered events frame
        self.regevents_frame = Frame(self.activity_frame, bd=2, height=8, width=100, bg='antique white', relief=SOLID)
        self.regevents_frame.pack(pady=1, anchor=W)

        #Registered Competitions frame
        self.regcomp_frame = Frame(self.activity_frame, bd=2, height=8, width=100, bg='antique white', relief=SOLID)
        self.regcomp_frame.pack(pady=140, anchor=W)

        regcomp_title = Label(self.regcomp_frame, text ='Registered Competitions', font = ('Arial', 20), bg='antique white' )
        regcomp_title.grid(row=0, column=0, sticky=N, pady=5, columnspan=3)

        compname_lbl = Label(self.regcomp_frame, text ='Comp Name', font = ('Arial', 14,'bold'),bg='antique white' )
        compname_lbl.grid(row=1, column=0, sticky=W, pady=5, padx=20 )

        date_lbl= Label(self.regcomp_frame, text ='Date', font = ('Arial', 14,'bold'),bg='antique white')
        date_lbl.grid(row=1, column=1, sticky=W, pady=5, padx=55)

        time_lbl= Label(self.regcomp_frame, text ='Time', font = ('Arial', 14,'bold'),bg='antique white')
        time_lbl.grid(row=1, column=2, sticky=W, pady=5, padx=55 )

        #get user email from entry
        getuser_lbl=Label(self, text='Enter email to view \nregistered activites', font=('Arial',12),bg='antique white')
        getuser_lbl.place(x=40, y=150)
        useremail=Entry(self, font=f, width=15)
        useremail.place(x=180, y=160)

        def view_activites():
            self.regcomp_frame.forget()
            self.regevents_frame.forget()

            self.regevents_frame = Frame(self.activity_frame, bd=2, height=8, width=100, bg='antique white', relief=SOLID)
            self.regevents_frame.pack(pady=1, anchor=W)
            self.regcomp_frame = Frame(self.activity_frame, bd=2, height=8, width=100, bg='antique white', relief=SOLID)
            self.regcomp_frame.pack(pady=140, anchor=W)

            #registered events columns
            regevents_title = Label(self.regevents_frame, text ='Registered Events', font = ('Arial', 20), bg='antique white' )
            regevents_title.grid(row=0, column=0, sticky=N, pady=5, columnspan=3)

            eventname_lbl = Label(self.regevents_frame, text ='Event Name', font = ('Arial', 14,'bold'),bg='antique white' )
            eventname_lbl.grid(row=1, column=0, sticky=W, pady=5, padx=20 )

            date_lbl= Label(self.regevents_frame, text ='Date', font = ('Arial', 14,'bold'),bg='antique white')
            date_lbl.grid(row=1, column=1, sticky=W, pady=5, padx=55)

            time_lbl= Label(self.regevents_frame, text ='Time', font = ('Arial', 14,'bold'),bg='antique white')
            time_lbl.grid(row=1, column=2, sticky=W, pady=5, padx=55 )

            #registered competitions columns
            regcomp_title = Label(self.regcomp_frame, text ='Registered Competitions', font = ('Arial', 20), bg='antique white' )
            regcomp_title.grid(row=0, column=0, sticky=N, pady=5, columnspan=3)

            compname_lbl = Label(self.regcomp_frame, text ='Comp Name', font = ('Arial', 14,'bold'),bg='antique white' )
            compname_lbl.grid(row=1, column=0, sticky=W, pady=5, padx=20 )

            date_lbl= Label(self.regcomp_frame, text ='Date', font = ('Arial', 14,'bold'),bg='antique white')
            date_lbl.grid(row=1, column=1, sticky=W, pady=5, padx=55)

            time_lbl= Label(self.regcomp_frame, text ='Time', font = ('Arial', 14,'bold'),bg='antique white')
            time_lbl.grid(row=1, column=2, sticky=W, pady=5, padx=55 )
            
            #connect to database to show events
            email=useremail.get()
            conn = sqlite3.connect('eventsystem.db')
            cursor=conn.cursor()

            regevent_set=cursor.execute('''SELECT EventRegistrationStudent.EventName, EventRegistrationAdmin.Date, EventRegistrationAdmin.Time
                                            FROM EventRegistrationStudent
                                            INNER JOIN EventRegistrationAdmin ON EventRegistrationStudent.EventName LIKE EventRegistrationAdmin.EventName 
                                            WHERE EventRegistrationStudent.email =?''',(email,))
            # e_set=cursor.fetchall()
            i=0 # row value inside the loop 
            for EventRegistrationAdmin in regevent_set: 
                for j in range(len(EventRegistrationAdmin)):
                    eventdetails = tk.Label(self.regevents_frame, width=18, height=2, font=('Arial', 11),text=EventRegistrationAdmin[j], pady=5, relief='solid', wraplength=180, justify=CENTER) 
                    eventdetails.grid(row=i+2, column=j)
                i=i+1


            #connect to database to show competitions
            # conn = sqlite3.connect('eventsystem.db')
            # cursor=conn.cursor()
            regcomp_set=cursor.execute('''SELECT CompRegistrationStudent.CompetitionName, CompRegistrationAdmin.Date, CompRegistrationAdmin.Time
                                            FROM CompRegistrationStudent
                                            INNER JOIN CompRegistrationAdmin ON CompRegistrationStudent.CompetitionName LIKE CompRegistrationAdmin.CompetitionName
                                            WHERE CompRegistrationStudent.email =?''',(email,))
            # e_set=cursor.fetchall()
            i=0 # row value inside the loop 
            for CompRegistrationAdmin in regcomp_set: 
                for j in range(len(CompRegistrationAdmin)):
                    compdetails = tk.Label(self.regcomp_frame, width=18, height=2, font=('Arial', 11),text=CompRegistrationAdmin[j], pady=5, relief='solid', wraplength=180, justify=CENTER) 
                    compdetails.grid(row=i+2, column=j)
                i=i+1
        view_activites()
        
        view_btn=Button(self, text='View', font=f, width=5, height=1, command=view_activites)
        view_btn.place(x=356, y=150)

        # re_btn = Button(self, text="Refresh", font=f, width=8, height=1, command=view_activites_again)
        # re_btn.place(x=425, y=150)


        #Calendar
        cal_frame = Frame(self, bd=1, height=8, width=100, bg='antique white' )
        cal_frame.place(x=725, y=155)

        
        today=datetime.date.today()
        events_cal = Calendar(cal_frame, font=f, selectmode = 'day', date_pattern='dd/mm/yyyy', year = today.year, month = today.month, day = today.day, background="SkyBlue1", 
                                            disabledbackground="LightSteelBlue1", bordercolor="black", headersbackground="LightSkyBlue2", normalbackground="DeepSkyBlue2", weekendbackground='DeepSkyBlue3', 
                                                                       selectbackground='black', othermonthbackground='lightblue1', othermonthwebackground='lightblue1', foreground='black', normalforeground='black', weekendforeground='black', headersforeground='black')
        events_cal.pack(fill='both', expand=True)

        event_frame = Frame(self, bd=1, height=8, width=100, bg='antique white' )
        comp_frame = Frame(self, bd=1, height=8, width=100, bg='antique white' )
        
        def show_evnt():
            #show eventsframe
            event_frame.pack(side='right', anchor=S, pady=240)
            comp_frame.forget()

            eventname_lbl = Label(event_frame, text ='Event Name', font = ('Arial', 14,'bold'),bg='antique white' )
            eventname_lbl.grid(row=1, column=0, sticky=W, pady=5, padx=28 )

            date_lbl= Label(event_frame, text ='Date', font = ('Arial', 14,'bold'),bg='antique white')
            date_lbl.grid(row=1, column=1, sticky=W, pady=5, padx=55 )

            #connect to database to show events
            conn = sqlite3.connect('eventsystem.db')
            cursor=conn.cursor()
            e_set=cursor.execute('''SELECT EventName,Date FROM EventRegistrationAdmin WHERE  `EventName` LIKE ? OR `Date` LIKE ? LIMIT 0,5''', ('%'+(events_cal.get_date())+'%', '%'+(events_cal.get_date())+'%'))
            # e_set=cursor.fetchall()
            i=0 # row value inside the loop 
            for EventRegistrationAdmin in e_set: 
                for j in range(len(EventRegistrationAdmin)):
                    eventdetails = tk.Label(event_frame, width=23, height=2, font=('Arial', 11),text=EventRegistrationAdmin[j], pady=5, relief='solid', wraplength=180, justify=CENTER) 
                    eventdetails.grid(row=i+2, column=j)
                i=i+1

        def show_comp():
            #show compframe
            comp_frame.pack(side='right', anchor=S, pady=240)
            event_frame.forget()
            
            compname_lbl = Label(comp_frame, text ='Comp Name', font = ('Arial', 14,'bold'),bg='antique white' )
            compname_lbl.grid(row=1, column=0, sticky=W, pady=5, padx=28 )

            date_lbl= Label(comp_frame, text ='Date', font = ('Arial', 14,'bold'),bg='antique white')
            date_lbl.grid(row=1, column=1, sticky=W, pady=5, padx=55 )

            #connect to database to show events
            conn = sqlite3.connect('eventsystem.db')
            cursor=conn.cursor()
            c_set=cursor.execute('''SELECT CompetitionName,Date FROM CompRegistrationAdmin WHERE  `CompetitionName` LIKE ? OR `Date` LIKE ? LIMIT 0,5''', ('%'+(events_cal.get_date())+'%', '%'+(events_cal.get_date())+'%'))
            # e_set=cursor.fetchall()
            i=0 # row value inside the loop 
            for CompRegistrationAdmin in c_set: 
                for j in range(len(CompRegistrationAdmin)):
                    eventdetails = tk.Label(comp_frame, width=23, height=2, font=('Arial', 11),text=CompRegistrationAdmin[j], pady=5, relief='solid', wraplength=180, justify=CENTER) 
                    eventdetails.grid(row=i+2, column=j)
                i=i+1
        
        # Add Button and Label
        Button(cal_frame, text = "Show Events",command = show_evnt, font=f).pack(side='left', pady=5,padx=5)
        Button(cal_frame, text = "Show Comp",command = show_comp, font=f).pack(side='right', pady=5,padx=5)


class Announcements(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='antique white')


        #inti logo
        inti_logo(self)
        #top buttons
        top_buttons(self,controller)
        #show date and clock
        clock(self)
        today_date(self)

        #Announcements Title
        w = Label(self, text ='Announcements', font = ('Arial', 28), bg='antique white' )
        w.pack()
        w.place(x=445, y=80)

        #Lost and found Frame
        lf_frame = Frame(self, bd=2, bg='antique white', relief=SOLID)
        lf_frame.place(x=30, y=135)

        #Lost and FOund word
        lf_lbl= Label(lf_frame, text ='Lost & Found \U0001F631', font =('Rockwell',20), bg='antique white')
        lf_lbl.grid(row=1, column=1, columnspan=2, sticky=W, pady=5)

        #show image from database
        conn = sqlite3.connect('eventsystem.db')
        cursor=conn.cursor()
        l_set=cursor.execute('''SELECT id, Image, Description FROM LostFound''')
        l_set=cursor.fetchall()
        
        global rec_no
        rec_no=0
        img2= Image.open(io.BytesIO(l_set[rec_no][1]))
        img2 = img2.resize((300,220))
        img2 = ImageTk.PhotoImage(img2)
        lf_image=tk.Label(lf_frame, image=img2)
        lf_image.grid(row=2, column=0, columnspan=2, sticky=W, pady=5)
        lf_image.image=img2

        lf_details=Label(lf_frame, text= "Description: "+ l_set[rec_no][2], wraplength=225, font=f)
        lf_details.grid(row=2, column=2, columnspan=2, sticky=W, pady=5)

        def previous():
            global lf_image
            global rec_no
            if rec_no>0:
                rec_no=rec_no-1

            if rec_no==0:
                prev_btn.config(state=DISABLED)
            else:
                prev_btn.config(state=NORMAL)
                next_btn.config(state=NORMAL)

            img2= Image.open(io.BytesIO(l_set[rec_no][1]))
            img2 = img2.resize((300,220))
            img2 = ImageTk.PhotoImage(img2)
            lf_image=tk.Label(lf_frame, image=img2)
            lf_image.grid(row=2, column=0, columnspan=2, sticky=W, pady=5)
            lf_image.image=img2
            
            lf_details.config(text="Description: "+ l_set[rec_no][2])

        def next():
            global lf_image
            global rec_no
            if rec_no < (len(l_set)-1):
                rec_no=rec_no+1
            if rec_no == (len(l_set)-1):
                next_btn.config(state=DISABLED)
            else:
                next_btn.config(state=NORMAL)
                prev_btn.config(state=NORMAL)
        
            img2= Image.open(io.BytesIO(l_set[rec_no][1]))
            img2 = img2.resize((300,220))
            img2 = ImageTk.PhotoImage(img2)
            lf_image=tk.Label(lf_frame, image=img2)
            lf_image.grid(row=2, column=0, columnspan=2, sticky=W, pady=5)
            lf_image.image=img2

            lf_details.config(text="Description: "+ l_set[rec_no][2])

        # #Previous image button
        prev_btn=tk.Button(lf_frame, height=1, width=4, text="<<",  command=previous, font=f)
        prev_btn.grid(row=3, column=0, sticky=W, pady=5, padx=5)
        # #Next image button
        next_btn=tk.Button(lf_frame, height=1, width=4, text=">>", command=next, font=f)
        next_btn.grid(row=3, column=3, sticky=W, pady=5, padx=5)


        # #Countdown frame
        self.countdown_frame = Frame(self, bd=2, bg='antique white', relief=SOLID)
        self.countdown_frame.place(x=30, y=485)

        # #Countdown word (take from database)
        ctdwn_title = Label(self.countdown_frame, text ='Countdown \U0001F912', font = ('Rockwell', 20), bg='antique white' )
        ctdwn_title.pack(side='top')

        self.sub_countdown_frame = Frame(self.countdown_frame, bd=2, bg='antique white', relief=SOLID)
        self.sub_countdown_frame.pack(pady=50)

        def show_countdown():
            self.sub_countdown_frame.forget()

            self.sub_countdown_frame = Frame(self.countdown_frame, bd=2, bg='antique white', relief=SOLID)
            self.sub_countdown_frame.pack(pady=10)

            conn = sqlite3.connect('eventsystem.db')
            cursor=conn.cursor()
            r_set=cursor.execute('''SELECT EventName, Year, Month, Date FROM EventCountdown LIMIT 0,5''')
            r_set=cursor.fetchall()

            i=0
            for EventCountdown in r_set:
                    countdown_details = Label(self.sub_countdown_frame, text =EventCountdown[0]+' '+ str(EventCountdown[3])+'/'+str(EventCountdown[2])+'/'+str(EventCountdown[1]), font = ('Rockwell', 15), bg='antique white',pady=5 )
                    countdown_details.grid(row=i+2, column=0)
                
                    # event date
                    day_of_year = date(EventCountdown[1],EventCountdown[2],EventCountdown[3]).timetuple().tm_yday

                    # #Countdown
                    today=date.today()
                    todays_day_number = int(today.strftime("%j"))

                    # #Calculate days left
                    days_left = day_of_year - todays_day_number

                    # #Days left text
                    countdown_label = Label(self.sub_countdown_frame, bg='antique white', text=f'({days_left} days left!)' , font=('Arial', 15, 'bold'), fg='red')
                    countdown_label.grid(row=i+2, column=1)
                    i+=1
        show_countdown()

        #refresh button
        re_countdown_btn=Button(self.countdown_frame, height=1, width=8, text="Refresh", command= show_countdown, font=f)
        re_countdown_btn.pack(side='right')
        

        #What's new frame
        whatnew_frame = Frame(self, bd=2, bg='antique white', relief=SOLID)
        whatnew_frame.place(x=580, y=135)

        #What's new section
        w = Label(whatnew_frame, height=1, width=15, text ='What\'s new \U0001F632', font =('Rockwell',20), bg='antique white').grid(row=1, column=1, columnspan=2, sticky=W, pady=5)

        #register EVENT FORM for students popup 
        def open_popup2():
            top= Toplevel(ws)
            top.geometry("500x550")
            top.title("Event Registration Form")
            top.resizable(False,False)

            conn = sqlite3.connect('eventsystem.db')
            cursor=conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS EventRegistrationStudent (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                                Fullname TEXT NOT NULL,
                                                                                StudentID NUMBER NOT NULL,
                                                                                Email TEXT NOT NULL,
                                                                                Gender TEXT NOT NULL, 
                                                                                EventName TEXT NOT NULL, 
                                                                                LevelOfStudy TEXT NOT NULL,
                                                                                Vaccination TEXT NOT NULL,
                                                                                ContactNo NUMBER NOT NULL,
                                                                                FOREIGN KEY (Fullname)
                                                                                REFERENCES userdetails (name))''')
            conn.commit()

            gender = StringVar()
            gender.set('Male')
            levelofstudy=StringVar()
            levelofstudy.set('Select')
            vac= StringVar()
            vac.set('Yes')
            
            def insert_record():
                check_counter=0
                warn = " "
                if name1.get() == "":
                    warn = 'Please enter a name.'
                else:
                    check_counter += 1
                        
                if studentID.get() == "":
                    warn='Please enter student ID.'
                else:
                    check_counter += 1

                if email.get() == "":
                    warn = 'Please enter an email.'
                else:
                    check_counter += 1

                if gender.get() == "":
                    warn = 'Select Gender'
                else:
                    check_counter += 1

                if eventname.get() == "":
                    warn = 'Enter Event Name.'
                else:
                    check_counter += 1

                if levelofstudy.get() == "Select":
                    warn = 'Select Level of Study'
                else:
                    check_counter += 1

                if vac.get() == "":
                    warn = 'Select Vaccination'
                else:
                    check_counter += 1

                if Contact1.get() == "":
                    warn = 'Please enter contact number.'
                else:
                    check_counter += 1

                if check_counter == 8:
                        try:
                            conn= sqlite3.connect('eventsystem.db')
                            cursor=conn.cursor()
                            cursor.execute("INSERT INTO EventRegistrationStudent VALUES (:id, :Fullname, :StudentID, :Email, :Gender, :EventName, :LevelOfStudy, :Vaccination, :ContactNo)", {
                            'id':None,
                            'Fullname':name1.get(),
                            'StudentID':studentID.get(),
                            'Email':email.get(),
                            'Gender':gender.get(),
                            'EventName': eventname.get(),
                            'LevelOfStudy':levelofstudy.get(),
                            'Vaccination':vac.get(),
                            'ContactNo':Contact1.get()
                            })
                            conn.commit()
                            messagebox.showinfo('Confirmation', 'Event Registered')
                            top.destroy()

                        except Exception as ep:
                            messagebox.showerror('', ep)

                else:
                    messagebox.showerror('Error', warn)


            #registration form widgets
            label_0 = Label(top, text=" Event Registration Form",width=20,font=("bold", 22))
            label_0.place(x=85,y=30)
                    
                    
            label_1 = Label(top, text="Full Name",width=20,font=("bold", 10))
            label_1.place(x=75,y=100)
                    
            name1 = Entry(top)
            name1.place(x=240,y=100)

            label_2 = Label(top, text="Student ID",width=20,font=("bold", 10))
            label_2.place(x=75,y=150)
                    
            studentID = Entry(top)
            studentID.place(x=240,y=150)
                    
            label_3 = Label(top, text="Email",width=20,font=("bold", 10))
            label_3.place(x=71,y=200)
                    
            email = Entry(top)
            email.place(x=240,y=200)

            label_4 = Label(top, text="Contact Number",width=20,font=("bold", 10))
            label_4.place(x=70,y=250)

            Contact1 = Entry(top)
            Contact1.place(x=240,y=250)
                    
            label_5 = Label(top, text="Gender",width=20,font=("bold", 10))
            label_5.place(x=70,y=300)
                    
            Radiobutton(top, text="Male",padx = 5, variable=gender, value='Male').place(x=235,y=300)
            Radiobutton(top, text="Female",padx = 20, variable=gender, value='Female').place(x=290,y=300)

            eventname = Label(top, text="Event Name",width=20,font=("bold", 10))
            eventname.place(x=70,y=350)

            eventname = Entry(top)
            eventname.place(x=240,y=350)
                    
            label_7 = Label(top, text="Level of Study",width=20,font=("bold", 10))
            label_7.place(x=70,y=400)
                    
            list1 = ['Certificate','Foundation', 'Diploma', 'Bachelor Degree', 'Masters', 'Working', 'Doctorate'];
                    
            droplist=OptionMenu(top,levelofstudy, *list1)
            droplist.config(width=15)
            # LevelOfStudy.set('select') 
            droplist.place(x=240,y=400)
                    
            label_8 = Label(top, text="Vaccination",width=20,font=("bold", 10))
            label_8.place(x=70,y=450)
            # var2= IntVar()
            Radiobutton(top, text="Yes",padx = 5, variable=vac, value='Yes').place(x=235,y=450)
            Radiobutton(top, text="No",padx = 20, variable=vac, value='No').place(x=290,y=450)
                    
            Button(top, text='Submit',width=20,bg='red',fg='white', cursor='hand2', command=insert_record).place(x=180,y=500)

        #connect to class cancel database
        conn = sqlite3.connect('eventsystem.db')
        cursor=conn.cursor()
        r_set=cursor.execute('''SELECT * FROM ClassCancel ORDER BY ROWID ASC LIMIT 1''')
        r_set=cursor.fetchone()

        #cancellation of class frame
        w = Label(whatnew_frame, text ='\U0000274C Cancellation\nof Class', font = ('Rockwell', 15), fg='red').grid(row=2, column=0, sticky=W, pady=5)

        #class cancellation description (take from database)
        w = Label(whatnew_frame, text =
        'Subject: '+ r_set[1] +
         '\n Date: ' + r_set[2] + 
        ' \n Time: ' + r_set[3] + 
        '\n Venue: ' + r_set[4] +
        '\n Class Replacement '+ r_set[5], font = ('Arial', 12) ).grid(row=2, column=1, columnspan=2, sticky=W, pady=5) 

        #connect to class replace database
        conn = sqlite3.connect('eventsystem.db')
        cursor=conn.cursor()
        q_set=cursor.execute('''SELECT * FROM ClassReplace ORDER BY ROWID ASC LIMIT 1''')
        q_set=cursor.fetchone()

        #replacement of class frame
        w = Label(whatnew_frame, text ='\U000026A0 Replacement\nof Class', font = ('Rockwell', 15), fg='red').grid(row=3, column=0, sticky=W, pady=5)

        #class replacement description (take from database)
        w = Label(whatnew_frame, text =
        'Subject: '+ q_set[1] +
         '\n Date: ' + q_set[2] + 
        ' \n Time: ' + q_set[3] + 
        '\n Venue: ' + q_set[4],
         font = ('Arial', 12) ).grid(row=3, column=1, columnspan=2, sticky=W, pady=5) 

        #connect to events database
        conn = sqlite3.connect('eventsystem.db')
        cursor=conn.cursor()
        r_set=cursor.execute('''SELECT * FROM EventRegistrationAdmin ORDER BY ROWID ASC LIMIT 1''')
        r_set=cursor.fetchone()

        # #wcit image     (take from database)
        image=Image.open(io.BytesIO(r_set[12]))
        img3=image.resize((200,175))
        my_img3=ImageTk.PhotoImage(img3)
        whatnew_image=tk.Label(whatnew_frame, image=my_img3)
        whatnew_image.grid(row=4, column=0, rowspan=2, sticky=W, pady=5)
        whatnew_image.image=my_img3

        # #wcit description      (take from daatbase)
        w = Label(whatnew_frame, text =
        'Event Name: '+r_set[5]+
        '\nDate: '+ r_set[8]+
        '\nTime: '+ r_set[9]+
        '\nLocation: '+r_set[10]+
        '\nRequirements: '+r_set[11] , font = ('Arial', 12) ).grid(row=4, column=1, columnspan=2, sticky=W)


        #link clicked from learn more button
        def learn_more():
            top= Toplevel(ws)
            top.geometry("650x220")
            top.title("Learn more...")
            Label(top, text= r_set[6], wraplength=700,  font=f).place(x=30,y=20)
            top.resizable(False,False)
           

        #learn more button for event 
        button10=tk.Button(whatnew_frame, height=1, width=10, text="Learn More...", command= learn_more, font=f)
        button10.grid(row=5, column=1,  sticky=W, pady=5)

        #register button for event
        button11=tk.Button(whatnew_frame, height=1, width=10, text="Register", command= open_popup2, font=f)
        button11.grid(row=5, column=2,sticky=W, pady=5)

        #connect to database
        conn = sqlite3.connect('eventsystem.db')
        cursor=conn.cursor()
        p_set=cursor.execute('''SELECT * FROM EventRegistrationAdmin ORDER BY ROWID ASC LIMIT 1,1''')
        p_set=cursor.fetchone()
        

        #prom image     (take from database)
        image=Image.open(io.BytesIO(p_set[12]))
        img4=image.resize((200,175))
        my_img4=ImageTk.PhotoImage(img4)
        whatnew2_image=tk.Label(whatnew_frame, image=my_img4)
        whatnew2_image.grid(row=6, column=0, rowspan=2, sticky=W, pady=5)
        whatnew2_image.image=my_img4

        #prom details     (take from database)
        w = Label(whatnew_frame, text =
        'Event Name: '+p_set[5]+
        '\nDate: '+ p_set[8]+
        '\nTime: '+ p_set[9]+
        '\nLocation: '+p_set[10]+
        '\nRequirements: '+p_set[11], font = ('Arial', 12) ).grid(row=6, column=1, columnspan=2, sticky=W, pady=5)

        #learn more button popup    (take from database)
        def open_popup3():
            top= Toplevel(ws)
            top.geometry("650x220")
            top.title("Learn more")
            Label(top, text= p_set[6], wraplength=700, font=f).place(x=30,y=20)
            top.resizable(False,False)

        #learn more button
        button12=tk.Button(whatnew_frame, height=1, width=10, text="Learn More...", command= open_popup3, font=f)
        button12.grid(row=7, column=1,sticky=W, pady=5)

        
        #register for prom button
        button13=tk.Button(whatnew_frame, height=1, width=10, text="Register", command= open_popup2, font=f)
        button13.grid(row=7, column=2, sticky=W, pady=5)

class Events(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='antique white')
        
        #inti logo
        inti_logo(self)
        #top buttons
        top_buttons(self,controller)
        #show date and clock
        clock(self)
        today_date(self)

        #Events title
        w = Label(self, text ='Events', font = ('Arial', 28) , bg='antique white')
        w.pack()
        w.place(x=480, y=80)

        label_1 = Label(self, text="Upcoming Events",width=20,font=('Arial',20),background= "Antique White")
        label_1.place(x=10,y=130)

        #upcoming events frame
        self.upevents_frame = Frame(self, bd=2, bg='AntiqueWhite1')
        self.upevents_frame.place(x=35, y=170)

        self.sub_upevents_frame = Frame(self.upevents_frame, bd=2, bg='AntiqueWhite1', relief=SOLID)
        self.sub_upevents_frame.pack(pady=2)

        def show_upevents():
            self.sub_upevents_frame.forget()

            self.sub_upevents_frame = Frame(self.upevents_frame, bd=2, bg='AntiqueWhite1', relief=SOLID)
            self.sub_upevents_frame.pack(pady=2)
            eventname_lbl = Label(self.sub_upevents_frame, text ='Event Name', font = ('Arial', 14,'bold'),bg='antique white' )
            eventname_lbl.grid(row=1, column=0, sticky=W, pady=5, padx=20 )

            date_lbl= Label(self.sub_upevents_frame, text ='Date', font = ('Arial', 14,'bold'),bg='antique white')
            date_lbl.grid(row=1, column=1, sticky=W, pady=5, padx=55 )

            # #show event from db
            conn = sqlite3.connect('eventsystem.db')
            r_set=conn.execute('''SELECT EventName, Date from EventRegistrationAdmin WHERE  Date LIKE '%/12/2022%' OR Date LIKE '%/2023%'  LIMIT 0,5''');
            i=0 # row value inside the loop 
            for EventRegistrationAdmin in r_set: 
                for j in range(len(EventRegistrationAdmin)):
                    e = tk.Label(self.sub_upevents_frame, width=20, height=2, font=('Arial', 11),text=EventRegistrationAdmin[j], pady=5, relief='solid', wraplength=180, justify=CENTER) 
                    e.grid(row=i+2, column=j) 
                i=i+1
        show_upevents()

        #refresh button
        re_upevents_btn=Button(self,text="Refresh",width=7,font=f, command=show_upevents)
        re_upevents_btn.place(x=300,y=130)

        #events frame
        events_frame=Frame(self, bd=2, bg='Antique white', relief=SOLID)
        events_frame.place(x=450, y=170)

        #events slideshow
        conn = sqlite3.connect('eventsystem.db')
        cursor=conn.cursor()
        e_set=cursor.execute('''SELECT EventName, EventDescription, Date, Time, Location, Requirements, EventImage FROM EventRegistrationAdmin''')
        e_set=cursor.fetchall()

        global eventrec_no
        eventrec_no=0
        img1= Image.open(io.BytesIO(e_set[eventrec_no][6]))
        img1 = img1.resize((190,180))
        img1 = ImageTk.PhotoImage(img1)
        e_image=tk.Label(events_frame, image=img1)
        e_image.grid(row=0, column=0, rowspan=4, columnspan=2, sticky=W)
        e_image.image=img1

        e_name=Label(events_frame, text='Name: '+ e_set[eventrec_no][0], font=f, bg='antique white')
        e_name.grid(row=0, column=2, sticky=W)

        e_datetime = Label(events_frame, text='Date/Time: '+ e_set[eventrec_no][2]+ ', '+ e_set[eventrec_no][3], font=f, bg='antique white')
        e_datetime.grid(row=1, column=2, sticky=W)

        e_loc =Label(events_frame, text='Location: '+ e_set[eventrec_no][4], font=f, bg='antique white')
        e_loc.grid(row=2, column=2, sticky=W)

        e_req = Label(events_frame, text='Requirements: '+ e_set[eventrec_no][5], font=f, bg='antique white')
        e_req.grid(row=3, column=2, sticky=W)

        e_des = Label(events_frame, text='Description: '+ e_set[eventrec_no][1], wraplength=442, font=f, justify='left', bg='antique white')
        e_des.grid(row=4, column=2, sticky=W, rowspan=2)

        #event slideshow frame buttons
        def eventreg_popup():
            top= Toplevel(ws)
            top.geometry("500x550")
            top.title("Event Registration Form")
            top.resizable(False,False)

            conn = sqlite3.connect('eventsystem.db')
            cursor=conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS EventRegistrationStudent (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                                Fullname TEXT NOT NULL,
                                                                                StudentID NUMBER NOT NULL,
                                                                                Email TEXT NOT NULL,
                                                                                Gender TEXT NOT NULL, 
                                                                                EventName TEXT NOT NULL, 
                                                                                LevelOfStudy TEXT NOT NULL,
                                                                                Vaccination TEXT NOT NULL,
                                                                                ContactNo NUMBER NOT NULL,
                                                                                FOREIGN KEY (Fullname)
                                                                                REFERENCES userdetails (name))''')
            conn.commit()

            gender = StringVar()
            gender.set('Male')
            levelofstudy=StringVar()
            levelofstudy.set('Select')
            vac= StringVar()
            vac.set('Yes')
            
            def insert_record():
                check_counter=0
                warn = " "
                if name1.get() == "":
                    warn = 'Please enter a name.'
                else:
                    check_counter += 1
                        
                if studentID.get() == "":
                    warn='Please enter student ID.'
                else:
                    check_counter += 1

                if email.get() == "":
                    warn = 'Please enter an email.'
                else:
                    check_counter += 1

                if gender.get() == "":
                    warn = 'Select Gender'
                else:
                    check_counter += 1

                if eventname.get() == "":
                    warn = 'Enter Event Name.'
                else:
                    check_counter += 1

                if levelofstudy.get() == "Select":
                    warn = 'Select Level of Study'
                else:
                    check_counter += 1

                if vac.get() == "":
                    warn = 'Select Vaccination'
                else:
                    check_counter += 1

                if Contact1.get() == "":
                    warn = 'Please enter contact number.'
                else:
                    check_counter += 1

                if check_counter == 8:
                        try:
                            conn= sqlite3.connect('eventsystem.db')
                            cursor=conn.cursor()
                            cursor.execute("INSERT INTO EventRegistrationStudent VALUES (:id, :Fullname, :StudentID, :Email, :Gender, :EventName, :LevelOfStudy, :Vaccination, :ContactNo)", {
                            'id':None,
                            'Fullname':name1.get(),
                            'StudentID':studentID.get(),
                            'Email':email.get(),
                            'Gender':gender.get(),
                            'EventName': eventname.get(),
                            'LevelOfStudy':levelofstudy.get(),
                            'Vaccination':vac.get(),
                            'ContactNo':Contact1.get()
                            })
                            conn.commit()
                            messagebox.showinfo('Confirmation', 'Event Registered')
                            top.destroy()

                        except Exception as ep:
                            messagebox.showerror('', ep)

                else:
                    messagebox.showerror('Error', warn)


            #registration form widgets
            label_0 = Label(top, text=" Event Registration Form",width=20,font=("bold", 22))
            label_0.place(x=85,y=30)
                    
                    
            label_1 = Label(top, text="Full Name",width=20,font=("bold", 10))
            label_1.place(x=75,y=100)
                    
            name1 = Entry(top)
            name1.place(x=240,y=100)

            label_2 = Label(top, text="Student ID",width=20,font=("bold", 10))
            label_2.place(x=75,y=150)
                    
            studentID = Entry(top)
            studentID.place(x=240,y=150)
                    
            label_3 = Label(top, text="Email",width=20,font=("bold", 10))
            label_3.place(x=71,y=200)
                    
            email = Entry(top)
            email.place(x=240,y=200)

            label_4 = Label(top, text="Contact Number",width=20,font=("bold", 10))
            label_4.place(x=70,y=250)

            Contact1 = Entry(top)
            Contact1.place(x=240,y=250)
                    
            label_5 = Label(top, text="Gender",width=20,font=("bold", 10))
            label_5.place(x=70,y=300)
                    
            Radiobutton(top, text="Male",padx = 5, variable=gender, value='Male').place(x=235,y=300)
            Radiobutton(top, text="Female",padx = 20, variable=gender, value='Female').place(x=290,y=300)

            eventname = Label(top, text="Event Name",width=20,font=("bold", 10))
            eventname.place(x=70,y=350)

            eventname = Entry(top)
            eventname.place(x=240,y=350)
                    
            label_7 = Label(top, text="Level of Study",width=20,font=("bold", 10))
            label_7.place(x=70,y=400)
                    
            list1 = ['Certificate','Foundation', 'Diploma', 'Bachelor Degree', 'Masters', 'Working', 'Doctorate'];
                    
            droplist=OptionMenu(top,levelofstudy, *list1)
            droplist.config(width=15)
            # LevelOfStudy.set('select') 
            droplist.place(x=240,y=400)
                    
            label_8 = Label(top, text="Vaccination",width=20,font=("bold", 10))
            label_8.place(x=70,y=450)
            # var2= IntVar()
            Radiobutton(top, text="Yes",padx = 5, variable=vac, value='Yes').place(x=235,y=450)
            Radiobutton(top, text="No",padx = 20, variable=vac, value='No').place(x=290,y=450)
                    
            Button(top, text='Submit',width=20,bg='red',fg='white', cursor='hand2', command=insert_record).place(x=180,y=500)
       
        def previous():
            global e_image
            global eventrec_no
            if eventrec_no>0:
                eventrec_no=eventrec_no-1

            if eventrec_no==0:
                prev_btn.config(state=DISABLED)
            else:
                prev_btn.config(state=NORMAL)
                next_btn.config(state=NORMAL)

            img1= Image.open(io.BytesIO(e_set[eventrec_no][6]))
            img1 = img1.resize((190,180))
            img1 = ImageTk.PhotoImage(img1)
            e_image=tk.Label(events_frame, image=img1)
            e_image.grid(row=0, column=0, rowspan=4, columnspan=2, sticky=W)
            e_image.image=img1

            e_name.config(text="Name: "+ e_set[eventrec_no][0])
            e_datetime.config(text='Date/Time: '+ e_set[eventrec_no][2]+ ', '+ e_set[eventrec_no][3])
            e_loc.config(text='Location: '+ e_set[eventrec_no][4])
            e_req.config(text='Requirements: '+ e_set[eventrec_no][5])
            e_des.config(text='Description: '+ e_set[eventrec_no][1])

        def next():
            global e_image
            global eventrec_no
            if eventrec_no < (len(e_set)-1):
                eventrec_no=eventrec_no+1
            if eventrec_no == (len(e_set)-1):
                next_btn.config(state=DISABLED)
            else:
                next_btn.config(state=NORMAL)
                prev_btn.config(state=NORMAL)

            img1= Image.open(io.BytesIO(e_set[eventrec_no][6]))
            img1 = img1.resize((190,180))
            img1 = ImageTk.PhotoImage(img1)
            e_image=tk.Label(events_frame, image=img1)
            e_image.grid(row=0, column=0, rowspan=4, columnspan=2, sticky=W)
            e_image.image=img1

            e_name.config(text="Name: "+ e_set[eventrec_no][0])
            e_datetime.config(text='Date/Time: '+ e_set[eventrec_no][2]+ ', '+ e_set[eventrec_no][3])
            e_loc.config(text='Location: '+ e_set[eventrec_no][4])
            e_req.config(text='Requirements: '+ e_set[eventrec_no][5])
            e_des.config(text='Description: '+ e_set[eventrec_no][1])

        register_btn = Button(events_frame, height=1, width=7, command=eventreg_popup, text='Register', font=f)
        register_btn.grid(row=4, column=0, columnspan=2, sticky=NS, pady=5)

        prev_btn = Button(events_frame, height=1, width=4, command=previous, text='<<', font=f)
        prev_btn.grid(row=5, column=0,  sticky=NS, pady=5)
        
        next_btn = Button(events_frame, height=1, width=4, command=next, text='>>', font=f)
        next_btn.grid(row=5, column=1, sticky=NS, pady=5)

        #events category
        label_2 = Label(self, text="View events by category:",font=f,background= "Antique White")
        label_2.place(x=70,y=520)

        #category popup
        def edu_popup():
            top = Toplevel(ws)
            top.geometry('900x450')
            top.title("Educational Events")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))
            style.configure('Treeview', rowheight=40)

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Educational Events', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=250, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            my_tree['columns'] = ('ID', 'Event Name', 'Date', 'Time', 'Location')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Event Name', width=300, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
            my_tree.column('Location', width=160, anchor=CENTER, stretch=NO)

            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Event Name', text='Event Name', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Location', text='Location', anchor=CENTER)

            #show events from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, EventName, Date, Time, Location from EventRegistrationAdmin WHERE EventType="Educational"''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #register button
            register_btn = Button(top, height=1, width=7, command=eventreg_popup, text='Register', font=f)
            register_btn.place(x=420, y=390)

        def gathering_popup():
            top = Toplevel(ws)
            top.geometry('900x450')
            top.title("Gathering Events")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))
            style.configure('Treeview', rowheight=40)

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Gathering Events', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=250, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            my_tree['columns'] = ('ID', 'Event Name', 'Date', 'Time', 'Location')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Event Name', width=300, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
            my_tree.column('Location', width=160, anchor=CENTER, stretch=NO)

            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Event Name', text='Event Name', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Location', text='Location', anchor=CENTER)

            #show events from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, EventName, Date, Time, Location from EventRegistrationAdmin WHERE EventType="Gathering"''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #register button
            register_btn = Button(top, height=1, width=7, command=eventreg_popup, text='Register', font=f)
            register_btn.place(x=420, y=390)

        def seminar_popup():
            top = Toplevel(ws)
            top.geometry('900x450')
            top.title("Seminar Events")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))
            style.configure('Treeview', rowheight=40)

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Seminar Events', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=250, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            my_tree['columns'] = ('ID', 'Event Name', 'Date', 'Time', 'Location')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Event Name', width=300, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
            my_tree.column('Location', width=160, anchor=CENTER, stretch=NO)

            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Event Name', text='Event Name', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Location', text='Location', anchor=CENTER)

            #show events from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, EventName, Date, Time, Location from EventRegistrationAdmin WHERE EventType="Seminar"''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #register button
            register_btn = Button(top, height=1, width=7, command=eventreg_popup, text='Register', font=f)
            register_btn.place(x=420, y=390)

        #category pic bind pic to button
        image2=Image.open('educational.png')
        img2=image2.resize((220,150))
        my_img2=ImageTk.PhotoImage(img2)
        science_pic=Label(image=my_img2)
        science_pic.image=my_img2
        
        image3=Image.open('gathering.png')
        img3=image3.resize((220,150))
        my_img3=ImageTk.PhotoImage(img3)
        maths_pic=Label(image=my_img3)
        maths_pic.image=my_img3

        image4=Image.open('seminar.png')
        img4=image4.resize((220,150))
        my_img4=ImageTk.PhotoImage(img4)
        business_pic=Label(image=my_img4)
        business_pic.image=my_img4

        #buttons bind with category pic
        edu_btn = tk.Button(self, image=my_img2, cursor='hand2', command=edu_popup)
        edu_btn.place(x=130,y=550)

        gather_btn = tk.Button(self,image=my_img3, cursor='hand2', command=gathering_popup)
        gather_btn.place(x=430,y=550)

        sem_btn = tk.Button(self, image=my_img4, cursor='hand2', command=seminar_popup)
        sem_btn.place(x=730,y=550)


class Competitions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='antique white')


        #inti logo
        inti_logo(self)
        #top buttons
        top_buttons(self,controller)
        #show date and clock
        clock(self)
        today_date(self)

        #Competitions title
        w = Label(self, text ='Competitions', font = ('Arial', 28) , bg='antique white')
        w.pack()
        w.place(x=465, y=80)

        #view competitions by category label
        w = Label(self, text ='View competitions by category', bg='antique white', font = f )
        w.pack()
        w.place(x=70, y=520)

        #search bar
        label2 = Label(self,text="Search for competitions here",bg= 'antique white', font=f)
        label2.place(x=50,y=160)
        search_entry = Entry(self,width = 20, font=f)
        search_entry.place(x=300,y=160)
        
        def searchcomp():
            top= Toplevel(ws)
            top.geometry("800x400")
            top.title("Search Competitions")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))
            style.configure('Treeview', rowheight=40)

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Search Competitions', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=240, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            my_tree['columns'] = ('Comp Name', 'Date', 'Time', 'Location')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            # my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Comp Name', width=300, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
            my_tree.column('Location', width=160, anchor=CENTER, stretch=NO)

            #column headings
            my_tree.heading('#0', text='', anchor=W)
            # my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Comp Name', text='Event Name', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Location', text='Location', anchor=CENTER)

            #show competitions from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT CompetitionName, Date, Time, Location from CompRegistrationAdmin ''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #fetch data from searchbar
            if search_entry.get() != "":
                my_tree.delete(*my_tree.get_children())
                conn = sqlite3.connect("eventsystem.db")
                c = conn.cursor()
                r_set=c.execute("SELECT CompetitionName, Date, Time, Location, CompetitionType FROM `CompRegistrationAdmin` WHERE `CompetitionName` LIKE ? OR `Date` LIKE ? OR `Time` LIKE ? OR `Location` LIKE ? OR `CompetitionType` LIKE  ?", ('%'+(search_entry.get())+'%', '%'+(search_entry.get())+'%', '%'+(search_entry.get())+'%', '%'+(search_entry.get())+'%', '%'+(search_entry.get())+'%'))
                r_set = c.fetchall()
                for data in r_set:
                    my_tree.insert('', 'end', values=(data))
                c.close()
                conn.close()
            
            #register for competition button
            register_btn = Button(top, height=1, width=7, command=register_comp, text='Register', font=f)
            register_btn.place(x=350, y=345)
                
        searchbtn= Button(self,text= "Search",bg="red",fg="white",font=f, command=searchcomp)
        searchbtn.place(x=535,y=150)
        
        #frame in the middle
        frame2 = Frame(self,bg="white",width=675,height=230, relief=SOLID, bd=2)
        frame2.pack()
        frame2.place(x=135, y=200)

        #competitions slideshow in frame
        #connect to database
        #show image from database
        conn = sqlite3.connect('eventsystem.db')
        cursor=conn.cursor()
        c_set=cursor.execute('''SELECT id, CompetitionName, CompetitionDescription, Date, Time, Location, Requirements, CompImage FROM CompRegistrationAdmin''')
        c_set=cursor.fetchall()

        global comprec_no
        comprec_no=0
        img1= Image.open(io.BytesIO(c_set[comprec_no][7]))
        img1 = img1.resize((200,180))
        img1 = ImageTk.PhotoImage(img1)
        comp_image=tk.Label(frame2, image=img1)
        comp_image.grid(row=0, column=0, rowspan=4, columnspan=2, sticky=W, pady=5)
        comp_image.image=img1

        comp_name=Label(frame2, text='Name: '+ c_set[comprec_no][1], font=f, bg='white')
        comp_name.grid(row=0, column=2, sticky=W)

        comp_datetime = Label(frame2, text='Date/Time: '+ c_set[comprec_no][3]+ ', '+ c_set[comprec_no][4], font=f, bg='white')
        comp_datetime.grid(row=1, column=2, sticky=W)

        comp_loc =Label(frame2, text='Location: '+ c_set[comprec_no][5], font=f, bg='white')
        comp_loc.grid(row=2, column=2, sticky=W)

        comp_req = Label(frame2, text='Requirements: '+ c_set[comprec_no][6], font=f, bg='white')
        comp_req.grid(row=3, column=2, sticky=W)

        comp_des = Label(frame2, text='Description: '+ c_set[comprec_no][2], wraplength=700, font=f, justify='left', bg='white')
        comp_des.grid(row=4, column=2, sticky=W, rowspan=2)

        #def register competition popup
        def register_comp():
                    top= Toplevel(ws)
                    top.geometry("500x550")
                    top.title("Competition Registration Form")
                    top.resizable(False,False)

                    conn = sqlite3.connect('eventsystem.db')
                    cursor=conn.cursor()
                    cursor.execute('''CREATE TABLE IF NOT EXISTS CompRegistrationStudent (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                                        Fullname TEXT NOT NULL,
                                                                                        StudentID NUMBER NOT NULL,
                                                                                        Email TEXT NOT NULL,
                                                                                        Gender TEXT NOT NULL, 
                                                                                        CompetitionName TEXT NOT NULL, 
                                                                                        LevelOfStudy TEXT NOT NULL,
                                                                                        Vaccination TEXT NOT NULL,
                                                                                        ContactNo NUMBER NOT NULL,
                                                                                        FOREIGN KEY (Fullname)
                                                                                        REFERENCES userdetails (name))''')
                    conn.commit()

                    gender = StringVar()
                    gender.set('Male')
                    levelofstudy=StringVar()
                    levelofstudy.set('Select')
                    vac= StringVar()
                    vac.set('Yes')
                    
                    def insert_record():
                        check_counter=0
                        warn = " "
                        if name1.get() == "":
                            warn = 'Please enter a name.'
                        else:
                            check_counter += 1
                                
                        if studentID.get() == "":
                            warn='Please enter student ID.'
                        else:
                            check_counter += 1

                        if email.get() == "":
                            warn = 'Please enter an email.'
                        else:
                            check_counter += 1

                        if gender.get() == "":
                            warn = 'Select Gender'
                        else:
                            check_counter += 1

                        if compname.get() == "":
                            warn = 'Enter Competition Name.'
                        else:
                            check_counter += 1

                        if levelofstudy.get() == "Select":
                            warn = 'Select Level of Study'
                        else:
                            check_counter += 1

                        if vac.get() == "":
                            warn = 'Select Vaccination'
                        else:
                            check_counter += 1

                        if Contact1.get() == "":
                            warn = 'Please enter contact number.'
                        else:
                            check_counter += 1

                        if check_counter == 8:
                                try:
                                    conn= sqlite3.connect('eventsystem.db')
                                    cursor=conn.cursor()
                                    cursor.execute("INSERT INTO CompRegistrationStudent VALUES (:id, :Fullname, :StudentID, :Email, :Gender, :CompetitionName, :LevelOfStudy, :Vaccination, :ContactNo)", {
                                    'id':None,
                                    'Fullname':name1.get(),
                                    'StudentID':studentID.get(),
                                    'Email':email.get(),
                                    'Gender':gender.get(),
                                    'CompetitionName': compname.get(),
                                    'LevelOfStudy':levelofstudy.get(),
                                    'Vaccination':vac.get(),
                                    'ContactNo':Contact1.get()
                                    })
                                    conn.commit()
                                    messagebox.showinfo('Confirmation', 'Event Registered')
                                    top.destroy()

                                except Exception as ep:
                                    messagebox.showerror('', ep)

                        else:
                            messagebox.showerror('Error', warn)


                    #registration form widgets
                    label_0 = Label(top, text="Competition Registration Form",width=26,font=("bold", 22))
                    label_0.place(x=50,y=30)
                            
                            
                    label_1 = Label(top, text="Full Name",width=20,font=("bold", 10))
                    label_1.place(x=75,y=100)
                                
                    name1 = Entry(top)
                    name1.place(x=240,y=100)

                    label_2 = Label(top, text="Student ID",width=20,font=("bold", 10))
                    label_2.place(x=75,y=150)
                            
                    studentID = Entry(top)
                    studentID.place(x=240,y=150)
                            
                    label_3 = Label(top, text="Email",width=20,font=("bold", 10))
                    label_3.place(x=71,y=200)
                            
                    email = Entry(top)
                    email.place(x=240,y=200)

                    label_4 = Label(top, text="Contact Number",width=20,font=("bold", 10))
                    label_4.place(x=70,y=250)

                    Contact1 = Entry(top)
                    Contact1.place(x=240,y=250)
                            
                    label_5 = Label(top, text="Gender",width=20,font=("bold", 10))
                    label_5.place(x=70,y=300)
                            
                    Radiobutton(top, text="Male",padx = 5, variable=gender, value='Male').place(x=235,y=300)
                    Radiobutton(top, text="Female",padx = 20, variable=gender, value='Female').place(x=290,y=300)

                    label_6 = Label(top, text="Competition Name",width=20,font=("bold", 10))
                    label_6.place(x=70,y=350)

                    compname = Entry(top)
                    compname.place(x=240,y=350)
                            
                    label_7 = Label(top, text="Level of Study",width=20,font=("bold", 10))
                    label_7.place(x=70,y=400)
                            
                    list1 = ['Certificate','Foundation', 'Diploma', 'Bachelor Degree', 'Masters', 'Working', 'Doctorate'];
                            
                    droplist=OptionMenu(top,levelofstudy, *list1)
                    droplist.config(width=15)
                    # LevelOfStudy.set('select') 
                    droplist.place(x=240,y=400)
                            
                    label_8 = Label(top, text="Vaccination",width=20,font=("bold", 10))
                    label_8.place(x=70,y=450)
                    # var2= IntVar()
                    Radiobutton(top, text="Yes",padx = 5, variable=vac, value='Yes').place(x=235,y=450)
                    Radiobutton(top, text="No",padx = 20, variable=vac, value='No').place(x=290,y=450)
                            
                    Button(top, text='Submit',width=20,bg='red',fg='white', cursor='hand2', command=insert_record).place(x=180,y=500)

        def previous():
            global comp_image
            global comprec_no
            if comprec_no>0:
                comprec_no=comprec_no-1

            if comprec_no==0:
                prev_btn.config(state=DISABLED)
            else:
                prev_btn.config(state=NORMAL)
                next_btn.config(state=NORMAL)

            img1= Image.open(io.BytesIO(c_set[comprec_no][7]))
            img1 = img1.resize((200,180))
            img1 = ImageTk.PhotoImage(img1)
            comp_image=tk.Label(frame2, image=img1)
            comp_image.grid(row=0, column=0, rowspan=4, columnspan=2, sticky=W, pady=5)
            comp_image.image=img1
            
            comp_name.config(text="Name: "+ c_set[comprec_no][1])
            comp_datetime.config(text='Date/Time: '+ c_set[comprec_no][3]+ ', '+ c_set[comprec_no][4])
            comp_loc.config(text='Location: '+ c_set[comprec_no][5])
            comp_req.config(text='Requirements: '+ c_set[comprec_no][6])
            comp_des.config(text='Description: '+ c_set[comprec_no][2])

        def next():
            global comp_image
            global comprec_no
            if comprec_no < (len(c_set)-1):
                comprec_no=comprec_no+1
            if comprec_no == (len(c_set)-1):
                next_btn.config(state=DISABLED)
            else:
                next_btn.config(state=NORMAL)
                prev_btn.config(state=NORMAL)            
        
            img1= Image.open(io.BytesIO(c_set[comprec_no][7]))
            img1 = img1.resize((200,180))
            img1 = ImageTk.PhotoImage(img1)
            comp_image=tk.Label(frame2, image=img1)
            comp_image.grid(row=0, column=0, rowspan=4, columnspan=2, sticky=W, pady=5)
            comp_image.image=img1
            
            comp_name.config(text="Name: "+ c_set[comprec_no][1])
            comp_datetime.config(text='Date/Time: '+ c_set[comprec_no][3]+ ', '+ c_set[comprec_no][4])
            comp_loc.config(text='Location: '+ c_set[comprec_no][5])
            comp_req.config(text='Requirements: '+ c_set[comprec_no][6])
            comp_des.config(text='Description: '+ c_set[comprec_no][2])

        #register for competition button
        register_btn = Button(frame2, height=1, width=7, command=register_comp, text='Register', font=f)
        register_btn.grid(row=4, column=0, columnspan=2, sticky=NS, pady=5)

        prev_btn = Button(frame2, height=1, width=4, command=previous, text='<<', font=f)
        prev_btn.grid(row=5, column=0,  sticky=NS, pady=5)
        
        next_btn = Button(frame2, height=1, width=4, command=next, text='>>', font=f)
        next_btn.grid(row=5, column=1, sticky=NS, pady=5)

        #popup for category btns
        def sci_popup():
            top = Toplevel(ws)
            top.geometry('900x450')
            top.title("Science Competitions")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))
            style.configure('Treeview', rowheight=40)

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Science Competitions', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=300, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            my_tree['columns'] = ('ID', 'Comp Name', 'Date', 'Time', 'Location')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Comp Name', width=300, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
            my_tree.column('Location', width=160, anchor=CENTER, stretch=NO)

            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Comp Name', text='Event Name', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Location', text='Location', anchor=CENTER)

            #show competitions from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, CompetitionName, Date, Time, Location from CompRegistrationAdmin WHERE CompetitionType="Science"''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #register button
            register_btn = Button(top, height=1, width=7, command=register_comp, text='Register', font=f)
            register_btn.place(x=420, y=390)

        def math_popup():
            top = Toplevel(ws)
            top.geometry('900x450')
            top.title("Mathematics Competitions")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))
            style.configure('Treeview', rowheight=40)

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Mathematics Competitions', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=260, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            my_tree['columns'] = ('ID', 'Comp Name', 'Date', 'Time', 'Location')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Comp Name', width=300, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
            my_tree.column('Location', width=160, anchor=CENTER, stretch=NO)

            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Comp Name', text='Comp Name', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Location', text='Location', anchor=CENTER)

            #show events from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, CompetitionName, Date, Time, Location from CompRegistrationAdmin WHERE CompetitionType="Mathematics"''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #register button
            register_btn = Button(top, height=1, width=7, command=register_comp, text='Register', font=f)
            register_btn.place(x=420, y=390)

        def bus_popup():
            top = Toplevel(ws)
            top.geometry('900x450')
            top.title("Business Competitions")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))
            style.configure('Treeview', rowheight=40)

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Business Competitions', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=300, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            my_tree['columns'] = ('ID', 'Comp Name', 'Date', 'Time', 'Location')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Comp Name', width=300, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
            my_tree.column('Location', width=160, anchor=CENTER, stretch=NO)

            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Comp Name', text='Comp Name', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Location', text='Location', anchor=CENTER)

            #show events from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, CompetitionName, Date, Time, Location from CompRegistrationAdmin WHERE CompetitionType="Business"''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #register button
            register_btn = Button(top, height=1, width=7, command=register_comp, text='Register', font=f)
            register_btn.place(x=420, y=390)
  
        def others_popup():
            top = Toplevel(ws)
            top.geometry('900x450')
            top.title("Other Competitions")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))
            style.configure('Treeview', rowheight=40)

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Other Competitions', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=300, y=10)

            tree_frame = Frame(top)
            tree_frame.pack(pady=70)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)

            my_tree['columns'] = ('ID', 'Comp Name', 'Date', 'Time', 'Location')

            #format columns
            my_tree.column('#0', width=0, stretch=NO)
            my_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            my_tree.column('Comp Name', width=300, anchor=CENTER, stretch=NO)
            my_tree.column('Date', width=150, anchor=CENTER, stretch=NO)
            my_tree.column('Time', width=140, anchor=CENTER, stretch=NO)
            my_tree.column('Location', width=160, anchor=CENTER, stretch=NO)

            #column headings
            my_tree.heading('#0', text='', anchor=W)
            my_tree.heading('ID', text='ID', anchor=CENTER)
            my_tree.heading('Comp Name', text='Comp Name', anchor=CENTER)
            my_tree.heading('Date', text='Date', anchor=CENTER)
            my_tree.heading('Time', text='Time', anchor=CENTER)
            my_tree.heading('Location', text='Location', anchor=CENTER)

            #show events from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, CompetitionName, Date, Time, Location from CompRegistrationAdmin WHERE CompetitionType="Others"''')
            r_set=c.fetchall()
            for row in r_set:
                my_tree.insert("", tk.END, values=row)

            #register button
            register_btn = Button(top, height=1, width=7, command=register_comp, text='Register', font=f)
            register_btn.place(x=420, y=390)

        #category pic bind pic to button
        image2=Image.open('Science.png')
        img2=image2.resize((220,150))
        my_img2=ImageTk.PhotoImage(img2)
        science_pic=Label(image=my_img2)
        science_pic.image=my_img2
        
        image3=Image.open('Maths.png')
        img3=image3.resize((220,150))
        my_img3=ImageTk.PhotoImage(img3)
        maths_pic=Label(image=my_img3)
        maths_pic.image=my_img3

        image4=Image.open('Business.png')
        img4=image4.resize((220,150))
        my_img4=ImageTk.PhotoImage(img4)
        business_pic=Label(image=my_img4)
        business_pic.image=my_img4

        image5=Image.open('others.png')
        img5=image5.resize((220,150))
        my_img5=ImageTk.PhotoImage(img5)
        others_pic=Label(image=my_img5)
        others_pic.image=my_img5

        #buttons bind with category pic
        science_btn = tk.Button(self, image=my_img2, cursor='hand2', command= sci_popup)
        science_btn.place(x=70,y=550)

        math_btn = tk.Button(self,image=my_img3, cursor='hand2', command=math_popup)
        math_btn.place(x=320,y=550)

        business_btn = tk.Button(self, image=my_img4, cursor='hand2', command=bus_popup)
        business_btn.place(x=570,y=550)

        others_btn = tk.Button(self, image=my_img5, cursor='hand2', command=others_popup)
        others_btn.place(x=820,y=550)

class Profile(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='antique white')
        global login_details

        #inti logo
        inti_logo(self)
        #top buttons
        top_buttons(self,controller)
        #show date and clock
        clock(self)
        today_date(self)

        #Profile Title
        w = Label(self, text ='Profile', font = ('Arial', 28), bg='antique white')
        w.pack()
        w.place(x=500, y=80)

        
        #Welcome name title
        self.lbl_welcome = Label(self, text ='', font = ('Arial', 20), bg='antique white' )
        self.lbl_welcome.pack()
        self.lbl_welcome.place(x=40, y=130)
        #show userdetails frame
        self.userdetails_frame = Frame(self, bd=2, bg='antique white', relief=SOLID)
        self.userdetails_frame.place(x=50, y=190)

        #userdetails word
        w = Label(self.userdetails_frame, text ='User Details', font = ('Rockwell', 20), bg='antique white' ).grid(row=0, column=1, sticky=W, pady=5, padx=25, columnspan=2)
        
        # def user_details(self):
        name_title = Label(self.userdetails_frame, text='Name: ', font=('Arial',15))
        name_title.grid(row=1, column=0, sticky=W, pady=5)

        self.lbl_name = Label(self.userdetails_frame, text='',font = ('Arial', 15), bg='antique white' )
        self.lbl_name.grid(row=1, column=1, sticky=W, pady=5)

        gender_title = Label(self.userdetails_frame, text='Gender: ', font=('Arial',15))
        gender_title.grid(row=2, column=0, sticky=W, pady=5)

        self.lbl_gender = Label(self.userdetails_frame, text='',font = ('Arial', 15), bg='antique white' )
        self.lbl_gender.grid(row=2, column=1, sticky=W, pady=5)

        email_title = Label(self.userdetails_frame, text='Email: ', font=('Arial',15))
        email_title.grid(row=3, column=0, sticky=W, pady=5)

        self.lbl_email = Label(self.userdetails_frame, text='',font = ('Arial', 15), bg='antique white' )
        self.lbl_email.grid(row=3, column=1, sticky=W, pady=5)

        contact_title = Label(self.userdetails_frame, text='Contact: ', font=('Arial',15))
        contact_title.grid(row=4, column=0, sticky=W, pady=5)

        self.lbl_contact = Label(self.userdetails_frame, text='',font = ('Arial', 15) , bg='antique white')
        self.lbl_contact.grid(row=4, column=1, sticky=W, pady=5)

        #edit details popup
        def editdetails_popup():
                    top= Toplevel(ws)
                    top.geometry("300x300")
                    top.title("Edit Details")
                    top.resizable(False,False)  
                    w = Label(top, text ='Name: ', font = ('Arial', 15) )
                    w.grid(row=0, column=0, sticky=W, pady=5)

                    w = Label(top, text ='Email: ', font = ('Arial', 15) )
                    w.grid(row=1, column=0, sticky=W, pady=5)

                    w = Label(top, text ='Gender: ', font = ('Arial', 15) )
                    w.grid(row=2, column=0, sticky=W, pady=5)

                    w = Label(top, text ='Contact: ', font = ('Arial', 15) )
                    w.grid(row=3, column=0, sticky=W, pady=5)

                    w = Label(top, text ='Password: ', font = ('Arial', 15) )
                    w.grid(row=4, column=0, sticky=W, pady=5)

                    
                    edit_name_entry = tk.Entry(top, font=f,  width=15)
                    edit_name_entry.grid(row=0, column=1, sticky=W, pady=5)
                    edit_email_entry = tk.Entry(top, font=f,  width=15)
                    edit_email_entry.grid(row=1, column=1, sticky=W, pady=5)
                    edit_gender_entry = tk.Entry(top, font=f, width=15)
                    edit_gender_entry.grid(row=2, column=1, sticky=W, pady=5)
                    edit_contact_entry = tk.Entry(top, font=f,  width=15)
                    edit_contact_entry.grid(row=3, column=1, sticky=W, pady=5)
                    edit_pw_entry = tk.Entry(top, font=f,  width=15, show='*')
                    edit_pw_entry.grid(row=4, column=1, sticky=W, pady=5)

                    #show records in entry box
                    edit_name_entry.insert(0, login_details[0])
                    edit_email_entry.insert(0,login_details[2])
                    edit_gender_entry.insert(0,login_details[5])
                    edit_contact_entry.insert(0,login_details[3])
                    edit_pw_entry.insert(0, login_details[6])


                    def save_details():
                        conn=sqlite3.connect('eventsystem.db')
                        c=conn.cursor()

                        c.execute("""UPDATE UserDetails SET 
                                                email =:email,
                                                gender =:gender,
                                                contact= :contact ,
                                                password =:password

                                                WHERE name = :name""",
                                                {
                                                    'name' : edit_name_entry.get(),
                                                    'email' : edit_email_entry.get(),
                                                    'gender': edit_gender_entry.get(),
                                                    'contact': edit_contact_entry.get(),
                                                    'password': edit_pw_entry.get()
                                                })
                        conn.commit()

                        conn.close()

                    #show/hide password
                    def toggle_password():
                        if edit_pw_entry.cget('show') == '':
                            edit_pw_entry.config(show='*')
                            pwd_btn.config(text='Show')
                        else:
                            edit_pw_entry.config(show='')
                            pwd_btn.config(text='Hide')
                    pwd_btn=Button(top, text='Show', width=4, font=('Arial', 9), command=toggle_password)
                    pwd_btn.place(x=238,y=161)

                    save_btn=tk.Button(top, height=1, width=7, command=save_details, text='Save', font=f)
                    save_btn.grid(row=5, column=1, sticky=W, pady=5)
                    

        #edit details button
        editdetails_btn=tk.Button(self.userdetails_frame, height=1, width=10, text="Edit details", command=editdetails_popup, font=f)
        editdetails_btn.grid(row=7, column=1, sticky=W, pady=5, padx=5)

        # #refresh details
        # def refresh_details(self):
        #     user_details(self)

        # #refresh details button
        # redetails_btn=tk.Button(self.userdetails_frame, height=1, width=6, text="Refresh", command=refresh_details(self), font=f)
        # redetails_btn.grid(row=0, column=0, sticky=W, pady=5, padx=20)

        #helpdesk frame
        helpdesk_frame = Frame(self, bd=2, bg='antique white', relief=SOLID)
        helpdesk_frame.place(x=610, y=190)

        #Helpdesk word
        w = Label(helpdesk_frame, text ='Helpdesk', font = ('Rockwell', 20) , bg='antique white').grid(row=1, column=0, sticky=W, pady=5, padx=115)

        w = Label(helpdesk_frame, text ='FAQs ', font = ('Arial', 18, 'bold') ).grid(row=2, column=0, sticky=W, pady=5)

        w = Label(helpdesk_frame, text ='Question 1: \'How do I Logout from the system?\' ', font = ('Arial', 15) ).grid(row=3, column=0, sticky=W)

        w = Label(helpdesk_frame, text ='Answer: You can Logout under the Profile Page', font = ('Arial', 15) ).grid(row=4, column=0, sticky=W, pady=5)

        w = Label(helpdesk_frame, text ='Question 2: \'How to register for an event?\'', font = ('Arial', 15) ).grid(row=5, column=0, sticky=W)

        w = Label(helpdesk_frame, text ='Answer: Click register under the Events Page', font = ('Arial', 15) ).grid(row=6, column=0, sticky=W, pady=5)

        w = Label(helpdesk_frame, text ='Question 3: \'How to edit profile details?\'', font = ('Arial', 15) ).grid(row=7, column=0, sticky=W)

        w = Label(helpdesk_frame, text ='Answer: Go to Profile, press edit details.', font = ('Arial', 15) ).grid(row=8, column=0, sticky=W, pady=5)

            #ask question with chatbot
        def askquestion_popup():
            top= Toplevel(ws)
            # top.geometry("300x300")
            top.title("Ask a question with chatbot")
            top.resizable(False,False)

            BG_COLOR = "antiquewhite2"

            FONT = "Helvetica 14"
            FONT_BOLD = "Helvetica 13 bold"

            # Send function
            def send():
                send = "You -> " + e.get()
                txt.insert(END, "\n" + send)

                user = e.get().lower()

                if (user == "hello"):
                    txt.insert(END, "\n" + "Bot -> Hi there, how can I help?")

                elif (user == "hi" or user == "hii" or user == "hiiii"):
                    txt.insert(END, "\n" + "Bot -> Hi there, what can I do for you?")

                elif (user == "register events" or user =="register for events" or user =="i want to register for events" or user =="events" or user =="view events" or user =="i want to view events"):
                    txt.insert(END, "\n" + "Bot -> Proceed to Announcements Page or Events Page to register or view events.")

                elif (user == "register competitions" or user == "competition" or user == "competitions" or user == "view competitions" or user == "i want to register for competitions" or user == "competitions"):
                    txt.insert(END, "\n" + "Bot -> Proceed to Competitions Page to register or view competitions.")

                elif (user == "class cancel" or user == "replacement" or user == "class replacement" or user == "view class cancellation" or user == "view class replacement" ):
                    txt.insert(END, "\n" + "Bot -> Proceed to Announcements Page to view class replacement or cancellation notice.")

                elif (user == "countdown" or user == "add countdown" or user == "view countdown"):
                    txt.insert(END, "\n" + "Bot -> Countdown activites can be viewed in Announcements Page and can be added under Profile page.")

                elif (user == "user details" or user == "edit user details" or user == "change contact" or user == "edit contact" or user == "view user details"   ):
                    txt.insert(
                        END, "\n" + "Bot -> User details can be viewed and edited under Profile page section.")

                elif (user == "logout" or user == "log out" or user == "sign out"):
                    txt.insert(END, "\n" + "Bot -> Users can log out at Profile page.")
                    
                else:
                    txt.insert(END, "\n" + "Bot -> Sorry! I didn't understand that. Any enquiries, please contact us at bob@gmail.com")

                e.delete(0, END)


            wlc_lbl = Label(top, bg=BG_COLOR,  text="Welcome to chatbot", font=FONT_BOLD, pady=10, height=1)
            wlc_lbl.grid(row=0)

            txt = Text(top, bg=BG_COLOR, wrap=WORD,font=FONT, width=60)
            txt.grid(row=1, column=0, columnspan=2)

            scrollbar = Scrollbar(txt)
            scrollbar.place(relheight=1, relx=0.974)

            e = Entry(top, bg="light yellow", font=FONT, width=55)
            e.grid(row=2, column=0)

            send = Button(top, text="Send", font=FONT_BOLD, bg="wheat1",command=send)
            send.grid(row=2, column=1)

        #ask question button
        ask_btn=tk.Button(helpdesk_frame, height=1, width=12, command=askquestion_popup, text='Ask question', font=f)
        ask_btn.grid(row=9, column=0,padx=50)


        #add to countdown frame
        countdown_frame = Frame(self, bd=2, bg='antique white', relief=SOLID)
        countdown_frame.place(x=80, y=510)

        #Add to countdown title
        w=Label(countdown_frame, text='Add to Countdown',  font=('Rockwell', 20), bg='antique white').grid(row=1, column=0, sticky=W, pady=5, padx=5, columnspan=3)

        #add to countdown box
        def add_countdown_popup():
            top= Toplevel(ws)
            top.geometry("400x250")
            top.title("Add to Countdown")
            top.resizable(False,False)  
            #database
            conn = sqlite3.connect('eventsystem.db')
            cursor=conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS EventCountdown (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                        EventName TEXT NOT NULL,
                                                                        Year Number NOT NULL,
                                                                        Month Number NOT NULL, 
                                                                        Date Number NOT NULL)''')
            conn.commit()

            def insert_record():
                check_counter=0
                warn = " "
                if name.get() == "":
                    warn = 'Please enter event name.'
                else:
                    check_counter += 1
                    
                if year.get() == "":
                    warn='Please enter event year.'
                else:
                    check_counter += 1

                if mnth.get() == "":
                    warn = 'Please enter event month.'
                else:
                    check_counter += 1

                if date.get() == "":
                    warn = 'Please enter event date.'
                else:
                    check_counter += 1

                if check_counter == 4:
                    try:
                        conn= sqlite3.connect('eventsystem.db')
                        cursor=conn.cursor()
                        cursor.execute("INSERT INTO EventCountdown VALUES (:id, :EventName, :Year, :Month, :Date)", {
                        'id':None,
                        'EventName':name.get(),
                        'Year':year.get(),
                        'Month':mnth.get(),
                        'Date':date.get()
                        })
                        conn.commit()
                        messagebox.showinfo('Confirmation', 'Countdown added')
                        top.destroy()

                    except Exception as ep:
                        messagebox.showerror('', ep)

                else:
                    messagebox.showerror('Error', warn)

            #Add to countdown title, widgets, entries
            cntdwn_title= Label(top, text='Add to Countdown Page', font=("Arial", 18))
            cntdwn_title.grid(row=0, column=0, sticky=W, pady=5, columnspan=4)

            evntname_lbl= Label(top, text=' Event Name', font=f)
            evntname_lbl.grid(row=1, column=0, sticky=W, pady=5, columnspan=4)

            name = Entry(top, font=f, width=18)
            name.grid(row=1, column=1, sticky=W, pady=5, columnspan=4)

            evntdate_lbl= Label(top, text='Event Date \nYYYY/MM/DD', font=f)
            evntdate_lbl.grid(row=2, column=0, sticky=W, pady=5)

            year_lbl=Label(top, text='Year(YYYY)', font=('Arial', 10))
            year_lbl.grid(row=3, column=1, sticky=W, pady=5)

            year =Entry(top, font=f,  width=5)
            year.grid(row=2, column=1, sticky=W, pady=5)

            month_lbl=Label(top, text='Month(MM)', font=('Arial', 10))
            month_lbl.grid(row=3, column=2, sticky=W, pady=5)

            mnth =Entry(top, font=f,  width=5)
            mnth.grid(row=2, column=2, sticky=W, pady=5)

            date_lbl=Label(top, text='Date(DD)', font=('Arial', 10))
            date_lbl.grid(row=3, column=3, sticky=W, pady=5)

            date =Entry(top, font=f, width=5)
            date.grid(row=2, column=3, sticky=W, pady=5)


            add_event_btn=tk.Button(top,height=1,width=9, command=insert_record, text='Add Event', font=f)
            add_event_btn.grid(row=4, column=1,sticky=W, pady=5, columnspan=4)

        #edit countdown box
        def edit_countdown_popup():
            top = Toplevel(ws)
            top.geometry('800x450')
            top.title("Edit Countdown Event")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))
            style.configure('Treeview', rowheight=19)


            #view all compertitions label
            allcomp_lbl = Label(top, text ='Edit Countdown Event', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=210, y=10)

            eventtree_frame = Frame(top)
            eventtree_frame.pack(pady=70)

            tree_scroll = Scrollbar(eventtree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            event_tree = ttk.Treeview(eventtree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            event_tree.pack()

            tree_scroll.config(command=event_tree.yview)

            event_tree['columns'] = ('ID', 'Event Name', 'Year', 'Month', 'Date')

            #format columns
            event_tree.column('#0', width=0, stretch=NO)
            event_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            event_tree.column('Event Name', width=220, anchor=CENTER, stretch=NO)
            event_tree.column('Year', width=150, anchor=CENTER, stretch=NO)
            event_tree.column('Month', width=140, anchor=CENTER, stretch=NO)
            event_tree.column('Date', width=160, anchor=CENTER, stretch=NO)

            #column headings
            event_tree.heading('#0', text='', anchor=W)
            event_tree.heading('ID', text='ID', anchor=CENTER)
            event_tree.heading('Event Name', text='Event Name', anchor=CENTER)
            event_tree.heading('Year', text='Year', anchor=CENTER)
            event_tree.heading('Month', text='Month', anchor=CENTER)
            event_tree.heading('Date', text='Date', anchor=CENTER)

            #show events from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, EventName, Year, Month, Date from EventCountdown ''')
            r_set=c.fetchall()
            for row in r_set:
                event_tree.insert("", tk.END, values=row)

            #entry boxes for editing db
            id_lbl = Label(top, text='ID', font=f)
            id_lbl.place(x=35, y=320)
            id_entry = Entry(top, width=5, font=f)
            id_entry.place(x=150, y=320)

            eventname_lbl = Label(top, text="Event Name", font=f)
            eventname_lbl.place(x=35, y=360)
            eventname_entry = Entry(top, width=16, font=f)
            eventname_entry.place(x=150,y=360)

            year_lbl = Label(top, text="Year", font=f)
            year_lbl.place(x=35, y=400)
            year_entry = Entry(top, width=16, font=f)
            year_entry.place(x=150,y=400)

            month_lbl = Label(top, text="Month", font=f)
            month_lbl.place(x=360, y=320)
            month_entry = Entry(top, width=16, font=f)
            month_entry.place(x=475,y=320)

            date_lbl = Label(top, text="Date", font=f)
            date_lbl.place(x=360, y=360)
            date_entry = Entry(top, width=16, font=f)
            date_entry.place(x=475,y=360)

            #Show record
            def show_record(e):
                # Clear entry boxes
                id_entry.delete(0,END)
                eventname_entry.delete(0, END)
                year_entry.delete(0, END)
                month_entry.delete(0, END)
                date_entry.delete(0, END)
                

                # Grab the record number
                selected = event_tree.focus()
                # Grab record values
                values= event_tree.item(selected, 'values')

                # outputs to entry boxes
                id_entry.insert(0, values[0])
                eventname_entry.insert(0, values[1])
                year_entry.insert(0, values[2])
                month_entry.insert(0, values[3])
                date_entry.insert(0, values[4])
                

            # Update record
            def save_details():
                # Grab the record number
                    selected = event_tree.focus()
                # Update record
                    event_tree.item(selected, text="", values=(id_entry.get(),eventname_entry.get(), year_entry.get(), month_entry.get(), date_entry.get()))
                    conn=sqlite3.connect('eventsystem.db')
                    c=conn.cursor()

                    c.execute("""UPDATE EventCountdown SET
                                            EventName =:name,
                                            Year =:year,
                                            Month= :month,
                                            Date= :date
                                            WHERE id = :id """,
                                             {  
                                                'id'   : id_entry.get(),
                                                'name' : eventname_entry.get(),
                                                'year': year_entry.get(),
                                                'month': month_entry.get(),
                                                'date' : date_entry.get()
                                             })
                    conn.commit()

                    conn.close()

            save_btn=tk.Button(top, height=1, width=6, command=save_details, text='Edit', font=f)
            save_btn.place(x=700,y=360)

            event_tree.bind('<ButtonRelease-1>', show_record)
            
        #delete add to countdown
        def del_countdown_popup():
            top = Toplevel(ws)
            top.geometry('800x450')
            top.title("Delete Countdown Event")
            top.resizable(False,False)

            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', font=f)
            style.configure('Treeview', font=('Arial', 13))
            style.configure('Treeview', rowheight=19)

            #view all compertitions label
            allcomp_lbl = Label(top, text ='Delete Countdown Event', font = ('Arial', 25,'bold'))
            allcomp_lbl.place(x=210, y=10)

            eventtree_frame = Frame(top)
            eventtree_frame.pack(pady=70)

            tree_scroll = Scrollbar(eventtree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            event_tree = ttk.Treeview(eventtree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
            event_tree.pack()

            tree_scroll.config(command=event_tree.yview)

            event_tree['columns'] = ('ID', 'Event Name', 'Year', 'Month', 'Date')

            #format columns
            event_tree.column('#0', width=0, stretch=NO)
            event_tree.column('ID', width=30, anchor=CENTER, stretch=NO)
            event_tree.column('Event Name', width=220, anchor=CENTER, stretch=NO)
            event_tree.column('Year', width=150, anchor=CENTER, stretch=NO)
            event_tree.column('Month', width=140, anchor=CENTER, stretch=NO)
            event_tree.column('Date', width=160, anchor=CENTER, stretch=NO)

            #column headings
            event_tree.heading('#0', text='', anchor=W)
            event_tree.heading('ID', text='ID', anchor=CENTER)
            event_tree.heading('Event Name', text='Event Name', anchor=CENTER)
            event_tree.heading('Year', text='Year', anchor=CENTER)
            event_tree.heading('Month', text='Month', anchor=CENTER)
            event_tree.heading('Date', text='Date', anchor=CENTER)

            #show events from db
            conn = sqlite3.connect('eventsystem.db')
            c=conn.cursor()
            r_set=c.execute('''SELECT id, EventName, Year, Month, Date from EventCountdown ''')
            r_set=c.fetchall()
            for row in r_set:
                event_tree.insert("", tk.END, values=row)

            #entry boxes for editing db
            id_lbl = Label(top, text='ID', font=f)
            id_lbl.place(x=35, y=320)
            id_entry = Entry(top, width=5, font=f)
            id_entry.place(x=150, y=320)

            eventname_lbl = Label(top, text="Event Name", font=f)
            eventname_lbl.place(x=35, y=360)
            eventname_entry = Entry(top, width=16, font=f)
            eventname_entry.place(x=150,y=360)

            year_lbl = Label(top, text="Year", font=f)
            year_lbl.place(x=35, y=400)
            year_entry = Entry(top, width=16, font=f)
            year_entry.place(x=150,y=400)

            month_lbl = Label(top, text="Month", font=f)
            month_lbl.place(x=360, y=320)
            month_entry = Entry(top, width=16, font=f)
            month_entry.place(x=475,y=320)

            date_lbl = Label(top, text="Date", font=f)
            date_lbl.place(x=360, y=360)
            date_entry = Entry(top, width=16, font=f)
            date_entry.place(x=475,y=360)

            #Show record
            def show_record(e):
                # Clear entry boxes
                id_entry.delete(0,END)
                eventname_entry.delete(0, END)
                year_entry.delete(0, END)
                month_entry.delete(0, END)
                date_entry.delete(0, END)
                

                # Grab the record number
                selected = event_tree.focus()
                # Grab record values
                values= event_tree.item(selected, 'values')

                # outputs to entry boxes
                id_entry.insert(0, values[0])
                eventname_entry.insert(0, values[1])
                year_entry.insert(0, values[2])
                month_entry.insert(0, values[3])
                date_entry.insert(0, values[4])
                

            # Update record
            def del_record():
                x = event_tree.selection()[0]
                event_tree.delete(x)

                conn = sqlite3.connect('eventsystem.db')
                c = conn.cursor()

                # Delete From Database
                c.execute("DELETE from EventCountdown WHERE oid=" + id_entry.get())

                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear entry boxes
                id_entry.delete(0,END)
                eventname_entry.delete(0, END)
                year_entry.delete(0, END)
                month_entry.delete(0, END)
                date_entry.delete(0, END)

                # Add a little message box for fun
                messagebox.showinfo("Alert", "Event Deleted.")
                

            #Delete button
            del_btn=tk.Button(top,height=1, width=6, font=f, command=del_record, text='Delete')
            del_btn.place(x=700, y=360)

            event_tree.bind('<ButtonRelease-1>', show_record)
            
        add_btn=tk.Button(countdown_frame, height=1, width=7, command=add_countdown_popup, text='Add', font=f)
        add_btn.grid(row=2, column=0,padx=5, pady=5)
            
        edit_btn=tk.Button(countdown_frame, height=1, width=7, command=edit_countdown_popup, text='Edit', font=f)
        edit_btn.grid(row=2, column=1,padx=5, pady=5)

        del_btn=tk.Button(countdown_frame, height=1, width=7, command=del_countdown_popup, text='Delete', font=f)
        del_btn.grid(row=2, column=2,padx=5, pady=5)



        #Logout
        def log_out():
            controller.show_frame(Loginpage)
            messagebox.showinfo('Logout Status', 'Logged out successfully!')
        logout_btn=tk.Button(self, height=1, width=7, font=f, command=log_out, text='Logout')
        logout_btn.place(x=980 ,y=130)


#window
ws=App()
ws.title("INTI Event System")
ws.geometry('1100x770')
ws.resizable(False,False)

ws.mainloop()