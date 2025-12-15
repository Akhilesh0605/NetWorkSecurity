import sys
from networksecurity.logging.logger import logging
class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()

        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occured in script: {self.file_name} at line number: {self.lineno} with message: {self.error_message}"
        self.file_name,self.lineno,self.error_message

if __name__=="__main__":
    try:
        
        a=1/0
    except Exception as e:
        raise NetworkSecurityException(e,sys)