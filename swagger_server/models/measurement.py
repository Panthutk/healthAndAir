class Measurement:
    def __init__(self, id, temperature, heartbeat_bpm, humidity, aqi, pm25, pm10,
                 o3, no2, co, so2, dew, pressure, wind, wind_gust, dominentpol,
                 light, latitude, longitude, timestamp, source):
        self.id = id
        self.temperature = temperature
        self.heartbeat_bpm = heartbeat_bpm
        self.humidity = humidity
        self.aqi = aqi
        self.pm25 = pm25
        self.pm10 = pm10
        self.o3 = o3
        self.no2 = no2
        self.co = co
        self.so2 = so2
        self.dew = dew
        self.pressure = pressure
        self.wind = wind
        self.wind_gust = wind_gust
        self.dominentpol = dominentpol
        self.light = light
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp
        self.source = source

    def to_dict(self):
        return self.__dict__
