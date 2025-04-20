from pathlib import Path
import sys
import pymysql
from dbutils.pooled_db import PooledDB
from config import OPENAPI_STUB_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME
from swagger_server import models

# Append OPENAPI_STUB_DIR to sys.path for module imports
sys.path.append(OPENAPI_STUB_DIR)

# Initialize database connection pool
pool = PooledDB(
    creator=pymysql,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWD,
    database=DB_NAME,
    maxconnections=1,
    blocking=True
)


def get_one_day_data_aqi():
    """Fetch AQI data for the current day, excluding NULL columns."""
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, temperature, humidity, latitude, longitude, timestamp, source
            FROM secondaryData
            WHERE source = 'aqi' AND timestamp >= CURDATE()
        """)
        result = cs.fetchall()
        measurements = []
        for row in result:
            measurement = models.Measurement(
                id=row[0],
                temperature=row[1],
                heartbeat_bpm=None,
                humidity=row[2],
                aqi=None,
                pm25=None,
                pm10=None,
                o3=None,
                no2=None,
                co=None,
                so2=None,
                dew=None,
                pressure=None,
                wind=None,
                wind_gust=None,
                dominentpol=None,
                light=None,
                latitude=row[3],
                longitude=row[4],
                timestamp=row[5],
                source=row[6]
            )
            measurements.append(measurement.to_dict())
        return measurements


def get_one_week_data_aqi():
    """Fetch AQI data for the past week, excluding NULL columns."""
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, temperature, humidity, latitude, longitude, timestamp, source
            FROM secondaryData
            WHERE source = 'aqi' AND timestamp >= CURDATE() - INTERVAL 7 DAY
        """)
        result = cs.fetchall()
        measurements = []
        for row in result:
            measurement = models.Measurement(
                id=row[0],
                temperature=row[1],
                heartbeat_bpm=None,
                humidity=row[2],
                aqi=None,
                pm25=None,
                pm10=None,
                o3=None,
                no2=None,
                co=None,
                so2=None,
                dew=None,
                pressure=None,
                wind=None,
                wind_gust=None,
                dominentpol=None,
                light=None,
                latitude=row[3],
                longitude=row[4],
                timestamp=row[5],
                source=row[6]
            )
            measurements.append(measurement.to_dict())
        return measurements


def get_one_day_data_kidbright():
    """Fetch Kidbright data for the current day, excluding NULL columns."""
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, temperature, heartbeat_bpm, humidity, dew, pressure, wind, wind_gust, light, latitude, longitude, timestamp, source
            FROM secondaryData
            WHERE source = 'kidbright' AND timestamp >= CURDATE()
        """)
        result = cs.fetchall()
        measurements = []
        for row in result:
            measurement = models.Measurement(
                id=row[0],
                temperature=row[1],
                heartbeat_bpm=row[2],
                humidity=row[3],
                aqi=None,
                pm25=None,
                pm10=None,
                o3=None,
                no2=None,
                co=None,
                so2=None,
                dew=row[4],
                pressure=row[5],
                wind=row[6],
                wind_gust=row[7],
                dominentpol=None,
                light=row[8],
                latitude=row[9],
                longitude=row[10],
                timestamp=row[11],
                source=row[12]
            )
            measurements.append(measurement.to_dict())
        return measurements


def get_one_week_data_kidbright():
    """Fetch Kidbright data for the past week, excluding NULL columns."""
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, temperature, heartbeat_bpm, humidity, dew, pressure, wind, wind_gust, light, latitude, longitude, timestamp, source
            FROM secondaryData
            WHERE source = 'kidbright' AND timestamp >= CURDATE() - INTERVAL 7 DAY
        """)
        result = cs.fetchall()
        measurements = []
        for row in result:
            measurement = models.Measurement(
                id=row[0],
                temperature=row[1],
                heartbeat_bpm=row[2],
                humidity=row[3],
                aqi=None,
                pm25=None,
                pm10=None,
                o3=None,
                no2=None,
                co=None,
                so2=None,
                dew=row[4],
                pressure=row[5],
                wind=row[6],
                wind_gust=row[7],
                dominentpol=None,
                light=row[8],
                latitude=row[9],
                longitude=row[10],
                timestamp=row[11],
                source=row[12]
            )
            measurements.append(measurement.to_dict())
        return measurements


def get_one_day_data_tmd():
    """Fetch TMD data for the current day, excluding NULL columns."""
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, temperature, humidity, dew, pressure, wind, wind_gust, latitude, longitude, timestamp, source
            FROM secondaryData
            WHERE source = 'TMD' AND timestamp >= CURDATE()
        """)
        result = cs.fetchall()
        measurements = []
        for row in result:
            measurement = models.Measurement(
                id=row[0],
                temperature=row[1],
                heartbeat_bpm=None,
                humidity=row[2],
                aqi=None,
                pm25=None,
                pm10=None,
                o3=None,
                no2=None,
                co=None,
                so2=None,
                dew=row[3],
                pressure=row[4],
                wind=row[5],
                wind_gust=row[6],
                dominentpol=None,
                light=None,
                latitude=row[7],
                longitude=row[8],
                timestamp=row[9],
                source=row[10]
            )
            measurements.append(measurement.to_dict())
        return measurements


def get_one_week_data_tmd():
    """Fetch TMD data for the past week, excluding NULL columns."""
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, temperature, humidity, dew, pressure, wind, wind_gust, latitude, longitude, timestamp, source
            FROM secondaryData
            WHERE source = 'TMD' AND timestamp >= CURDATE() - INTERVAL 7 DAY
        """)
        result = cs.fetchall()
        measurements = []
        for row in result:
            measurement = models.Measurement(
                id=row[0],
                temperature=row[1],
                heartbeat_bpm=None,
                humidity=row[2],
                aqi=None,
                pm25=None,
                pm10=None,
                o3=None,
                no2=None,
                co=None,
                so2=None,
                dew=row[3],
                pressure=row[4],
                wind=row[5],
                wind_gust=row[6],
                dominentpol=None,
                light=None,
                latitude=row[7],
                longitude=row[8],
                timestamp=row[9],
                source=row[10]
            )
            measurements.append(measurement.to_dict())
        return measurements
