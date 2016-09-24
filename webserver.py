import os

from flask import Flask
from flask import render_template

app = Flask(__name__, static_url_path='/cogs/simulationcraft/output')


# noinspection PyUnresolvedReferences
@app.route('/')
def root():
    files = [i for i in os.listdir('./static')]
    return render_template('index.html', files=files)


@app.route("/<path:path>")
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == '__main__':
    app.run()
