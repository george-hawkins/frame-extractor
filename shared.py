import subprocess


def run(args):
    return subprocess.run([str(e) for e in args], capture_output=True, text=True).stdout.strip()
