import subprocess

def run_script(script):
    """Run AppleScript and return the result."""
    osa_script = f"osascript -e '{script}'"
    result = subprocess.run(osa_script, shell=True, capture_output=True, text=True)
    return result.stdout

