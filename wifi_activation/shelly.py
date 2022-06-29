import time
import requests

def switchPlug(toggle: str = None) -> None:
    url1 = "http://192.168.11.190/relay/0?turn="
    url2 = "http://192.168.11.191/relay/0?turn="
    if toggle is None:
        url1 += "toggle"
        url2 += "toggle"
    elif toggle == "off":
        url1 += "off"
        url2 += "off"
    elif toggle == "on":
        url1 += "on"
        url2 += "on"

    r1 = requests.get(url1)
    time.sleep(.3)
    r2 = requests.get(url2)

    print(f"request1 {r1.json()}")
    print(f"request2 {r2.json()}")
    return

def main():
    switchPlug()


if __name__ == "__main__":
    main()
