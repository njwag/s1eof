# Sentinel-1 Orbit File Downloader

## General information

Downloads Sentinel-1 orbit files from the [Copernicus Sentinels POD Data Hub](https://scihub.copernicus.eu/gnss/#/home). The software can automatically detect Sentinel-1 files (zipped or unzipped) that conform to the Sentinel-1 naming convention. Alternatively the user can choose to download all orbit files for a given date range or download the full archive.

## Contents

* `s1eof.py` - main script to be run with Python
* `utils/` - download functions
* `tests/` - basic test routines

## Installation and required Python dependencies

The first step is to clone the s1eof repository and check out the s1eof directory.

```console
$ git clone https://github.com/CCI-Tools/cate.git
$ cd cate
```

Run the following command to install dependencies from requirements.txt:

```console
$ pip install -r path\to\requirements.txt
```

Using conda:

```console
$ conda create --name s1eof
$ conda activate s1eof
$ pip install -r path\to\requirements.txt
```

Alternatively, using conda you can install all required dependencies in a new environment called s1eof using the environment.yml file:

```console
$ conda env create -f path\to\environment.yml
```

## Using the Sentinel-1 Orbit File Downloader

Run s1eof.py in the command line. You can either pass a start and end date using the -s and -e flags respectively. Alternatively, you can pass a Sentinel-1 directory using the -d flag containing Sentinel-1 files (zipped or unzipped) that follow the Sentinel-1 naming convention. Fitting orbit files will be identified and downloaded automatically.

The orbit directory (-o flag) is mandatory. This is where the downloaded orbit files will be stored.

```console
$ s1eof.py [-h] [-d SENTINEL1 DIRECTORY] [-s START DATE] [-e END DATE] [-o] Orbit Directory
```

```console
$ python s1eof.py -h

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

Note: I do not control, guarantee, approve, or endorse the information or products available on the sites linked.