import datetime
from time import gmtime, strftime
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

class write_file:
    """ Writes logs to a file """
    def __init__(self, name_environ="logs", name_file="logs.txt"):
        self.environ = name_environ
        self.file = open(name_file, 'a')
        date = str(datetime.datetime.now())
    def error(self, message):
        date = str(datetime.datetime.now())
        self.file.write('ERROR [%s]: %s: %s'% (date, self.environ, message))
    def info(self, message):
        date = str(datetime.datetime.now())
        self.file.write('INFO [%s]: %s: %s'% (date, self.environ, message))
    def warning(self, message):
        date = str(datetime.datetime.now())
        self.file.write('WARNING [%s]: %s: %s'% (date, self.environ, message))
    def valid(self, message):
        date = str(datetime.datetime.now())
        self.file.write('VALID [%s]: %s: %s'% (date, self.environ, message))
class simple_log:
    def __init__(self, name_environ="logs"):
        self.environ = name_environ
    def error(self, message):
       
        print(" [ERROR] %s: %s"% (date, self.environ, message))
    def info(self, message):
   
        print(" [INFO] %s: %s"% (date, self.environ, message))
    def warning(self, message):
       
        print(" [WARNING] %s: %s"% (date, self.environ, message))
    def valid(self, message):
     
        print(" [VALID] %s: %s"% (date, self.environ, message))
    
class color_log:
    """ Displays simple and colorful newspapers on screen """
    def __init__(self, name_environ="logs"):
        self.environ = name_environ
    def error(self, message):
       
        print("%s [ERROR] %s: %s %s"% (FAIL, self.environ, message, ENDC))
    def info(self, message):
       
        print("%s [INFO] %s: %s %s"% (OKBLUE, self.environ, message, ENDC))
    def warning(self, message):
       
        print("%s [WARNING] %s: %s %s"% (WARNING,  self.environ, message, ENDC))
    def valid(self, message):
    
        print("%s [VALID] %s: %s %s"% (OKGREEN,  self.environ, message, ENDC))
    def ask(self, message):
     
        return input("%s[VALID] %s: %s %s"% (OKGREEN,  self.environ, message, ENDC))
    
class sign_log:
    """ View advanced logs """
    def __init__(self, name_environ="logs"):
        self.environ = name_environ
    def error(self, message):
     
        print(" [x] %s: %s "% (self.environ, message))
    def info(self, message):
     
        print(" [*] %s: %s "% (self.environ, message))
    def warning(self, message):
       
        print(" [!] %s: %s "% (self.environ, message))
    def valid(self, message):
     
        print(" [*] %s: %s %s"% (self.environ, message))
    def ask(self, message):
      
        return input("[?] %s: %s"% (self.environ, message))
    
class sign_color_log:
    """ Displays advanced and colorful logs """
  
    def __init__(self, name_environ="logs"):
        self.environ = name_environ
    def error(self, message):
        print(f"{BOLD} {FAIL} [x] {ENDC} {self.environ}: {message}")
    def info(self, message):
        print(f"{BOLD} {OKCYAN} [*] {ENDC} {self.environ}: {message}")
    def warning(self, message):
        print(f"{BOLD} {WARNING} [!] {ENDC} {self.environ}: {message}")
    def valid(self, message):
        print(f"{BOLD} {OKGREEN} [*] {ENDC} {self.environ}: {message}")
    def ask(self, message):      
        return   input(f"{BOLD} {OKBLUE} [?] {ENDC} {self.environ}: {message}: ")
    
