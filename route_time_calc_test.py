from telemetry_data import SharedMemory
import time

class TimeCalc:
    def gametime_to_real(self, hours, mins) -> str:
        from datetime import datetime

        game_time_secs = (int(hours)*60 + int(mins))*60

        real_time_secs = game_time_secs / 10
        real_time_hours = real_time_secs // 60**2
        real_time_mins = round(real_time_secs / 60**2 - real_time_hours, 3) * 60

        now = datetime.strptime(f"{round(real_time_hours)}:{round(real_time_mins)}", '%H:%M')
        return now.strftime('%H:%M')

    def dist_speed_to_realtime(self, dist:int, speed:int) -> str:
        from datetime import datetime

        game_time_secs = ((round((dist / speed)))*60 + (round(((dist / speed) - round((dist / speed),0)) * 60)))*60

        real_time_secs = game_time_secs / 10
        real_time_hours = real_time_secs // 60**2
        real_time_mins = round(real_time_secs / 60**2 - real_time_hours, 3) * 60

        if real_time_hours > 23:
            return "err"

        route = datetime.strptime(f"{round(real_time_hours)}:{round(real_time_mins)}", "%H:%M")
        target = datetime.strptime(f"{round(real_time_hours + datetime.today().hour)}:{round(real_time_mins + datetime.today().minute)}", "%H:%M")
        return (route.strftime("%H:%M"), target.strftime("%H:%M"))

if __name__ == "__main__":
    Telemety = SharedMemory()
    data = Telemety.update()

    speed_arr = []

    while True:
        if data.sdkActive == True:
            data = Telemety.update()

            try:
                speed_arr.insert(0, (data.speed * 3.6 + 75) / 2)
                speed_arr.pop(101)

                if data.speedLimit == 0:
                    speed = round(abs(sum(speed_arr) / len(speed_arr)),2)
                elif data.cruiseControl == False:
                    speed = round(abs(((sum(speed_arr) / len(speed_arr)) * 4 + data.speedLimit * 3.6) / 5),2)
                else:
                    speed = round(abs(((sum(speed_arr) / len(speed_arr)) * 4 + data.speedLimit * 3.6 + data.cruiseControlSpeed * 3.6) / 6),2)
        
                print(f"{TimeCalc().dist_speed_to_realtime(data.routeDistance / 1000, speed)} {speed} {round(data.routeDistance / 1000, 3)} {round(data.cruiseControlSpeed * 3.6, 2)}")
            except Exception as e:
                print(e)

            time.sleep(0.1)
