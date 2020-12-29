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

Features so far (checked means implemented):

- [x] Anonymize images by deleting EXIF data out of them.
- [x] Change/Overwrite the metadata on a WEBM.
- [x] Combine/Hide two images within each other by messing with PNG gamma values and brightness
- [x] Add command line interface to the program.
- [x] Add feature to hide image in grey background by messing with PNG "trns" chunks and colors.
- [x] Add feature to "curse" webm or mp4 video file duration by messing with the file headers. <- note that these do not get buffered, so very large files will probably crash. The upload size limit on most imageboards probably makes this irrelevant though.

Note that the help messages of argparse have some custom syntax:

 * Brackets [] contain the expected arguments.
 * Arguments in parentheses () are optional.
 * Arguments in braces {} are possible example values.

## Troubleshooting

If you get some error from the check_call command, or the error message otherwise states that "ffmpeg" or "pngcrush" aren't executables, you need to add their savelocation to the windows PATH variable.
