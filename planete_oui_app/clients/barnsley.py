from pandas import DataFrame
import os
import requests
from retrying import retry

class Barnsley():
    """
    Barnsley Api client class
    """
    
    url = os.getenv("BARNSLEY_URL")
    
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
            df = DataFrame(response.json())
            
            #Return result with column modify for merging all result after
            return df.rename(
            columns={"start_time": "start", "end_time": "end", "value": "power"})
        except requests.RequestException as exception:
            raise str(exception)
        
