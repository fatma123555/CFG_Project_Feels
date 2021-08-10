"""

this folder will just run the 'create app' function in the __init___ python file inside the website folder

"""
from src.website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)