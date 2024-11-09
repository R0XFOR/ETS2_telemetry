from telemetry_data import SharedMemory
from time import sleep

if __name__ == "__main__":
    #while True:
        data = SharedMemory().update()
        print(data.sdkActive, data.shifterType)
        #sleep(0.1)
