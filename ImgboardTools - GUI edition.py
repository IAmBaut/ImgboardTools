import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk,filedialog,messagebox
from ImgboardTools import *
try:
    from PIL import Image,ImageTk
except ImportError:
    print("Module PIL missing.\nAborting.")


class App:
    def __init__(self, root):
        self.items=[] # List containing pointers to active objects in current window (except for the program title and navigation)
        self.options=["Delete image Exif data from image","Change webm metadata","Create \"hidden\" double image","Create hidden monochrome image","Create cursed video[mp4/webm]","Distort .webm aspect ratios","Generate base64 encoded md5 hash"] #Contains options of dropdown menu
        #setting title
        root.title("ImageboardTools - GUI edition")
        #setting window size
        width=600
        height=550
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        #Setting a label with the title again
        TitleLabel=tk.Label(root)
        ft = tkFont.Font(family='Times',size=28)
        TitleLabel["font"] = ft
        TitleLabel["fg"] = "#000000"
        TitleLabel["justify"] = "center"
        TitleLabel["text"] = "Imageboard tools - GUI edition"
        TitleLabel.place(x=0,y=20,width=600,height=40)
        #Setting label + combobox for users to choose functionality they want
        InfoLabel1=tk.Label(root)
        ft = tkFont.Font(family='Times',size=15)
        InfoLabel1["font"] = ft
        InfoLabel1["fg"] = "#000000"
        InfoLabel1["justify"] = "center"
        InfoLabel1["text"] = "Choose functionality:"
        InfoLabel1.place(x=70,y=80,width=187,height=31)

        self.Combo=ttk.Combobox(root,values=self.options,state="readonly")
        self.Combo.set("Click here to choose functionality.")
        self.Combo.pack(padx=5,pady=5)
        self.Combo.place(x=270,y=80,width=250,height=30)
        self.Combo.bind("<<ComboboxSelected>>", self.comboChange)


    #---------

    #Buttons are handled here

    def LeftFileButton_command(self):
        #Opens file dialog and puts data of filedialog in LeftFileEntry
        self.filename=filedialog.askopenfilename(initialdir = self.LeftFileEntry.get(),title = "Select file",filetypes = (("images","*.jpg *.png"),("all files","*.*")))
        self.LeftFileEntry.delete(0,tk.END)
        self.LeftFileEntry.insert(0,self.filename)
        #Load the image the filedialog chose, if this fails, load example image
        updateImg(self,30,180)

    def RightFileButton_command(self):
        #Opens file dialog and puts data of filedialog in LeftFileEntry
        root.filename2=filedialog.askopenfilename(initialdir = self.RightFileEntry.get(),title = "Select file",filetypes = (("images","*.jpg *.png"),("all files","*.*")))
        self.RightFileEntry.delete(0,tk.END)
        self.RightFileEntry.insert(0,root.filename2)
        #Load the image the filedialog chose, if this fails, load example image
        try:
            imagedata=loadImg(self,root.filename2)
            self.myimage2.destroy()
            self.myimage2=tk.Label(root,image=imagedata[0])
            self.myimage2.image=imagedata[0]
            self.myimage2.place(x=int(320+100-imagedata[1]/2),y=int(180+100-imagedata[2]/2))
            self.items+=[self.myimage2]
        except:
            tk.messagebox.showinfo('Error','Problem loading your image, try again or choose another image.')
            imagedata=loadImg(self,"./GUI_images/issue.png")
            self.myimage2.destroy()
            self.myimage2=tk.Label(root,image=imagedata[0])
            self.myimage2.image=imagedata[0]
            self.myimage2.place(x=int(320+100-imagedata[1]/2),y=int(180+100-imagedata[2]/2))
            self.items+=[self.myimage2]

    def confirmButton_command(self):
        if(hideIMG(self.LeftFileEntry.get(),self.RightFileEntry.get())):
            self.HideLabelInfo3["text"]="Done!"

    def WebmButtonTop_command(self):
        self.filename=filedialog.askopenfilename(initialdir = self.WebmEntryTop.get(),title = "Select file",filetypes = (("webm files","*.webm"),("all files","*.*")))
        self.WebmEntryTop.delete(0,tk.END)
        self.WebmEntryTop.insert(0,self.filename)
        self.WebmEntryBottom["state"]="normal"

    def WebmButtonConfirmation_command(self):
        if (changeWebmTitle(self.WebmEntryBottom.get(),self.WebmEntryTop.get())):
            self.WebmLabelInfo4["text"]="Done!"


    def ExifButtonFile_command(self):
        self.filename=filedialog.askopenfilename(initialdir = self.ExifEntryMain.get(),title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.ExifEntryMain.delete(0,tk.END)
        self.ExifEntryMain.insert(0,self.filename)
        #Load the image the filedialog chose, if this fails, load example image
        updateImg(self,200,200)

    def ExifButtonConfirm_command(self):
        if (deleteExif(self.filename)):
            self.ExifLabelInfo3["text"]="Done!"

    def MONOButtonFile_command(self):
        self.filename=filedialog.askopenfilename(initialdir = self.MONOEntryMain.get(),title = "Select file",filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))
        self.MONOEntryMain.delete(0,tk.END)
        self.MONOEntryMain.insert(0,self.filename)
        #Load the image the filedialog chose, if this fails, load example image
        updateImg(self,160,260)

    def MONOButtonConfirm_command(self):
        RGB=self.MONOEntrySec.get()
        if RGB:
            RGB=RGB.strip().split()
            if len(RGB)==3:
                for i in range(len(RGB)):
                    RGB[i]=int(RGB[i])
                if (greyifyImg(self.MONOEntryMain.get(),R=RGB[0],G=RGB[1],B=RGB[2])):
                    self.MONOLabelInfo3["text"]="Done."
            else:
                tk.messagebox.showinfo('Error','You didn\'t give three arguments. Please give 3 integers (R G B) between 0-255 seperated by spaces.')
        else:
            if (greyifyImg(self.MONOEntryMain.get())):
                self.MONOLabelInfo3["text"]="Done."

    def CURSEButtonFile_command(self):
        self.filename=filedialog.askopenfilename(initialdir = self.CURSEEntryMain.get(),title = "Select file",filetypes = (("video files(webm/mp4)","*.webm *.mp4"),("all files","*.*")))
        self.CURSEEntryMain.delete(0,tk.END)
        self.CURSEEntryMain.insert(0,self.filename)

    def CURSEButtonConfirm_command(self):
        loc=self.CURSEEntryMain.get()
        hexdata=self.CURSEEntrySec.get()
        if len(hexdata)!=16:
            tk.messagebox.showinfo('Error','This process expects a hexstring length of 16 (= 8 bytes).')
            hexdata=""
        if (self.CURSEEntryMain.get()):
            if (hexdata):
                if (curseVid(loc,hexdata)):
                    self.CURSELabelInfo2["text"]="Done."
            else:
                if (curseVid(loc)):
                    self.CURSELabelInfo2["text"]="Done."
        else:
            tk.messagebox.showinfo('Error','You didn\'t specify a file.')

    def DISTORTButtonFile_command(self):
        self.filename=filedialog.askopenfilename(initialdir = self.DISTORTEntryMain.get(),title = "Select file",filetypes = (("video files(webm)","*.webm"),("all files","*.*")))
        self.DISTORTEntryMain.delete(0,tk.END)
        self.DISTORTEntryMain.insert(0,self.filename)

    def DISTORTButtonConfirm_command(self):
        loc=self.DISTORTEntryMain.get()
        distort=self.DISTORTEntrySec.get()
        out=self.DISTORTEntryTert.get()
        try:
            distort=int(distort)
        except Exception:
            tk.messagebox.showinfo('Error','Please specify a valid integer as distortions/second value.')
        if not out:
            if aspectMagic(loc,distort):
                self.DISTORTLabelInfo2["text"]="Done."
            else:
                tk.messagebox.showinfo('Error','Something went wrong. Make sure the input file path is valid.')
        else:
            if aspectMagic(loc,distort,out):
                self.DISTORTLabelInfo2["text"]="Done."
            else:
                tk.messagebox.showinfo('Error','Something went wrong. Make sure the input file path is valid.')

    def md5FileButtonTop_command(self):
        self.filename=filedialog.askopenfilename(initialdir = self.md5FileEntryTop.get(),title = "Select file")
        self.md5FileEntryTop.delete(0,tk.END)
        self.md5FileEntryTop.insert(0,self.filename)
        self.md5HexOut.delete(0,tk.END)
        self.md5HexOut2.delete(0,tk.END)
    
    def Md5ButtonConfirmation_command(self):
        loc=self.md5FileEntryTop.get()
        if not loc:
            tk.messagebox.showinfo('Error','No input file was specified. Make sure the input file path is valid.')
        else:
            ret=generateMd5(loc)
            self.md5HexOut.delete(0,tk.END)
            self.md5HexOut.insert(0,ret[1])
            self.md5HexOut2.delete(0,tk.END)
            self.md5HexOut2.insert(0,ret[0])

    #Function to handle user choosing a program functionality
    def comboChange(self,event):
        cleanup(self.items)
        self.items=[]
        chosen=self.options.index((self.Combo.get()))
        if chosen==0:
            setupEXIF(self)
        elif chosen==1:
            setupWebm(self)
        elif chosen==2:
            setupHide(self)
        elif chosen==3:
            setupMONO(self)
        elif chosen==4:
            setupCURSE(self)
        elif chosen==5:
            setupDISTORT(self)
        elif chosen==6:
            setupMd5(self)



def loadImg(self,imagename):
    image = Image.open(imagename)
    aspect = max(image.size[0],image.size[1])/200
    newx = int(image.size[0]/aspect)
    newy = int(image.size[1]/aspect)
    image = image.resize((newx,newy))
    photo = ImageTk.PhotoImage(image)
    return (photo,newx,newy)

def updateImg(self,posx,posy):
    try:
        imagedata=loadImg(self,self.filename)
        self.previmage.destroy()
        self.previmage=tk.Label(root,image=imagedata[0])
        self.previmage.image=imagedata[0]
        self.previmage.place(x=int(posx+100-imagedata[1]/2),y=int(posy+100-imagedata[2]/2))
        self.items+=[self.previmage]
    except:
        tk.messagebox.showinfo('Error','Problem loading your image, try again or choose another image.')
        imagedata=loadImg(self,"./GUI_images/issue.png")
        self.previmage.destroy()
        self.previmage=tk.Label(root,image=imagedata[0])
        self.previmage.image=imagedata[0]
        self.previmage.place(x=int(posx+100-imagedata[1]/2),y=int(posy+100-imagedata[2]/2))
        self.items+=[self.previmage]

def setupHide(self):
    self.LeftFileEntry=tk.Entry(root)
    self.LeftFileEntry["borderwidth"] = "2px"
    ft = tkFont.Font(family='Times',size=10)
    self.LeftFileEntry["font"] = ft
    self.LeftFileEntry["fg"] = "#000000"
    self.LeftFileEntry["justify"] = "left"
    self.LeftFileEntry["text"] = "LeftFileEntry"
    self.LeftFileEntry.place(x=30,y=130,width=200,height=30)
    self.items+=[self.LeftFileEntry]

    self.LeftFileButton=tk.Button(root)
    self.LeftFileButton["bg"] = "#181a1b"
    ft = tkFont.Font(family='Times',size=20)
    self.LeftFileButton["font"] = ft
    self.LeftFileButton["fg"] = "#e8e6e3"
    self.LeftFileButton["justify"] = "center"
    self.LeftFileButton["text"] = "open"
    self.LeftFileButton.place(x=240,y=130,width=40,height=30)
    self.LeftFileButton["command"] = self.LeftFileButton_command
    self.items+=[self.LeftFileButton]

    self.RightFileEntry=tk.Entry(root)
    self.RightFileEntry["borderwidth"] = "2px"
    ft = tkFont.Font(family='Times',size=10)
    self.RightFileEntry["font"] = ft
    self.RightFileEntry["fg"] = "#000000"
    self.RightFileEntry["justify"] = "left"
    self.RightFileEntry["text"] = "RightFileEntry"
    self.RightFileEntry.place(x=320,y=130,width=200,height=30)
    self.items+=[self.RightFileEntry]

    self.RightFileButton=tk.Button(root)
    self.RightFileButton["bg"] = "#181a1b"
    ft = tkFont.Font(family='Times',size=20)
    self.RightFileButton["font"] = ft
    self.RightFileButton["fg"] = "#e8e6e3"
    self.RightFileButton["justify"] = "center"
    self.RightFileButton["text"] = "open"
    self.RightFileButton.place(x=530,y=130,width=40,height=30)
    self.RightFileButton["command"] = self.RightFileButton_command
    self.items+=[self.RightFileButton]

    self.confirmButton=tk.Button(root)
    self.confirmButton["bg"] = "#181a1b"
    ft = tkFont.Font(family='Times',size=20)
    self.confirmButton["font"] = ft
    self.confirmButton["fg"] = "#e8e6e3"
    self.confirmButton["justify"] = "center"
    self.confirmButton["text"] = "Create hidden .png"
    self.confirmButton.place(x=160,y=450,width=291,height=55)
    self.confirmButton["command"] = self.confirmButton_command
    self.items+=[self.confirmButton]

    photo1=loadImg(self,"./GUI_images/preview.png")
    self.previmage = tk.Label(root,image=photo1[0])
    self.previmage.image=photo1[0]
    self.previmage.place(x=int(30+100-photo1[1]/2),y=int(180+100-photo1[2]/2))
    self.items+=[self.previmage]

    photo2=loadImg(self,"./GUI_images/preview.png")
    self.myimage2 = tk.Label(root,image=photo2[0])
    self.myimage2.image=photo2[0]
    self.myimage2.place(x=int(320+100-photo2[1]/2),y=int(180+100-photo2[2]/2))
    self.items+=[self.myimage2]

    self.HideLabelInfo1=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    self.HideLabelInfo1["font"] = ft
    self.HideLabelInfo1["fg"] = "#000000"
    self.HideLabelInfo1["justify"] = "left"
    self.HideLabelInfo1["text"] = "Thumbnail image"
    self.HideLabelInfo1.place(x=30,y=400,width=200,height=25)
    self.items+=[self.HideLabelInfo1]

    self.HideLabelInfo2=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    self.HideLabelInfo2["font"] = ft
    self.HideLabelInfo2["fg"] = "#000000"
    self.HideLabelInfo2["justify"] = "left"
    self.HideLabelInfo2["text"] = "\"Hidden\" image"
    self.HideLabelInfo2.place(x=330,y=400,width=200,height=25)
    self.items+=[self.HideLabelInfo2]

    self.HideLabelInfo3=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    self.HideLabelInfo3["font"] = ft
    self.HideLabelInfo3["fg"] = "#000000"
    self.HideLabelInfo3["justify"] = "left"
    self.HideLabelInfo3["text"] = ""
    self.HideLabelInfo3.place(x=460,y=450,width=85,height=55)
    self.items+=[self.HideLabelInfo3]


def setupEXIF(self):
    self.ExifLabelInfo1=tk.Label(root)
    ft = tkFont.Font(family='Times',size=15)
    self.ExifLabelInfo1["font"] = ft
    self.ExifLabelInfo1["fg"] = "#000000"
    self.ExifLabelInfo1["anchor"] = "w"
    self.ExifLabelInfo1["text"] = "Choose Image:"
    self.ExifLabelInfo1.place(x=110,y=130,width=300,height=25)
    self.items+=[self.ExifLabelInfo1]

    self.ExifEntryMain=tk.Entry(root)
    self.ExifEntryMain["borderwidth"] = "2px"
    ft = tkFont.Font(family='Times',size=10)
    self.ExifEntryMain["font"] = ft
    self.ExifEntryMain["fg"] = "#000000"
    self.ExifEntryMain["justify"] = "left"
    self.ExifEntryMain["text"] = "ExifEntryMain"
    self.ExifEntryMain.place(x=110,y=160,width=300,height=30)
    self.items+=[self.ExifEntryMain]

    self.ExifButtonFile=tk.Button(root)
    self.ExifButtonFile["bg"] = "#181a1b"
    ft = tkFont.Font(family='Times',size=18)
    self.ExifButtonFile["font"] = ft
    self.ExifButtonFile["fg"] = "#e8e6e3"
    self.ExifButtonFile["justify"] = "center"
    self.ExifButtonFile["text"] = "open"
    self.ExifButtonFile.place(x=420,y=160,width=70,height=30)
    self.ExifButtonFile["command"] = self.ExifButtonFile_command
    self.items+=[self.ExifButtonFile]

    self.ExifButtonConfirm=tk.Button(root)
    self.ExifButtonConfirm["bg"] = "#181a1b"
    ft = tkFont.Font(family='Times',size=20)
    self.ExifButtonConfirm["font"] = ft
    self.ExifButtonConfirm["fg"] = "#e8e6e3"
    self.ExifButtonConfirm["justify"] = "center"
    self.ExifButtonConfirm["text"] = "Clear EXIF data"
    self.ExifButtonConfirm.place(x=150,y=430,width=300,height=30)
    self.ExifButtonConfirm["command"] = self.ExifButtonConfirm_command
    self.items+=[self.ExifButtonConfirm]

    self.ExifLabelInfo2=tk.Label(root)
    ft = tkFont.Font(family='Times',size=10)
    self.ExifLabelInfo2["font"] = ft
    self.ExifLabelInfo2["fg"] = "#000000"
    self.ExifLabelInfo2["justify"] = "center"
    self.ExifLabelInfo2["text"] = "Image"
    self.ExifLabelInfo2.place(x=150,y=400,width=300,height=30)
    self.items+=[self.ExifLabelInfo2]

    photo=loadImg(self,"./GUI_images/preview.png")
    self.previmage = tk.Label(root,image=photo[0])
    self.previmage.image=photo[0]
    self.previmage.place(x=int(200+100-photo[1]/2),y=int(200+100-photo[2]/2))
    self.items+=[self.previmage]

    self.ExifLabelInfo3=tk.Label(root)
    ft = tkFont.Font(family='Times',size=20)
    self.ExifLabelInfo3["font"] = ft
    self.ExifLabelInfo3["fg"] = "#000000"
    self.ExifLabelInfo3["justify"] = "center"
    self.ExifLabelInfo3["text"] = ""
    self.ExifLabelInfo3.place(x=470,y=430,width=80,height=30)
    self.items+=[self.ExifLabelInfo3]

def setupMONO(self):
    self.MONOLabelInfo1=tk.Label(root)
    ft = tkFont.Font(family='Times',size=15)
    self.MONOLabelInfo1["font"] = ft
    self.MONOLabelInfo1["fg"] = "#000000"
    self.MONOLabelInfo1["anchor"] = "w"
    self.MONOLabelInfo1["text"] = "Choose Image:"
    self.MONOLabelInfo1.place(x=110,y=110,width=300,height=25)
    self.items+=[self.MONOLabelInfo1]

    self.MONOEntryMain=tk.Entry(root)
    self.MONOEntryMain["borderwidth"] = "2px"
    ft = tkFont.Font(family='Times',size=10)
    self.MONOEntryMain["font"] = ft
    self.MONOEntryMain["fg"] = "#000000"
    self.MONOEntryMain["justify"] = "left"
    self.MONOEntryMain["text"] = "MONOEntryMain"
    self.MONOEntryMain.place(x=110,y=140,width=300,height=30)
    self.items+=[self.MONOEntryMain]

    self.MONOEntrySec=tk.Entry(root)
    self.MONOEntrySec["borderwidth"] = "2px"
    ft = tkFont.Font(family='Times',size=10)
    self.MONOEntrySec["font"] = ft
    self.MONOEntrySec["fg"] = "#000000"
    self.MONOEntrySec["justify"] = "left"
    self.MONOEntrySec["text"] = "MONOEntrySec"
    self.MONOEntrySec.place(x=110,y=210,width=300,height=30)
    self.items+=[self.MONOEntrySec]

    self.MONOButtonFile=tk.Button(root)
    self.MONOButtonFile["bg"] = "#181a1b"
    ft = tkFont.Font(family='Times',size=18)
    self.MONOButtonFile["font"] = ft
    self.MONOButtonFile["fg"] = "#e8e6e3"
    self.MONOButtonFile["justify"] = "center"
    self.MONOButtonFile["text"] = "open"
    self.MONOButtonFile.place(x=420,y=140,width=70,height=30)
    self.MONOButtonFile["command"] = self.MONOButtonFile_command
    self.items+=[self.MONOButtonFile]

    self.MONOButtonConfirm=tk.Button(root)
    self.MONOButtonConfirm["bg"] = "#181a1b"
    ft = tkFont.Font(family='Times',size=18)
    self.MONOButtonConfirm["font"] = ft
    self.MONOButtonConfirm["fg"] = "#e8e6e3"
    self.MONOButtonConfirm["justify"] = "center"
    self.MONOButtonConfirm["text"] = "Create ninja .png"
    self.MONOButtonConfirm.place(x=110,y=470,width=300,height=30)
    self.MONOButtonConfirm["command"] = self.MONOButtonConfirm_command
    self.items+=[self.MONOButtonConfirm]

    photo=loadImg(self,"./GUI_images/preview.png")
    self.previmage = tk.Label(root,image=photo[0])
    self.previmage.image=photo[0]
    self.previmage.place(x=int(160+100-photo[1]/2),y=int(260+100-photo[2]/2))
    self.items+=[self.previmage]

    self.MONOLabelInfo3=tk.Label(root)
    ft = tkFont.Font(family='Times',size=20)
    self.MONOLabelInfo3["font"] = ft
    self.MONOLabelInfo3["fg"] = "#000000"
    self.MONOLabelInfo3["justify"] = "center"
    self.MONOLabelInfo3["text"] = ""
    self.MONOLabelInfo3.place(x=470,y=470,width=80,height=30)
    self.items+=[self.MONOLabelInfo3]

    self.MONOLabelInfo4=tk.Label(root)
    ft = tkFont.Font(family='Times',size=12)
    self.MONOLabelInfo4["font"] = ft
    self.MONOLabelInfo4["fg"] = "#000000"
    self.MONOLabelInfo4["anchor"] = "w"
    self.MONOLabelInfo4["text"] = "(optional) RGB values (seperated by spaces):"
    self.MONOLabelInfo4.place(x=110,y=180,width=300,height=25)
    self.items+=[self.MONOLabelInfo4]

def setupWebm(self):
    self.WebmEntryTop=tk.Entry(root)
    self.WebmEntryTop["borderwidth"] = "2px"
    ft = tkFont.Font(family='Times',size=10)
    self.WebmEntryTop["font"] = ft
    self.WebmEntryTop["fg"] = "#000000"
    self.WebmEntryTop["justify"] = "left"
    self.WebmEntryTop["text"] = "WebmEntryTop"
    self.WebmEntryTop.place(x=110,y=180,width=300,height=30)
    self.items+=[self.WebmEntryTop]

    self.WebmEntryBottom=tk.Entry(root)
    self.WebmEntryBottom["borderwidth"] = "2px"
    ft = tkFont.Font(family='Times',size=10)
    self.WebmEntryBottom["font"] = ft
    self.WebmEntryBottom["fg"] = "#000000"
    self.WebmEntryBottom["justify"] = "left"
    self.WebmEntryBottom["text"] = "WebmEntryBottom"
    self.WebmEntryBottom["state"]='disabled'
    self.WebmEntryBottom.place(x=110,y=260,width=300,height=30)
    self.items+=[self.WebmEntryBottom]

    self.WebmButtonTop=tk.Button(root)
    self.WebmButtonTop["bg"] = "#181a1b"
    ft = tkFont.Font(family='Times',size=18)
    self.WebmButtonTop["font"] = ft
    self.WebmButtonTop["fg"] = "#e8e6e3"
    self.WebmButtonTop["justify"] = "center"
    self.WebmButtonTop["text"] = "open"
    self.WebmButtonTop.place(x=430,y=180,width=70,height=30)
    self.WebmButtonTop["command"] = self.WebmButtonTop_command
    self.items+=[self.WebmButtonTop]

    self.infoLabel2=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    self.infoLabel2["font"] = ft
    self.infoLabel2["fg"] = "#000000"
    self.infoLabel2["anchor"] = "w"
    self.infoLabel2["text"] = "Choose webm:"
    self.infoLabel2.place(x=110,y=140,width=200,height=25)
    self.items+=[self.infoLabel2]

    self.infoLabel3=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    self.infoLabel3["font"] = ft
    self.infoLabel3["fg"] = "#000000"
    self.infoLabel3["anchor"] = "w"
    self.infoLabel3["text"] = "Choose new metadata:"
    self.infoLabel3.place(x=110,y=220,width=300,height=30)
    self.items+=[self.infoLabel3]

    self.WebmButtonConfirmation=tk.Button(root)
    self.WebmButtonConfirmation["bg"] = "#181a1b"
    ft = tkFont.Font(family='Times',size=20)
    self.WebmButtonConfirmation["font"] = ft
    self.WebmButtonConfirmation["fg"] = "#e8e6e3"
    self.WebmButtonConfirmation["justify"] = "center"
    self.WebmButtonConfirmation["text"] = "Change metadata"
    self.WebmButtonConfirmation.place(x=110,y=360,width=300,height=30)
    self.WebmButtonConfirmation["command"] = self.WebmButtonConfirmation_command
    self.items+=[self.WebmButtonConfirmation]

    self.WebmLabelOutput=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    self.WebmLabelOutput["font"] = ft
    self.WebmLabelOutput["fg"] = "#c8c3bc"
    self.WebmLabelOutput["justify"] = "center"
    self.WebmLabelOutput["text"] = "."
    self.WebmLabelOutput.place(x=110,y=320,width=300,height=25)
    self.items+=[self.WebmLabelOutput]

    self.WebmLabelInfo4=tk.Label(root)
    ft = tkFont.Font(family='Times',size=20)
    self.WebmLabelInfo4["font"] = ft
    self.WebmLabelInfo4["fg"] = "#000000"
    self.WebmLabelInfo4["justify"] = "center"
    self.WebmLabelInfo4["text"] = ""
    self.WebmLabelInfo4.place(x=450,y=360,width=80,height=30)
    self.items+=[self.WebmLabelInfo4]

def setupCURSE(self):
    self.CURSELabelInfo1=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    self.CURSELabelInfo1["font"] = ft
    self.CURSELabelInfo1["fg"] = "#000000"
    self.CURSELabelInfo1["anchor"] = "w"
    self.CURSELabelInfo1["text"] = "Choose video file:"
    self.CURSELabelInfo1.place(x=110,y=215,width=300,height=25)
    self.items+=[self.CURSELabelInfo1]

    self.CURSELabelInfo2=tk.Label(root)
    ft = tkFont.Font(family='Times',size=12)
    self.CURSELabelInfo2["font"] = ft
    self.CURSELabelInfo2["fg"] = "#000000"
    self.CURSELabelInfo2["anchor"] = "w"
    self.CURSELabelInfo2["text"] = "(optional) HEX data to insert"
    self.CURSELabelInfo2.place(x=110,y=285,width=300,height=25)
    self.items+=[self.CURSELabelInfo2]

    self.CURSEEntryMain=tk.Entry(root)
    self.CURSEEntryMain["borderwidth"] = "2px"
    ft = tkFont.Font(family='Times',size=10)
    self.CURSEEntryMain["font"] = ft
    self.CURSEEntryMain["fg"] = "#000000"
    self.CURSEEntryMain["justify"] = "left"
    self.CURSEEntryMain["text"] = "CURSEEntryMain"
    self.CURSEEntryMain.place(x=110,y=250,width=300,height=30)
    self.items+=[self.CURSEEntryMain]

    self.CURSEEntrySec=tk.Entry(root)
    self.CURSEEntrySec["borderwidth"] = "2px"
    ft = tkFont.Font(family='Times',size=10)
    self.CURSEEntrySec["font"] = ft
    self.CURSEEntrySec["fg"] = "#000000"
    self.CURSEEntrySec["justify"] = "left"
    self.CURSEEntrySec["text"] = "CURSEEntrySec"
    self.CURSEEntrySec.place(x=110,y=310,width=300,height=30)
    self.items+=[self.CURSEEntrySec]

    self.CURSEButtonFile=tk.Button(root)
    self.CURSEButtonFile["bg"] = "#181a1b"
    ft = tkFont.Font(family='Times',size=18)
    self.CURSEButtonFile["font"] = ft
    self.CURSEButtonFile["fg"] = "#e8e6e3"
    self.CURSEButtonFile["justify"] = "center"
    self.CURSEButtonFile["text"] = "open"
    self.CURSEButtonFile.place(x=420,y=250,width=70,height=30)
    self.CURSEButtonFile["command"] = self.CURSEButtonFile_command
    self.items+=[self.CURSEButtonFile]

    self.CURSEButtonConfirm=tk.Button(root)
    self.CURSEButtonConfirm["bg"] = "#181a1b"
    ft = tkFont.Font(family='Times',size=20)
    self.CURSEButtonConfirm["font"] = ft
    self.CURSEButtonConfirm["fg"] = "#e8e6e3"
    self.CURSEButtonConfirm["justify"] = "center"
    self.CURSEButtonConfirm["text"] = "Create cursed video"
    self.CURSEButtonConfirm.place(x=110,y=430,width=300,height=30)
    self.CURSEButtonConfirm["command"] = self.CURSEButtonConfirm_command
    self.items+=[self.CURSEButtonConfirm]

    self.CURSELabelInfo2=tk.Label(root)
    ft = tkFont.Font(family='Times',size=20)
    self.CURSELabelInfo2["font"] = ft
    self.CURSELabelInfo2["fg"] = "#000000"
    self.CURSELabelInfo2["justify"] = "center"
    self.CURSELabelInfo2["text"] = ""
    self.CURSELabelInfo2.place(x=470,y=430,width=80,height=30)
    self.items+=[self.CURSELabelInfo2]

def setupDISTORT(self):
    self.DISTORTLabelInfo1=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    self.DISTORTLabelInfo1["font"] = ft
    self.DISTORTLabelInfo1["fg"] = "#000000"
    self.DISTORTLabelInfo1["anchor"] = "w"
    self.DISTORTLabelInfo1["text"] = "Choose video file:"
    self.DISTORTLabelInfo1.place(x=110,y=155,width=300,height=25)
    self.items+=[self.DISTORTLabelInfo1]

    self.DISTORTLabelInfo3=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    self.DISTORTLabelInfo3["font"] = ft
    self.DISTORTLabelInfo3["fg"] = "#000000"
    self.DISTORTLabelInfo3["anchor"] = "w"
    self.DISTORTLabelInfo3["text"] = "Choose distortions/second:"
    self.DISTORTLabelInfo3.place(x=110,y=220,width=300,height=25)
    self.items+=[self.DISTORTLabelInfo3]

    self.DISTORTLabelInfo4=tk.Label(root)
    ft = tkFont.Font(family='Times',size=10)
    self.DISTORTLabelInfo4["font"] = ft
    self.DISTORTLabelInfo4["fg"] = "#000000"
    self.DISTORTLabelInfo4["anchor"] = "w"
    self.DISTORTLabelInfo4["text"] = "(Must be int, best if it's a divisor of the framerate)"
    self.DISTORTLabelInfo4.place(x=110,y=240,width=300,height=25)
    self.items+=[self.DISTORTLabelInfo4]

    self.DISTORTLabelInfo5=tk.Label(root)
    ft = tkFont.Font(family='Times',size=15)
    self.DISTORTLabelInfo5["font"] = ft
    self.DISTORTLabelInfo5["fg"] = "#000000"
    self.DISTORTLabelInfo5["anchor"] = "w"
    self.DISTORTLabelInfo5["text"] = "(optional) Outputfile path/name:"
    self.DISTORTLabelInfo5.place(x=110,y=300,width=300,height=25)
    self.items+=[self.DISTORTLabelInfo5]

    self.DISTORTEntryMain=tk.Entry(root)
    self.DISTORTEntryMain["borderwidth"] = "2px"
    ft = tkFont.Font(family='Times',size=10)
    self.DISTORTEntryMain["font"] = ft
    self.DISTORTEntryMain["fg"] = "#000000"
    self.DISTORTEntryMain["justify"] = "left"
    self.DISTORTEntryMain["text"] = "DISTORTEntryMain"
    self.DISTORTEntryMain.place(x=110,y=190,width=300,height=30)
    self.items+=[self.DISTORTEntryMain]

    self.DISTORTEntrySec=tk.Entry(root)
    self.DISTORTEntrySec["borderwidth"] = "2px"
    ft = tkFont.Font(family='Times',size=10)
    self.DISTORTEntrySec["font"] = ft
    self.DISTORTEntrySec["fg"] = "#000000"
    self.DISTORTEntrySec["justify"] = "left"
    self.DISTORTEntrySec["text"] = "DISTORTEntrySec"
    self.DISTORTEntrySec.place(x=110,y=270,width=300,height=30)
    self.items+=[self.DISTORTEntrySec]

    self.DISTORTEntryTert=tk.Entry(root)
    self.DISTORTEntryTert["borderwidth"] = "2px"
    ft = tkFont.Font(family='Times',size=10)
    self.DISTORTEntryTert["font"] = ft
    self.DISTORTEntryTert["fg"] = "#000000"
    self.DISTORTEntryTert["justify"] = "left"
    self.DISTORTEntryTert["text"] = "DISTORTEntryTert"
    self.DISTORTEntryTert.place(x=110,y=330,width=300,height=30)
    self.items+=[self.DISTORTEntryTert]

    self.DISTORTButtonFile=tk.Button(root)
    self.DISTORTButtonFile["bg"] = "#181a1b"
    ft = tkFont.Font(family='Times',size=18)
    self.DISTORTButtonFile["font"] = ft
    self.DISTORTButtonFile["fg"] = "#e8e6e3"
    self.DISTORTButtonFile["justify"] = "center"
    self.DISTORTButtonFile["text"] = "open"
    self.DISTORTButtonFile.place(x=420,y=190,width=70,height=30)
    self.DISTORTButtonFile["command"] = self.DISTORTButtonFile_command
    self.items+=[self.DISTORTButtonFile]

    self.DISTORTButtonConfirm=tk.Button(root)
    self.DISTORTButtonConfirm["bg"] = "#181a1b"
    ft = tkFont.Font(family='Times',size=20)
    self.DISTORTButtonConfirm["font"] = ft
    self.DISTORTButtonConfirm["fg"] = "#e8e6e3"
    self.DISTORTButtonConfirm["justify"] = "center"
    self.DISTORTButtonConfirm["text"] = "Create distorted video"
    self.DISTORTButtonConfirm.place(x=110,y=430,width=300,height=30)
    self.DISTORTButtonConfirm["command"] = self.DISTORTButtonConfirm_command
    self.items+=[self.DISTORTButtonConfirm]

    self.DISTORTLabelInfo2=tk.Label(root)
    ft = tkFont.Font(family='Times',size=20)
    self.DISTORTLabelInfo2["font"] = ft
    self.DISTORTLabelInfo2["fg"] = "#000000"
    self.DISTORTLabelInfo2["justify"] = "center"
    self.DISTORTLabelInfo2["text"] = ""
    self.DISTORTLabelInfo2.place(x=470,y=430,width=80,height=30)
    self.items+=[self.DISTORTLabelInfo2]

def setupMd5(self):
    self.md5FileEntryTop=tk.Entry(root)
    self.md5FileEntryTop["borderwidth"] = "2px"
    ft = tkFont.Font(family='Times',size=10)
    self.md5FileEntryTop["font"] = ft
    self.md5FileEntryTop["fg"] = "#000000"
    self.md5FileEntryTop["justify"] = "left"
    self.md5FileEntryTop["text"] = "md5FileEntryTop"
    self.md5FileEntryTop.place(x=110,y=180,width=300,height=30)
    self.items+=[self.md5FileEntryTop]

    self.md5FileButtonTop=tk.Button(root)
    self.md5FileButtonTop["bg"] = "#181a1b"
    ft = tkFont.Font(family='Times',size=18)
    self.md5FileButtonTop["font"] = ft
    self.md5FileButtonTop["fg"] = "#e8e6e3"
    self.md5FileButtonTop["justify"] = "center"
    self.md5FileButtonTop["text"] = "open"
    self.md5FileButtonTop.place(x=430,y=180,width=70,height=30)
    self.md5FileButtonTop["command"] = self.md5FileButtonTop_command
    self.items+=[self.md5FileButtonTop]

    self.infoLabel1=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    self.infoLabel1["font"] = ft
    self.infoLabel1["fg"] = "#000000"
    self.infoLabel1["anchor"] = "w"
    self.infoLabel1["text"] = "Choose file:"
    self.infoLabel1.place(x=110,y=140,width=200,height=25)
    self.items+=[self.infoLabel1]

    self.Md5ButtonConfirmation=tk.Button(root)
    self.Md5ButtonConfirmation["bg"] = "#181a1b"
    ft = tkFont.Font(family='Times',size=20)
    self.Md5ButtonConfirmation["font"] = ft
    self.Md5ButtonConfirmation["fg"] = "#e8e6e3"
    self.Md5ButtonConfirmation["justify"] = "center"
    self.Md5ButtonConfirmation["text"] = "Generate Md5"
    self.Md5ButtonConfirmation.place(x=110,y=230,width=300,height=30)
    self.Md5ButtonConfirmation["command"] = self.Md5ButtonConfirmation_command
    self.items+=[self.Md5ButtonConfirmation]

    self.md5LabelOutput=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    self.md5LabelOutput["font"] = ft
    self.md5LabelOutput["fg"] = "#000000"
    self.md5LabelOutput["anchor"] ="w"
    self.md5LabelOutput["text"] = "MD5 (Hex format): "
    self.md5LabelOutput.place(x=110,y=300,width=300,height=20)
    self.items+=[self.md5LabelOutput]

    self.md5HexOut=tk.Entry(root)
    ft = tkFont.Font(family='Times',size=18)
    self.md5HexOut["font"] = ft
    self.md5HexOut["fg"] = "#000000"
    self.md5HexOut["text"] = ""
    self.md5HexOut.place(x=110,y=330,width=400,height=25)
    self.items+=[self.md5HexOut]

    self.md5Label2=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    self.md5Label2["font"] = ft
    self.md5Label2["fg"] = "#000000"
    self.md5Label2["anchor"] ="w"
    self.md5Label2["text"] = "Base 64 encoded MD5 hash:"
    self.md5Label2.place(x=110,y=370,width=300,height=20)
    self.items+=[self.md5Label2]

    self.md5HexOut2=tk.Entry(root)
    ft = tkFont.Font(family='Times',size=18)
    self.md5HexOut2["font"] = ft
    self.md5HexOut2["fg"] = "#000000"
    self.md5HexOut2["text"] = ""
    self.md5HexOut2.place(x=110,y=400,width=400,height=25)
    self.items+=[self.md5HexOut2]  


def cleanup(items):
    for i in items:
        i.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
