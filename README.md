# ImgboardTools

Python code for a CLI tool with various features, mostly for use on imageboards.

Stuff is probably not very optimized and has no error handling, but it works.

## Requirements

You need the following python libraries:
* Pillow, get it with `pip install pillow`

You also need the following software/executables:
* ffmpeg
* pngcrush

## Usage

Works as a CLI tool. To get started use

    python ImgboardTools.py -h

Features so far (checked means implemented):

- [x] Anonymize images by deleting EXIF data out of them.
- [x] Change/Overwrite the metadata on a WEBM.
- [x] Combine/Hide two images within each other by messing with PNG gamma values and brightness
- [x] Add command line interface to the program.
- [x] Add feature to hide image in grey background by messing with PNG "trns" chunks and colors.

Note that the help messages of argparse have some custom syntax:

 * Brackets [] contain the expected arguments.
 * Arguments in parentheses () are optional.
 * Arguments in braces {} are possible example values.