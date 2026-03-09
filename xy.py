import requests
import time
from datetime import datetime

url = "http://localhost:8220/status"

def get_value(text, key):
    try:
        return text.split(key + "=")[1].split("\n")[0].strip()
    except:
        return "NA"

with open("telescope_log.txt", "a") as f:

    f.write("Time | RA | DEC | AZ | ALT | Mount_State\n")

    while True:
        try:
            r = requests.get(url)
            text = r.text

            ra = get_value(text, "ra_apparent_hours")
            dec = get_value(text, "dec_apparent_degs")
            az = get_value(text, "azimuth_degs")
            alt = get_value(text, "altitude_degs")

            slewing = get_value(text, "mount.is_slewing")
            tracking = get_value(text, "mount.is_tracking")

            # Determine mount state
            if slewing == "true":
                state = "SLEWING"
            elif tracking == "true":
                state = "TRACKING"
            else:
                state = "IDLE"

            t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            line = f"{t} | {ra} | {dec} | {az} | {alt} | {state}\n"

            f.write(line)
            f.flush()

            print(line.strip())

            time.sleep(2)

        except Exception as e:
            print("Error:", e)
            time.sleep(2)