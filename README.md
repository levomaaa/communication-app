# Communication application

The application shows discussion forums, each of which has a specific topic. The forums contain different discussion threads where users can send messages. Every user is either a regular user or an administrator.

## Features of the application:

* User can log in and out and create a new account.
* On the front page of the app, the user sees a list of discussion forums, the number of threads and messages in each forum, and the date of the last message sent.
* The user can create a new chain in the area by entering the title of the chain and the content of the start message.
* The user can write a new message in an existing chain.
* The user can edit the title of the chain he/she has created, as well as the content of the message he/she has sent. The user can also delete the chain or message.
* The user can search for all messages that are part of a given word.
* The administrator can add and remove discussion areas.
* The administrator can create a secret area and determine which users have access to the area.

## Present situation:

* User can log in and out and create a new account.
* The username is unique and no one can have the same as you.
* The user sees forums while logged in. You can't see them if you aren't logged in.
* Users can create new forums and see who has created the already existing ones.
* The layout has been modified to be a bit prettier and more practical.
* For now, the product can only be tested locally, but hopefully also online in the future.

## Startup instructions:

Clone this repository on your own computer and go to its root folder. Create a .env file in the folder and specify its contents as follows:
* DATABASE_URL="datadase-local-address"
* SECRET_KEY="secret-key"

Next, activate the virtual environment and install the application dependencies with commands:
* python3 -m venv venv
* source venv/bin/activate
* pip install flask
* pip install flask-sqlalchemy
* pip install psycopg2

Next start the database and configure the database schema with the command:
* psql < schema.sql

If "pip install psycopg2" failed the previous try, try it again now.

Now you can start the application with command:
* flask run
