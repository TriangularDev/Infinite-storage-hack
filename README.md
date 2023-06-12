# Infinite storage hack.
Fuck Google am I right.

Get infinite (But slow as fuck) storage by storing your data as youtube videos.

## "But somebody has already done that!!!!!"'

Yes, somebody has already done that. It even made news on some nerdy tech sites.

[YDrive by Tensorneko](https://github.com/tensorneko/YDrive) does a similar thing by turning each one and zero into an individual pixel.

## My approach

The problem is Youtube compresses the shit out of their videos. Youtube also changes the pixels on their end. 

So I'm gonna store them as QR codes instead.

QR codes can be scaled and shrunk because of how they are designed.

QR codes have error correction so compression is less likley to ruin the QR code.

My algorithm does this:

 1. Make a thread for each chunk of the file.
 2. Each thread compresses the chunk with gzip, encodes it in base64, and makes a qr code.
 3. The master thread takes all of these photos and merges them into a 1fps video.

This is slow as hell but it can store files of any size. And is practically compression-proof. (Youtube does have length limits but that should be no big deal.)

## Enough nerd shit!!! HOW USE???
Figure it out. If it was hard to write it should be hard to execute.
Just kidding, I wonder how many low attention-span 12 year olds clicked off.

### Install dependencies

Install Python3. If you ran python scripts before or you ran suspicious shit from a user on discord, then you probably have Python.

Run this in your terminal.

    pip install qrcode pyzbar pillow

The  required zbar  DLLs are included with the Windows Python wheels for the pyzbar module. On other operating systems, you will need to install the  zbar  shared library.

Mac OS X:

    brew install zbar

Linux:

    sudo apt-get install libzbar0

### Download

Download the files and extract it. If you need help doing that you are genetically defecitve.

### Run

While in the folder with the code. In your terminal, run one of the following.

Encoding:

    python3 encode.py

Decoding:

    python3 decode.py