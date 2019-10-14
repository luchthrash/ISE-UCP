# ISE-UCP
This is the collection of files that are necessary to run this implementation of UCP (User Password Change) portal for ISE.
The web-app is written in Python and based on Flask so you'll need to install Python3 and Flask on the server that will host the portal.
The authentication against ISE is done via TACACS so the "tacacs_plus" package is also required. 

Once you have installed all the required packages on your server, you will need to follow this file structure:

/ -> place here "config.py", "forms.py", "ucp-webpage.py"
/templates -> place here ucp-home.html

Don't forget to update "ucp-webpage.py" with your details where indicated by a comment ("#"). 

Before running the app, on the ISE you will to do the following tasks:

1) Create an API admin user with enough privileges to modify passwords for Internal Users 
2) Create a new TACACS network device for the server that hosts the portal using a secret of your choice
3) Create an authorisation rule to allow access for your API admin from the portal server

Once you've completed the setup,  you can start the application by running "python ucp-webpage.py"

