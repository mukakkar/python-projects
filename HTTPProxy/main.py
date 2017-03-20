import os
import socket
import SocketServer
import json
import urllib
import logging
import logging.config

logger = None 
config={}


class MyTCPHandler(SocketServer.BaseRequestHandler):


    def handle(self):

        buf=self.get_buffer(self.request)

        """read the first 2 line to decode the host parameters """

        idx=buf.find(b"\r\n")
        if( idx < 0):
            logger.error("Couldn't decode http request {}".format(buf))
            self.request.sendall(buf)
            return

        http_request_first= buf[ :idx]
        idx2=buf.find(b"\r\n",idx +2)

        if( idx2 <0 or idx2 > len(buf)):
            logger.error("Couldn't decode http request {}".format(buf))
            self.request.sendall(buf)
            return


        http_request_second= buf[(idx+2) : idx2]
        logger.debug("idx,idx2 = {},{}".format(idx,idx2))
        

        url=http_request_first.split(' ')[1]
        hostport = http_request_second.split(' ')[1]

        """Open a new socket 

        1. send the buffered contnents to remote server
        2. Wait for Reply and send back the contents to the original server 

        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remoteip=socket.gethostbyname(config[hostport].split(':')[0])
        remoteport=config[hostport].split(':')[1]

        try:
            logger.debug("Proxying the http request to {}:{}".format(remoteip,remoteport))
            s.connect((remoteip,int(remoteport)))
            s.sendall(buf)
            buf=self.get_buffer(s)
            self.request.sendall(buf)

        except Exception as e:
            logger.error("something went wrong {}".format(repr(e)))
            self.request.sendall(buf)
            s.close() 



    """ get the http buffer """
    def get_buffer(self,s): 

        BUFF_LEN=8192
        MAX_BUFF_SIZE=BUFF_LEN * 10
        lenbuff=0
        buff=b""

        while True:
            data =s.recv(BUFF_LEN)
            buff +=data
            lenbuff +=len(data)
            if(lenbuff > MAX_BUFF_SIZE):
                return b""

            if (data.find(b"\r\n\r\n") > 0 ) :
                logger.debug("Found 2 newlinews http request complete now")
                break 
            
        return buff

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
        pass

def main(): 
    
    global logger,config 

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'hostmap.json'),'r') as f: 
        json_conf=json.loads(f.read())
        for conf in json_conf['hostmapping']:
            config[conf['orig:port']]=conf['dest:port']
    
    logger=logging.getLogger('my_module') 
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'logging.json'),'r') as f: 
        logging.config.dictConfig(json.load(f)) 
    
    HOST, PORT = socket.gethostname(), 8080 
    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler) 
    server.serve_forever()




if __name__ == "__main__":
    main()


