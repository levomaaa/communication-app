# Communication application

The application shows discussion forums, each of which has a specific topic. The forums contain different discussion threads where users can send messages. Every user is either a regular user or an administrator.

## Features of the application:

* User can log in and out and create a new account.
* On the front page of the app, the user sees a list of discussion forums, the number of threads in each forum and the name of the forum creator.
* On the thread page, the user can see the number of messages in each thread, the creator, and the date of the last message sent.
* The user can create new forums, threads and messages.
* The user can write make a new thread to an existing forum and a new message in an existing thread.
* The user can edit the title of the (forum, thread) he/she has created, as well as the content of the message he/she has sent. The user can also delete the (forum, thread) or message he/she has created.
* The administrator can add and remove forums, threads and messages.
* The administrators can communicate with other administrators in their own administrators page which only they can see.
* The administrators page has topics and messages in them.
* The administrator can make other users as administrators.

* The product can only be tested locally.

## Startup instructions:

Clone this repository on your own computer and go to its root folder. Create a .env file in the folder and specify its contents as follows:
* DATABASE_URL="datadase-local-address"
* SECRET_KEY="secret-key"

Next, activate the virtual environment and install the application dependencies with commands:
* python3 -m venv venv
* source venv/bin/activate
* pip install -r ./requirements.txt

Next start the database and configure the database schema with the command:
* psql < schema.sql

Now you can start the application with command:
* flask run
