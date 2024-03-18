# Adopted from Sample Flask application for a BSG database, snapshot of BSG_people design
# souce: https://github.com/osu-cs340-ecampus/flask-starter-app

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import random
import jsonify
import requests

app = Flask(__name__)

# database connection info
app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_sunyus'  #osu username
app.config['MYSQL_PASSWORD'] = '8409'        #last 4 of db pass   
app.config['MYSQL_DB'] = 'cs340_sunyus'    #osu username 
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes
# have homepage route to /people by default for convenience, generally this will be your home route with its own template
@app.route("/")
def home():
    return redirect("/recipes")

# route for recipes page
@app.route("/recipes", methods=["POST", "GET"])
def recipes():
    # Separate out the request methods, in this case this is for a POST
    # insert a recipes into the Recipes entity
    if request.method == "POST":
        # fire off if user presses the Add Recipe button
        if request.form.get("Add_Recipe"):
            # grab user form inputs
            recipe_name = request.form["recipe_name"]
            serving_size = request.form["serving_size"]
            ingredients = request.form["ingredients"]
            steps = request.form["steps"]


        # example as no null inputs
            query = "INSERT INTO Recipes (recipe_name, serving_size, ingredients, steps) VALUES (%s,%s,%s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (recipe_name, serving_size, ingredients, steps))
            mysql.connection.commit()          


            # redirect back to people page
            return redirect("/recipes")

    # Grab Recipes table data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the recipes in Recipes table
        ###################################################
        ####### Needs o work on using Adopter's name ######
        
        query = "SELECT * FROM Recipes"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_recipes page passing our data to the edit_recipes template
        return render_template("recipes.j2", data=data)
    
@app.route("/recipes/<int:recipe_id>", methods=["POST", "GET"])
def recipe_detail(recipe_id):
    # mySQL query to grab the info of the cat with our passed id
    if request.method == "GET":
        query = "SELECT * FROM Recipes WHERE recipe_id = %s" % (recipe_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_cats page passing our query data and adopter data to the edit_cats template
        return render_template("search_results.j2", data=data)

@app.route('/random_recipe', methods=['GET'])
def get_products():
    response = requests.get("http://localhost:5555/random")
    if response.status_code != 200:
        return jsonify({'error': response.json()['message']}), response.status_code
    else:
        random_number = int(response.json()['random'])
        query1 = "SELECT COUNT(recipe_id) FROM Recipes"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        index = cur.fetchone()
        print(index)
        num = index['COUNT(recipe_id)']
        
        random_number = random_number % num +1

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Recipes WHERE recipe_id = %s', (random_number,))
        recipe = cur.fetchone()

    return render_template('random_recipe.j2', data=recipe, random_number=random_number)
    
# @app.route('/random_recipe')
# def random_recipe():
#     random_number = random.randint(1, 4)
#     print(random_number)
#     cur = mysql.connection.cursor()
#     cur.execute('SELECT * FROM Recipes WHERE recipe_id = %s', (random_number,))
#     recipe = cur.fetchone()

#     return render_template('random_recipe.j2', data=recipe, random_number=random_number)
    
@app.route("/create")
def create():
    return render_template('create_recipe.j2')

@app.route("/tutorial")
def tutorial():
    return redirect("../static/Recipe Manager Tutorial.pdf")

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search', '')  
    if search_query:
        query = "SELECT * FROM Recipes WHERE recipe_name LIKE %s"
        cur = mysql.connection.cursor()
        cur.execute(query, ('%' + search_query + '%',))
        results = cur.fetchall()
        return render_template('search_results.j2', data=results)
    else:
        # If there's no search query, you might want to redirect or show all recipes
        return redirect('/recipes')



# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_recipes/<int:recipe_id>")
def delete_recipes(recipe_id):
    # mySQL query to delete the person with our passed id
    #query = "DELETE FROM bsg_people WHERE id = '%s';"
    query = "DELETE FROM Recipes WHERE recipe_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (recipe_id,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/recipes")


# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_recipes/<int:recipe_id>", methods=["POST", "GET"])
def edit_recipes(recipe_id):
    if request.method == "GET":
        # mySQL query to grab the info of the recipe with our passed id
        query = "SELECT * FROM Recipes WHERE recipe_id = %s" % (recipe_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_recipes page passing our query data and adopter data to the edit_recipes template
        return render_template("edit_recipes.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Recipe' button
        if request.form.get("Edit_Recipe"):
            # grab user form inputs
            recipe_name = request.form["recipe_name"]
            serving_size = request.form["serving_size"]
            ingredients = request.form["ingredients"]
            steps = request.form["steps"]

            # example as no null inputs
            query = "UPDATE Recipes SET recipe_name=%s,  serving_size=%s, ingredients=%s, steps=%s"
            cur = mysql.connection.cursor()
            cur.execute(query, (recipe_name, serving_size, ingredients, steps))
            mysql.connection.commit()        


            # redirect back to recipes page after we execute the update query
            return redirect("/recipes")


# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=64327, debug=True)