import utils.utils as utils
import argparse
from dateutil.parser import parse
from os.path import join, isdir, dirname, realpath
from gooey import Gooey, GooeyParser
#from message import display_message

#%%


# @Gooey(dump_build_config=True, 
#        program_name="Sentinel-1 EOF Downloader", 
#        default_size=(610, 530),
#        required_cols=1,
#        optional_cols=1
#        )
def main():
    desc = "Download Sentinel-1 orbit files"

    #parser = GooeyParser(description=desc)
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(
        "Orbit Directory", help="Location where orbit files will be stored") #, widget="DirChooser")
    
    parser.add_argument( '-d',
        "--Sentinel1 Directory", help="Directory where S1 files are stored") #, widget="DirChooser")
    parser.add_argument('-s', '--Start date', type=str,
                                help='Start date for orbit file search \"YYYY-MM-DD\"') #, widget='DateChooser')
    parser.add_argument('-e', '--End date', type=str,
                                help='End date for orbit file search \"YYYY-MM-DD\"') #, widget='DateChooser')
    parser.add_argument(
        "-o", "--overwrite", action="store_true", help="Overwrite output file (if present). Default is False.")

    parser.parse_args()
    args = vars(parser.parse_args())
    return(args)
    #display_message()


def is_date(string, fuzzy=False):
    """
    
    Returns True if string is date, False otherwise.

    Parameters
    ----------
    string : str, User input string.
    fuzzy : bool, Ignore unknown tokens in string if True.

    Returns
    -------
    Boolean

    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

#%%
if __name__ == '__main__':
    args = main() # dictionnary

    if args['Sentinel1 Directory'] is not None:
        if not isdir(args['Sentinel1 Directory']):
                print('Sentinel-1 directory does not exist. Please enter again.')
        else:
            download_dates = utils.check_existing(args["Sentinel1 Directory"])
            urls = utils.get_urls(download_dates)
            download_list = utils.get_orbits(urls)
    elif is_date(args['Start date']) and is_date(args['End date']):
        urls = utils.get_urls_daterange(args['Start date'], args['End date'])
        download_list = utils.get_orbits(urls,daterange=True)
    else:
        print('Provide either Sentinel-1 directory or valid start and end date.')
    
    utils.download_orbits(download_list,args["Orbit Directory"])