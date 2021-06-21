import os
import requests
from io import StringIO
from pandas import read_csv
from retrying import retry

class Hounslow():
    """
    Hounslow Api client class
    """
    
    url = os.getenv("HOUNSLOW_URL")
    
    def __init__(self, from_date: str, to_date: str):
        self.from_date = from_date
        self.to_date = to_date
        
    def _do_get(self):
        return requests.get("{}?from={}&to={}".format(self.url, self.from_date, self.to_date))
        
    def retry_if_connection_error(exception):
        return isinstance(exception, ConnectionError)

    @retry(retry_on_exception=retry_if_connection_error, wait_fixed=2000)
    def call(self):
            try:
                response = self._do_get()
                df = read_csv(StringIO(str(response.content, "utf-8")))
                
                #Return result with column modify for merging all result after
                df = df.rename(columns={"debut": "start", "fin": "end", "valeur": "power"})
                return df
            except requests.RequestException as exception:
                raise str(exception)