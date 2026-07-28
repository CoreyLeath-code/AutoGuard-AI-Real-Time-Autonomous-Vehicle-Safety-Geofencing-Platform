import os

import snowflake.connector


def load_sensor_data():
    conn = snowflake.connector.connect(
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        account=os.environ["SNOWFLAKE_ACCOUNT"],
    )
    cs = conn.cursor()
    cs.execute("SELECT * FROM VEHICLE_SENSOR_DATA")
    return cs.fetchall()
