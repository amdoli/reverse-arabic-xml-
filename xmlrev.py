import os
import re
import sys
import subprocess
import json
import time

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

JSON_FILE='config.json'

class Xml:
    def __init__(self):
        self.filename=self.setfile()     # get the file from setfile function
        self.operation=self.check_json() # check if there are any method enabled
    
    def check(self):       # check if self.filename is real then return true
        if self.filename != "":
            return True
        else:
            return False
        
    def save(self,operation):
        with open(JSON_FILE,"w") as f:
            json.dump(operation,f,indent=4)
            
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
            counter=0
            with open(self.filename,'r',encoding='utf-8') as f:
                print(f"\n## READING IN: {self.filename} ##\n\n")
                old_line_num=1
                for line_num , line in enumerate(f,1):
                    updated_line = line
                    checks=re.finditer(arabic_pattern,line)   # check if pattern can applie on the line
                    for check in checks:
                        word=check.group(0)
                        reversed_word=word[::-1] 
                        start,end=check.span()
                        updated_line=updated_line[:start]+reversed_word+updated_line[:end]
                        #print(f"start={start} end={end}")
                        self.append(updated_line,line_num)
                        #print(f"{word[::-1]} {line_num}")                     
        else:
            print(f"{self.filename} not found or not in a directory!")
    def append(self,updated_line,line_num):
        shift_down="\n"*line_num
        with open(self.filename,"a") as f:
            f.write(f"{shift_down}{updated_line}")
        
    def check_json(self):
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE,"r")as f:
                operation=json.load(f)
        if operation["method"]["all_except"] == True and operation["method"]["only"] == False:
            return 0
        elif operation["method"]["only"] == True and operation["method"]["all_except"] == False:
            return 1
        elif operation["method"]["only"] == True and operation["method"]["all_except"] == True:
            print("You have both methods True!\n")
            time.sleep(0.5)
            print("1-All_except")
            print("2-Only")
            print("3-None of them (reverse everything)")
            answer=input("\nPlease chose on of the three:\n")
            if answer in ("1","all","all_except","except","ALL_EXCEPT","ALL","All_except","All except","all except"):
                operation["method"]["only"] = False
                self.save(operation)
                return 0
            elif answer in ("2","only","ONLY","o","O"):
                operation["method"]["all_except"] = False
                self.save(operation)
                return 1
            elif answer in ("3","NONE","None","none","None of them","None of them (reverse everything)","None_of_them",""):
                operation["method"]["all_except"] = False
                operation["method"]["only"] = False
                self.save(operation)
                return 2

    def check_config(self,line_number): # still under devoloping
        list_of_numbers=[]
        with open("all_except.txt",'r') as f:
            for lines in f:
                line=lines
                if line[0]!="#":
                    if line.isdigit():
                        list_of_numbers.append(line)
                        print(line)
        if line_number in list_of_numbers:
            return True
        else:
            return False
        
def install_packages():     # check for dependenceys
    for package in REQ_PACKAGES:
        print(f"Dependency '{package}' not found. Installing...")
        subprocess.check_call([sys.executable,"-m","pip","install",package])
        print(f"{package} installed succesfully!")

    
if __name__=="__main__":
    print("\033[2J\033[H")
    xml_file = Xml()
    #xml_file.check_json()
    #xml_file.check_config(4)
    xml_file.reverse()

#if user_input_match:
  #  for words in user_input_match:
   #     print(f"{words}\n")

    