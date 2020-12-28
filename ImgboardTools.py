from PIL import Image,ImageChops
import subprocess
import os
import argparse

"""
'''
# save locations - These aren't being used at the moment.
If you don't have the executables used (ffmpeg&pngcrush) in your PATH variable on windows you need to specify the path here.
Note that the variables aren't being used at the moment, but could be added by replacing the calls.
'''
ffmpeg_saveloc_win=r"C:\Program Files (x86)\execs\ffmpeg-4.3.1-2020-11-19-essentials_build\bin\ffmpeg.exe"
ffmpeg_saveloc_lin=""
pngcrush_saveloc_win=r"C:\Program Files\execs\pngcrush.exe"
pngcrush_saveloc_lin=r""

#making sure software works on windows and linux
if os.name=="posix":
    ffmpeg_saveloc=ffmpeg_saveloc_lin
    pngcrush_saveloc=pngcrush_saveloc_lin
elif os.name=="nt":
    ffmpeg_saveloc=ffmpeg_saveloc_win
    pngcrush_saveloc=pngcrush_saveloc_win
"""

def deleteExif(imagename):
    image = Image.open(imagename)
    image.save(imagename)
    print("EXIF data deleted")

def changeWebmTitle(title,inputfile="vid.webm",outputfile=""):
    if len(inputfile)>=6 and inputfile[-5:]!=".webm":
        inputfile+=".webm"
    if outputfile=="":
        outputfile=inputfile
    elif len(outputfile)>=6 and outputfile[-5:]!=".webm":
        outputfile+=".webm"
    os.rename((inputfile),("I_"+inputfile))
    subprocess.check_call(["ffmpeg","-i","I_"+inputfile,"-metadata","title="+title,"-codec","copy",outputfile])
    os.remove("I_"+inputfile)
    print("Webm metadata edited.")

def hideIMG(thumbnail_img,hidden_img,mode=""):
    image_2=Image.open(thumbnail_img).convert("RGBA")
    image_1=Image.open(hidden_img).convert("RGBA").resize(image_2.size) #hidden image
    im1=image_1.load()
    im2=image_2.load()
    maxlower=210
    maxupper=214
    for x in range(image_2.size[0]):
        for y in range(image_2.size[1]):
            if x%2==1 and y%2==1:
                temp=list(im1[x,y])
                for i in range(len(im1[x,y])-1):
                    temp[i]=int(maxupper+(im1[x,y][i]/255)*(255-maxupper))
                im2[x,y]=tuple(temp)
            else:
                temp=list(im2[x,y])
                for i in range(len(im2[x,y])-1):
                    temp[i]=int(temp[i]/255*maxlower)
                im2[x,y]=tuple(temp)
    if mode!="":
        image_2=image_2.convert(mode)
    image_2.save("need_gAMA.png")
    subprocess.check_call(["pngcrush -replace_gamma","0.023","need_gAMA.png","output.png"])
    os.remove("need_gAMA.png")
    print("Done. Your new file is 'output.png'.")

def greyifyImg(imagepath):
    #load image
    image=Image.open(imagepath)
    #remove transparency
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            alpha = image.convert('RGBA').split()[-1]
            bg = Image.new("RGBA", image.size, (255,255,255) + (255,))
            bg.paste(image, mask=alpha)
            image=bg
    #Invert image
    image=ImageChops.invert(image).convert("1")
    image=image.convert("RGB")
    #Change colors
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            px=image.getpixel((x,y))
            if px==(0,0,0):
                image.putpixel((x,y),(127, 127, 126))
            elif px==(255,255,255):
                image.putpixel((x,y),(127, 127, 127))
    image.save("hidden_need_trns.png")
    subprocess.check_call("pngcrush -trns 0 127 127 126 0 hidden_need_trns.png hidden.png".split())
    os.remove("hidden_need_trns.png")
    print("Done. Your new file is 'hidden.png'.")


"""
Parser info
"""
def main():
    parser = argparse.ArgumentParser(description="Features for imageboard content.")
    parser.add_argument("-a",nargs=1,help="Delete identifying EXIF data on a jpg. [filename]",dest='anonymize')
    parser.add_argument("-w",nargs="+",help="Change \"title\" metadata of a webm. [title,(inputfilename=vid.webm),(outputfilename=inputfilename)]",dest="webm")
    parser.add_argument("-m",nargs="+",help="Hide image in another image. [thumbnail_img, hidden_img,(mode{L,RGB,RGBA,CMYK})]",dest="mix")
    parser.add_argument("-g",nargs=1,help="Hide image on grey background. [imagepath]",dest="greyify")
    args=parser.parse_args()

    if args.anonymize:
        deleteExif(*args.anonymize)
    if args.webm:
        changeWebmTitle(*args.webm)
    if args.mix:
        hideIMG(*args.mix)
    if args.greyify:
        greyifyImg(*args.greyify)

if __name__ == '__main__':
    main()
