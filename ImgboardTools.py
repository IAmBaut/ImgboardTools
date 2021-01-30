try:
    from PIL import Image,ImageChops
except ImportError:
    sys.exit("Module PIL missing.\nAborting.")
from random import randint
import subprocess
import os
import argparse
import shutil

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
    position=inputfile.rfind("/")
    if position!=-1:
        tempfile=inputfile[:position+1]+"I_"+inputfile[position+1:]
    position=inputfile.rfind("\\")
    if position!=-1:
        tempfile=inputfile[:position+1]+"I_"+inputfile[position+1:]
    os.rename(inputfile,tempfile)
    #Calling the ffmpeg command to change metadata.
    subprocess.check_call(["ffmpeg","-i",tempfile,"-metadata","title="+title,"-codec","copy",outputfile])
    os.remove(tempfile)
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

def curseVid(inputfile,secarg="",hexdata=""):#secarg="cursed"
    """
    Creates "cursed" videofiles where the duration seems bugged by messing with header data:
    For mp4 files the duration is set as very very long
    For webm files the furation is buged in such a way that some players will show it as constantly growing.
    Note that this function does not chunk the inputfiles, so too big files (or too little RAM) might result in crashes.
    """
    isHexDef=False
    #Argparse passes arguments as positional arguments, without identifiers. This is to find out what kind of argument was given.
    if (len(secarg)>=5 and secarg[-4:]==".mp4") or (len(secarg)>=6 and secarg[-5:]==".webm"):
        outputname=secarg
        if hexdata:
            hexstring=hexdata
            isHexDef=True
    else:
        if len(secarg)==16:
            hexstring=secarg
            isHexDef=True
        if (len(inputfile)>=5 and inputfile[-4:]==".mp4"):
            outputname="cursed.mp4"
        elif (len(inputfile)>=6 and inputfile[-5:]==".webm"):
            outputname="cursed.webm"
        if hexdata:
            print("Error, either the second argument is not a valid video file, or you gave multiple hexdata strings as arguments")
    if len(inputfile)>=5 and inputfile[-4:]==".mp4":
        if not hexdata and not isHexDef:
            hexstring="000000017FFFFFFF"    #The first 4 bytes are the units per second, the second are the total units.
        else:
            if len(hexdata)==16:
                hexstring=hexdata
            else:
                print("Error. Please specify 8 bytes of data (=string of length 16)")
        with open(inputfile,"rb") as f:
            content=f.read().hex() #Turn file into a string of hex values
            #The header info we are looking for in a mp4 file starts with "mvhd" which is "6d 76 68 64"
            #Every 2 indexes of our string = 1 Hex value.
            startindex=content.find("6d766864")+8 #We jump 4 hex values to skip our mvhd string.
            workingindex=startindex+24 #12 bytes after that is the relevant data
            content=content[:workingindex]+hexstring+content[workingindex+16:] #Adding fake header data
            with open(outputname,"wb") as file: #Saving file
                file.write(bytes.fromhex(content))
                return True
    elif len(inputfile)>=6 and inputfile[-5:]==".webm":
        if not hexdata and not isHexDef:
            hexstring="4ff0000000000000"
        else:
            if len(hexstring)!=16:
                print("Error. Please specify 8 bytes of data (=string of length 16)")
        with open(inputfile,"rb") as f:
            content=f.read().hex()
            startindex=content.find("2ad7b1")+6 #First we find 2A D7 B1
            index=content.find("4489",startindex)+4 #Then from there the first occurance of 44 89 is our relevant index
            if content[index:index+2]=="84": #This Hex byte contains the length of the duration header. If it is 84 we change it to 88 and have to add empty bytes to the file.
                content=content[:index]+"88"+"00000000"+content[index+2:]
            content=content[:index+2]+hexstring+content[index+2+len(hexstring):] #Insert the new bugged headerchunk
            with open(outputname,"wb") as output: #Saving file
                output.write(bytes.fromhex(content))
                return True

def aspectMagic(inputfile,changesPerSec,outputfile="aspectMagic.webm"):
    """
    Expects a .webm and "animates" the aspect ratio, by assigning parts of it random height and width values in intervals
    and then stitching these video files together again.
    Works best when changesPerSec is a divisor of the framerate. If not things might desync.
    Also the resulting file will be larger in filesize than the original.
    """
    #Function to get desired data from ffprobe return string.
    def getdata(identifier,searchstr,inFormat=False):
        key=identifier+"="
        if not inFormat:
            start=0
        else:
            start=info.find("[FORMAT]")
        pos=searchstr.find(key,start)
        end=searchstr.find("\n",pos+len(identifier))
        return searchstr[pos+len(key):end][:-1]
    changesPerSec=int(changesPerSec)   #Defines how many "transformations" we want every second. Making sure it's an int.
    command='ffprobe -v quiet -show_format -show_streams'.split()+[inputfile]
    info=subprocess.check_output(command).decode("utf-8")
    #Getting the height, width, duration and bitrate of the webm.
    #This bitrate value might not always be 100% correct, so if there are ever issues, it migh be worth investigating here.
    duration=float(getdata("duration",info,True))#This is in seconds
    width=int(getdata("width",info))
    height=int(getdata("height",info))
    bitrate=float(getdata("bit_rate",info,True))
    #Create a folder to put temporary files into. First remove old folder in case it still exists.
    if os.path.isdir("ImgboardTools_cache"):
        shutil.rmtree("ImgboardTools_cache")
    os.mkdir("ImgboardTools_cache")
    #String to contain data that ffmpeg expects for concatenating files.
    filestring=""
    numberOfSegs=int((duration*changesPerSec)+1)
    segmentLength=round(1/changesPerSec,4)
    print("Starting to generate the temporary files needed...")
    for i in range(numberOfSegs):
        if i==0:
            scale_w=1
            scale_h=1
        else:
            #Generating random values for scaling between 0.01 and 0.99.
            scale_w=round(randint(1,99)/100,2)
            scale_h=round(randint(1,99)/100,2)
        startpoint=round(i*segmentLength,4)
        print("Generating temporary segment {:4d}/{:4d} with aspect ratio {:3.2f}:{:3.2f} at {:5.2f} seconds".format((i+1),numberOfSegs,scale_w,scale_h,startpoint))
        outfile="tempfile_"+str(i)+".webm"
        filestring+="file '"+outfile+"'\n"
        #Calling ffmpeg to create the temporary files with different aspect ratios.
        command=['ffmpeg','-hide_banner','-loglevel','quiet','-i',inputfile,"-ss",str(startpoint),"-t",str(segmentLength),"-vf",("scale=w=iw*"+str(scale_w)+":h=ih*"+str(scale_h)),"-an","-c:v","libvpx","-b:v",str(bitrate)+"k","ImgboardTools_cache/"+outfile]
        subprocess.check_call(command)
    #Writing the filestring to a .txt file because that's what ffmpeg needs.
    with open("ImgboardTools_cache/data.txt",mode="w") as file:
        file.write(filestring[:-1]) #Cutting off unneeded newline at end here.
    #Deleting temporary_needAudio.webm if needed (because the program was interrupted in an earlier run)
    try:
        os.remove("temporary_needAudio.webm")
    except Exception:
        pass
    #Concatenating videos.
    command=['ffmpeg',  '-hide_banner', '-loglevel', 'quiet','-f', 'concat', '-safe', '0', '-i', 'ImgboardTools_cache/data.txt', '-an', '-c:v', 'copy', 'temporary_needAudio.webm']
    subprocess.check_call(command)
    #Removing temporary files we created earlier.
    shutil.rmtree("ImgboardTools_cache")
    #Delete file with same name as outputfile if necessary.
    try:
        os.remove(outputfile)
    except Exception:
        pass
    #Copy the audio of the inputfile to the newly created concatenated video.
    command="ffmpeg -hide_banner -loglevel quiet -i".split()+["temporary_needAudio.webm","-i",inputfile]+"-map 0:v -map 1:a? -c copy ".split()+[str(outputfile)]
    subprocess.check_call(command)
    #Removing last bit of temporary data.
    os.remove("temporary_needAudio.webm")
    print("Done. The webm",outputfile,"now changes its aspect ratio",changesPerSec,"times per second.")
    return True

"""
Parser info
"""
def main():
    parser = argparse.ArgumentParser(description="Features for imageboard content.")
    parser.add_argument("-a",nargs=1,help="Delete identifying EXIF data on a jpg. [filename]",dest='anonymize')
    parser.add_argument("-w",nargs="+",help="Change \"title\" metadata of a webm. [title,(inputfilename=vid.webm),(outputfilename=inputfilename)]",dest="webm")
    parser.add_argument("-m",nargs="+",help="Hide image in another image. [thumbnail_img, hidden_img,(mode{L,RGB,RGBA,CMYK})]",dest="mix")
    parser.add_argument("-g",nargs="+",help="Hide image on grey background. [imagepath,(R),(G),(B))]",dest="greyify")
    parser.add_argument("-c",nargs="+",help="Curse a webm or mp4 video file length [inputfile,(outputfile),(hexdata)]",dest="curse")
    parser.add_argument("-d",nargs="+",help="Randomly change webm height and width. Works best if changesPerSec is divisor of framerate. [inputfile,changesPerSec,(outputfile)]",dest="distort")
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
    if args.distort:
        aspectMagic(*args.distort)

if __name__ == '__main__':
    main()
