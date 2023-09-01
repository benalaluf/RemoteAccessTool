import subprocess

result = subprocess.run(['cat', 'attacker_main.py'], capture_output=True)
print(result.stdout.decode())
