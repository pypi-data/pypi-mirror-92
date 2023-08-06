import sys
sys.path.insert(0,'..')
from chipmunkdb.ChipmunkDb import ChipmunkDb
import time
import pandas as pd
from influxdb import DataFrameClient
from influxdb import InfluxDBClient

import duckdb
import io

db = ChipmunkDb("localhost", 8091)

db.dropColumn("testss", "color")


db.dropColumn("testdomain", "*", domain="chart1")