from flask import Flask
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--port', type = int, default = 8000)

args = parser.parse_args()
app = Flask(__name__)

@app.route('/')
def index():
    return 'Web App with Python Flask!'

app.run(host='0.0.0.0', port=args.port)

#docker run -it --rm -p $PORT:$PORT -e XPRA_PORT=$PORT -e XPRA_EXIT_WITH_CLIENT="no" ghcr.io/napari/napari-xpra