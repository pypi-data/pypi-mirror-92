import os
import argparse
from itertools import chain
def filter_exceptions(file,exceptions):
    for i in chain(*exceptions):
        if file.endswith(i):
            return False
    return True
my_parser = argparse.ArgumentParser(description='Sort a folder by their extensions')
my_parser.add_argument('--l','-l', action='store',default=os.getcwd(),type=str,help=' Folder Location, Example: -l c:/desktop/')
my_parser.add_argument('--e','-e', action='append',default=[],type=str,nargs="+",help=' Give exceptions, Example: -e pdf png')

args = my_parser.parse_args()

exceptions = args.e
folder_location = args.l+'//'
os.chdir(folder_location)

print(folder_location,os.getcwd())
_OG_files = os.listdir()
_OG_files = filter(lambda x: filter_exceptions(x,exceptions),_OG_files)
files = []
extensions = []
for i in _OG_files:
    if '.' in i and 'lnk' not in i:
        files.append(i)
        extensions.append(i.split('.')[-1])
        
extensions = list(set(extensions))

for i in extensions:
    try:
        os.mkdir(i)
    except:
        pass
for i in extensions:
    for x in files:
        if x.endswith(i):
            os.replace(folder_location+x,folder_location+i+'/'+x)
undo=input('undo? (y or n) ')
if undo == 'y':
    for i in extensions:
        for x in files:
            if x.endswith(i):
                os.replace(folder_location+i+'/'+x,folder_location+x)
