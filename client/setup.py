import os
import requests
from dotenv import load_dotenv

load_dotenv() if ".env" in os.listdir() else None

if (
    ".env" not in os.listdir()
    and not os.environ.get("USERNAME")
    and not os.environ.get("PASSWORD")
):
    with open(".env", "w") as f:
        f.write(
            """
USERNAME={}
PASSWORD={}
""".format(
                input("Username: "), input("Password: ")
            )
        )

    result = requests.post(
        "http://localhost:8000/users/add",
        json={
            "username": os.environ.get("USERNAME"),
            "password": os.environ.get("PASSWORD"),
        },
    ).json()


print("Starting client...")
print("Logged in as {}".format(os.environ.get("USERNAME")))
load_dotenv()
