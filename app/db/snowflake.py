import snowflake.connector
import os

# Database Connection Details
def get_snowflake_conn():
    conn = snowflake.connector.connect(
        user=os.getenv("SNOW_USER"),
        password=os.getenv("SNOW_PASS"),
        account=os.getenv("SNOW_ACCOUNT"),
        warehouse="INVEST_WH",
        database="INVEST_DB",
        schema="PUBLIC"
    )
    try:
        yield conn
    finally:
        conn.close()