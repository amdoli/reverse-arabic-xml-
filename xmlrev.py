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

try:                                                  
    from arabic_reshaper import reshape
except ImportError:
    install_packages(arabic-reshaper)


# if you want to add other packages insert them here
REQ_PACKAGES = [          
    "arabic-reshaper",
]

JSON_FILE='config.json'
ALL_EXCEPT_FILE="all_except.txt"
ONLY_FILE="only.txt"

class FileHandler:
    def __init__(self):
        self.filename = self.setfile()

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
    
    def check(self):       # check if self.filename is real then return true
        if self.filename != "":
            return True
        else:
            return False
    
    def writee(self,lines):    # to overwrite the file with only the updated arabic
        if os.path.exists(self.filename): 
            with open(self.filename,"w",encoding="utf-8") as f:
                for i in range(len(lines)):
                    f.write(lines[i])

class Config:
    def __init__(self):
        self.json_content=self.load_json()

    def save(self,operation):
        with open(JSON_FILE,"w") as f:
            json.dump(operation,f,indent=4)

    def chech_methods(self):     # to check methodes 
        # loads json content
        operation=self.json_content 

        if operation["method"]["all_except"] == True and operation["method"]["only"] == False:
            return 0
        
        elif operation["method"]["only"] == True and operation["method"]["all_except"] == False:
            return 1
        
        # here there is a problem so the app make sure that never happen!
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
    
    def check_reshape(self):
        content=self.json_content # Load json content
        if content["features"]["reshape"]: 
            return True
        else:
            return False
    
    def check_reverse(self):
        content=self.json_content # Load json content
        if content["features"]["reverse"]: 
            return True
        else:
            return False
    
    def load_json(self):
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE,"r") as f:
                return json.load(f)
        else:
            print(f"Error. {JSON_FILE} does not exist!")
            return {}
        
    def all_except(self,line_number): 
        list_of_numbers=[]
        if os.path.exists(ALL_EXCEPT_FILE):
            with open(ALL_EXCEPT_FILE,'r') as f:
                for lines in f:
                    line=lines
                    if line[0]!="#":
                        if line.isdigit():
                            list_of_numbers.append(line)

            if str(line_number) in list_of_numbers:
                return True
            else:
                return False
        else:
            print("Error.  all_except.txt file does not exist!")
        
    def only(self,line_number):
        list_of_numbers=[]
        if os.path.exists(ONLY_FILE):
            with open(ONLY_FILE,'r') as f:
                for lines in f:
                    line=lines
                    if line[0]!="#":
                        if line.isdigit():
                            list_of_numbers.append(line)
                            
            if str(line_number) in list_of_numbers:
                return True
            else:
                return False
        else:
            print("Error.  only.txt file does not exist!")

class Xml:
    def __init__(self,FileHandler,Config):
        # classes
        self.file_handler=FileHandler     # make it in touch with FileHandler class
        self.config=Config                # make it in touch with Config class

        self.filename=self.file_handler.filename   # for readability
        self.operation=self.config.chech_methods() # check if there are any method enabled
    
    def load_content(self):     # to load or get the content from the file
        if os.path.exists(self.filename): #
            lines=[]
            with open(self.filename,'r',encoding="utf-8") as f: #
                for line in f:
                    lines.append(line)
            return lines
        
        else:
            print("didn't find it")
            return []
    
    def reshapes(self,content):
        return reshape(content)

    def reverse(self): # reverse arabic data
        arabic_pattern = r'[\u0600-\u06FF\uFE00-\uFEFF](?:[\u0600-\u06FF\uFE00-\uFEFF \!\.\,]*[\u0600-\u06FF\uFE00-\uFEFF\!\.])?'

        if self.file_handler.check():
            lines=self.load_content()   # first get the whole content
            print(f"\n## READING IN: {self.filename} ##\n\n") #

            for line_num , line in enumerate(lines,1):

                # all_except.conf condition
                if self.config.chech_methods() == 0:
                    if self.config.all_except(line_num):
                        continue

                # only.conf condition
                elif self.config.chech_methods() == 1:
                    if not self.config.only(line_num):
                        continue

                updated_line = line
                matches=list(re.finditer(arabic_pattern,line))   # check if pattern can applie on the line

                for match in reversed(matches): # start from the end to not destroy the spaces and postion
                    content=match.group(0)
                    # if reshape feature is true in json file it will reshape
                    if self.config.check_reshape():
                        content=reshape(content)

                    if any('\u0600' <= c <= '\u06FF' or '\uFE70' <= c <= '\uFEFF' for c in content):    # to catch only arabic letters

                        if self.config.check_reverse():
                            content=content[::-1] # reversed content

                        start,end=match.span()
                        updated_line=updated_line[:start]+content+updated_line[end:]

                lines[line_num-1]=updated_line

            self.file_handler.writee(lines)
                 
        else:
            print(f"{self.filename} not found or not in a directory!")
          
if __name__=="__main__":
    print("\033[2J\033[H")
    file_handler=FileHandler()
    config=Config()
    xml_file = Xml(file_handler,config)
    xml_file.reverse()
