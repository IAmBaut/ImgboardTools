# ImgboardTools

Python code for a CLI tool with various features, mostly for use on imageboards.

Stuff is probably not very optimized and has no error handling, but it works.

## Requirements

You obviously need python.

For python you need the following libraries:
* Pillow, get it with `pip install pillow`

You also need the following software/executables:
* ffmpeg
* pngcrush

## Usage

Works as a CLI tool. To get started use

    python ImgboardTools.py -h

which will display the help window:

      -h, --help            show this help message and exit
      -a ANONYMIZE          Delete identifying EXIF data on a jpg. [filename]
      -w WEBM               Change "title" metadata of a webm. [title,(inputfilename=vid.webm),(outputfilename=inputfilename)]
      -m MIX                Hide image in another image. [thumbnail_img, hidden_img,(mode{L/RGB/RGBA/CMYK})]
      -g GREYIFY            Hide image on grey background. [imagepath,(R),(G),(B)]
      -c CURSE              Curse a webm or mp4 video file length [inputfile,(outputfile)]

Note that the help messages of argparse have some custom syntax:

* Brackets [] contain the expected arguments.
* Arguments in parentheses () are optional.
* Arguments in braces {} are possible example values.

## Examples

So for example to mix two images you would call:

    python ImgboardTools.py -m front.png back.png

Features so far (checked means implemented):

- [x] Anonymize images by deleting EXIF data out of them.
- [x] Change/Overwrite the metadata on a WEBM.
- [x] Combine/Hide two images within each other by messing with PNG gamma values and brightness
- [x] Add command line interface to the program.
- [x] Add feature to hide image in grey background by messing with PNG "trns" chunks and colors.
- [x] Add feature to "curse" .webm or .mp4 video file duration by messing with the file headers. <- note that these do not get buffered, so very large files will probably crash. The upload size limit on most imageboards probably makes this irrelevant though.
- [ ] Add a GUI application for the script. (This will most likely be an an affront to your eyes, but get the job done.)



## Troubleshooting

If you get some error from the check_call command, or the error message otherwise states that "ffmpeg" or "pngcrush" aren't executables, you need to add their savelocation to the windows PATH variable.
