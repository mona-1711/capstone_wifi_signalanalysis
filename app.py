from flask import Flask, render_template
import subprocess
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/measure_signal_strength')
def measure_signal_strength():
    ssid, signal_strength = get_wifi_info()

    if ssid is not None and signal_strength is not None:
        strength_category = determine_signal_health(signal_strength)
        return {
            "wifi_strength": signal_strength,
            "wifi_name": ssid,
            "signal_health": strength_category
        }
    else:
        return {"error": "Unable to retrieve Wi-Fi information"}

def get_wifi_info(interface="Wi-Fi"):
    try:
        cmd_output = subprocess.check_output(["netsh", "wlan", "show", "interfaces"]).decode("utf-8")

        signal_strength_match = re.search(r"Signal[ ]+: (\d+)%", cmd_output)
        ssid_match = re.search(r"SSID[ ]+: (.+)", cmd_output)

        if signal_strength_match and ssid_match:
            signal_strength = int(signal_strength_match.group(1))
            ssid = ssid_match.group(1)
            return ssid, signal_strength
        else:
            return None, None

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None, None

def determine_signal_health(strength):
    if strength >= 70:
        return "Strong"
    elif strength >= 40:
        return "Moderate"
    else:
        return "Weak"

if __name__ == '__main__':
    app.run(debug=True)
