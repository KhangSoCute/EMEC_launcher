# -*- coding: utf-8 -*-

import os
import time
import pathlib
import threading
import pandas
from datetime import datetime, timedelta
from queue import Queue
from utility import SQLUtils, SQLiteUtils, sql_failed
from rotatelogger import RotateLogger

class Processor():
    def __init__(self, name):
        self.basepath = os.path.dirname(__file__)
        self.logger = RotateLogger('Processor',
                                   os.path.join(self.basepath,'plog.txt'),
                                   10000000, 9, 'INFO')
        self.name = name
        self.stop_signal = False
        self.main_processor = None
        self.add_processor = None
        self.save_processor = None
        self.upload_processor = None
        self.inqueue = Queue()
        self.sqlite_conn = SQLiteUtils()
        self.sqlite_filedb_conn = SQLiteUtils(db='file.db3')
        self.dbconn = SQLUtils()
        self.counter = 0
        self.save_queue = Queue()
        self.cleanup_processor = None
        self.file_dir = r'D:\QC BioRad\Data\DxI'
        
    def timestr(self):
        return datetime.now().strftime('%Y%m%d%H%M%S')

    def time_sql_str(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def add_thread(self):
        counter = 0
        while not self.stop_signal:
            time.sleep(4)
            counter = counter + 1
            if counter == 15:
                counter = 0
                try:
                    flist = os.listdir(self.file_dir)
                    for filename in flist:
                        path = os.path.join(self.file_dir, filename)
                        if os.path.isfile(path):
                            #try move
                            if self.stop_signal:
                                break
                            tempdir = os.path.join(self.file_dir,'Temp')
                            pathlib.Path(tempdir).mkdir(parents=True, exist_ok=True)
                            newpath = os.path.join(tempdir, filename)
                            try:
                                os.rename(path, newpath)
                            except Exception:
                                pass
                            else:
                                intime = self.time_sql_str()
                                if not self.sqlite_filedb_conn.commit('''INSERT INTO file
                                          (file_name, intime)
                                          VALUES ( ?,? )''', newpath, intime ):
                                    time.sleep(5)
                                    self.sqlite_filedb_conn.commit('''INSERT INTO file
                                          (file_name, intime)
                                          VALUES ( ?,? )''', newpath, intime )
                except Exception:
                    self.logger.exception('File acquisition module: ')
                    
    
    def save_thread(self):
        self.logger.info('Processor module: save thread start')
        while not self.stop_signal:
            if self.save_queue.empty():
                time.sleep(5)
            else:
                try:
                    time.sleep(1)
                    data = self.save_queue.get()
                    intime = self.time_sql_str()
                    if self.sqlite_conn.commit('''INSERT INTO qcdata
                                          (message, intime)
                                          VALUES ( ?,? )''', data, intime ):
                        self.logger.info('Save: ' + intime)
                    else:
                        self.logger.error('Save failed:' + repr(data))
                        self.upload_queue.put(data)
                except Exception:
                    self.logger.exception('Save thread:')

    def process_thread(self):
        self.logger.info('Processor module: process thread start')
        counter = 40
        buffer = b''
        while not self.stop_signal:
            time.sleep(4)
            counter = counter + 1
            if counter == 48:
                counter = 0
                try:
                    val = self.sqlite_filedb_conn.fetch_all(
                        '''select  id, file_name from file order by file_name asc limit 10''', Config.INST)
                    tid = 0
                    if not val is sql_failed:
                        if len(val) > 0:
                            for tid, data in val:
                                file = pandas.read_table(iofile, encoding='latin-1', sep=';')
                                data = file[(file['Function']=='IRP_MJ_READ') & (file['Direction']=='UP') &(file['Data length']!='NaN')]
                                data = data.loc[:,['Data']]
                                for row in data.itertuples():
                                    self.buffer = self.buffer + bytes.fromhex(str(row[1]))                                
                                self.sqlite_filedb_conn.commit(
                                    '''update file set processed = 1 where id=?''', tid)

                            self.logger.info('Last id: ' +str(tid) )
                            #split file
                            start = b'\x021H|\\^&'
                            end = b'L|1|F\x0d\x03'
                            count = len(buffer.split(start))-1
                            self.logger.debug("Buffer length: "+ str(len(buffer)))
                            self.logger.debug("1H Count: "+ str(count))
                            for __ in range(0, count):
                                loc_start = buffer.find(start)
                                if loc_start >=0:
                                    buffer = buffer[loc_start:]
                                    #self.logger.info('Buffer: ' + repr(self.buffer))
                                    loc_start = 0
                                    loc_end = buffer.find(end)
                                    if loc_end > loc_start:
                                        data = buffer[loc_start:loc_end+5]
                                        self.logger.debug('Data: ' + repr(data))
                                        buffer = buffer[loc_end+5:]
                                        self.save_queue.put(data)
                                else:
                                    buffer = b''
                except Exception:
                    self.logger.exception('Process thread: ')

    def upload_thread(self):
        self.logger.info('Processor module: upload thread start')
        counter = 110
        while not self.stop_signal:
            counter +=1
            time.sleep(5)
            if counter > 120:
                counter = 0
                try:
                    result = self.sqlite_conn.fetch_all('''select id, message from qcdata
                                                        where upload=?''',0)
                    if result is not sql_failed:
                        for id, message in result:
                            self.logger.info('Uploading: '+ repr(message))
                            success = self.dbconn.commit('''insert into QCRawData (name,data)
                                                        values (?,?)''',  self.name, message.decode())
                            if success:
                                self.sqlite_conn.commit('''update qcdata 
                                                set upload=? where id=?''',1,id)
                                self.logger.info('Upload: id = ' + str(id))
                except Exception:
                    self.logger.exception('Upload thread: ')
    
    def cleanup_thread(self):
        counter = 1555190
        while not self.stop_signal:
            counter = counter + 1
            time.sleep(5)
            if counter > 1555200:
                counter = 0
                self.sqlite_conn.commit('''delete from qcdata where upload=? and intime <?''', 
                                        ((datetime.today() - timedelta(90)).strftime('%Y-%m-%d'),))

    
    def run(self):
        self.logger.info('Processor start')
        self.main_processor.start()
        self.save_processor.start()
        self.upload_processor.start()
        self.cleanup_processor.start()
        self.add_processor.start()
    
    def start(self):
        self.add_processor = threading.Thread(target=self.add_thread)
        self.cleanup_processor = threading.Thread(target=self.cleanup_thread)
        self.main_processor = threading.Thread(target=self.process_thread)
        self.save_processor = threading.Thread(target=self.save_thread)
        self.upload_processor = threading.Thread(target=self.upload_thread)

    
    def stop(self):
        try:
            self.stop_signal = True
            self.main_processor.join()
            self.save_processor.join()
            self.upload_processor.join()
            self.cleanup_processor.join()
            self.add_processor.join()
            self.logger.info('Processor module: stop')
        except Exception:
            self.logger.exception('Processor module: ')
