
# Gender Reveal Party Voting App

This project is a simple web application built with Flask to facilitate a fun and interactive gender reveal party. It allows guests to vote on the gender of the baby for two women, Nathalia and Greyce, and provides a way to view the votes, including guest names, messages, and the total number of votes.

## Features

- **Guest Voting**: Allows guests to submit their name, a message, and vote on whether they think Nathalia & Marcelo or Greyce & Winter are expecting a boy or a girl.
- **Vote Results**: Displays the total number of votes for each gender (boy/girl) for both women.
- **Guest Information**: Shows the name and message of each person who voted.

## Requirements

- Python 3.7+
- Flask

## Setup

### 1. Clone the Repository and install the required dependencies

```bash
git clone https://github.com/marceloaba/gender-reveal.git
cd gender-reveal
python3 -m virtualenv gender-reveal-venv
pip install -r requirements.txt
```

### Run the app locally
Set up the database: The app uses SQLite, and the database will be automatically created `src/gender_reveal.db` when you run the application for the first time.
   
```bash
export FLASK_PORT="5001"
python main.py
```
The application will be running at http://127.0.0.1:5001/.

### 2. Build and push app to docker hub

#### Build and push app to docker hub
```bash
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t marceloaba/gender_reveal:python3.10-v1.0 --push .
```

### 2. Run app using docker compose

```bash
docker-compose up -d
```

### Routes
http://127.0.0.1:5001/ - Displays the main page where guests can enter their name, leave a message, and vote.

http://127.0.0.1:5001/vote_results - Displays the total votes for each couple and shows the names and messages of the guests who voted.
