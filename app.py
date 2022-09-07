from capstone import app

if __name__ == '__main__':
    app.run(debug=True)

    # venv\Scripts\activate
    # set FLASK_APP=app     as in app.py
    # flask run

    # Debug mode was not turning on, had to use command below inside terminal 
    # set FLASK_DEBUG=1

    # to setup venv I entered 
    # py -m venv venv          second venv is the name of the virtual environment I believe


    # When time to initiate database for heroku, it is: heroku run python --app carflask308