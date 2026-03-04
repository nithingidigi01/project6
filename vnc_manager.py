import subprocess
import random
import os
import time


class VNCSession:

    def __init__(self):
        self.display_num = random.randint(100, 999)
        self.display = f":{self.display_num}"
        self.vnc_port = 5900 + self.display_num
        self.novnc_port = 6000 + self.display_num
        self.processes = []

    def start(self):

        xvfb = subprocess.Popen([
            "Xvfb", self.display,
            "-screen", "0", "1280x800x24"
        ])
        self.processes.append(xvfb)

        time.sleep(1)

        openbox = subprocess.Popen(
            ["openbox"],
            env={**os.environ, "DISPLAY": self.display}
        )
        self.processes.append(openbox)

        time.sleep(1)

        x11vnc = subprocess.Popen([
            "x11vnc",
            "-display", self.display,
            "-nopw",
            "-forever",
            "-rfbport", str(self.vnc_port)
        ])
        self.processes.append(x11vnc)

        time.sleep(1)

        novnc = subprocess.Popen([
            "websockify",
            "--web", "/usr/share/novnc",
            str(self.novnc_port),
            f"localhost:{self.vnc_port}"
        ])
        self.processes.append(novnc)

        return {
            "display": self.display,
            "url": f"http://localhost:{self.novnc_port}/vnc.html"
        }

    def stop(self):
        for p in self.processes:
            try:
                p.terminate()
            except:
                pass
        self.processes.clear()