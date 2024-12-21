import os
import json
import hashlib
import getpass
import pyperclip
from pathlib import Path


def clear() -> None:
    """"""
    os.system("clear" if os.name == "posix" else "cls")


def hash_password(password: str) -> str:
    """"""
    return hashlib.sha256(password.encode()).hexdigest()


def load_data() -> dict:
    """"""
    path = Path(__file__).parent / "data.json"
    if not path.exists():
        save_data({"password_hash": None, "data": {}})
        return {"password_hash": None, "data": {}}
    else:
        with open(path, "r") as f:
            data = json.load(f)
        return data


def authenticate(password: str, data: dict) -> bool:
    """"""
    return hash_password(password) == data["password_hash"]


def new_password() -> None:
    """"""
    password: str = getpass.getpass("New Password: ").strip()
    if bool(password):
        password_hash: str = hash_password(password)
        data = load_data()
        data["password_hash"] = password_hash
        save_data(data)

def save_data(data: dict) -> None:
    """"""
    path = Path(__file__).parent / "data.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def main() -> None:
    """"""
    data: dict = load_data()
    
    while True:
        if data["password_hash"] is None:
            new_password()
            data = load_data()
        else:
            password: str = getpass.getpass("Password: ")
            if authenticate(password, data):
                break
            print("Incorrect password")
    
    clear()
    
    while True:
        option: str = input("1. Add data\n2. Get data\n3. Delete data\n4. Reset password \n5. Exit\noption: ")
        match int(option):
            case 1:
                name: str = input("name: ")
                value: str = input(f"value of {name}: ")
                
                if name in data["data"]:
                    override: bool = bool(input(f"{name} already exists. would you like to override? (leave black for no): "))
                    if not override:
                        continue
                data["data"][name] = value
                
                save_data(data)
                clear()
                print(f"added {name}")
            case 2:
                name: str = input("name: ")
                if name not in data["data"]:
                    print(f"{name} not found")
                    continue
                pyperclip.copy(data["data"][name])
                clear()
                print(f"copied {name} to clipboard")
            case 3:
                name: str = input("name: ")
                if name not in data["data"]:
                    print(f"{name} not found")
                    continue
                del data["data"][name]
                save_data(data)
                clear()
                print(f"deleted {name}")
            case 4:
                new_password()
                clear()
                print("password reset successfully")
            case 5:
                break
            case _:
                clear()
                print(f"invalid option {option}")


if __name__ == "__main__":
    main()
