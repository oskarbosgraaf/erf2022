

import requests


def main() -> None:
    url = "http://192.168.11.190/0?turn=on"
    r = requests.get(url)
    print(r.json())


if __name__ == "__main__":
    main()
