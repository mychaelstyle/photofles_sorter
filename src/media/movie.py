import subprocess, time, os, sys

def get_datetime(path):
    proc = subprocess.run(["/usr/local/bin/ffprobe","-show_chapters","-hide_banner",path],
            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    response = proc.stdout.decode("utf8")+"\n"+(proc.stderr.decode("utf8"))
    for line in response.splitlines():
        if "creation_time" in line:
            str = line.strip().replace("creation_time","").strip().replace(": ","").strip().replace("T"," ").replace("Z","")
            return str.replace("-",":")

