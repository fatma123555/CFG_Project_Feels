"""

this folder will just run the 'create app' function in the __init___ python file inside the website folder

"""
try:
    from src.website import create_app
except Exception as e:
    print("Some modules are missing {}".format(e))

from src.website import create_app
# create the app that's created in the __init__ function
app = create_app()

# run the whole app through the top layer main python file
if __name__ == '__main__':
    app.run(debug=True)