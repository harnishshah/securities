import snowflake.connector
from fastapi import Depends
import os

# Database Connection Details
def get_snowflake_conn():
    return
   # conn = snowflake.connector.connect(
       # user=os.getenv("SNOW_USER"),
     #   password=os.getenv("SNOW_PASS"),
      #  account=os.getenv("SNOW_ACCOUNT"),1
       # warehouse="INVEST_WH",
        #database="INVEST_DB",
        #schema="PUBLIC"11212
  #  try:
    #    yield conn
  #  finally:
     #   conn.close()