import subprocess
import time
import signal

def main():
    backend = subprocess.Popen(["uvicorn", "app.main:app", "--reload"])
    time.sleep(3)
    ui = subprocess.Popen(["streamlit", "run", "ui/app.py"])

    try:
        backend.wait()
        ui.wait()
    except KeyboardInterrupt:
        backend.send_signal(signal.SIGINT)
        ui.send_signal(signal.SIGINT)
        backend.wait()
        ui.wait()

if __name__ == "__main__":
    main()
