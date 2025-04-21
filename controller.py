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


def fetch_latest_timestamp(source, conn, cs):
    cs.execute(
        "SELECT MAX(timestamp) FROM secondaryData WHERE source = %s", (source,))
    return cs.fetchone()[0]


def get_one_day_data_aqi():
    with pool.connection() as conn, conn.cursor() as cs:
        latest = fetch_latest_timestamp('aqi', conn, cs)
        if not latest:
            return []

        cs.execute("""
            SELECT id, temperature, humidity, aqi, pm25, pm10, o3, no2, co, so2,
                   dew, pressure, wind, dominentpol, light, latitude, longitude, timestamp, source
            FROM secondaryData
            WHERE source = 'aqi' AND timestamp BETWEEN %s - INTERVAL 1 DAY AND %s
        """, (latest, latest))

        return [models.Measurement(
            id=row[0], temperature=row[1], heartbeat_bpm=None, humidity=row[2], aqi=row[3],
            pm25=row[4], pm10=row[5], o3=row[6], no2=row[7], co=row[8], so2=row[9], dew=row[10],
            pressure=row[11], wind=row[12], wind_gust=None, dominentpol=row[13], light=row[14],
            latitude=row[15], longitude=row[16], timestamp=row[17], source=row[18]
        ).to_dict() for row in cs.fetchall()]


def get_one_week_data_aqi():
    with pool.connection() as conn, conn.cursor() as cs:
        latest = fetch_latest_timestamp('aqi', conn, cs)
        if not latest:
            return []

        cs.execute("""
            SELECT id, temperature, humidity, aqi, pm25, pm10, o3, no2, co, so2,
                   dew, pressure, wind, dominentpol, light, latitude, longitude, timestamp, source
            FROM secondaryData
            WHERE source = 'aqi' AND timestamp BETWEEN %s - INTERVAL 7 DAY AND %s
        """, (latest, latest))

        return [models.Measurement(
            id=row[0], temperature=row[1], heartbeat_bpm=None, humidity=row[2], aqi=row[3],
            pm25=row[4], pm10=row[5], o3=row[6], no2=row[7], co=row[8], so2=row[9], dew=row[10],
            pressure=row[11], wind=row[12], wind_gust=None, dominentpol=row[13], light=row[14],
            latitude=row[15], longitude=row[16], timestamp=row[17], source=row[18]
        ).to_dict() for row in cs.fetchall()]


def get_one_day_data_kidbright():
    with pool.connection() as conn, conn.cursor() as cs:
        latest = fetch_latest_timestamp('kidbright', conn, cs)
        if not latest:
            return []

        cs.execute("""
            SELECT id, temperature, heartbeat_bpm, humidity, aqi, dew, pressure, wind, wind_gust,
                   light, latitude, longitude, timestamp, source
            FROM secondaryData
            WHERE source = 'kidbright' AND timestamp BETWEEN %s - INTERVAL 1 DAY AND %s
        """, (latest, latest))

        return [models.Measurement(
            id=row[0], temperature=row[1], heartbeat_bpm=row[2], humidity=row[3], aqi=row[4],
            pm25=None, pm10=None, o3=None, no2=None, co=None, so2=None, dew=row[5],
            pressure=row[6], wind=row[7], wind_gust=row[8], dominentpol=None, light=row[9],
            latitude=row[10], longitude=row[11], timestamp=row[12], source=row[13]
        ).to_dict() for row in cs.fetchall()]


def get_one_week_data_kidbright():
    with pool.connection() as conn, conn.cursor() as cs:
        latest = fetch_latest_timestamp('kidbright', conn, cs)
        if not latest:
            return []

        cs.execute("""
            SELECT id, temperature, heartbeat_bpm, humidity, aqi, dew, pressure, wind, wind_gust,
                   light, latitude, longitude, timestamp, source
            FROM secondaryData
            WHERE source = 'kidbright' AND timestamp BETWEEN %s - INTERVAL 7 DAY AND %s
        """, (latest, latest))

        return [models.Measurement(
            id=row[0], temperature=row[1], heartbeat_bpm=row[2], humidity=row[3], aqi=row[4],
            pm25=None, pm10=None, o3=None, no2=None, co=None, so2=None, dew=row[5],
            pressure=row[6], wind=row[7], wind_gust=row[8], dominentpol=None, light=row[9],
            latitude=row[10], longitude=row[11], timestamp=row[12], source=row[13]
        ).to_dict() for row in cs.fetchall()]


def get_one_day_data_tmd():
    with pool.connection() as conn, conn.cursor() as cs:
        latest = fetch_latest_timestamp('TMD', conn, cs)
        if not latest:
            return []

        cs.execute("""
            SELECT id, temperature, humidity, dew, pressure, wind, wind_gust,
                   latitude, longitude, timestamp, source
            FROM secondaryData
            WHERE source = 'TMD' AND timestamp BETWEEN %s - INTERVAL 1 DAY AND %s
        """, (latest, latest))

        return [models.Measurement(
            id=row[0], temperature=row[1], heartbeat_bpm=None, humidity=row[2], aqi=None,
            pm25=None, pm10=None, o3=None, no2=None, co=None, so2=None, dew=row[3],
            pressure=row[4], wind=row[5], wind_gust=row[6], dominentpol=None, light=None,
            latitude=row[7], longitude=row[8], timestamp=row[9], source=row[10]
        ).to_dict() for row in cs.fetchall()]


def get_one_week_data_tmd():
    with pool.connection() as conn, conn.cursor() as cs:
        latest = fetch_latest_timestamp('TMD', conn, cs)
        if not latest:
            return []

        cs.execute("""
            SELECT id, temperature, humidity, dew, pressure, wind, wind_gust,
                   latitude, longitude, timestamp, source
            FROM secondaryData
            WHERE source = 'TMD' AND timestamp BETWEEN %s - INTERVAL 7 DAY AND %s
        """, (latest, latest))

        return [models.Measurement(
            id=row[0], temperature=row[1], heartbeat_bpm=None, humidity=row[2], aqi=None,
            pm25=None, pm10=None, o3=None, no2=None, co=None, so2=None, dew=row[3],
            pressure=row[4], wind=row[5], wind_gust=row[6], dominentpol=None, light=None,
            latitude=row[7], longitude=row[8], timestamp=row[9], source=row[10]
        ).to_dict() for row in cs.fetchall()]
