import sys
sys.path.insert(0,'..')
from chipmunkdb.ChipmunkDb import ChipmunkDb
import time
import pandas as pd


def loadNewDf():
    import duckdb
    import io
    con = duckdb.connect(database='minutelytestdata.duck', read_only=False)
    rel = con.execute("SELECT * FROM parquet_scan('minutelytestdata.parquet');")
    df = rel.df()

    df['Datetime'] = pd.to_datetime(df['__index_level_0__'])
    df = df.set_index(['Datetime'])

    return df

testdata = loadNewDf()

db = ChipmunkDb("localhost", 8091)

collections = db.collections()

print("Currently collections", collections)


collection = db.collection_info("testss")

if collection is not None and "rows" in collection:
    db.dropCollection("testss")

collection = db.collection_info("testss")

if collection is None or "rows" not in collection or collection["rows"] <= 0:
    # we create the empty colleciton
    df = testdata
    start = time.time()
   ## subset = df.loc[:, ["main:open", "main:close", "main:high", "main:low", "main:volume"]]
    db.save_as_pandas(df[["main:open", "main:close", "main:high", "main:low", "main:volume"]], "testss")
    end = time.time()
    print("create ohlc dataframe", end - start)


### lets read the data from the collection

start = time.time()
df = db.collection_as_pandas("testss")
end = time.time()
print("read dataframe", end - start)


start = time.time()
db.save_as_pandas(testdata[["ema_1:y"]], "testss", mode="append")
end = time.time()
print("appended two indicator columns", end - start)

start = time.time()
df = db.collection_as_pandas("testss")
end = time.time()
print("read dataframe with indicator again", end - start)


start = time.time()
half_indi = testdata[["color"]].tail(3)
db.save_as_pandas(half_indi, "testss", mode="append")
end = time.time()
print("appended only head(10) indicator column by datetime", end - start)

start = time.time()
df = db.collection_as_pandas("testss")
end = time.time()
print("read dataframe with half indicator again", end - start)

start = time.time()
half_indi = testdata[["color"]].head(3)
db.save_as_pandas(half_indi, "testss", mode="append")
end = time.time()
print("appended only tail(10) half indicator column by datetime", end - start)

start = time.time()
df = db.collection_as_pandas("testss")
end = time.time()
print("read dataframe with half indicator again", end - start)
print(df)

start = time.time()
d = db.query("SELECT * FROM testss LIMIT 10000")
end = time.time()
print("extract only a part out of it", end - start)

