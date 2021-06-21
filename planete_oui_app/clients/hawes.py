from pandas import DataFrame, read_csv
import os
import requests
from retrying import retry

class Hawes():
    """
    Hawes Api client class
    """
    
    url = os.getenv("HAWES_URL")
    
    def __init__(self, from_date, to_date):
        self.from_date = from_date
        self.to_date = to_date
    
    def _do_get(self):
        return requests.get("{}?from={}&to={}".format(self.url, self.from_date, self.to_date))
        
    def retry_if_connection_error(exception):
        return isinstance(exception, ConnectionError)
       
    @retry(retry_on_exception=retry_if_connection_error, wait_fixed=2000) 
    def call(self):
        try:
            response = self._do_get();
            df = DataFrame(response.json())
            return df
        except requests.RequestException as exception:
            raise str(exception)


