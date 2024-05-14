import os
from flask import Flask, redirect, session, url_for, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv


load_dotenv()

APP_SECRET = os.environ.get('APP_SECRET')
OAUTH_NAME = os.environ.get('OAUTH_NAME')
OAUTH_CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID')
OAUTH_CLIENT_SECRET = os.environ.get('OAUTH_CLIENT_SECRET')
OAUTH_AUTHORIZE_URL = os.environ.get('OAUTH_AUTHORIZE_URL')
OAUTH_ACCESS_TOKEN_URL = os.environ.get('OAUTH_ACCESS_TOKEN_URL')
OAUTH_API_BASE_URL = os.environ.get('OAUTH_API_BASE_URL')
SCOPE = os.environ.get('SCOPE')


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = APP_SECRET
oauth = OAuth(app)

github = oauth.register(
    name=OAUTH_NAME,
    client_id=OAUTH_CLIENT_ID,
    client_secret=OAUTH_CLIENT_SECRET,
    authorize_url=OAUTH_AUTHORIZE_URL,
    access_token_url=OAUTH_ACCESS_TOKEN_URL,
    api_base_url=OAUTH_API_BASE_URL,
    client_kwargs={'scope': SCOPE},
)

AIO_USERNAME = os.environ.get('AIO_USERNAME')
app.config['MQTT_BROKER_URL'] = os.environ.get('AIO_SERVER')
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = AIO_USERNAME
app.config['MQTT_PASSWORD'] = os.environ.get('AIO_KEY')
app.config['MQTT_KEEPALIVE'] = 30
AIO_FEED = os.environ.get('AIO_FEED')
AIO_FEED_UPDATE = os.environ.get('AIO_FEED_UPDATE')

mqtt_client = Mqtt(app)
socketio = SocketIO(app)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe(f'{AIO_USERNAME}/feeds/{AIO_FEED}')  # subscribe topic
    else:
        print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print('Received message on topic: {topic} with payload: {payload}'.format(**data))
    socketio.emit('mqtt_message', data=data)


@app.route('/')
def hello_world():
    user = session.get('user')
    if user:
        return render_template('home.html', user=user, door=session['door'])
    else:
        return render_template('login.html')


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('door', None)

    return redirect('/')


@app.route('/sensor')
def sensor():
    publish_result = mqtt_client.publish(f'{AIO_USERNAME}/feeds/{AIO_FEED_UPDATE}', b'1')
    session['door'] = publish_result[1]
    return {
        'status': 200,
        'message': 'OK'
    }


@app.route('/authorize')
def authorize():
    try:
        token = github.authorize_access_token()
        resp = github.get('user', token=token)
        user = resp.json()
        session['user'] = user
        session['door'] = None
    finally:
        return redirect('/')

