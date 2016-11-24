## DIDmap
This tool downloads all files from a webpage which uses the aps.net file download (".asp?id=").
You will be surprised what kind of content people publish on their website which is publicly available.

## USAGE:
Pass the URL as an argument and run the script. For example:
```
python DIDmap.py www.example.com/downloadfile.asp?id=
```
The script will start with ID=1,ID=2,ID=3 ect. and continue to download till 250 empty ID's. Then it will automatically stop.
