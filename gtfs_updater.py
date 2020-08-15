from ftplib import FTP
import zipfile
import os
import time
from tqdm import tqdm

SAVE_DIR = "D:/Temp/"
GTFS_DIR = "D:/gtfs/"
GTFS_NAME = "israel-public-transportation.zip"

ftp = FTP('199.203.58.18')
ftp.login()
print("Connected")

def gtfs_download():
    with open(GTFS_NAME, 'wb') as fd:
        total = int(ftp.size(GTFS_NAME))

        with tqdm(total=total, unit='B', unit_scale=True) as pbar:
            def cb(data):
                l = int(len(data))
                pbar.update(l)
                fd.write(data)

            ftp.retrbinary('RETR {}'.format(GTFS_NAME), cb)

def main():

    if not os.path.isdir(SAVE_DIR):
        print('Temp directory is not present. Creating a new one.')
        os.mkdir(SAVE_DIR)
    else:
        print('Temp directory is present.')

    os.chdir(SAVE_DIR)

    remote_datetime = ftp.voidcmd("MDTM " + GTFS_NAME)[4:].strip()
    remote_timestamp = time.mktime(time.strptime(remote_datetime, '%Y%m%d%H%M%S'))

    if os.path.isfile(SAVE_DIR + "/" + GTFS_NAME):
        print("Found local gtfs archive.")

    else:
        print("Local gtfs archive not found, Downloading.")
        gtfs_download()

    local_gtfs_timestamp = os.path.getmtime(GTFS_NAME)

    if int(remote_timestamp) > int(local_gtfs_timestamp):
        print("Local file has expired, Retriving up to date file")
        gtfs_download()

    else:
        print("Local file is up to date.")

    FTP.quit(ftp)

    if not os.path.isdir(GTFS_DIR):
        print('Working directory is not present. Creating a new one.')
        os.mkdir(GTFS_DIR)
    else:
        print('Working directory is present.')

    with zipfile.ZipFile(GTFS_DIR) as zip:
        print("Extracting")
        for item in tqdm(zip.infolist(), total=len(zip.namelist()), unit='Files'):
            zip.filename = os.path.basename(zip.filename)
            try:
                zip.extract(item, GTFS_DIR)
            except zipfile.error() as error:
                pass

    zip.close()
    print("Extracted to ../gtfs/ folder.")

if __name__ == "__main__":
    main()