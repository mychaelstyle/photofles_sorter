import subprocess
import os

def get_datetime(path):
    print("path: %s" % path)
    if not os.path.exists(path):
        return None
    proc = subprocess.run(["/usr/local/bin/ffprobe","-show_chapters","-hide_banner", path],
            stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding = "utf8", errors='ignore')
    response = proc.stdout+"\n"+(proc.stderr)
    print(response)
    for line in response.splitlines():
        if "creation_time" in line:
            str = line.strip().replace("creation_time","").strip().replace(": ","").strip().replace("T"," ").replace("Z","")
            return str.replace("-",":")

