import os
import shutil
import sys
import json
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import io
import re
import threading
import logging
from datetime import datetime
from logger import RotateLogger
from utils import save_registry_int,save_registry_string,load_registry

class IMMUNLITE(win32serviceutil.ServiceFramework):

    _base_ = os.path.dirname(__file__)
    _svc_name_ = "IMMUNLITE"
    _svc_display_name_ = "IMMUNLITE"
    _svc_description_ = "READ txt , READ update and CUT marker"

    def __init__(self, args):
        #TODO: Add more Log for monitoring
        self.log = RotateLogger(name=self._svc_name_,fpath=os.path.join(self._base_,"log.log"),bk_count=9,level=logging.WARNING)
        self.log.info("START!")
        try:
            with open(os.path.join(self._base_,"config.json")) as f:
                self.config = json.load(f)
        except Exception as e:
            self.log.error(f"Error loading JSON file: {e}")
            self.SvcStop()
        # TODO: CHECK config HERE
        self.path_txt = self.config["PATH_TXT_IN"]
        if not os.path.exists(self.path_txt):
            self.log.error(f"{self.path_txt} is not exist")
            self.SvcStop()
            
        else:
            self.log.info(f"{self.path_txt} is exist")

        self.folder_out = self.config["PATH_FOLDER_OUT"]
        if not os.path.exists(self.folder_out):
            self.log.warning(f"{self.folder_out} does not exist. Creating folder...")
            os.makedirs(self.folder_out)
        else:
            self.log.info(f"{self.folder_out} is exist, check it!")

        self.stop_cd = True
        self.stop_sig = True
        self.stop_event = threading.Event()

        #Load regedit
        try:
            self.count = load_registry("FILE_COUNT_EXPORT")
            if self.count is None:
                self.log.warning(f"Not find: FILE_COUNT_EXPORT, so count = 0")
                save_registry_int(0,"FILE_COUNT_EXPORT")
        except Exception as e:
            self.log.error(f"Error loading REGEDIT file: {e}")
            self.SvcStop()

        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    
    def SvcStop(self):
        servicemanager.LogInfoMsg("STOPED SERVICE!")
        
        #TODO: CREATE TEMP IF STOP,SAVE CONTENT AND DATE IF IN DATE THEN LOAD IT
        if hasattr(self, 'new_contents'):
            with open(os.path.join(self._base_,'temp.txt'), 'w') as f:
                f.write(self.new_contents)

        if hasattr(self, 'count'):
            self.log.info(f"SAVE COUNT FILE: {self.count}")
            save_registry_int(self.count,"FILE_COUNT_EXPORT")

        self.log.info("STOP!")
        self.stop_cd = False
        self.stop_sig = False
        try:
            if hasattr(self, 'realtime_thread'):
                self.log.info("CLOSE thread!")
                self.stop_event.set()
                if self.realtime_thread.is_alive():
                    self.realtime_thread.join()
            else:
                pass
        except Exception as e:
            self.log.warning(f"Error close thread: {e}")
            pass
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
    
    def SvcShutdown(self):
        servicemanager.LogInfoMsg("STOPED SERVICE!")
        if hasattr(self, 'new_contents'):
            with open(os.path.join(self._base_,'temp.txt'), 'w') as f:
                f.write(self.new_contents)
        
        if hasattr(self, 'count'):
            self.log.info(f"SAVE COUNT FILE: {self.count}")
            save_registry_int(self.count,"FILE_COUNT_EXPORT")

        self.log.info("SHUTDOWN!")
        self.stop_cd = False
        self.stop_sig = False
        
        try:
            if hasattr(self, 'realtime_thread'):
                self.log.info("CLOSE thread!")
                self.stop_event.set()
                if self.realtime_thread.is_alive():
                    self.realtime_thread.join()
            else:
                pass
        except Exception as e:
            self.log.warning(f"Error close thread: {e}")
            pass
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        # self.read_and_write_file()
        self.check_folder()
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def check_folder(self):
        previous_value = None
        self.log.info("REALTIME GO!")
        while self.stop_sig:
            time.sleep(2)
            now = datetime.now()
            formatted_date = now.strftime("%d-%m-%Y")

            if self.count > 10000:
                self.log.info("COUNT = 10000, reset COUNT=0!!!!!!!!!")
                self.count = 0

            if os.path.exists(os.path.join(self.path_txt,formatted_date)):
                #####
                # START new day
                if previous_value != formatted_date:
                    self.log.info(f"EXIST FOLDER: {os.path.join(self.path_txt,formatted_date)}")
                    self.log.info("CHECKING... TXT IN IT")
                    previous_value = formatted_date
                    try:
                        if hasattr(self, 'realtime_thread'):
                            current_thread = threading.current_thread()
                            self.log.info(f"DELETE thread: {current_thread}")
                            self.stop_event.set()
                            self.realtime_thread.join(5)
                            self.stop_event.clear()
                        else:
                            pass
                    except Exception as e:
                        self.log.error(f"Error check thread: {e}")
                        self.SvcStop()
                        pass
                    # Alway delete at first time, need more condition
                    try:
                        if hasattr(self, 'new_contents'):
                            if os.path.exists(os.path.join(self._base_,'temp.txt')):
                                self.log.info("DECTECT temp file: DELETED IT!!!")
                                os.remove(os.path.join(self._base_,'temp.txt'))
                            else:
                                os.log.info("NOT DECTECT temp file: DELETED IT!!!")
                                self.SvcStop()

                    except Exception as e:
                        self.log.error(f"Something wrong detect Temp file: {e}")
                        pass
                    flag = False
                    while not flag:
                        time.sleep(1)
                        for file in os.listdir(os.path.join(self.path_txt,formatted_date)):
                            if file.endswith(".txt"):
                                self.log.info(f"EXIST .txt file {file}. READ IT")
                                self.realtime_thread = threading.Thread(target = lambda: self.read_and_write_file(os.path.join(os.path.join(self.path_txt,formatted_date),file)))
                                self.realtime_thread.start()
                                flag = True
                                break
                pass
            else:
                pass

    def delete_before_AM_PM(self,txt):
        index = txt.find('AM') if txt.find('AM') != -1 else txt.find('PM')
        if index != -1:
            txt = txt[index:]
        return txt
                    
    def read_and_write_file(self,path_txt):
        self.log.info("CHECK FILE PHASE!")
        try:
            if os.path.exists(os.path.join(self._base_,'temp.txt')):
                with open(self.path_txt, 'r') as f:
                    contents = f.read()
                os.remove(os.path.join(self._base_,'temp.txt'))
            else:
                contents = ''
        except Exception as e:
            self.log.error(f"ERROR input Temp file: {e}")
            # contents = ''
            self.SvcStop()
            
        temp = []
        mode = False

        while not self.stop_event.is_set():
            time.sleep(1) 

            with open(path_txt, 'r') as file:
                self.new_contents = file.read()

            if self.new_contents != contents:
                self.log.info("UPDATING.....")
                text = self.new_contents.replace(contents, '')
                contents = self.new_contents
                content_list = text.split('\n')
                self.log.info(f"LIST new content: {content_list}")
                true_content_list = [self.delete_before_AM_PM(item)[9:] for item in content_list]
                filter_content_list = list(filter(None, true_content_list))
                filter_upcase_list = [item for item in filter_content_list if item[0].isupper()]
                self.log.info(f"AFTER filter: {filter_upcase_list}")
                for item in filter_upcase_list:
                    
                    #Something wrong when START_MARK occur 2 times??
                    if self.config["START_MARK"] in item:
                        # self.log.info(f"GET start mark in: {item}")
                        if mode:
                            self.log.warning(f"OCCUR: 2 times START_MARK continouly")
                            temp = []
                        else:
                            mode = True
                        time.sleep(0.0005)

                    if mode:
                        temp.append(item)

                    if (self.config["END_MARK"] in item) and (mode == True):
                        self.log.info(f"NEW DATA: {temp}")
                        time.sleep(0.0005)
                        mode = False
                        try:
                            with open(os.path.join(self.folder_out,f'{self.count}.txt'), 'w') as outfile:
                                outfile.write('\n'.join(temp))
                            self.log.info(f"EXPORT to: {os.path.join(self.folder_out,f'{self.count}.txt')}")
                            self.count+=1
                            time.sleep(1)
                        except Exception as e:
                            self.log.error(f"Something wrong when export txt: {e}")
                            pass
                        temp = []

#TODO: NEED THREAD CHECK FILE OUTPUT
if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(IMMUNLITE)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(IMMUNLITE)

# try:
    #         text = self.new_contents.replace(contents, '')
        # except Exception as e:
        #     tb = traceback.format_exc()
        #     self.log.error(f"Error occurred in file {__file__}, line {tb.tb_lineno}: {e}")
