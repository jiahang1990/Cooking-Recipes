# Freshcook 

___

[Freshcook](https://freshcook.herokuapp.com/) is used for user to find recipe and it will save the user viewed recipe in local database to analysis user preference. The end goal of this project is to find insight based on user search activities.

It is developed based on [spoonacular API] (https://spoonacular.com/food-api)

___

The package contains following files:
> * app.py
> * form.py
> * models.py
> * test_home_view.py
> * test_login_view.py
> * test_recipe_ingredient_model.py
> * test_recipe_view.py
> * test_user_model.py
> * README.md
> * requirements.txt
> * runtime.txt
> * statics
> 	* images
> 		* food_background.jpeg
> 		* profile_default.jpg
> 		* recipe_default.gif
> 	* style.css
> * templates
> 	* Instruction.html
> 	* anonymous_user_nav.html
> 	* base.html
> 	* content.html
> 	* home.html
> 	* ingredient.html
> 	* login.html
> 	* login_user_nav.html
> 	* recipe.html
> 	* signup.html
> 	* user_home.html
> 	* user_nav_section.html
 
___
##Installation
In the terminal, create a virutal environment
>     python -m venv venv
>     source venv/bin/activate

To install necessary package in the terminal run
>     pip install -r requirements.txt

Make sure you have psql install in your local machine, if not installed go to PostgreSQL website [https://www.postgresql.org/](https://www.postgresql.org/)

Open PostgreSQL and create local database
> 		createdb recipes-app

##Deployment

In the terminal run
> 		flask run

The terminal will show the app attributes as below:
> 		* Environment: development
> 		* Debug mode: on
> 		* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
> 		* Restarting with stat
> 		* Debugger is active!
> 		* Debugger PIN: 185-505-248

##Instructions

####route: / 

In the home page, it will show 30 random recipes for user, after click the recipe, the recipe's name, image and ingredient will be saved in our local database.

####route: /recipe/\<recipe-id\>
After click the recipe it will redirect to the recipe page, it contains the name of the recipe, ingredient and instructions

####route: /signup
This route is for new user to sign up, if the username or email is already exists, it will show error after click sign up button. 

After sign up, user will be redirect to home page with his/her username on the navigation bar, and logout button

####route: /login
This route is for registerd user, if username or password dont match, it will show errors after click Login button

After login, user will be redirect to home page with his/her username on the navigation bar, and logout button