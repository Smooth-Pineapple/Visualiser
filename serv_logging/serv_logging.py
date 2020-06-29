import sys
import os
import os.path

import datetime

class Logging:
    __instance = None
    __log_file = None

    __path_str = None

    DEB = ("Debug", 0)
    INF = ("Info", 1)
    WAR = ("Warning", 2)
    ERR = ("Error", 3)

    def __init__(self, level):
        self.__level = level
        if Logging.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Logging.__instance = self

    @staticmethod 
    def getInstance(level):
        if Logging.__instance == None:
            Logging(level)
        return Logging.__instance

    def open(self, path_str):
        self.__path_str = path_str

        self.fileSizeCheck()

        self.__log_file = open(self.__path_str , 'a+')

    def write(self, level, message):
        if self.__log_file is not None:
            new_file = self.fileSizeCheck()
            if new_file:
                self.__log_file = open(self.__path_str, 'a+')

            now = datetime.datetime.now()

            if level[1] >= self.__level[1]:
                self.__log_file.write(level[0] + " " + now.strftime("[%Y-%m-%d %H:%M:%S] ") + sys._getframe(1).f_code.co_name + ": " + message + "\n")
                self.__log_file.flush()
        else:
            raise Exception("Log file is not open for message: " + message)
        
    def read(self):
        if self.__log_file is not None:
            with(open(self.__path_str, 'r')) as file:
                return file.read().splitlines()
        else:
            raise Exception("Log file is not open for read")

    def close(self):
        if self.__log_file is not None:
            self.__log_file.close()
            self.__log_file = None

    def fileSizeCheck(self):
        if os.path.isfile(self.__path_str):
            file_size_b = os.stat(self.__path_str).st_size
            if file_size_b > 5242880: #5mb
                self.close()

                f = open(self.__path_str, 'w')
                f.close()

                return True
        
        return False        