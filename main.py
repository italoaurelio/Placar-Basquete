import subprocess
import time
import sys

placar_proc = subprocess.Popen(["python", "placar.py"])
time.sleep(2)
controle_proc = subprocess.Popen(["python", "controle.py"])

# Aguarda o fechamento do controlador
controle_proc.wait()

# Fecha o placar e finaliza
placar_proc.terminate()
placar_proc.wait()

sys.exit(0)
