import sys
sys.path.insert(0,'..')
from chipmunkdb.ChipmunkDb import ChipmunkDb
import time
import pandas as pd
from influxdb import DataFrameClient
from influxdb import InfluxDBClient

import duckdb
import io

### loading all samples for domains
con = duckdb.connect(database='testdata.duck', read_only=False)
rel = con.execute("SELECT * FROM parquet_scan('minutelytestdata.parquet');")
testdata = rel.df()
testdata['Datetime'] = pd.to_datetime(testdata['__index_level_0__'])
testdata = testdata.set_index(['Datetime'])

rel = con.execute("SELECT * FROM parquet_scan('fiveminutetestdata.parquet');")
fiveminutetestdata = rel.df()
fiveminutetestdata['Datetime'] = pd.to_datetime(fiveminutetestdata['__index_level_0__'])
fiveminutetestdata = fiveminutetestdata.set_index(['Datetime'])

rel = con.execute("SELECT * FROM parquet_scan('hourlytestdata.parquet');")
hourlytestdata = rel.df()
hourlytestdata['Datetime'] = pd.to_datetime(hourlytestdata['__index_level_0__'])
hourlytestdata = hourlytestdata.set_index(['Datetime'])

db = ChipmunkDb("localhost", 8091)

collections = db.collections()

print("Currently collections", collections)

collection = db.collection_info("testdomain")

if collection is not None and "rows" in collection:
    db.dropCollection("testdomain")

collection = db.collection_info("testdomain")

start = time.time()
## subset = df.loc[:, ["main:open", "main:close", "main:high", "main:low", "main:volume"]]
db.save_as_pandas(testdata[["main:open", "main:close", "main:high", "main:low", "main:volume"]], "testdomain", domain="chart1")
db.save_as_pandas(fiveminutetestdata[["main:open", "main:close", "main:high", "main:low", "main:volume"]], "testdomain", domain="chart2")
db.save_as_pandas(hourlytestdata[["main:open", "main:close", "main:high", "main:low", "main:volume"]], "testdomain", domain="chart3")
end = time.time()
print("create ohlc dataframe", end - start)


### lets read the data from the collection

start = time.time()
df = db.collection_as_pandas("testdomain", domain="chart1")
end = time.time()
print("read dataframe", end - start)

print(df)

start = time.time()
db.save_as_pandas(testdata[["ema_1:y"]], "testdomain", mode="append", domain="chart1")
end = time.time()
print("appended two indicator columns", end - start)

start = time.time()
df = db.collection_as_pandas("testdomain", domain="chart1")
end = time.time()
print("read dataframe with indicator again", end - start)

print(df)


start = time.time()
df = db.collection_as_pandas("testdomain")
end = time.time()
print("read complete dataframe with indicator again", end - start)

print(df)




start = time.time()
half_indi = testdata[["color"]].tail(3)
db.save_as_pandas(half_indi, "testdomain", mode="append", domain="chart1")
end = time.time()
print("appended only head(10) indicator column by datetime", end - start)

start = time.time()
df = db.collection_as_pandas("testdomain")
end = time.time()
print("read dataframe with half indicator again", end - start)

start = time.time()
half_indi = testdata[["color"]].head(3)
db.save_as_pandas(half_indi, "testdomain", mode="append", domain="chart1")
end = time.time()
print("appended only tail(10) half indicator column by datetime", end - start)

start = time.time()
df = db.collection_as_pandas("testdomain", domain="chart1")
end = time.time()
print("read dataframe with half indicator again", end - start)
print(df)

start = time.time()
d = db.query("SELECT * FROM testdomain LIMIT 10000", domain="chart1")
end = time.time()
print("extract only a part out of it", end - start)

