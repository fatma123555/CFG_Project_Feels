"""

this folder will just run the 'create app' function in the __init___ python file inside the website folder

"""
try:
    from src.website import create_app
except Exception as e:
    print("Some modules are missing {}".format(e))


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)