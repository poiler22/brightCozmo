import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
import sys
import CozmoMainCode
import threading
from PIL import ImageTk, Image
import os
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2
import json
import ast
import os.path
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        #container = tk.Frame(self)
        container = tk.Frame(self,width=500,height=500)
        container.pack(side="top", fill="both", expand=False)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, ConversationPage, ListOfEmailPage,
                  ListOfSongPage,AddSong,DeleteSong,Add_Email,Add_User_Email):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        frame.update()




class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="The Bright Cozmo", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        b = tk.Button(self)
        image = ImageTk.PhotoImage(file="cozmohaha.jpg")
        b.config(image=image, height=300)
        b.image = image
        b.pack()

        button1 = tk.Button(self, text="Edit",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Start",
                            command=lambda: [controller.show_frame("ConversationPage"),threading.Thread(target=CozmoMainCode.run).start()])
                            # command=lambda: [controller.show_frame("ConversationPage"),CozmoMainCode.run()])

        button3 = tk.Button(self, text="End", command=lambda: sys.exit())
        #button4 = tk.Button(self, text="Restart",
         #command=lambda: [os.execl(sys.executable, sys.executable, *sys.argv),SampleApp().mainloop()])
        button2.pack(pady=10)
        button1.pack(pady=10)
        #button4.pack(pady=10)
        button3.pack(pady=10)





class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Edit Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=20)
        button0 = tk.Button(self, text="Email",
                           command=lambda: controller.show_frame("ListOfEmailPage"))
        button1 = tk.Button(self, text="Song",
                           command=lambda: controller.show_frame("ListOfSongPage"))
        button2 = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button0.pack(pady=10)
        button1.pack(pady=10)
        button2.pack(pady=10)

class ListOfSongPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="List of the songs:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=20)
        json_file = open('texttest.json')
        json_str = json_file.read()
        json_data = ast.literal_eval(json_str)
        ListOfSong = json_data

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side='right', fill='y')
        ListOfSongPage.mylist = tk.Listbox(self, yscrollcommand=scrollbar.set, width= 80, height=5)#,width=300,height=300))
        ListOfSongPage.mylist.pack(side="left", fill="both", expand=True)
        for idx, item in enumerate(ListOfSong['song']):
            ListOfSongPage.mylist.insert('end',"Song's name: " + item['name'] )#, 'URL: ' + item['url'])

        ListOfSongPage.mylist.pack(side='top', expand=True)
        scrollbar.config(command=ListOfSongPage.mylist.yview)
        # label1 = tk.Label(self, text=ListOfSong, font=controller.title_font, anchor='center')
        #label.pack(side="top", fill="x", pady=10)

        button0 = tk.Button(self, text="add song",
                           command=lambda: controller.show_frame("AddSong"))
        button0.pack(pady=20,side='left',expand=True)
        # button1 = tk.Button(self, text="delete song",
        #                    command=lambda: controller.show_frame("DeleteSong"))
        button1 = tk.Button(self, text="delete song",
                            # command=lambda: mylist.delete('anchor'))
                            command=lambda: brightDeleting2(ListOfSongPage.mylist.get('active'), ListOfSongPage.mylist))
        button1.pack(pady=20,side='left',expand=True)
        button2 = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button3 = tk.Button(self, text="back",
                            command=lambda: controller.show_frame("PageOne"))
        button3.pack(pady=20, side='left', expand=True)
        button2.pack(pady=20,side='left',expand=True)




class ListOfEmailPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="List of the emails:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=20)
        json_file = open('emailtext.json')
        json_str = json_file.read()
        #print(json_str)
        json_data = ast.literal_eval(json_str)
        ListOfSong = json_data

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side='right', fill='y')
        ListOfEmailPage.mylist = tk.Listbox(self, yscrollcommand=scrollbar.set, width= 80, height=5)#,width=300,height=300))
        ListOfEmailPage.mylist.pack(side="left", fill="both", expand=True)
        for idx, item in enumerate(ListOfSong['email']):
            ListOfEmailPage.mylist.insert('end',"User's name: " + item['name'] )#, 'URL: ' + item['url'])

        ListOfEmailPage.mylist.pack(side='top', expand=True)
        scrollbar.config(command=ListOfEmailPage.mylist.yview)
        # label1 = tk.Label(self, text=ListOfSong, font=controller.title_font, anchor='center')
        #label.pack(side="top", fill="x", pady=10)

        button0 = tk.Button(self, text="add email",
                           command=lambda: controller.show_frame("Add_Email"))
        button0.pack(pady=20,side='left',expand=True)
        # button1 = tk.Button(self, text="delete song",
        #                    command=lambda: controller.show_frame("DeleteSong"))
        button1 = tk.Button(self, text="delete email",
                            # command=lambda: mylist.delete('anchor'))
                            command=lambda: bright_Email_Deleting(ListOfEmailPage.mylist.get('active'), ListOfEmailPage.mylist))
        button1.pack(pady=10,side='left',expand=True)
        button2 = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button3 = tk.Button(self, text="back",
                            command=lambda: controller.show_frame("PageOne"))
        button4 = tk.Button(self, text="Connect your email", command=lambda: controller.show_frame("Add_User_Email"))
        button4.pack(pady=5, side='left', expand=True)

        button3.pack(pady=10, side='left', expand=True)
        button2.pack(pady=10,side='left',expand=True)


class ConversationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Conversation Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

def bright_Song_Adding(nameOfSong,keyOfSong):
    json_file = open('texttest.json')
    json_str = json_file.read()
    dictOfSong = ast.literal_eval(json_str)
    d = {"name": nameOfSong, "url": keyOfSong}
    for listofname in range(len(dictOfSong['song'])):
        print(dictOfSong['song'][listofname]['name'])
        if dictOfSong['song'][listofname]['name'] == nameOfSong:
            return alreadyNotification()
    dictOfSong['song'].append(d)
    output_file = open('texttest.json', 'w')
    output_file.write(str(dictOfSong))
    ListOfSongPage.mylist.insert('end', "Song's name: " + nameOfSong)
    doneNotification()

def bright_Email_Adding(nameOfUser,keyOfEmail):
    json_file = open('emailtext.json')
    json_str = json_file.read()
    dictOfEmail = ast.literal_eval(json_str)
    d = {"name": nameOfUser, "url": keyOfEmail}
    for listofname in range(len(dictOfEmail['email'])):
        print(dictOfEmail['email'][listofname]['name'])
        if dictOfEmail['email'][listofname]['name'] == nameOfUser:
            return alreadyNotification()
    dictOfEmail['email'].append(d)
    output_file = open('emailtext.json', 'w')
    output_file.write(str(dictOfEmail))
    ListOfEmailPage.mylist.insert('end', "User's name: " + nameOfUser)
    doneNotification()

def create_User_Email_Adding(nameOfEmail,keyOfPassword):
    json_file = open('useradding.json')
    json_str = json_file.read()
    dictOfUser = ast.literal_eval(json_str)
    d = {"name": nameOfEmail, "password": keyOfPassword}
    dictOfUser['email'].clear()
    dictOfUser['email'].append(d)
    output_file = open('useradding.json', 'w')
    output_file.write(str(dictOfUser))
    doneNotification()
def brightDeleting(nameOfSong):
    json_file = open('texttest.json')
    json_str = json_file.read()
    dictOfSong = ast.literal_eval(json_str)
    for index in range(len(dictOfSong['song'])):
        if dictOfSong['song'][index]['name'] == nameOfSong:
            dictOfSong['song'].pop(index)
            break
    output_file = open('texttest.json','w')
    output_file.write(str(dictOfSong))

def brightAdding2(nameOfSong,keyOfSong, mylist):
    json_file = open('texttest.json')
    json_str = json_file.read()
    dictOfSong = ast.literal_eval(json_str)
    d = {"name": nameOfSong, "url": keyOfSong}
    dictOfSong['song'].append(d)
    output_file = open('texttest.json', 'w')
    output_file.write(str(dictOfSong))

def bright_Email_Adding2(nameOfUser,keyOfEmail, mylist):
    json_file = open('emailtext.json')
    json_str = json_file.read()
    dictOfEmail = ast.literal_eval(json_str)
    d = {"name": nameOfUser, "url": keyOfEmail}
    dictOfEmail['email'].append(d)
    output_file = open('emailtext.json', 'w')
    output_file.write(str(dictOfEmail))

def brightDeleting2(nameOfSong, mylist):
    nameOfSong = (nameOfSong.split(':'))[1].strip()
    # print(nameOfSong)
    json_file = open('texttest.json')
    json_str = json_file.read()
    dictOfSong = ast.literal_eval(json_str)

    for index in range(len(dictOfSong['song'])):
        if dictOfSong['song'][index]['name'] == nameOfSong:
            dictOfSong['song'].pop(index)
            break
    output_file = open('texttest.json','w')
    output_file.write(str(dictOfSong))
    mylist.delete('anchor')


def doneNotification():
    toplevel = tk.Toplevel()
    label1 = tk.Label(toplevel, text="Done!", height=5, width=10)
    label1.pack()

def alreadyNotification():
    toplevel = tk.Toplevel()
    label1 = tk.Label(toplevel, text="Name already been used! \n Please use other names.", height=10, width=30)
    label1.pack()


def bright_Email_Deleting(nameOfSong, mylist):
    nameOfSong = (nameOfSong.split(':'))[1].strip()
    # print(nameOfSong)
    json_file = open('emailtext.json')
    json_str = json_file.read()
    dictOfSong = ast.literal_eval(json_str)

    for index in range(len(dictOfSong['email'])):
        if dictOfSong['email'][index]['name'] == nameOfSong:
            dictOfSong['email'].pop(index)
            break
    output_file = open('emailtext.json','w')
    output_file.write(str(dictOfSong))
    mylist.delete('anchor')

class Add_Email(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Please insert name and email", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        #print("First Name: \nLast Name: ")
        tk.Label(self, text="Name of the User: ").pack(anchor='n')
        nameOfUser = tk.Entry(self)
        nameOfUser.pack(anchor='n')
        tk.Label(self, text="Email: ").pack(anchor='n')
        keyOfEmail = tk.Entry(self)
        keyOfEmail.pack(anchor='n')


        button0 = tk.Button(self, text="OK",command=lambda: bright_Email_Adding(nameOfUser.get(), keyOfEmail.get()) )
        button1 = tk.Button(self, text="Clear",command=lambda: [keyOfEmail.delete(0,'end'),nameOfUser.delete(0,'end')] )
        button2 = tk.Button(self, text="Go to the start page",command=lambda: controller.show_frame("StartPage"))
        button0.pack(pady=5, side='left', expand=True)
        button1.pack(pady=5, side='left', expand=True)
        button3 = tk.Button(self, text="back",
                            command=lambda: controller.show_frame("ListOfEmailPage"))
        button3.pack(pady=5, side='left', expand=True)
        button2.pack(pady=5, side='left', expand=True)

class Add_User_Email(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Please insert email and password", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        #print("First Name: \nLast Name: ")
        tk.Label(self, text="Your email: ").pack(anchor='n')
        nameOfEmail = tk.Entry(self)
        nameOfEmail.pack(anchor='n')
        tk.Label(self, text="Password: ").pack(anchor='n')
        keyOfPassword = tk.Entry(self, show="*")
        #Entry(parent, show="*", width=15)
        keyOfPassword.pack(anchor='n')


        button0 = tk.Button(self, text="OK",command=lambda: create_User_Email_Adding(nameOfEmail.get(), keyOfPassword.get()) )
        button1 = tk.Button(self, text="Clear",command=lambda: [nameOfEmail.delete(0,'end'),keyOfPassword.delete(0,'end')] )
        button2 = tk.Button(self, text="Go to the start page",command=lambda: controller.show_frame("StartPage"))
        button0.pack(pady=5, side='left', expand=True)
        button1.pack(pady=5, side='left', expand=True)
        button3 = tk.Button(self, text="back",
                            command=lambda: controller.show_frame("ListOfEmailPage"))
        button3.pack(pady=5, side='left', expand=True)
        button2.pack(pady=5, side='left', expand=True)

class AddSong(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Please insert name and link of the song", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        #print("First Name: \nLast Name: ")
        tk.Label(self, text="Name of the song: ").pack(anchor='n')
        nameOfSong = tk.Entry(self)
        nameOfSong.pack(anchor='n')
        tk.Label(self, text="URL (or a link): ").pack(anchor='n')
        keyOfSong = tk.Entry(self)
        keyOfSong.pack(anchor='n')


        button0 = tk.Button(self, text="OK",command=lambda: bright_Song_Adding(nameOfSong.get(), keyOfSong.get()) )
        button1 = tk.Button(self, text="Clear",command=lambda: [nameOfSong.delete(0,'end'),keyOfSong.delete(0,'end')])
        button2 = tk.Button(self, text="Go to the start page",command=lambda: controller.show_frame("StartPage"))
        button0.pack(pady=5, side='top', expand=True)
        button1.pack(pady=5, side='top', expand=True)
        button3 = tk.Button(self, text="back",
                            command=lambda: controller.show_frame("ListOfSongPage"))
        button3.pack(pady=5, side='top', expand=True)
        button2.pack(pady=5, side='top', expand=True)



class DeleteSong(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Deleting Song", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        #print("First Name: \nLast Name: ")
        tk.Label(self, text="Name of the song: ").pack(anchor='n')
        nameOfSong = tk.Entry(self)
        nameOfSong.pack(anchor='n')
        #tk.Label(self, text="URL key: ").pack(anchor='n')
        #keyOfSong = tk.Entry(self)
        #keyOfSong.pack(anchor='n')


        button0 = tk.Button(self, text="OK",command=lambda: brightDeleting(nameOfSong.get()))
        button1 = tk.Button(self, text="Clear")
        button2 = tk.Button(self, text="Go to the start page",command=lambda: controller.show_frame("StartPage"))
        button0.pack(pady=5, side='top', expand=True)
        button1.pack(pady=5, side='top', expand=True)
        button2.pack(pady=5, side='top', expand=True)

class Delete(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Conversation Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

if __name__ == "__main__":
    #app = SampleApp()
    SampleApp().mainloop()