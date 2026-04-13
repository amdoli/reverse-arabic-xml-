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
    
    def load_content(self):     # to load or get the content from the file
        if os.path.exists(self.filename):
            lines=[]
            with open(self.filename,'r') as f:
                for line in f:
                    lines.append(line)
            return lines
        else:
            print("didn't find it")
            return []

    def reverse(self): # reverse arabic data
        arabic_pattern = r'[\u0600-\u06FF\uFE00-\uFEFF](?:[\u0600-\u06FF\uFE00-\uFEFF \!\.\,]*[\u0600-\u06FF\uFE00-\uFEFF\!\.])?'

        if self.check():
            lines=self.load_content()   # first get the whole content
            print(f"\n## READING IN: {self.filename} ##\n\n")

            for line_num , line in enumerate(lines,1):

                # all_except.conf condition
                if self.check_json() == 0:
                    if self.all_except(line_num):
                        continue

                # only.conf condition
                elif self.check_json() == 1:
                    if not self.only(line_num):
                        continue

                updated_line = line
                matches=list(re.finditer(arabic_pattern,line))   # check if pattern can applie on the line

                for match in reversed(matches): # start from the end to not destroy the spaces and postion
                    content=match.group(0)

                    if any('\u0600' <= c <= '\u06FF' or '\uFE70' <= c <= '\uFEFF' for c in content):    # to catch only arabic letters
                        reversed_content=content[::-1] 

                        start,end=match.span()
                        updated_line=updated_line[:start]+reversed_content+updated_line[end:]
                lines[line_num-1]=updated_line
            self.writee(lines)
                    #print(updated_line)
                    #print(f"num={num_of_word} list={len(list_of_words)}")
                    #print(f"start={start} end={end}")
                    #print(f"{line_num}-{updated_line}")
                    #print(f"{word[::-1]} {line_num}")                     
        else:
            print(f"{self.filename} not found or not in a directory!")

    def writee(self,lines,):    # to overwrite the file with only the updated arabic
        if os.path.exists(self.filename):
            with open(self.filename,"w",encoding="utf-8") as f:
                for i in range(len(lines)):
                    f.write(lines[i])
        else:
            print(f"{self.filename} not found!")
        
    def check_json(self):               # still not available this idea is to leet the script be smarter
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

    def all_except(self,line_number): # still under devoloping |||||||||
        list_of_numbers=[]
        with open("all_except.txt",'r') as f:
            for lines in f:
                line=lines
                if line[0]!="#":
                    if line.isdigit():
                        list_of_numbers.append(line)
                        print(list_of_numbers)

        if str(line_number) in list_of_numbers:
            return True
        else:
            return False
        
    def only(self,line_number):
        list_of_numbers=[]
        with open("only.txt",'r') as f:
            for lines in f:
                line=lines
                if line[0]!="#":
                    if line.isdigit():
                        list_of_numbers.append(line)
                        
        if str(line_number) in list_of_numbers:
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
    #xml_file.load_content()
    xml_file.reverse()

#if user_input_match:
  #  for words in user_input_match:
   #     print(f"{words}\n")

    