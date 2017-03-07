from os import listdir
from os.path import isfile,join
import boto
import re
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import gzip
import shutil



class S3Copy(object):

    def __init__(self, json_data= None):
        self.json_data = json_data
        self.conn = boto.connect_s3() 
   
    def process(self):

        for config in self.json_data['configelem']:
            orig=config['orig']
            p=re.compile(config['filter'])
            filestocopy=[orig + "/" + f for f in listdir(orig) if isfile(join(orig,f)) and p.match(f) is not None ]
            bucket=self.conn.get_bucket(config['dest'].split('//')[1].rstrip('/'))
            self.copy_filestos3(filestocopy,bucket,config['key'],config['compression'])


        
    
    def copy_filestos3(self,filestocopy=None,bucket=None,keyname=None,compression = None):

        for filename in filestocopy: 

            key=Key(bucket)
            for fname in filename.split('/'): 
                pass
            keyname +=("/" + fname)
        
            if(compression is not None and compression =='.gz'): 
                with open(filename, 'rb') as f_in, gzip.open(filename+'.gz', 'wb') as f_out: 
                    shutil.copyfileobj(f_in, f_out)
                    filename+='.gz'
                    keyname +='.gz'

            key.key=keyname 
            with open(filename,'rb') as f:
                    key.set_contents_from_file(f)
                    f.close()







        

