import connexion
import argparse
from flask import render_template
import bacon_number.actor as actor


app = connexion.App('Bacon Number', specification_dir='./')

app.add_api('bacon_number/actor_swagger.yml')

def init(data_dir='./data'):
    actor.load_bacons_number(data_dir)

@app.route("/")
def home():
    """
    Default page for the api.

    :return:        the rendered template 'home.html'
    """
    return render_template("home.html")


@app.app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    if app.app.config['ENV'] == 'development':
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='Activate the debug option')
    parser.set_defaults(use_csv=False)
    parser.add_argument('--dev', dest='dev', action='store_true',
                        help='Activate the development environment')
    parser.set_defaults(use_csv=False)
    parser.add_argument('--port', type=int, default=8080,
                        help='Port where the server is running')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                        help='Host where the server is running')
    parser.add_argument('--data_dir', type=str, default='./data',
                        help='Directory where the data will be stored')
    params = parser.parse_args()

    init(data_dir=params.data_dir)
    app.run(host=params.host, port=params.port, debug=params.debug)