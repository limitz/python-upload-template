#!/usr/bin/python3
import os
import time

import logging
import logging.handlers
from asyncio import Queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AFUploader(FileSystemEventHandler):

    log = None
    observer = None
    queue = None
    uploadDirectory = ''
    logDirectory = ''
    logBackup = 10
    logPath = ''

    #increate logMaxSize for production
    #logMaxSize = 10*1024*1024
    logMaxSize = 10*1024
    

    def __init__(self, uploadDirectory, logDirectory):
        self.uploadDirectory = uploadDirectory
        self.logDirectory = logDirectory
        self.logPath = os.path.join(self.logDirectory, 'autofill-upload.log')

        if not os.path.exists(self.uploadDirectory):
            os.mkdir(self.uploadDirectory)

        if not os.path.exists(self.logDirectory):
            os.mkdir(self.logDirectory)
        
        logFormatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

        self.log = logging.getLogger('autofill_upload')
        self.log.setLevel(logging.DEBUG)
        
        fileHandler = logging.handlers.RotatingFileHandler(
                self.logPath, 
                maxBytes = self.logMaxSize, #increase this value, just low for testing
                backupCount = self.logBackup)
        fileHandler.setFormatter(logFormatter)

        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(logFormatter)

        self.log.addHandler(fileHandler)
        self.log.addHandler(streamHandler)
   
        self.queue = Queue() 
        self.observer = Observer();
        self.observer.schedule(self, self.uploadDirectory, recursive=True);
        
        self.log.debug('Upload service initialized')


    def start(self):
        
        self.log.info('Starting autofill upload service')
        self.log.info('Upload directory: %s', self.uploadDirectory) 
        self.log.info('Log file: %s', self.logPath)
       
        #process files that are already in the upload dir
        #the capture service may be running while the upload service is down
        for f in os.listdir(self.uploadDirectory):
            fullPath = os.path.join(self.uploadDirectory, f)
            if (os.path.isfile(fullPath)):
                self.log.info('Preexisting file detected: %s', fullPath)
                self.queue.put_nowait(fullPath)
        
        self.observer.start();
        self.log.debug('Observer started')


    def stop(self):
        self.log.info('Stopping autofill upload service')
        
        self.observer.stop()
        self.log.debug('Observer stopped')
        
        self.observer.join()
        self.log.debug('Observer joined')

        self.queue.join()
        self.log.debug('Queue joined') 
        self.log.info('Stopped autofill upload service')


    def on_created(self, event):
        if event.is_directory: 
            self.log.warn('Unexpected creation of directory in upload path %s', self.uploadDirectory)
            return

        self.log.info('File detected: %s', event.src_path)
        self.queue.put_nowait(event.src_path)


    def process(self):        
        if (self.queue.empty()):
            time.sleep(1)
            return

        path = self.queue.get_nowait()
        if os.path.exists(path):
            self.log.info('Uploading file: %s', path)
               
            #placeholder for upload of file
            time.sleep(30)

            self.log.info('Done. Uploaded file: %s', path)
            os.remove(path);

if __name__ == '__main__':

    uploadDirectory = os.path.join(os.getcwd(), 'upload')
    logDirectory = os.path.join(os.getcwd(), 'log')

    uploader = AFUploader(uploadDirectory, logDirectory)
    
    try:
        uploader.start()
        while (True):
            uploader.process()

    finally:
        uploader.stop()
    
