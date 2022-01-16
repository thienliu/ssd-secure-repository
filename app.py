from flask.cli import FlaskGroup

from api import create_app

app = create_app('development')

cli = FlaskGroup(app)

@app.route("/")
def home():
    return "<p>Home Page!</p>"

# @cli.command()

if __name__ == '__main__':
    cli()