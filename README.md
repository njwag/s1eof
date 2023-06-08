# Sentinel-1 Orbit File Downloader
Author: Nicolas Wagener

## General information

Downloads Sentinel-1 orbit files from the [Copernicus Sentinels POD Data Hub](https://scihub.copernicus.eu/gnss/#/home). The software can automatically detect Sentinel-1 files (zipped or unzipped) thath conform to the Sentinel-1 naming convention. Alternatively the user can choose to download all orbit files for a given date range or download the full archive.

## Required Python dependencies

Run the following command to install dependencies from requirements.txt:

```console
pip install -r path\to\requirements.txt
```

## Using the Sentinel-1 Orbit File Downloader

```console
s1eof.py [-h] [-d SENTINEL1 DIRECTORY] [-s START DATE] [-e END DATE] [-o] Orbit Directory
```

```console
& python s1eof.py -h

usage: s1eof.py [-h] [-d SENTINEL1 DIRECTORY] [-s START DATE] [-e END DATE] [-o] Orbit Directory

Download Sentinel-1 orbit files

positional arguments:
  Orbit Directory       Location where orbit files will be stored

optional arguments:
  -h, --help            show this help message and exit
  -d SENTINEL1 DIRECTORY, --Sentinel1 Directory SENTINEL1 DIRECTORY
                        Directory where S1 files are stored
  -s START DATE, --Start date START DATE
                        Start date for orbit file search "YYYY-MM-DD"
  -e END DATE, --End date END DATE
                        End date for orbit file search "YYYY-MM-DD"
  -o, --overwrite       Overwrite output file (if present)
```