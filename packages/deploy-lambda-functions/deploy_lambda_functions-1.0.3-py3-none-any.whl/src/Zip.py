import os, shutil

class Zip:
    def __init__(self,name,path):
        self.zip = self.__compress(name,path)

    def get_bytes(self):
        with open(self.zip, 'rb') as file:
            return file.read()
    
    def __compress(self,name,path):
        print("Compressing code dir: {}".format(path))
        format = "zip"
        return shutil.make_archive(name, format, path)
        
