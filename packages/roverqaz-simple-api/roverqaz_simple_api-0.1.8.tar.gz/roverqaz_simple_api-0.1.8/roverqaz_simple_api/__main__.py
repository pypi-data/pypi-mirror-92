from roverqaz_simple_api import app

if __name__ == '__main__':
    # create table defined in Users class
    app.db.create_all()
    # run Flask app
    app.app.run(debug=True)