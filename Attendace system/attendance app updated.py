from tkinter import *
from tkinter import messagebox as ms
from tkinter import Message ,Text
import tkinter.ttk as ttk
import tkinter.font as font
from PIL import ImageTk, Image 
import cv2
import os
import csv
import numpy as np
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def attendance_mail(d,filem):
     fromaddr = "yashtb123@gmail.com"
     toaddr = "baargav15cmpunk@gmail.com"
     passw = "rzjhmoewhshvdpes"
     msg = MIMEMultipart()
     msg['From'] = fromaddr
     msg['To'] = toaddr  

     msg['Subject'] = "{} DAILY ATTENDANCE".format(d)

     body = "Good evening Sir/Mam \n Today's attendance are attanched below"

     msg.attach(MIMEText(body, 'plain'))

     filename = "ATTENDANCE{}.csv".format(d)
     attachment = open(filem,'rb')

     p = MIMEBase('application', 'octet-stream')

     p.set_payload((attachment).read())

     encoders.encode_base64(p)

     p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

     msg.attach(p)

     s = smtplib.SMTP('smtp.gmail.com', 587)


     s.starttls()

     s.login(fromaddr, passw )


     text = msg.as_string()


     s.sendmail(fromaddr, toaddr, text)


     s.quit()


with sqlite3.connect('Files/Account_database.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL PRIMARY KEY,password TEX NOT NULL);')
db.commit()
db.close()

class main:
    def __init__(self,master):
    	# Window 
        self.master = master
        # Some Usefull variables
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.n_cn_password = StringVar()
        #Create Widgets
        self.widgets()

    #Login Function
    def login(self):
    	#Establish Connection
        with sqlite3.connect('Files/Account_database.db') as db:
            c = db.cursor()

        #Find user If there is any take proper action
        find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
        c.execute(find_user,[(self.username.get()),(self.password.get())])
        result = c.fetchall()
        if self.username.get()=='' or self.password.get()=='':
            ms.showerror('Error!','Kindly enter all the data')

        elif result:
            self.logf.pack_forget()
            self.head['text'] = self.username.get() + '\n Logged In'
            self.head['pady'] = 150
            def test():
                window=Toplevel(root)
                window.title("Attendance Application")
                window.resizable(False, False)
                window.geometry('1280x720')
                window.configure(background='gray')
                window.grid_rowconfigure(0, weight=1)
                window.grid_columnconfigure(0, weight=1)
                window.iconbitmap('Files/src_images/icon.ico')
                load = Image.open('Files/src_images/atten.png')
                render = ImageTk.PhotoImage(load)
                img = Label(window, image=render)
                img.place(x=0, y=0, relwidth=1, relheight=1)

                message = Label(window, text="Attendance-Management-System"   ,fg="black"    ,height=1,font=('times', 40, 'bold underline')) 
                message.place(x=300, y=20)
                lbl = Label(window, text="Enter student ID",width=26  ,height=1  ,fg="white"  ,bg="#004d4d" ,font=('times', 15, ' bold ') ) 
                lbl.place(x=40, y=200)

                txt = Entry(window,bd=5,width=20  ,bg="#004d4d" ,fg="white",font=('times', 18, ' bold '))
                txt.place(x=40, y=250)

                lbl2 = Label(window, text="Enter student Name",width=20  ,fg="white"  ,bg="#004d4d"    ,height=1 ,font=('times', 15, ' bold ')) 
                lbl2.place(x=40, y=320)

                txt2 = Entry(window,bd=5,width=20  ,bg="#004d4d"  ,fg="white",font=('times', 18, ' bold ')  )
                txt2.place(x=40, y=370)

                lbl3 = Label(window, text="Notification : ",width=20  ,fg="white"  ,bg="#004d4d"  ,height=1 ,font=('times', 15, ' bold underline ')) 
                lbl3.place(x=100, y=580)

                message = Label(window, text="" ,bg="#004d4d"  ,fg="white"  ,width=60  ,height=1, activebackground = "#004d4d" ,font=('times', 20, ' bold ')) 
                message.place(x=40, y=630)

                lbl3 = Label(window, text="Attendance",width=15  ,fg="white"  ,bg="#21556A"  ,height=2 ,font=('times', 31, ' bold  underline')) 
                lbl3.place(x=466, y=100)


                message2 = Label(window, text="" ,fg="white"   ,bg="#21556A",activeforeground = "green",width=30  ,height=10  ,font=('times', 15, ' bold ')) 
                message2.place(x=466, y=300)
                  
                def clear():
                    txt.delete(0, 'end')    
                    res = ""
                    message.configure(text= res)

                def clear2():
                    txt2.delete(0, 'end')    
                    res = ""
                    message.configure(text= res)    
                    
                def is_number(s):
                    try:
                        float(s)
                        return True
                    except ValueError:
                        pass
                 
                    try:
                        import unicodedata
                        unicodedata.numeric(s)
                        return True
                    except (TypeError, ValueError):
                        pass
                 
                    return False
            
                def TakeImages():        
                    Id=(txt.get())
                    name=(txt2.get())
                    if(is_number(Id) and name.isalpha()):
                        cam = cv2.VideoCapture(0)
                        recognizer = cv2.face.LBPHFaceRecognizer_create()

                        #recognizer = cv2.face.LBPHFaceRecognizer_create()
                        harcascadePath ="Files/haarcascade_frontalface_default.xml"
                        detector =cv2.CascadeClassifier(harcascadePath)
                        sampleNum=0
                        while(True):
                            ret, img = cam.read()
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            faces=detector.detectMultiScale(gray,1.3,5)
                            for (x,y,w,h) in faces:
                                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                                sampleNum=sampleNum+1
                                cv2.imwrite("Files/TrainingImage\\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                                
                                cv2.imshow('frame',img)
                            
                            if cv2.waitKey(100) & 0xFF == ord('q'):
                                break
                            
                            elif sampleNum>60:
                                break
                        cam.release()
                        cv2.destroyAllWindows() 
                        res = "Images Saved for ID : " + Id +" Name : "+ name
                        row = [Id , name]
                        with open(r'Files/StudentDetails/StudentDetails.csv','a+') as csvFile:
                            writer = csv.writer(csvFile)
                            writer.writerow(row)
                        csvFile.close()
                        message.configure(text= res)
                    else:
                        if(is_number(Id)):
                            res = "Enter Alphabetical Name"
                            message.configure(text= res)
                        if(name.isalpha()):
                            res = "Enter Numeric Id"
                            message.configure(text= res)
                    
                def TrainImages():
                    recognizer = cv2.face.LBPHFaceRecognizer_create()
                    harcascadePath =r"Files/haarcascade_frontalface_default.xml" 
                    detector =cv2.CascadeClassifier(harcascadePath)
                    faces,Id = getImagesAndLabels(r"Files/TrainingImage")
                    recognizer.train(faces, np.array(Id))
                    recognizer.save(r"Files/TrainingImageLabel/Trainner.yml")
                    res = "Image Trained"
                    message.configure(text= res)

                def getImagesAndLabels(path):
                    
                    imagePaths=[os.path.join(path,f)for f in os.listdir(path)]                 
                    
                    
                    faces=[]
                    
                    Ids=[]
                    
                    for imagePath in imagePaths:
                        
                        pilImage=Image.open(imagePath).convert('L')
                        
                        imageNp=np.array(pilImage,'uint8')
                        
                        Id=int(os.path.split(imagePath)[-1].split(".")[1])
                        
                        faces.append(imageNp)
                        Ids.append(Id)        
                    return faces,Ids

                def TrackImages():
                    recognizer = cv2.face.LBPHFaceRecognizer_create()
                    recognizer.read(r"Files/TrainingImageLabel/Trainner.yml")
                    harcascadePath=r"Files/haarcascade_frontalface_default.xml"
                    faceCascade = cv2.CascadeClassifier(harcascadePath);    
                    df=pd.read_csv(r'Files/StudentDetails/StudentDetails.csv')
                    cam = cv2.VideoCapture(0)
                    font = cv2.FONT_HERSHEY_SIMPLEX        
                    col_names =  ['Id','Name','Date','Time']
                    attendance = pd.DataFrame(columns = col_names)    
                    while True:
                        ret, im =cam.read()
                        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
                        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
                        for(x,y,w,h) in faces:
                            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
                            if(conf < 50):
                                ts = time.time()      
                                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                                aa=df.loc[df['Id'] == Id]['Name'].values
                                tt=str(Id)+"-"+aa
                                if aa.size>0:
                                    attendance.loc[len(attendance)] = [Id,aa[0],date,timeStamp]
                                
                            else:
                                Id='Unknown'                
                                tt=str(Id)  
                            if(conf > 75):
                                noOfFile=len(os.listdir("Files/ImagesUnknown"))+1
                                cv2.imwrite(r"Files/ImagesUnknown/Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
                            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
                        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
                        cv2.imshow('image Detected',im) 
                        if (cv2.waitKey(1)==ord('q')):
                            break
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    Hour,Minute,Second=timeStamp.split(":")
                    fileName=r"Files/Attendance/Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
                    attendance.to_csv(fileName,index=False)
                    cam.release()
                    cv2.destroyAllWindows()
                    print(attendance)
                    res=attendance
                    message2.configure(text= res)
                    attendance_mail(d=date,filem="Files/Attendance/Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv")



                def stf_show_att():
                    total_stud_details=pd.read_csv(r'Files/StudentDetails/StudentDetails.csv')
                    stf_atten_report_window = Toplevel(window)
                    stf_atten_report_window.title("Students Attendance")

                    stf_atten_report_window.geometry("600x450")
                    stf_atten_report_window.iconbitmap('Files/src_images/icon.ico')
                    stf_atten_report_window.resizable(False, False)
                    stf_atten_report_window.configure(background='gray')
                    Download_logo_photo = PhotoImage(file = r"Files/src_images/download-logo-12.png")

                    scroll_bar = Scrollbar(stf_atten_report_window)
                    scroll_bar.pack( side = RIGHT,fill = Y )
                    mylist = Listbox(stf_atten_report_window,font = ('calibri', 22, ' bold '),background='gray',yscrollcommand = scroll_bar.set )



                    stud_atten_report_files=os.listdir('Files/Attendance')
                    for linenum,line in enumerate(stud_atten_report_files):
                        mylist.insert(END,str(linenum+1)+'. '+str(line))
                        mylist.insert(END,'\n')
                    mylist.pack( side = TOP, fill = BOTH ,expand=True )
                    scroll_bar.config( command = mylist.yview )
                    frame = Frame(stf_atten_report_window)
                    frame.pack(fill=X,side=BOTTOM)
                    lbt1=Label(frame,text="Click here-->",font = ('calibri', 22, ' bold '))
                    lbt1.pack(fill = X,side=LEFT)

                        
                    def predicting_atten(filename):
                         atten_data=pd.read_csv(filename)
                         atten_data.dropna(inplace=True)
                         id_data=list(atten_data['Id'])
                         name_data=list(atten_data['Name'])
                         date_data=list(atten_data['Date'])
                         time_data=list(atten_data['Time'])                         
                         
                         predicting_atten_window=Toplevel(stf_atten_report_window)
                         predicting_atten_window.geometry("1200x600")
                         predicting_atten_window.iconbitmap('Files/src_images/icon.ico')
                         predicting_atten_window.resizable(False, False)
                         predicting_atten_window.configure(background='gray')
                         frame = Frame(predicting_atten_window)
                         frame.pack(fill=X,side=TOP)
                         lbt1=Label(frame,text="Attendance Report",font=("Imprint MT Shadow",35))
                         lbt1.pack(fill = X, expand = True,side=TOP)
                         frame1 = Frame(predicting_atten_window)
                         frame1.pack(fill=X,side=TOP)
                         lbl1=Label(frame1,text="Id              ",font=('calibri', 30, ' bold '))
                         lbl1.pack(side=LEFT)
                         lbl2=Label(frame1,text="Time                       ",font=('calibri', 30, ' bold '))
                         lbl2.pack(side=LEFT)
                         lbl3=Label(frame1,text="Date                       ",font=('calibri', 30, ' bold '))
                         lbl3.pack(side=LEFT)
                         lbl4=Label(frame1,text="Name                       ",font=('calibri', 30, ' bold '))
                         lbl4.pack(side=LEFT)
                         
                       
                         
                         
                         
                         scroll_bar = Scrollbar(predicting_atten_window)     

                         mylist = Listbox(predicting_atten_window,font = ('calibri', 26, ' bold '),background='gray',yscrollcommand = scroll_bar.set)

                         atten_list=[]
                         atten_r=[]
                         total_stud_details=pd.read_csv(r'Files/StudentDetails/StudentDetails.csv')
                         total_stud_names=list(total_stud_details['Name'])
                         for iname in total_stud_names:
                              if iname in name_data:
                                   id_v=atten_data.loc[atten_data['Name'] == iname]['Id'].values
                                   time_val=atten_data.loc[atten_data['Name'] == iname]['Time'].values
                                   date_val=atten_data.loc[atten_data['Name'] == iname]['Date'].values
                                   atten_r.append("Present")               
                                   
                                   mylist.insert(END,str(id_v[0])+'              '+str(time_val[0])+'                      '+str(date_val[0])+'              '+str(iname))
                                   mylist.insert(END,'\n')
                              elif iname:
                                   id_v2=total_stud_details.loc[total_stud_details['Name'] == iname]['Id'].values
                                   if id_v2.size>0:
                                    mylist.insert(END,str(int(id_v2[0]))+'              '+str('Unknown')+'                      '+str('Unknown')+'              '+str(iname))
                                    mylist.insert(END,'\n')
                                    atten_r.append("Absent")

                         atten_r_d={"Atten":atten_r}                      
                                   
  
                         
                         def pred_atten_report_graph():
                              plt.figure(figsize=(10,4))
                              num = pd.value_counts(atten_r_d['Atten']).sort_index()
                              num.plot(kind='bar',color=['orange','lime'])
                              plt.title("Student Attendance Report ")
                              plt.xlabel("Attendance")
                              plt.ylabel("no of students")
                              plt.xticks(rotation=0)
                              
                              plt.show()

                         frame2 = Frame(predicting_atten_window)
                         frame2.pack(fill=X,side=TOP)
                         
                         
                         blbl1=Label(frame2,text="To View graph the total Attendance report",font=('calibri', 20, ' bold '),fg="black"  ,bg="lightblue", activebackground = "#002266",activeforeground="#80b3ff" )
                         blbl1.pack(fill = X, expand = True,side=LEFT,padx=10)
                         blbl2=Button(frame2,text="show graph",command=pred_atten_report_graph,font=('calibri', 20, ' bold '),fg="black"  ,bg="lightblue", activebackground = "#002266",activeforeground="#80b3ff")
                         blbl2.pack(fill = X, expand = True,side=LEFT,padx=10)
                         

                         scroll_bar.pack( side = RIGHT,fill = Y )
                         mylist.pack( side = TOP, fill = BOTH ,expand=True )
                         scroll_bar.config( command = mylist.yview )
                         
                         predicting_atten_window.mainloop()

                    def openfilename_atten_mk():
                         filename='Files/Attendance/'+clicked.get()

                         if filename.endswith('.csv'):
                              csv_stu_data=pd.read_csv(filename)
                              csv_stu_data_col=list(csv_stu_data.columns)

                              if 'Id' in csv_stu_data_col and 'Name' in csv_stu_data_col and 'Date' in csv_stu_data_col and 'Time':

                                   predicting_atten(filename)
                              else:
                                   ms.showerror('Error!','Selected file does not have required colums \n Id, Name, Date,Time.',parent=stf_atten_report_window)  
                         else:
                              ms.showerror('Error!','Selected file is not csv file \nMake sure it is csv file.',parent=stf_atten_report_window)


                    stasgnup_btn1=Button(frame,image=Download_logo_photo,command=openfilename_atten_mk)
                    stasgnup_btn1.pack(side=LEFT)
                    clicked = StringVar()
                    clicked.set( stud_atten_report_files[-1] )
                    drop_atten = OptionMenu( frame , clicked , *stud_atten_report_files )
                    drop_atten.config( font=('calibri', 20, ' bold '))
                    drop_atten.pack(fill = X,side=LEFT)
                    stf_atten_report_window.mainloop()
              
                clearButton = Button(window, text="Clear", command=clear  ,bd=5,fg="white"  ,bg="#004d4d"  ,activebackground = "#33ff33" ,font=('times', 15, ' bold '))
                clearButton.place(x=300, y=245)
                clearButton2 = Button(window, text="Clear", command=clear2  ,bd=5,fg="white"  ,bg="#004d4d"  , activebackground = "#33ff33" ,font=('times', 15, ' bold '))
                clearButton2.place(x=300, y=365)    
                takeImg = Button(window, text="Add Student Images", command=TakeImages  ,bd=5,fg="white"  ,bg="#004d4d"  ,width=20  ,height=1, activebackground = "#33ff33" ,font=('times', 20, ' bold '))
                takeImg.place(x=40, y=430)
                trainImg = Button(window, text="Train with the Images", command=TrainImages  ,bd=5,fg="white"  ,bg="#004d4d"  ,width=20  ,height=1, activebackground = "#33ff33" ,font=('times', 20, ' bold '))
                trainImg.place(x=40, y=500)
                trackImg = Button(window, text="Take Attendance", command=TrackImages  ,bd=5,fg="white"  ,bg="#004d4d"  ,width=20  ,height=1, activebackground = "#33ff33" ,font=('times', 20, ' bold '))
                trackImg.place(x=900, y=200)
                trackImg = Button(window, text="Attendance Report", command=stf_show_att  ,bd=5,fg="white"  ,bg="#004d4d"  ,width=20  ,height=1, activebackground = "#33ff33" ,font=('times', 20, ' bold '))
                trackImg.place(x=900, y=400)
                quitWindow = Button(window, text="Quit", command=root.destroy  ,bd=5,fg="white"  ,bg="#004d4d"  ,width=20  ,height=1, activebackground = "#33ff33" ,font=('times', 20, ' bold '))
                quitWindow.place(x=900, y=500)
                
                window.mainloop()
            test()    
        else:
            ms.showerror('Oops!','Username and password Not Found.')
            
    def new_user(self):
    	#Establish Connection
        with sqlite3.connect('Files/Account_database.db') as db:
            c = db.cursor()

        #Find Existing username if any take proper action
        find_user = ('SELECT username FROM user WHERE username = ?')
        c.execute(find_user,[(self.n_username.get())])
        if self.n_username.get() and self.n_password.get():

            if c.fetchall():
                ms.showerror('Error!','Username Taken Try a Diffrent One.')
            elif self.n_password.get()==self.n_cn_password.get() :
                #Create New Account 
                insert = 'INSERT INTO user(username,password) VALUES(?,?)'
                c.execute(insert,[(self.n_username.get()),(self.n_password.get())])
                db.commit()
                ms.showinfo('Success!','Account Created!')
                self.log()
            else:
                ms.showerror('Error!','Password and Confirm Password are not same')
        else:
            ms.showerror('Error!','Kindly enter all the data')
        

        #Frame Packing Methords
    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()
    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()
        
    #Draw Widgets
    def widgets(self):
        self.head = Label(self.master,text = 'LOGIN',font = ('',35),pady = 10)
        self.head.pack()
        self.logf = Frame(self.master,padx =10,pady = 10)
        Label(self.logf,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.username,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.logf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
        
        Button(self.logf,text = ' Create Account ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.cr).grid(row=2,column=0)
        Button(self.logf,text = '      Login     ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.login).grid(row=2,column=1)
        self.logf.pack()
        
        self.crf = Frame(self.master,padx =10,pady = 10)
        Label(self.crf,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_username,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.crf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
        Label(self.crf,text = 'Confirm Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_cn_password,bd = 5,font = ('',15),show = '*').grid(row=2,column=1)
        Button(self.crf,text = '  Go to Login  ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.log).grid(row=3,column=0)
        Button(self.crf,text = ' Create Account ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.new_user).grid(row=3,column=1)
        
    
if __name__ == '__main__':
    root = Tk()
    root.title('Login Form')
    root.iconbitmap('Files/src_images/icon.ico')
    root.resizable(False, False)
    main(root)
    root.mainloop()
