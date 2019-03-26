import json
import requests
import pandas as pd

class OpenBNMAPy:
    
    def __init__(self, default_rtype = 'json'):
        self.base_url = "https://api.bnm.gov.my/public"
        self.headers = {"Accept" : "application/vnd.BNM.API.v1+json"}
        self.default_rtype = default_rtype
        
        # TO DO: Move to constants file
        self.swift_codes = ['BKKBMYKL', 'CIBBMYKL', 'CITIMYKL', 'HLBBMYKL', 'HBMBMYKL', 'ICBKMYKL', 
                            'MBBEMYKL', 'OCBCMYKL', 'PBBEMYKL', 'RHBBMYKL', 'SCBLMYKX', 'UOVBMYKL', 
                            'AIBBMYKL', 'ALSRMYKL', 'AISLMYKL', 'BIMBMYKL', 'BMMBMYKL', 'CTBBMYKL', 
                            'HLIBMYKL', 'HMABMYKL', 'KFHOMYKL', 'MBISMYKL', 'AFBQMYKL', 'OABBMYKL', 
                            'PUIBMYKL', 'RHBAMYKL', 'SCSRMYKK', 'AGOBMYKL', 'BSNAMYK1', 'PHBMMYKL', 
                            'MFBBMYKL', 'ARBKMYKL', 'BKCHMYKL', 'RJHIMYKL', 'BKRMMYKL']
        
    def _send_get_request(self, req_url, **params):
        # Parse params
        
        # Send request
        
        r = requests.get(req_url, headers=self.headers)
        
        # Handle Response
        if r.status_code == 200 or r.status_code == 201:
            return r
        else:
            return
            # To-Do: Handle error codes and exceptions here
            
    def _return_response(self, response, rtype):
        if rtype is None:
            rtype = self.default_rtype
        if rtype =='json':
            return response.json()
        if rtype == 'df':
            # TO-DO: Handle to dataframes
            return
        
    def _validate_date(self, date, dformat="YYYY/MM/DD"):
        return
    
    def base_rates(self, swift_code=None,rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/base-rate')
        
        # Append additional argument if present
        if swift_code:
            # Validate if its a valid swift code
            if swift_code in self.swift_codes:
                req_url = "{}/{}".format(req_url, swift_code)
            else:
                # To-DO: Handle the exception for invalid params value
                raise ValueError("Wrong Swift Code")
        
        res = self._send_get_request(req_url)
        
        return self._return_response(res, rtype)