import argparse
import sys
import s3copy
import os
import json


parser = argparse.ArgumentParser(
            description='Copy the files from Local machine to S3 bucket')

parser.add_argument( 
        '-c', '--config', 
        help='Config file for the application',
        default='s3copy.config.json') 

parser.add_argument( 
        '-v', '--version', 
        help='prints the version',
        default=False,
        action='store_true')


def main(args):

    if args.version :
        print "Version 1.0"
        sys.exit(0)

    json_data=None
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),args.config),'r') as f:
            json_data=json.loads(f.read())
            obj = s3copy.S3Copy(json_data)
            obj.process(25)

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)


