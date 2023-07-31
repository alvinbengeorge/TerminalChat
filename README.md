# TerminalChat
This is a project that I built for SRMKzilla's internal hackathon, encouraging members of the club to make something new. This project was inspired because I felt that there was a lack of communicating ability from the terminal

## `Tech Stack`
- FastAPI
- Textual
- MongoDB

<img width="705" alt="image" src="https://github.com/alvinbengeorge/TerminalChat/assets/69302420/038c82b9-9aef-431a-a0f0-694383c3b81a">

## `Installation`

[▶️](https://www.python.org/) Install python for your Operating System if you do not have it

### `In the client side:`
```sh
cd client
python -m venv venv

# Windows
./venv/Scripts/activate

# Linux
source ./venv/bin/activate

pip3 install -r requirements.txt
python main.py [person you want to text]
```

### `In the server side:`
```sh
cd server
python -m venv venv

# Windows
./venv/Scripts/activate

# Linux
source ./venv/bin/activate

pip3 install -r requirements.txt
uvicorn main:app
```

## `The future`
This application has a lot of potential to be bigger and useful, supporting many features like image upload, etc. but as of now it's a basic text application

