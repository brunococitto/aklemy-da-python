import logging as log
import os
from datetime import datetime

os.makedirs('logs', exist_ok=True)

FORMAT="[%(levelname)s] @ %(asctime)s | file %(filename)s | line %(lineno)s: %(message)s"

log.basicConfig(
    format=FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
    level=log.INFO,
    handlers=[
        log.StreamHandler(),
        log.FileHandler(f"logs/{datetime.now().strftime('ALKEMY-DA-LOG-%Y-%m-%d')}.txt",'a')
    ]
)