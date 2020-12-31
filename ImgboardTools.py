try:
    from PIL import Image,ImageChops
except ImportError:
    sys.exit("Module PIL missing.\nAborting.")
import subprocess
import os
import argparse

def deleteExif(imagename):
    #Deletes Exif data from files by copying and saving the image.
    image = Image.open(imagename)
    image.save(imagename)
    print("EXIF data deleted")
    return True

def changeWebmTitle(title,inputfile="vid.webm",outputfile=""):
    #changes the title attribute of the webm metadata
    #Adding .webm to the end if the user forgot it.
    if len(inputfile)>=6 and inputfile[-5:]!=".webm":
        inputfile+=".webm"
    if outputfile=="":
        outputfile=inputfile
    elif len(outputfile)>=6 and outputfile[-5:]!=".webm":
        outputfile+=".webm"
    os.rename((inputfile),("I_"+inputfile))
    #Calling the ffmpeg command to change metadata.
    subprocess.check_call(["ffmpeg","-i","I_"+inputfile,"-metadata","title="+title,"-codec","copy",outputfile])
    os.remove("I_"+inputfile)
    print("Webm metadata edited.")
    return True

def hideIMG(thumbnail_img,hidden_img,mode=""):
    """
    Hides image in another by overlaying them over each other and mapping them to different brightness values.
    Then adds a gAMA .png file chunk with a very low value which makes the bright parts visible and the dark parts invisible.
    Further reading: https://hsivonen.fi/png-gamma/ Relevant part for the trick is under the "Correction" heading.
    """
    #Open images and change their color info to RGBA
    image_2=Image.open(thumbnail_img).convert("RGBA")
    image_1=Image.open(hidden_img).convert("RGBA").resize(image_2.size) #resize to fit thumbnail_img
    im1=image_1.load()
    im2=image_2.load()
    """
    Defining the values the brightness will be mapped to:
    thumbnail_img will be mapped to a brightness of 0-maxlower
    hidden_img will be mapped to a brightness of maxupper-255
    """
    maxlower=210
    maxupper=214
    #Looping over the pixels in the images and replacing every pixel in uneven rows with uneven index with the hidden image
    for x in range(image_2.size[0]):
        for y in range(image_2.size[1]):
            if x%2==1 and y%2==1:
                temp=list(im1[x,y])
                for i in range(len(im1[x,y])-1):
                    temp[i]=int(maxupper+(im1[x,y][i]/255)*(255-maxupper)) #Mapping the pixels in the hidden image to the higher brightness range.
                im2[x,y]=tuple(temp)
            else:
                temp=list(im2[x,y])
                for i in range(len(im2[x,y])-1):
                    temp[i]=int(temp[i]/255*maxlower) #Mapping the pixels in the thumbnail image to the lower brightness range.
                im2[x,y]=tuple(temp)
    if mode!="":
        image_2=image_2.convert(mode)
    image_2.info = {} #Removing anxiliary png file chunks. Without this certain chunks could make pngcrush choke.
    image_2.save("need_gAMA.png")
    #Calling pngcrush to add gAMA chunk with value 0.023
    subprocess.check_call(["pngcrush","-replace_gamma","0.023","need_gAMA.png","output.png"])
    os.remove("need_gAMA.png") #Removing temporary file.
    print("Done. Your new file is 'output.png'.")
    return True

def greyifyImg(imagepath,R=127,G=127,B=127):
    """
    Turns image into monochrome image, then adds it in background with almost the same color.
    By adding a tRNS chunk we can make it so the barely different background becomes transparent upon opening the file.
    Works best with images with transparent background.
    """
    color=[int(R),int(G),int(B)]
    bgc=color[:] #Otherwise this just copies the pointer
    #Shifting color of background by value of 1
    if bgc[2]>0:
        bgc[2]=bgc[2]-1
    else:
        bgc[2]=bgc[2]+1
    bgc=tuple(bgc)
    color=tuple(color)
    #Load image
    image=Image.open(imagepath)
    #Remove transparency
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            alpha = image.convert('RGBA').split()[-1]
            bg = Image.new("RGBA", image.size, (255,255,255) + (255,))
            bg.paste(image, mask=alpha)
            image=bg
    #Invert image
    image=ImageChops.invert(image).convert("1")
    image=image.convert("RGB")
    #Give foreground and background almost the same colors
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            px=image.getpixel((x,y))
            if px==(0,0,0):
                image.putpixel((x,y),bgc)
            elif px==(255,255,255):
                image.putpixel((x,y),color)
    image.save("hidden_need_trns.png")
    #Add tRNS chunk with pngcrush
    subprocess.check_call(("pngcrush -trns 0 "+str(bgc[0])+" "+str(bgc[1])+" "+str(bgc[2])+" 0 hidden_need_trns.png hidden.png").split())
    os.remove("hidden_need_trns.png")
    print("Done. Your new file is 'hidden.png'.")
    return True

def curseVid(inputfile,outputfile="cursed"):
    """
    Creates "cursed" videofiles where the duration seems bugged by messing with header data:
    For mp4 files the duration is set as very very long
    For webm files the furation is buged in such a way that some players will show it as constantly growing.
    Note that this function does not chunk the inputfiles, so too big files (or too little RAM) might result in crashes.
    """
    #Checking filetype
    if len(inputfile)>=5 and inputfile[-4:]==".mp4":
        if len(outputfile)<5 or outputfile[-4:]!=".mp4":
            outputname=outputfile+".mp4"
        else:
            outputname=outputfile
        with open(inputfile,"rb") as f:
            content=f.read().hex() #Turn file into a string of hex values
            #The header info we are looking for in a mp4 file starts with "mvhd" which is "6d 76 68 64"
            #Every 2 indexes of our string = 1 Hex value.
            startindex=content.find("6d766864")+8 #We jump 4 hex values to skip our mvhd string.
            workingindex=startindex+24 #12 bytes after that is the relevant data
            unitspersec="00000001"
            totalunits="7FFFFFFF" #max value, can also be negative
            content=content[:workingindex]+unitspersec+totalunits+content[workingindex+16:] #Adding fake header data
            with open(outputname,"wb") as file: #Saving file
                file.write(bytes.fromhex(content))
                print("Done. Your mp4 file "+outputname+" now has a very long corrupted length header.")
    elif len(inputfile)>=6 and inputfile[-5:]==".webm":
        if len(outputfile)<6 or outputfile[-5:]!=".webm":
            outputname=outputfile+".webm"
        else:
            outputname=outputfile
        with open(inputfile,"rb") as f:
            content=f.read().hex()
            startindex=content.find("2ad7b1")+6 #First we find 2A D7 B1
            index=content.find("4489",startindex)+4 #Then from there the first occurance of 44 89 is our relevant index
            if content[index:index+2]=="84": #This Hex byte contains the length of the duration header. If it is 84 we change it to 88 and have to add empty bytes to the file.
                content=content[:index]+"88"+"00000000"+content[index+2:]
            lengthchunk="3ff0000000000000"
            content=content[:index+2]+lengthchunk+content[index+2+len(lengthchunk):] #Insert the new bugged headerchunk
            with open(outputname,"wb") as output: #Saving file
                output.write(bytes.fromhex(content))
                print("Done. The webm file "+outputname+" now has corrupted length.")
                return True

"""
Parser info
"""
def main():
    parser = argparse.ArgumentParser(description="Features for imageboard content.")
    parser.add_argument("-a",nargs=1,help="Delete identifying EXIF data on a jpg. [filename]",dest='anonymize')
    parser.add_argument("-w",nargs="+",help="Change \"title\" metadata of a webm. [title,(inputfilename=vid.webm),(outputfilename=inputfilename)]",dest="webm")
    parser.add_argument("-m",nargs="+",help="Hide image in another image. [thumbnail_img, hidden_img,(mode{L,RGB,RGBA,CMYK})]",dest="mix")
    parser.add_argument("-g",nargs="+",help="Hide image on grey background. [imagepath,(R,G,B)]",dest="greyify")
    parser.add_argument("-c",nargs="+",help="Curse a webm or mp4 video file length [inputfile,(outputfile)]",dest="curse")
    args=parser.parse_args()

    if args.anonymize:
        deleteExif(*args.anonymize)
    if args.webm:
        changeWebmTitle(*args.webm)
    if args.mix:
        hideIMG(*args.mix)
    if args.greyify:
        greyifyImg(*args.greyify)
    if args.curse:
        curseVid(*args.curse)

if __name__ == '__main__':
    main()
