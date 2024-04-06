# Final Project - Plant Database

&nbsp;&nbsp;&nbsp;&nbsp; This is my final project for the CS50 Web Programming with Python and JavaScript course that I took. I decided to apply all I learned in this course to construct this web-based plant database website to display the data of every plant in Rajamangalaphisek Education Park for the database developmnet team in Sukhothai Thammathirat Open University. This is the original design before I make changes to match the theme of the other database.

## Main Components

* Home Page

* Search Function

* Advance Search Function (in home page)

* Plant List Page - Display all plants in the database

* Letter Index List - Display all plants based on the index letter

* Family Index List - Display all the plants according to their family names

* Login / Logout - To use the administrative system

* Manage - Acess the Administration System Page

    * Search Function (Admin)

    * Delete and Change Data Page

        * Delete Data

        * Change Data Page

    * Add Data Page

    * Logout

## Distinctiveness and Complexity

&nbsp;&nbsp;&nbsp;&nbsp;This project is not similar to any other project in this course. This project has pages where data can be shown with various functions. The user can only view the info provided and cannot change it. This system does not require the user to log in to access the functionality of each page. Unlike the network and commerce project, where the user must login to use some of the functionalities. The login/logout mechanism allows only the administrator to update, add, or delete data. Each data in each item is more complex than any project in this course. This project contains three search systems: normal, advanced, and admin, each with a different method of handling the result, as opposed to the wiki project, which only has one, and the search project, where the functionality will be performed by Google.

## Files Information

* The views.py file in the application folder includes all the backend functinality. The functions are:

    * index function - Return the main page of the website

    * plantList function - Return the all plant list page

    * letterIndexList function - Return the letter index list page 

    * familyIndexList function - Return the family index list page

    * familyNameSort function - Return list result contains all plant with same familyName page

    * login_user function - Return the login page

    * logout_user function - Logout system

    * dashboard function - Return admin dashboard page when the administrator logs into the system

    * plantData function - Return plant data page which display all information of that plant

    * deletePlant function - Delete plant system

    * familyNameCommonNameChecker function - Delete commonName and familyName that aren't in use

    * search function - Normal search engine function 

    * searchResult function - Return the result of normal search engine system funciton

    * advanceSearch function - Advance search engine function

    * advanceSearchResult function - Return the result of advance search engine system funciton

    * adminSearch function - Admin search engine function

    * adminSearchResult function -  Return the result of admin search engine system function
    
    * editPlant function - Edit plant page and system

    * create function - Create plant page and system

* The model.py file in the application folder includes all the model in the database. The models are:

    * familyName model - Store all the family name of plants in the database

    * commonName model - Store all the common name of plants in the database
    
    * plantImage model  - Store all the image link to the image store in the media file

    * plant model - Store all the information of each plant in the database

* The urls.py file in the application folder includes urls that return the page or function of each url

* The admin.py file in the application folder includes all classes that connect to models to display information in django administration system

* apps.py, forms.py, test.py are all includes in the application folder

* In the static folder includes the bootstrap folder to use all the bootstrap tools, css folder, images folder which store the background of the webiste, and javascript folder

* Javascript folder includes all frontend javascript in the project
    * form.js - all frontend function in create and edit data function
    * index.js - function that clear all data in advance search in the home page
    * letterIndexList.js - Display all alphabets buttons in Thai and English
    * lsit.js - all function in the admin dashboard to delte, and go to edit page

* media folder includes all the static images of each plant in the database when the image was added

* plantDatabase folder includes asgi.py, settings.py, urls.py, and wsgi.py

## How to run the application
* Install project dependencies by running pip install -r requirements.txt
* Make and apply migrations by running python manage.py makemigrations and python manage.py migrate.
