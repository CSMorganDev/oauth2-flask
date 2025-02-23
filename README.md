# Flask OAuth2.0 & MQTT App

## Overview
This is a Flask application that integrates OAuth2.0 authentication with MQTT messaging and WebSocket communication. It allows users to log in via OAuth, subscribe to an MQTT topic, and receive real-time updates via WebSockets.

## Features
- OAuth2.0 authentication using a third-party provider (e.g., GitHub)
- MQTT client for subscribing and publishing messages
- WebSocket integration for real-time communication
- CORS support for cross-origin requests
- Secure session management

## Getting Started

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.x
- Flask
- A registered OAuth2.0 provider (e.g., GitHub, Google)
- An MQTT broker (e.g., Adafruit IO, Mosquitto)

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/CSMorganDev/oauth2-flask.git
   ```
2. Navigate to the project directory:
   ```sh
   cd oauth2-flask
   ```
3. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Set up environment variables in a `.env` file:
   ```sh
   APP_SECRET=<your-app-secret>
   OAUTH_NAME=<your-oauth-provider>
   OAUTH_CLIENT_ID=<your-client-id>
   OAUTH_CLIENT_SECRET=<your-client-secret>
   OAUTH_AUTHORIZE_URL=<your-authorize-url>
   OAUTH_ACCESS_TOKEN_URL=<your-access-token-url>
   OAUTH_API_BASE_URL=<your-api-base-url>
   SCOPE=<your-oauth-scope>
   AIO_USERNAME=<your-mqtt-username>
   AIO_SERVER=<your-mqtt-server>
   AIO_KEY=<your-mqtt-api-key>
   AIO_FEED=<your-mqtt-feed>
   AIO_FEED_UPDATE=<your-mqtt-feed-update>
   ```
6. Run the application:
   ```sh
   flask run
   ```

## API Endpoints
- `/` - Home page
- `/login` - Redirects to OAuth provider for authentication
- `/logout` - Logs out the user
- `/authorize` - Handles OAuth2.0 authorization callback
- `/sensor` - Publishes an MQTT message to trigger an update


