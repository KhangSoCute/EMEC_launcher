# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Service Gen 1
Recon
"""
import json
import os
import socket
import sys
import time
import subprocess
import threading
import servicemanager
import win32event
import win32service
import win32serviceutil

from rotatelogger import RotateLogger
from processor import Processor


class Service(win32serviceutil.ServiceFramework):
    base = os.path.dirname(__file__)
    _svc_name_ = "Cobas_36"
    _svc_display_name_ = 'Windows Service - Cobas'
    _svc_description_ = 'Windows Service - Cobas'

    def __init__(self, args):
        self.logger = RotateLogger(self._svc_name_,
                                   os.path.join(self.base, 'svlog.txt'),
                                   10000000, 9, level='INFO')
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_alive = False
        self.processor = Processor("Cobas_36")
        
    def stop(self):
        self.processor.stop()

    def start(self):
        self.processor.start()

    def main(self):
        self.processor.run()

    def SvcStop(self):
        self.is_alive = False
        self.stop()
        self.notify_thread.join()
        self.logger.info("Service stop")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcShutdown(self):
        self.is_alive = False
        self.stop()
        self.notify_thread.join()
        self.logger.info("Service stop")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.is_alive = True
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.logger.info("Service start")
        self.main()
        while self.is_alive:
            time.sleep(5)

			
if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(Service)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(Service)
