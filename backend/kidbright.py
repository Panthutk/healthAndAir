from machine import Pin, UART , ADC
import network
import time
import json
import math
from umqtt.robust import MQTTClient
import dht
from config import WIFI_SSID, WIFI_PASS, MQTT_BROKER, MQTT_USER, MQTT_PASS

# Onboard LED on Pin 2
led = Pin(2, Pin.OUT)

# Wi-Fi Setup
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def connect_wifi():
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        attempts = 0
        while not wlan.isconnected():
            attempts += 1
            print(f"Attempt {attempts}...")
            led.value(attempts % 2)  # Blink LED while connecting
            time.sleep(1)
            if attempts >= 10:
                print("Still not connected. Retrying connect...")
                wlan.disconnect()
                wlan.connect(WIFI_SSID, WIFI_PASS)
        print("WiFi Connected:", wlan.ifconfig())
        led.value(1)  # Turn LED on when connected

# MQTT Setup
mqtt = MQTTClient(client_id="sensor_client", server=MQTT_BROKER, user=MQTT_USER, password=MQTT_PASS, keepalive=60)

def connect_mqtt():
    connected = False
    attempts = 0
    while not connected:
        try:
            mqtt.connect()
            print("MQTT Connected")
            connected = True
            led.value(1)  # LED stays on when MQTT is connected
        except Exception as e:
            attempts += 1
            print(f"MQTT Connection Failed (attempt {attempts}):", e)
            led.value(attempts % 2)  # Blink LED while trying
            time.sleep(5)

connect_wifi()
connect_mqtt()

# Sensor Setup
dht_sensor = dht.DHT11(Pin(32))
uart = UART(2, baudrate=9600, tx=19, rx=18)
heartbeat_adc = ADC(Pin(35))
heartbeat_adc.atten(ADC.ATTN_11DB)
heartbeat_adc.width(ADC.WIDTH_12BIT)
ldr_adc = ADC(Pin(36))
ldr_adc.atten(ADC.ATTN_11DB)
ldr_adc.width(ADC.WIDTH_12BIT)

HEARTBEAT_WINDOW = 5000  # 5 seconds
heartbeat_timestamps = []

# Timestamp
timestamp = time.ticks_ms()

# MQTT Topic
topic = "b6610545421/sensors"

def calculate_aqi(pm25):
    if pm25 is None:
        return None
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 500.0, 301, 500)
    ]
    pm25 = min(pm25, 500.0)
    for c_low, c_high, i_low, i_high in breakpoints:
        if c_low <= pm25 <= c_high:
            aqi = ((i_high - i_low) / (c_high - c_low)) * (pm25 - c_low) + i_low
            return round(aqi)
    return 0

def read_dht11():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temp, humidity
    except OSError as e:
        print("Failed to read DHT11 Temp and Humid:", e)
        return None, None

def read_pms7003_aqi():
    try:
        uart.write(b'\x42\x4D\xE2\x00\x00\x01\x71')
        time.sleep(0.1)
        if uart.any():
            data = uart.read(32)
            
            if data and len(data) == 32 and data[0] == 0x42 and data[1] == 0x4D:
                pm2_5 = (data[6] << 8) | data[7]
                aqi = calculate_aqi(pm2_5)
                return aqi
        return None
    except Exception as e:
        print("Error reading PMS7003:", e)
        return None

def read_heartbeat_bpm():
    global heartbeat_timestamps
    current_time = time.ticks_ms()
    heartbeat_value = heartbeat_adc.read()
    THRESHOLD = 2000

    if heartbeat_value > THRESHOLD:
        if not heartbeat_timestamps or time.ticks_diff(current_time, heartbeat_timestamps[-1]) > 200:
            heartbeat_timestamps.append(current_time)
            print(f"Heartbeat detected at {current_time} ms")

    heartbeat_timestamps = [t for t in heartbeat_timestamps if time.ticks_diff(current_time, t) <= HEARTBEAT_WINDOW]

    if len(heartbeat_timestamps) >= 2:
        intervals = [time.ticks_diff(heartbeat_timestamps[i+1], heartbeat_timestamps[i]) 
                     for i in range(len(heartbeat_timestamps)-1)]
        avg_interval_ms = sum(intervals) / len(intervals)
        bpm = (60000 / avg_interval_ms)
        return round(bpm, 2)
    return None

def read_light_intensity():
    ldr_value = ldr_adc.read()
    lux = math.log(ldr_value + 1) * 10
    return lux

# Main Loop
while True:
    if not wlan.isconnected():
        led.value(0)
        connect_wifi()
    if not mqtt.sock:
        led.value(0)
        connect_mqtt()

    now = time.ticks_ms()
    if time.ticks_diff(now, timestamp) >= 600000:  # Every 30 minutes
        timestamp = now  # Reset timestamp

        temperature, humidity = read_dht11()
        aqi = read_pms7003_aqi()
        bpm = read_heartbeat_bpm()
        light_intensity = read_light_intensity()

        data = {
            "temperature": temperature,
            "humidity": humidity,
            "aqi": aqi,
            "heartbeat_bpm": bpm,
            "light": round(light_intensity, 2),
            "lat": 13.84629301687324,
            "lon": 100.56975912613683,
            "source": "kidbright"
        }

        try:
            mqtt.publish(topic, json.dumps(data))
            print(f"Published to {topic}: {data}")
        except Exception as e:
            print("Failed to publish:", e)
            connect_mqtt()

    time.sleep(1)
