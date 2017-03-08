from os import listdir
from os.path import isfile,join
import boto
import re
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import gzip
import shutil
from threading import Thread
from Queue import Queue
from time import sleep

class Worker(Thread):

        def __init__(self,tq): 
            Thread.__init__(self) 
            self.tq = tq 
            self.daemon = True 
            self.start() 
        
        def run(self): 
            while True: 

                func,args= self.tq.get() 
                try: 
                    func(*args) 
                except Exception, e: 
                    print e 
                        
                self.tq.task_done() 


class S3Copy(object):

    def __init__(self, json_data= None):
        self.json_data = json_data
        self.conn = boto.connect_s3() 
        self.taskq = Queue()
        """ 5 thread pool elements  to process the copying tasks """
        for _ in range(5):
            Worker(self.taskq)
   
    def process(self,stime): 
        
        def copy_filestos3(filestocopy=None,bucket=None,keyname=None,compression = None): 
            
            for filename in filestocopy: 

                key=Key(bucket) 
                for fname in filename.split('/'): 
                    pass 

                key_name = keyname + "/" + fname 
                
                if(compression is not None and compression =='.gz'): 
                    with open(filename, 'rb') as f_in, gzip.open(filename+'.gz', 'wb') as f_out: 
                        shutil.copyfileobj(f_in, f_out) 
                        filename+='.gz' 
                        key_name +='.gz' 
                
                key.key=key_name 

                with open(filename,'rb') as f: 
                    key.set_contents_from_file(f) 

        
        while True:

            for config in self.json_data['configelem']:

                orig=config['orig'] 
                p=re.compile(config['filter'])
                filestocopy=[orig + "/" + f for f in listdir(orig) if isfile(join(orig,f)) and p.match(f) is not None ]
                bucket=self.conn.get_bucket(config['dest'].split('//')[1].rstrip('/'))
                taskt=(copy_filestos3,(filestocopy,bucket,config['key'],config['compression']))
                self.taskq.put(taskt) 

            self.taskq.join()
            print "Sleeping for {} seconds".format(stime)
            sleep(stime)
            
