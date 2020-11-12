# Sudoku
Sudoku provides sudoku solver, where provided sudoku grid is solved by backtracking algorithm. Besides solver, 
random generator of sudoku grids is provided as well. It can be run as a web service where simple GUI is provided 
as simple web page through Flask environment.

# Getting started
## Installation
Requirements:
* Installed Python 3
* Created and activated virtual environment:
    * `python3 -m venv venv`
    * `source venv/bin/activate`
    * `pip install -r requirements.txt`
* Created .env file with configuration

## .env file
In order for application to work properly, env variables must be set inside `.env` file located in the root directory. 
Following code blocks show how to set these variables. Replace angular brackets `<>` with your values.

SECRET_KEY = '<your_key>'

DEBUG = 'true'

HOST = '<your_host_ip>'

PORT = '<your_port>'

# How to run
## Running python script
If you want to run just solver or generator without web service, go to `main.py` file in root directory where you have example.
There you can enter your own sudoku as numpy 2D array with zeros instead of empty cells and run `main.py` to solve it. In directory 
`constants` is example of Sudoku grid.

## Web service
If you want to run web service, go to `web_service` directory and run `app.py`. If you want ot run it on different host and port,
 define these values in `.env` file.

