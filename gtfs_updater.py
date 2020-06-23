from ftplib import FTP
import zipfile
import os
import glob
import shutil
import time
from tqdm import tqdm

savedir = "D:/Temp/"
gtfs_dir = "D:/gtfs/"
gtfs = "israel-public-transportation.zip"

if not os.path.isdir(savedir):
    print('The directory is not present. Creating a new one..')
    os.mkdir(savedir)
else:
    print('The directory is present.')

os.chdir(savedir)

ftp = FTP('199.203.58.18')
ftp.login()
print("Connected")

remote_datetime = ftp.voidcmd("MDTM " + gtfs)[4:].strip()
remote_timestamp = time.mktime(time.strptime(remote_datetime, '%Y%m%d%H%M%S'))

if os.path.isfile(savedir + "/" + gtfs):
    print("Found local file")

else:
    print("Local file not found, Downloading.")
    with open(gtfs, 'wb') as fd:
        total = int(ftp.size(gtfs))

        with tqdm(total=total, unit='B', unit_scale=True) as pbar:
            def cb(data):
                l = int(len(data))
                pbar.update(l)
                fd.write(data)

            ftp.retrbinary('RETR {}'.format(gtfs), cb)

local_gtfs_timestamp = os.path.getmtime(gtfs)

if int(remote_timestamp) > int(local_gtfs_timestamp):
    print("Retriving up to date file")
    file = open(gtfs, "wb")
    ftp.retrbinary("RETR " + gtfs, file.write)
    file.close()
    print("Retrived up to date file")
else:
    print("Local file is up to date.")

FTP.quit(ftp)

if not os.path.isdir(gtfs_dir):
    print('The directory is not present. Creating a new one..')
    os.mkdir(gtfs_dir)
else:
    print('The directory is present.')

with zipfile.ZipFile(gtfs) as zip:
    print("Extracting")
    for member in tqdm(zip.infolist(), total=len(zip.namelist()), unit='Files'):
        zip.filename = os.path.basename(zip.filename)
        try:
            zip.extract(member, gtfs_dir)
        except zipfile.error() as error:
            pass

zip.close()
print("Extracted to ../gtfs/ folder.")