# This project has a menu, a label, an image, a messageBox, and a scrollable text box.
# Simple enough, just import everything from tkinter.
from tkinter import *
from tkinter.scrolledtext import ScrolledText as Scrl
#from tkinter.messagebox import Message as MBox
from tkinter import messagebox

import logging

#download and install pillow:
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow
#Use `from PIL import Image` instead of `import Image`.
#Use pip version 19.2 or newer to install the downloaded .whl files. This page is not a pip package index.

from PIL import Image, ImageTk

#from boto3 import s3
import boto3
from botocore.exceptions import ClientError

# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # values: NOTSET (0), DEBUG (10), INFO (20), [default]WARNING (30), ERROR (40), CRITICAL (50)
        logger = logging.getLogger('server_logger')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('c:\\Temp\\PythonLog_092719.log')
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        # add the handlers to logger
        logger.addHandler(ch)
        logger.addHandler(fh)
        logger.info("This is a PySandGUIApp3 test info logging message") 
        logger.debug("This is a PySandGUIApp3 test debug logging message") 

        # changing the title of our master widget      
        self.master.title("Sandbox")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        menuTop = Menu(self.master)
        self.master.config(menu=menuTop)

        labelPythonSandbox = Label(self, text="Python Sandbox")
        #text.pack(side=LEFT)
        labelPythonSandbox.place(x=8, y=4)

        # create the file object)
        file = Menu(menuTop)

        # adds a top level menu command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        # this has no more commands under it
        file.add_command(label="Exit", command=self.client_exit)

        #add top level menu command "file" to our menu that has sub items under it
        menuTop.add_cascade(label="File", menu=file)

        # create the file object. Create the drop down menu under the Top Level "File" nemu selection
        menuEdit = Menu(menuTop)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        menuEdit.add_command(label="Show Img", command=self.showImg)
        menuEdit.add_command(label="Show Text", command=self.showText)
        menuEdit.add_command(label="Show Edit", command=self.showEdit)

        #added "file" to our menu
        menuTop.add_cascade(label="Edit", menu=menuEdit)

        strings2 = list() # [] #
        #s3_client = boto3.client('s3') #unable to locate credentials
        # Do not hard code credentials
        s3_client = boto3.client(
            's3',
            # Hard coded strings as credentials, not recommended.
            aws_access_key_id='AKIAJUENIVEUWAXOMURA',
            aws_secret_access_key='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'
        )
        response = s3_client.list_buckets()
        
        # Output the bucket names
        #print('Existing buckets:')
        strings2.append("Existing buckets:\n")
        for bucket in response['Buckets']:
            strings2.append(str(bucket["Name"]) + "\n")
            #print(f'  {bucket["Name"]}')
        verbiageS3 = ' ' 
        verbiageS3 = verbiageS3.join(strings2)

        #client = boto3.client(
        #    's3',
        #     aws_access_key_id=ACCESS_KEY,
        #     aws_secret_access_key=SECRET_KEY,
        #     aws_session_token=SESSION_TOKEN,
        #)
        
        #strings2.append("one" + "\n")

        #s3 = boto3.resource('s3')
        # Print out Bucket Names
        #for bucket in s3.buckets.all()
        #    print(bucket.name)

        #verbiage = """You pretty much want to install the latest version of Python 2.7 and 3.7+ from Python.org.
        #Update Visual Studio. Choose Help > Check for Updates. (2017+) Or start Visual Studio Installer.
        #Modify - Visual Studio. Add Python.
        #
        #Anaconda is a Python version with many libraries already included.
        #IronPython that uses .Net CLR seems nice, but also seems pointless.
        #
        #Install Python to Visual Studio 2017 from App Store.
        #py -3 --version"""
      
        ## Put the Text Box code here...
        ##foo=scrollTxtArea(root)
        scText1 = Scrl(self)
        scText1.place(x=10, y=28, height=200, width = 400)
        scText1.insert(END, verbiageS3)

        messagebox.showinfo("Title", "a Tk MessageBox")

### End def init_window(self):

    def client_exit(self):
        exit()

    def showMessageBox(self):
        text = Label(self, text="Hey there good lookin!")
        text.pack()        


    def showText(self):
        text = Label(self, text="Hey there good lookin!")
        text.pack()        


    def showEdit(self):
        edit = Text(root, height=2, width=30)
        edit.place(x=10, y=20)
        #edit.pack()
        #edit.insert(tk.END, "Just a text Widget\nin two lines\n")
        edit.insert(END, "Just a text Widget\nin two lines\n")

    # who shows an image???
    def showImg(self):
        load = Image.open("c:\\Temp\\Flowers_0819.png")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()

root.geometry("600x600")

#creation of an instance
app = Window(root)


#mainloop 
root.mainloop()  

