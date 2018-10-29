from glob import glob
import re

#Define function to pull file names
def get_file_names(regex_pattern):
    fnames = glob(regex_pattern)

    #get files from file Data/
    list_of_names = [re.sub('Data\/|\.txt', '', x) for x in fnames]
    return list_of_names
