The programe copies the files from a source directory to s3 bucket on aws . I have assumed the ec2 instance is running with a role with 
read and write access to the bucket . That's why no explicit credentials are used while creating the connection .

The configuration file is as below. Add more entries for DIR/BUCKET combination . You can specify filter to copy selecetd files only.

{
"configelem":[
  {"orig":"DIR", "dest":"s3://BUCKET/" , "key":"S3KEY", "compression":".gz" , "filter":"(.*).txt$"}
]
}

I am planning to add multiple filetr options i.e like --include parame in aws cli and <BUCKET/BUCKET> copy in future releases . 
