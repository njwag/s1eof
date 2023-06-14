import requests
import re
import feedparser
from os import listdir
from os.path import isfile, join, isdir, dirname, realpath
from datetime import timedelta, datetime
from dateutil.parser import parse
#from urllib.parse import urlparse

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


def check_existing(s1dir):
    """
    This function retrieves the start and end validity dates and Sentinel-1 mission identifiers 
    for Sentinel-1 orbit files from Sentinel-1 files (zipped or unzipped) that follow the
    Sentinel-1 naming convention.
    
    Parameters
    ----------
    s1dir : str, Directory where Sentinel-1 files (zipped or unzipped) are located.
            The file naming needs to conform to the Sentinel-1 naming convention.
            Alternatively, use user defined date range to search for orbit files.

    Returns
    -------
    Dates and platform identifier of orbit files to be downloaded.

    """
    download_dates = []
    for f in listdir(s1dir):
            if re.match('S1[AB]_.._...._[12][SA](SH|SV|DH|DV)_\d{8}T\d{6}_\d{8}T\d{6}_\w{18}\..*$',f): #regex expression
                satellite = f[1:3]
                date = datetime.strptime(f[17:25],'%Y%m%d')
                start = date - timedelta(days=1)
                end = date + timedelta(days=1)
                download_dates.append([satellite, start, end])
                
    download_dates = sorted(download_dates,reverse=True)
    return(download_dates)


def get_urls(download_dates,producttype='AUX_POEORB'):   
    """
    This function creates a list of Copernicus POD Data Hub query urls from a list of
    dates and mission identifiers for Sentinel-1.
    
    Parameters
    ----------
    download_dates : list, List of start and end dates for orbit file validity.
    
    Returns
    -------
    List of search query urls.

    """
    URLs = [''.join(['https://scihub.copernicus.eu/gnss/search?q=(platformname:Sentinel-1 ',
                     'AND producttype:',
                     producttype,' ',
                     'AND platformserialidentifier:',
                     satellite, ' ',
                     'AND beginposition:[',
                     start.strftime('%Y-%m-%d'),
                     'T00:00:00.000Z TO ',
                     start.strftime('%Y-%m-%d'),
                     'T23:59:59.000Z] ',
                     'AND endposition:[',
                     end.strftime('%Y-%m-%d'),
                     'T00:00:00.000Z TO ',
                     end.strftime('%Y-%m-%d'),
                     'T23:59:59.000Z])'])
            for satellite,start,end in download_dates]
    return(URLs)


def get_urls_daterange(start,end,producttype='AUX_POEORB'):
    """
    This function creates a Copernicus POD Data Hub query url from a user defined start and end date.
    
    Parameters
    ----------
    start : str, Start date for orbit file validity.
    end : str, End date for orbit file validity.
    
    Returns
    -------
    URL for requesting all products within the user defined date range.

    """
    #start = datetime.strptime(start, '%Y-%m-%d')
    #end = datetime.strptime(end, '%Y-%m-%d')
    start = parse(start)
    end = parse(end)
    
    start = start - timedelta(days=1)
    end = end + timedelta(days=1)
    
    URL = ''.join(['https://scihub.copernicus.eu/gnss/search?q=(platformname:Sentinel-1 ',
                     'AND producttype:',
                     producttype,' ',
                    'AND beginposition:[',
                    start.strftime('%Y-%m-%d'),
                    'T00:00:00.000Z TO ',
                    start.strftime('%Y-%m-%d'),
                    'T23:59:59.000Z] ',
                    'AND endposition:[',
                    end.strftime('%Y-%m-%d'),
                    'T00:00:00.000Z TO ',
                    end.strftime('%Y-%m-%d'),
                    'T23:59:59.000Z])',
                    '&rows=100'])
    return(URL)  
    
    
    

def get_orbits(URLs,username='gnssguest',password='gnssguest',daterange=False):
    """
    This function returns a list of download links from a list of Copernicus POD Data Hub query urls.
    
    Parameters
    ----------
    URLs : list, List of search query urls.
    
    username : str, For access to Copernicus Sentinels POD Data Hub. The default is 'gnssguest'.
    
    password : str, The default is 'gnssguest'.

    Returns
    -------
    List of download urls.

    """
    download_list = []
    
    if daterange == False:
        if check_internet() == True:
            for URL in URLs:
                # sending get request and saving the response as response object 
                r = requests.get(url = URL, auth=(username, password))
                feed = feedparser.parse(r.content)
                link = feed.entries[0].link
                title = [feed.entries[0].title,'EOF']
                filename = '.'.join(title)
                download_list.append([filename,link])
                
        elif check_internet() == False:
            print('No internet connection.')
            
    elif daterange == True:
        if check_internet() == True:
            r = requests.get(url = URLs, auth=(username, password))
            feed = feedparser.parse(r.content)
            totalitems = int(feed['feed']['opensearch_totalresults'])
            ind = int(feed['feed']['opensearch_startindex'])
            itemspp = int(feed['feed']['opensearch_itemsperpage'])
            
            while ind <= totalitems:
                url = URLs + '&start=' + str(ind)
                ind = ind + itemspp
                r = requests.get(url = url, auth=(username, password))
                feed = feedparser.parse(r.content)
                for e in feed.entries:
                    link = e.link
                    title = [e.title,'EOF']
                    filename = '.'.join(title)
                    download_list.append([filename,link])
                
        elif check_internet() == False:
            print('No internet connection.')
    
    if not download_list:
        print("No orbit files found. Check date range. \n"+
              "Note: aux_poeorb files are available 20 days after image acquisition \n"+
              "aux_resorb files are available 0 to 1 days after image acquisition. \n"+
              "Date range must be within Sentinel-1 mission life time.")
    else:
        return(download_list)


def download_orbits(download_list,orbitfolder,username='gnssguest',password='gnssguest'):
    """
    This function downloads .EOF orbit files from a list of download links and saves them to a 
    user-defined destination.
    
    Parameters
    ----------
    download_list : list, List of download urls.
    
    orbitfolder : str, Destination folder for orbit files
    
    username : str, For access to Copernicus Sentinels POD Data Hub. The default is 'gnssguest'.
    
    password : str, The default is 'gnssguest'.

    Returns
    -------
    None.

    """
    n = len(download_list)
    x = 1
    for filename, url in download_list:
        if (not isfile(join(orbitfolder,filename))):
            destination = join(orbitfolder,filename)
            r = requests.get(url, auth=(username,password))
            if r.status_code == 200:
                print('Downloading {} of {}'.format(x,n))
                x += 1
                with open(destination, 'wb') as out:
                    for bits in r.iter_content():
                        out.write(bits)
        else:
            print('File exists. Skipping...')
            x += 1