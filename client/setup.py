import os
import requests
import json
from dotenv import load_dotenv

load_dotenv() if ".env" in os.listdir() else None

if (
    ".env" not in os.listdir()
    or not os.environ.get("USERNAME")
    or not os.environ.get("PASSWORD")
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
    load_dotenv()

    result = requests.post(
        "http://localhost:8000/user/add",
        data=json.dumps(
            {
                "username": str(os.environ.get("USERNAME", "")),
                "password": str(os.environ.get("PASSWORD", "")),
            }
        ),
    ).json()
    if result and "error" in result:
        print("Error: {}".format(result["error"]))
        exit()


print("Starting client...")
print("Logged in as {}".format(os.environ.get("USERNAME")))
load_dotenv()
