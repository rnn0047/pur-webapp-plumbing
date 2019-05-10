# flask app using s3 to store files
import boto3
import logging
import os
import uuid
from botocore.exceptions import ClientError
from config import S3_BUCKET, S3_KEY, S3_SECRET, UPLOAD_FOLDER
#from filters import file_type
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap #provides ready css templates
from werkzeug import secure_filename
""" Remaining TODO
    1. A big brother Lambda function to delete all obj older than 12 hours
    2. How can this work without a server?
    3. Decide upload folder on flask server side
    4. Where will file sit for AI model to work on
    5. implement transformPhoto(idkey):
"""

s3_resource = boto3.resource(
        "s3",
        aws_access_key_id = S3_KEY,
        aws_secret_access_key = S3_SECRET
    )

FILENAME_KEYS = ['.photo', '.style']
ALLOWED_EXTENSIONS = set(['png', 'ico', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)
#app.jinja_env.filters['file_type'] = file_type

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/submit", methods=['POST'])
def postFiles():
    if 'styleFile' not in request.files and 'photoFile' not in request.files:
        return "No file key's present for upload in request.files"
    style = request.files['styleFile']
    photo = request.files['photoFile']
    if (style.filename != None and len(style.filename) > 2) and \
       (photo.filename != None and len(photo.filename) > 2) :
        hexkey = uuid.uuid1().hex
        s3_client = boto3.client('s3')
        for fkey in FILENAME_KEYS:
            #anonymize file in s3
            fkey1 = fkey.split('.')[1]
            fileObj = eval(fkey1)
            if allowed_file(fileObj.filename):
                filename = secure_filename(fileObj.filename)
                fileWPath = os.path.join(UPLOAD_FOLDER, filename)
                fileObj.save(fileWPath)
                objName    = hexkey + fkey
                try:
                    resp = s3_client.upload_file(
                            fileWPath, S3_BUCKET, objName)
                except ClientError as e:
                    logging.error(e)
                    return ("Couldn't upload to S3 - src:{} tar:{}".format(fileWPath,objName))
            else:
                logging.info("File {} not acceptable".format(fileObj.filename))
        return hexkey
    else:
        print("Check files selection - upload cancelled")
        return redirect("/")

@app.route("/xForm/<idkey>")
def transformPhoto(idkey):
    """
    input: idkey - hexuuid of the user

    Processing: Can this be all LAMBDA?
    1. from S3 should read photo and style
    2. do AI assisted xform of the photo
    3. store transformed image to S3

    returns:
    file descriptor from S3 bucket
    """
    return "####TODO### - transformPhoto() Not Fully Implemented"
    s3 = boto3.client('s3')
    for fkey in FILENAME_KEYS:
        try:
            key     = idkey + fkey
            outFile = os.path.join(UPLOAD_FOLDER, key)
            with open (outFile, 'wb') as f:
                s3.download_fileobj(S3_BUCKET, outFile, f)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                print ("Key: {} object doesn't exist".format(key))
            else:
                raise #some exception to be added later
        #call delegate class to do AI XFORM
        #cleanFiles(idkey)


@app.route("/CleanS3Bucket/<idkey>") #also called directly as above
def cleanFiles(idkey):
    """
    Utility function to wipe out content of the S3 bucket
    """
    for fkey in FILENAME_KEYS:
        key     = idkey + fkey
        s3_resource.Object(S3_BUCKET, key).delete()
    return "all files associated with key {} deleted"

@app.route("/listFiles")
def listFiles():
    """
    Utility function to check content of the S3
    """
    s3_resource = boto3.resource('s3')
    my_bucket   = s3_resource.Bucket(S3_BUCKET)
    summaries   = my_bucket.objects.all()
    return render_template('listFiles.html', my_bucket=my_bucket,
            files=summaries)

if __name__ == "__main__":
    app.run()

