from telemetry_data import SharedMemory
from time import sleep

if __name__ == "__main__":
    data = SharedMemory().update()
    for tr in data.trailer:
        print(tr.name)
