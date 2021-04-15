# ImgboardTools

Python code with various features for file modifications, mostly for use on imageboards.

Has both a CLI and GUI.

## Disclaimer for everyone

Jump to the index to see an overview of the topics discussed in this readme.

Jump to the "example images" section if you want to see the GUI version in action and some images created with the program. 

## Disclaimer for non programmers

(You can skip this if you know how to use a command line and how to install dependencies)

*I have no idea what a CLI is, nor do I know how to install dependencies and half those words don't even look like english*

If you have no idea what this whole thing is and you just wanted to install a program and be done with it, I have good and bad news:

The bad news is that this was never intended as a consumer level program. In fact I originally wrote it for personal use and it just grew from there. As a result this code uses dependencies, third party programs and is overall not optimized for a good user experience. Some things are intentionally made so they were easier to debug as a programmer.

The good news is that you don't need to be a programmer to use it, nor do you need to understand most of the stuff written in this readme. If things break however (and they probably will at some point) you are on your own. You can jump to the section "Installation for non programmers" for a more in depth step by step guide on how to install this program on windows in a few minutes.

## Features so far (checked means implemented):

- [x] Anonymize images by deleting EXIF data out of them.
- [x] Change/Overwrite the metadata on a WEBM.
- [x] Combine/Hide two images within each other by messing with PNG gamma values and brightness.
- [x] Command line interface (CLI) to access features.
- [x] Hide images in colored background by messing with PNG "trns" chunks. (sometimes called "ninja pngs")
- [x] "Curse" .webm or .mp4 video file duration by messing with the file headers. <- note that these do not get buffered, so very large files will probably crash. The upload size limit on most imageboards probably makes this irrelevant though.
- [x] GUI application for the script. (Ugly, but functional.)
- [x] Generate .webms that constantly change their own aspect ratio / sizes while playing.

If you prefer images showing examples of some of these features, scroll down to the end of the readme.

## Requirements

You need Python and the Python library *Pillow*, get it with `pip install pillow`.

You also need the following software/executables:
* ffmpeg (including ffprobe)
* pngcrush

If you are on a Windows system these need to either be located in the same directory as ImgboardTools.py, or added to the Windows PATH system variable.

## Usage

Works like most CLI tools. To get started use

    python ImgboardTools.py -h

which will display the help window:

       -h, --help                 show this help message and exit
       -a ANONYMIZE               Delete identifying EXIF data on a jpg. [filename]
       -w WEBM [WEBM ...]         Change "title" metadata of a webm. [title,(inputfilename=vid.webm),(outputfilename=inputfilename)]
       -m MIX [MIX ...]           Hide image in another image. [thumbnail_img, hidden_img,(mode{L,RGB,RGBA,CMYK})]
       -g GREYIFY [GREYIFY ...]   Hide image on grey background. [imagepath,(R,G,B)]
       -c CURSE [CURSE ...]       Curse a webm or mp4 video file length [inputfile,(outputfile),(hexdata)]
       -d DISTORT [DISTORT ...]   Randomly change webm height and width. Works best if changesPerSec is divisor of framerate. [inputfile,changesPerSec,(outputfile)]

Note that the help messages of argparse have some custom syntax:

* Brackets [] contain the expected arguments.
* Arguments in parentheses () are optional.
* Arguments in braces {} are possible example values.

There is also a GUI application to allow for access to the features of the script. It should work cross platform.

The GUI is experimental and may not be as up to date as the CLI and troubleshooting will be less obvious on it. Use at your own risk.

If you are on Windows you can save the GUI script as `.pyw` instead of `.py` to prevent the console from opening. This also means less feedback in case of errors though.

## Examples

So for example to mix two images you would call:

    python ImgboardTools.py -m front.png back.png

or to generate a light blue ninja png:

    python ImgboardTools.py -g image.png 173 216 230

## Explanations

Some info on how / why some of these tricks work or why you may want to try some of the features.

### EXIF data

You can think of "Exchangeable Image File Format" (EXIF) data as metadata for images, containing information about the camera, location the image was taken etc. On the web you will most likely encounter it attached to .jpg files.
While it contains plenty of info that is of use for photographers, it can also contain data that can be used to identify the person who shot it. Deleting EXIF data from photos is therefore a step you can take to protect your privacy.

### Webm metadata

Webms always contain metadata which can be used to add information on the artist, album etc. of the media shared. Especially the "title" attribute is widely supported.
A lot of people on imageboards use .webm title attributes to add the source of their content to the file, so in the case that someone downloads their file and changes the filename, that data isn't being lost.
This is especially important because some imageboards may change the filename upon download.
In addition the popular browser extension 4ChanX natively can display the title of .webms with a simple mouse hover over a "title" link next to the embedded media, making accessing it extremely easy.
If you do not have 4chanX, simply inspecting the properties of the file on Windows and various Linux distros also works.

### Png image with a different thumbnail and expanded view

The .png file format allows for various "chunks" of other data to be shipped with an image. One of these is the gAMA chunk, which basically tells a program to calculate the brightness of every pixel as the original brightness to the power of the gAMA chunk `x=x^gAMA` and display it with these modified values.

For further light reading on why gAMA chunks exist:  [Henri Sivonen's website](https://hsivonen.fi/png-gamma/)

To hide one image in another with the help of a gAMA chunk, we first need to map these images to two different brightness ranges.
We map the thumbnail image to a brightness range of 0-210 (which can be done by applying a linear transformation to each color value of `x=x/255*210`) and the brightness values of the hidden image to a range of 214-255 (with the linear transformation for each color value of `x=214+(x/255)*(255-214)`).
As a result the hidden image is now extremely bright and appears to the normal eye almost white.
Next we need to combine these two images. We do this by replacing every 4th pixel (so every pixel where both the x and y index are uneven) of the thumbnail image with the hidden image.
For a image with sufficiently high resolution this will just look like the thumbnail image has gotten slightly brighter.

Then we apply the gAMA chunk with a value of 0.023 to the image, which is extremely low. The program trying to display the png will now take the brightness of every pixel to the power of 0.023 and thus darken the image significantly.
As a result the thumbnail image pixels appear almost black, while the extremely bright pixels of the hidden image now become normal and the hidden image becomes visible. Unfortunately due to 3/4ths of the pixels now being black the hidden image will appear darker.

The last part to this is that a lot of programs don't apply the gAMA chunk consistently. A lot of imageboards (and some applications like Discord or even the Windows image previews) will ignore theses auxiliary chunks like the gAMA chunk in the preview, thus only making the thumbnail image visible. Once you expand the image the chunk gets applied and the hidden image becomes visible.

Note that you can't really rely on this trick working for others unless you know they use the same program/OS as you. If they use some program that completely ignores or completely applies these chunks, the trick won't work. Additionally these images can exhibit artifacts when seen on some screens with different resolutions, specifically [Moiré patterns](https://en.wikipedia.org/wiki/Moir%C3%A9_pattern). 

### Greyification / Ninja images

Ninja images use another trick that works due to how most browsers / programs ignore .png chunks in previews. This mode works best with images that have no background (so the background is transparent).

The motive is made monochrome (so pixels are either one color, or invisible), then inverted.
Then the pixels of the motive are given a color (default is grey) and the background is given a slightly different color (the blue channel is shifted by a value of 1).
This change is not visible to the naked eye, so the image seems one color.

Next a tRNS chunk is added with the color value of the background. In the preview this chunk is ignored, but when expanded it gets applied and the background is made transparent, so the image appears.

### Cursing video files

Video files tend to have header information for the video player to know what to display and how to display it. We can mess with this data at the right place to create weird effects or "cursed" videos.
To edit these things we need to know where this data is contained. You can find the documentation for the filetypes here:

* [.mp4 file documentation](https://www.cimarronsystems.com/wp-content/uploads/2017/04/Elements-of-the-H.264-VideoAAC-Audio-MP4-Movie-v2_0.pdf)
* [.webm file documentation](https://www.matroska.org/technical/elements.html)

You can also do these manipulations manually in a HEX editor.

For *.mp4*:

First we locate the string "mvhd" which has a hex value of 0x6D766864 (The 0x is a prefix to state that it's a hex value. In a Hex editor search for the bytes 6D 76 68 64). From there move another 12 bytes (1 byte = 1 hex value).
This is where the interesting data is at: The first 4 bytes state how many units there are per second, while the next 4 bytes after that are how many units long the video is.
To set this to a very big length we can set the first 4 bytes to 0x00000001 and the second 4 bytes to 0xFFFFFFFF (which is 4.294.967.295 in decimal).

For *.webm*:

First we locate the 3 bytes 0x2AD7B1. Then from there we search for the first occurrence of 0x4489.
Some sources say you can just search for the first occurrence of 0x4489 and not bother with starting the search at 0x2AD7B1, but personally I would do it, just to make sure. The byte after that can either be 0x84 or 0x88.
If this is 0x84 the next 4 bytes contain the information for the video length. If it is 0x88 the video length is contained in the next 8 bytes.
In the case of this script if the identifier is 0x84 we replace it with 0x88 and insert 4 empty bytes of 0x00000000. Then we replace the 8 bytes after the identifier
(just to clarify, this means we overwrite the empty bytes we just inserted as well) with the value 0x3ff0000000000000.
You can play around with those values to see what they do, this particular value creates the kind of .webm that scales its length while playing.

### Webms with changing aspect ratio / video size

Generates a webm that upon playing constantly changes its size and aspect ratio, making clicking the controls impossible.
This trick works on a lot of imageboards and certain Videoplayers (but not all of them). VLC seems to be too slow and will partially have a black screen while displaying the resulting webm (on windows that is. It seems to work fine on Linux), mpv will display them fairly well. Some players (like for example the discord player) will have a fixed player size and "pad" the scaling video so the aspect stays the same and thus have the controls stay in one play (which destroys the effect.).

The generation of such files is actually pretty simple, the original file is chopped into various segments with different height and width (randomly generated). Then these segments are concatenated. In the end the audio from the original file is copied to the new concatenated video. Thus it is mostly a matter of telling ffmpeg what values to use and how often.

## Example images

### GUI example

![Showcase gif of the GUI](https://gitlab.com/Baut/readme-images/-/raw/master/ImgboardTools/GUIExample.gif)

### Hidden image

This hidden image was generated with the following two images:

![Source images for hidden example image](https://gitlab.com/Baut/readme-images/-/raw/master/ImgboardTools/HiddenImageSource.png)

and appears as follows on imageboards:

![Hidden example image on imageboard](https://gitlab.com/Baut/readme-images/-/raw/master/ImgboardTools/HiddenImageExample.gif)

### Ninja .png image

![NinjaPng example on imageboard](https://gitlab.com/Baut/readme-images/-/raw/master/ImgboardTools/NinjaPngExample.gif)

### Distorting .webm / .webm with changing aspect ratios

In this case with a (very modest) 3 changes per second. This can be much more or less.

![Distorted .webm example](https://gitlab.com/Baut/readme-images/-/raw/master/ImgboardTools/DistortionExample3PerSec.gif)

## Installation for non programmers

In this section it will be assumed that you have none of the required dependencies installed, are running windows 10 and have little to no knowledge of git.

1. Installing Python: Python is the programming language this program was written in. You can download it from [their official website](https://www.python.org/downloads/). Just download a version of Python 3. In the installation process there will be a checkbox named "add Python to Windows PATH". **Make sure you check that.**

2. Installing pip: Pip is a program allowing for easier installation of Python dependencies. If your version of Python is older than 3.4 you already have it.

3. Installing Pillow: Pillow is an image modification library used in this code. Installing it is easy. First you open a command prompt (To do so, press `windows key + r` and enter cmd in the window. Alternatively you can search for "cmd" in your windows search when you just press the windows key once). A black window should appear. This is the command prompt. Type `pip install pillow` in this window and press enter. A bunch of text should appear and Pillow should install.

4. Executable dependencies: The program uses 3 (more like 2) external programs - ffmpeg (a very powerfull software that can do a lot of modifications of video files), ffprobe (included in ffmpeg) and pngcrush (a command line utility that can easily edit png metadata). You have two ways you can install this: In any location by changing the windows PATH system variable (more involved, won't be explained here) and locally in the same directory as ImgboardTools.py (easier and thus the one explained here).

5. Download ffmpeg: For a non programmer you just want to download some executables (.exe files). Thankfully [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) has these for easy downloading. A 7zip archive can be found here: [Download ffmpeg here](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z). If this link doesn't work, visit the gyan.dev site or ffmpeg site directly and manually download this archive. Then extract it using 7zip or other programs that can extract .7z files. You only want the two files in the "bin" folder named `ffmpeg.exe` and `ffprobe.exe`.

6. Download pngcrush: The site for pngcrush can be found [here](https://pmt.sourceforge.io/pngcrush/). The download link can be found on sourceforge [here](https://sourceforge.net/projects/pmt/files/pngcrush-executables/). You want to choose the folder with the newest version number and click `pngcrush_X_X_X_w64.exe` if you have a 64 bit system and `pngcrush_X_X_X_w32.exe` if you have a 32 bit system. The Xes are version numbers. Rename your executable to just pngcrush.exe.

7. Download this program: Almost done, now you need to download this program. If you are on github click the green button to the upper right with the download icon and the text "code". There click "Download ZIP". If you are on gitlab instead click on the download button without text (upper right) and choose your preferred archive type. If you don't know what that means, click "zip". After the ZIP file is downloaded, extract it and move the whole folder to wherever you want to program to exist.

8. Move executables: Copy (or move/cut) the three executables (pngcrush.exe, ffmpeg.exe and ffprobe.exe) to the folder you extracted in step 7. It should be in the same location as "ImgboardTools.py" and "ImgboardTools - GUI edition.py". You can now start the program by clicking on "ImgboardTools - GUI edition.py". If you want to have a shortcut on your desktop, right click the GUI edition file and select "send to" and there "Desktop". You can rename this shortcut as you please. You can now open the program by clicking this icon. Files you created will appear in the folder you installed "ImgboardTools - GUI edition.py" in unless otherwise specified.

## Troubleshooting

If you get some error from the check_call command, or the error message otherwise states that "ffmpeg" or "pngcrush" aren't executables, you need to add their savelocation to the windows PATH variable. If you are on Linux, make sure you have the dependencies installed.

If you were to create a .webm with cursed length (with the -c option), and then try to have it change its aspect ratio constantly (with the -d option), the resulting file will most likely be corrupted. Don't do it. If you do it the other way around, the result may not be corrupted, but it won't work either, so just refrain from stacking the video effects.

Make sure that the webm you use as input complies with the upload requirements of the imageboard you want to use (correct audio encoding, correct filesize). ImgboardTools does not change these settings, because not all imageboards have the same requirements. 

Note that during the process of the "aspectMagic()" function a lot of new data is added, as essentially every change of aspect ratio adds new file header information. As a result the files will grow in size considerably (proportional to the amount of changes). If your file was close to the upload limit in size before it is likely that it's too big after the changes. Encode/Compress your webm accordingly beforehand.