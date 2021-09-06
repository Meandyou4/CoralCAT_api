import glob
import os
import shutil
from os import path
import os
import pathlib

def moveit(extension):
    list_of_files = glob.glob('*.'+extension) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    #print(os.path.abspath(latest_file))

    source_path = os.path.abspath(latest_file)
    source=pathlib.Path(latest_file).parent.resolve()
    if path.exists(source_path):
        destination_path = "images"
        new_location = shutil.move(os.path.join(source, latest_file), os.path.join(destination_path, latest_file))
        print(new_location)
        print("The %s is moved to the location, %s" %(source_path, new_location))
    else:
        print("File does not exist.")

moveit("jpg")


#dst_filename = os.path.join(dst_dirname, os.path.basename(src_filename)); shutil.move(src_filename, dst_filename)