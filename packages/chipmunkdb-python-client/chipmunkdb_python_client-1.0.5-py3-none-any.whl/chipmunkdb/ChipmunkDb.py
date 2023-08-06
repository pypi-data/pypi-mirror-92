import requests
import io
import pyarrow as pa
import pyarrow.parquet as pq
import json
import pandas as pd

class ChipmunkDb():
    def __init__(self, host, port=8091, autoConnect=True):
        self.host = host
        self.port = port
        self.autoConnect = autoConnect
        self.initialize()

    def connect(self):

        return True

    def initialize(self):
        if (self.autoConnect):
            self.connect()
        return True

    def getHostAndPort(self):
        return 'http://'+str(self.host)+":"+str(self.port)

    def create_from_pandas(self, collection, df):
        return self.savePandas(collection, df, mode="create")

    def dropCollection(self, collection):
        res = requests.delete(url=self.getHostAndPort()+"/collection/"+collection+"/drop", data={"collection": collection, "drop": True})
        return res.json()

    def collections(self):
        res = requests.get(url=self.getHostAndPort()+"/collections")
        return res.json()["collections"]

    def collection_info(self, collection):
        res = requests.get(url=self.getHostAndPort()+"/collection/"+collection)
        data = res.json()
        if "error" in data:
            return None
        return data["collection"]

    def save_as_pandas(self, df, collection, mode="append", domain=None):
        f = io.BytesIO()

        table = pa.Table.from_pandas(df)
        pq.write_table(table, f)

        f.seek(0, 0)
        res = requests.post(url=self.getHostAndPort()+'/collection/' + str(collection) + '/insertRaw',
                            files={"data": f.getvalue()},
                            headers={"Content-Type": 'application/octet-stream', "x-data": json.dumps({"mode": mode, "domain": domain})})
        f.close()
        return True

    def query(self, query, domain=None):
        domainQ = ""
        if domain is not None:
            domainQ = "&domain="+domain
        res = requests.get(url=self.getHostAndPort()+"/query?q="+query+domainQ, headers={"x-data": json.dumps({"streamed-response": "true"})})
        data = res.json()

        return data["result"]

    def dropColumn(self, collection, columns, domain=None):
        res = requests.delete(url=self.getHostAndPort() + "/collection/" + collection + "/dropColumns",
                           headers={"Content-Type": 'application/octet-stream',
                                    "x-data": json.dumps({"columns": columns, "domain": domain})})
        data = res.content

        return data

    def collection_as_pandas(self, collection, columns=[], domain=None):
        res = requests.get(url=self.getHostAndPort()+"/collection/"+collection+"/rawStream",
                           headers={"Content-Type": 'application/octet-stream', "x-data": json.dumps({"columns": columns, "domain": domain})})
        data = res.content

        pq_file = io.BytesIO(data)
        df = pd.read_parquet(pq_file)

        return df


def main():
    print("Running")