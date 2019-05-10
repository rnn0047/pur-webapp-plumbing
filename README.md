### Flask based WebApp to meet Princeton Unv Reunion Project

This code covers the basic framework of marshalling AWS resources and hosting the WebApp on AWS.

The code will evolve into full scale web app in future with addition of Scaling, Load Balancer, Lambda functions and finetuned front end usign vue/node.js

Quick start instructions
-------------------------
Clone this repo to your local machine. In the top level directory, create a virtual environment:
```
$ virtualenv venv
OR
$ python3 -m venv (as i used python3)

$ source venv/bin/activate
```
Now install the required modules:
```
$ pip install -r requirements.txt
```
CHECK THE CONFIGURATION FILE .env if you want to use your own AWS account
To play with the app right away, run following commands
```
$ export FLASK_APP=app.py
$ export FLASK_DEBUG=1
flask run
And point your browser to http://localhost:5000
```
NOTE:
In order to meet the AWS Free Usage Tier, we need to adhere to following - 
1. Keep storage under 5GB
2. Keep Get Requests to 20,000 
3. Keep Put Requests to 2,000 and
4. 15GB of data transfer each month of one year
```
so please update .env files with your accesskey(S3_KEY), secretkey and bucket details
```

