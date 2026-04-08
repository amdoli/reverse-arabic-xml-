import os
import re
import sys
import subprocess

def install_packages(package):     # check for dependenceys
        print(f"Dependency '{package}' not found. Installing...")
        subprocess.check_call([sys.executable,"-m","pip","install",package])
        print(f"{package} installed succesfully!")

#try:                                                   maybe later I will need arabic_reshaper
#    from arabic_reshaper import reshape
#except ImportError:
#    install_packages(arabic-reshaper)


# if you want to add other packages insert them here
REQ_PACKAGES = [          
    "arabic-reshaper",
]

class Xml:
    def __init__(self):
        self.filename=self.setfile()     # get the file from setfile function
    
    def check(self):       # check if self.filename is real then return true
        if self.filename != "":
            return True
        else:
            return False
            
    def setfile(self):      # check for which file do you want
        files=[] 
        for file in os.listdir():
            ext=file.split(".")
            num_of_dot=file.count(".")  # count how many . to print the . for extenstion if there are multible dots
            if "xml" in ext[num_of_dot]:
                files.append(file)
        if len(files)==0:   # if there are no files return none
            return None
        counter=0
        print(f"---------------------------\n")
        for file in files:
            print(f"{counter}- {file}")
            counter+=1
        print("\n---------------------------")
        while True:
            user_input=input("\nwrite which one do you want\n")
            if user_input in files or (int(user_input) in range(counter) if user_input.isdigit() else False):
                if user_input.isdigit():
                    return files[int(user_input)]
                return user_input
            else:
                print("Please try again")

    def reverse(self): # reverse arabic data
        arabic_pattern = r'[\u0600-\u06FF\uFE00-\uFEFF]+'
        if self.check():
            with open(self.filename,'r',encoding='utf-8') as f:
                print(f"\n## READING IN: {self.filename} ##\n\n")
                for line in f:
                    checks=re.finditer(arabic_pattern,line)   # check if pattern can applie on the line
                    for check in checks:
                        print(check.group(0)[::-1])
        else:
            print(f"{self.filename} not found or not in a directory!")
            
    def context(self,filename):
        with open(filename) as f:
            lines=""
            for line in f:
                lines+=line
            return lines
        
def install_packages():     # check for dependenceys
    for package in REQ_PACKAGES:
        print(f"Dependency '{package}' not found. Installing...")
        subprocess.check_call([sys.executable,"-m","pip","install",package])
        print(f"{package} installed succesfully!")

    
if __name__=="__main__":
    print("\033[2J\033[H")
    xml_file = Xml()
    xml_file.reverse()

#if user_input_match:
  #  for words in user_input_match:
   #     print(f"{words}\n")

    