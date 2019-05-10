# NetworkMotifs

the application is run using Flask’s development server (something that would be altered in a final public release). 
With python installed, Flask can be obtained using the PIP python package manager by running the command “ pip install flask” 
(further information can be found at http://flask.pocoo.org/docs/1.0/installation/ ). 
The flask app “app.py” needs to be exported as an environment variable, which in the case of windows powershell can be achieved
by running “$env:FLASK_APP = "app.py", or “export FLASK_APP=app.py” for linux 
(further information can be found a http://flask.pocoo.org/docs/1.0/quickstart/ ).
Running “flask run”, which will begin the initialization. 
Once complete the terminal will give an IP address, at which the application can be accessed using a web browser.
