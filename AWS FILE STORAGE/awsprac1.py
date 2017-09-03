from flask import Flask,render_template,request
import boto3,os,sys
from botocore.client import Config
app = Flask(__name__)


access_key = [ACCESS KEY]
secret_key = [SECRET KEY]

conn = boto3.client('s3',
     aws_access_key_id = access_key,
     aws_secret_access_key = secret_key,
        #host = 'ec2-52-15-83-231.us-east-2.compute.amazonaws.com',
        #is_secure=False,               # uncomment if you are not using ssl
       # calling_format = boto3.s3.connection.OrdinaryCallingFormat(),
     config=Config(signature_version='s3v4'))
#create bucket
conn.create_bucket(Bucket='my-bucketpooja')

# Call S3 to list current buckets
response = conn.list_buckets()

# Get a list of all bucket names from the response
buckets = [bucket['Name'] for bucket in response['Buckets']]

# Print out the bucket list
print("Bucket List: %s" % buckets)

@app.route('/')
def hello_world():
    bucketobj = conn.list_objects(Bucket='buck1pooja')
    for obj in bucketobj['Contents']:
        print (obj)
    return render_template('updown.html', listobj=bucketobj['Contents'])


@app.route('/uploads',methods=['POST'])
def upload():
    
    #list_of_files = request.files.getlist('file')
    file = request.files['file']
    print (file)

    dir_path = os.path.dirname(os.path.realpath(__file__)) + '\uploads'
    path = dir_path + '\\'
    print(path)
    # contenttype = 'text/plain'

    # gpg = gnupg.GPG(gnupghome = os.getcwd() + '/.gnupg')
    # input_data = gpg.gen_key_input(key_type="RSA", key_length=1024, phrases = '')
    # key = gpg.gen_key(input_data)

    #for f in file:
    #print(f)
    filename = file.filename
    filepath = path + filename
    print(filepath)
    conn.upload_file(filepath, 'buck1pooja', filename)
    return '<h1>Upload Successful</h1>'
    # try:
    #     dir_path = os.path.dirname(os.path.realpath(__file__))+'\uploads'
    #     print dir_path
    #     file = request.files['file']
    #     filename = file.filename
    #     path=dir_path+'\\'+filename
    #
    #     print 'filename' + filename
    #     print path
    #     conn.upload_file(path,'buck1pooja', filename)
    #     return 'Uploaded successfully'
    # except:
    #     print (sys.exc_info()[0])



@app.route('/delete',methods=['POST'])
def delFile():
    file=request.form.get('file')
    print file
    conn.delete_object(Bucket='buck1pooja',Key=file)
    return'Deleted successfully'

port = os.getenv('PORT', '8080')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port))

