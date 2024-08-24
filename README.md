### GraphQLAPI_-_Django_connection: Retrieving Data from Django to Vue.js using GraphQL API

NB: You can follow steps in this file to get more knowledge on how to create the project. OR just clone the repository:

    ```bash
    $ git clone https://github.com/BlackCoder56/GraphQLAPI_-_Django_connection.git

## Features
- Django
- Vue.js
- GraphQL API
- GraphiQL

- Create, read, update, and delete operations for entries[employess], cities, and titles.
- Filtering and querying using GraphQL.
- Mutations for managing employees, cities, and titles.
- Django integration with GraphQL using `graphene` and `graphene-django`.


---

## Step 1: Create Project Root Directory
**Preparing project directories**
##    1. Create the project root/main directory:    

       ```bash       
       $ mkdir <dirName>

##    2. Enter the root project directory:

       ```bash       
       $ cd <dirName>

##    3. Create frontend and backend directories:

       ```bash      
        $ mkdir frontend backend

##  Step 2: Setting up the Backend
**Creating the Django Project**
*      -> First navigate to the backend folder:

       ```bash
       $ cd backend

##    1. Install Django:

       ```bash     
       $ pip install django

##    2. Create a virtual environment:

        ```bash
        $ python3 -m venv env##

##    3. Activate the virtual environment:

       ```bash
       $ source env/bin/activate

##    4. Create the Django project:

       ```bash
       $ django-admin startproject <projectName> .

##    5. Create a Django app (example: test):
       
       ```bash
       $ python manage.py startapp <appName>

       ## add app in installed apps in settings.py file

       INSTALLED_APPS = [
           …
           ‘<appName>’,
       ]
       
##    7. Define models in models.py and run migrations:
       
       ```bash
       $ python manage.py makemigrations
       $ python manage.py migrate

##    8. Update admin.py to register models and create a superuser:

       ```bash
       $ python manage.py createsuperuser

##    9. Run the server and log in as an admin to create some values:

       ```bash
       $ python manage.py runserver

##Step 3: Configuring the GraphQL API

##    1. Install necessary packages:

       ```bash       
       $ pip install graphene-django
       $ pip install django-filter

##    2. Update settings.py:##
##        ◦ Add 'graphene_django' to INSTALLED_APPS.

       INSTALLED_APPS = [
          …
          'graphene_django',
          ‘<appName>’,
       ]

##        ◦ Add the following in settings.py file to configure Graphene:
         
          GRAPHENE = {
              'SCHEMA': '<projectName>.schema.schema',}

##    3. Create schema.py files:
##        ◦ In the app directory (e.g., test/schema.py), define your schema.
##        ◦ In the project directory, create schema.py to tie all app schemas together.

##    4. Update urls.py in the project directory to include GraphQL IDE:
       
##       from django.urls import path
##       from graphene_django.views import GraphQLView
##       from django.views.decorators.csrf import csrf_exempt
       
       urlpatterns = [
           path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
       ]
