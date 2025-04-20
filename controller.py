from swagger_server import models
import sys
import pymysql
from dbutils.pooled_db import PooledDB
from config import OPENAPI_STUB_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME

sys.path.append(OPENAPI_STUB_DIR)

pool = PooledDB(creator=pymysql,
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWD,
                database=DB_NAME,
                maxconnections=1,
                blocking=True)


def get_one_hour_data():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, temperature, heartbeat_bpm, humidity, aqi, pm25, pm10,
                   o3, no2, co, so2, dew, pressure, wind, wind_gust,
                   dominentpol, light, latitude, longitude, timestamp, source
            FROM secondaryData
            WHERE timestamp >= NOW() - INTERVAL 1 HOUR
        """)
        return [models.Measurement(*row).to_dict() for row in cs.fetchall()]


def get_one_day_data():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, temperature, heartbeat_bpm, humidity, aqi, pm25, pm10,
                   o3, no2, co, so2, dew, pressure, wind, wind_gust,
                   dominentpol, light, latitude, longitude, timestamp, source
            FROM secondaryData
            WHERE timestamp >= CURDATE()
        """)
        return [models.Measurement(*row).to_dict() for row in cs.fetchall()]
