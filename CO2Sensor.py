import mh_z19 as sensor
import time
import json

class CO2Sensor:

    def __init__(self, period: int = 1200) -> None: #period default is 20min
        self.period = period
        self.running = True

    def stop(self):
        self.running = False

    def start(self):
        self.running = True

    def run(self):
        while(self.running):
            data = sensor.read_all() #returns { "co2": , "temperature": , "TT": , "SS": , "UhUl": } # works with UART TW/RX (corresponds to GPIO 14/15)
            current_date = time.strftime("%Y-%m-%d")
            current_time = time.strftime("%H:%M:%S")
            data_dict = {
                "date": current_date,
                "time": current_time,
                "co2": data["co2"],
                "temperature": data["temperature"]
            }
            existing_data = self.get_existing_data()
            existing_data.append(data_dict)
            self.save_data(existing_data)
            time.sleep(self.period)

    def calibrate(self):
        sensor.zero_point_calibration()

    def get_existing_data(self):
        current_date = time.strftime("%Y-%m-%d")
        try:
            with open("co2Data/{0}.json".format(current_date), 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []
        return existing_data

    def save_data(self, data):
        current_date = time.strftime("%Y-%m-%d")
        file = json.dumps(data)
        with open("co2Data/{0}.json".format(current_date), "w") as outfile:
            outfile.write(file)
