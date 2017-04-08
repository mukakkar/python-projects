import tornado
import json
from  tornado.web import RequestHandler
from tornado.ioloop import IOLoop
from sprockets.clients import dynamodb



class DynamodbHandler(RequestHandler):

    def initialize(self, db):
        self._db = db


    @tornado.gen.coroutine
    def get(self,userid):

        if isinstance(userid,unicode):
            userid = userid.encode('ascii')

        dct={"userId": userid }
        response = yield self._db.get_item('user',dct)
        self.write(response)
        self.finish()
            

def main():

    io_loop = IOLoop.instance()
    dynamo = dynamodb.DynamoDB()
    app_routes = [ 
            (r"/user/([^/]+)",DynamodbHandler,dict(db=dynamo)),
            ]

    app = tornado.web.Application(app_routes)
    app.io_loop = io_loop
    app.listen(8080)
    io_loop.start()


if __name__ == "__main__":
    main()
