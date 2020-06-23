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

ftp = FTP('199.203.58.18')
ftp.login()
print("Connected")

if not os.path.isdir(savedir):
    print('Temp directory is not present. Creating a new one.')
    os.mkdir(savedir)
else:
    print('Temp directory is present.')

os.chdir(savedir)

remote_datetime = ftp.voidcmd("MDTM " + gtfs)[4:].strip()
remote_timestamp = time.mktime(time.strptime(remote_datetime, '%Y%m%d%H%M%S'))

if os.path.isfile(savedir + "/" + gtfs):
    print("Found local gtfs archive.")

else:
    print("Local gtfs archive not found, Downloading.")
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
    print("Local file has expired, Retriving up to date file")
    with open(gtfs, 'wb') as fd:
        total = int(ftp.size(gtfs))

        with tqdm(total=total, unit='B', unit_scale=True) as pbar:
            def cb(data):
                l = int(len(data))
                pbar.update(l)
                fd.write(data)

            ftp.retrbinary('RETR {}'.format(gtfs), cb)

else:
    print("Local file is up to date.")

FTP.quit(ftp)

if not os.path.isdir(gtfs_dir):
    print('Working directory is not present. Creating a new one.')
    os.mkdir(gtfs_dir)
else:
    print('Working directory is present.')

with zipfile.ZipFile(gtfs) as zip:
    print("Extracting")
    for item in tqdm(zip.infolist(), total=len(zip.namelist()), unit='Files'):
        zip.filename = os.path.basename(zip.filename)
        try:
            zip.extract(item, gtfs_dir)
        except zipfile.error() as error:
            pass

zip.close()
print("Extracted to ../gtfs/ folder.")