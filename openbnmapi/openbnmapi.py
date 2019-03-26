import json
import requests
import pandas as pd

class OpenBNMAPy:
    
    """
    Initialise the OpenBNMAPy class.

    params:
    
    default_rtype: str
        Accepts either 'json' or 'dataframe'. Sets the default return type of data to either json or
        pandas DataFrame object. Defaults to 'json'.

    """
    def __init__(self, default_rtype = 'json'):
        self.base_url = "https://api.bnm.gov.my/public"
        self.headers = {"Accept" : "application/vnd.BNM.API.v1+json"}
        self.default_rtype = default_rtype
        
        # TO DO: Move to 'constants' file
        self.bank_codes = ['BKKBMYKL', 'CIBBMYKL', 'CITIMYKL', 'HLBBMYKL', 'HBMBMYKL', 'ICBKMYKL', 
                            'MBBEMYKL', 'OCBCMYKL', 'PBBEMYKL', 'RHBBMYKL', 'SCBLMYKX', 'UOVBMYKL', 
                            'AIBBMYKL', 'ALSRMYKL', 'AISLMYKL', 'BIMBMYKL', 'BMMBMYKL', 'CTBBMYKL', 
                            'HLIBMYKL', 'HMABMYKL', 'KFHOMYKL', 'MBISMYKL', 'AFBQMYKL', 'OABBMYKL', 
                            'PUIBMYKL', 'RHBAMYKL', 'SCSRMYKK', 'AGOBMYKL', 'BSNAMYK1', 'PHBMMYKL', 
                            'MFBBMYKL', 'ARBKMYKL', 'BKCHMYKL', 'RJHIMYKL', 'BKRMMYKL']

    """
    Helper function to send requests. Handles error codes and exceptions too.
    """ 
    def _send_get_request(self, req_url, params={}): 
        # Send request       
        print(params)
        r = requests.get(req_url, headers=self.headers, params=params)
        
        # Handle Response
        if r.status_code == 200 or r.status_code == 201:
            return r
        else:
            return
            # To-Do: Handle error codes and exceptions here
            
    """
    Helper function to handle return types of data
    """
    def _return_response(self, response, rtype):
        if rtype is None:
            rtype = self.default_rtype
        if rtype =='json':
            return response.json()
        if rtype == 'df':
            # TO-DO: Handle to dataframes
            return
    
    """
    Helper function to validate date formats
    """
    def _validate_date(self, date, dformat="YYYY/MM/DD"):
        return
    
    """
    Get Base Rates / BLR

    Optional Parameters:
        
        bank_codes : string
            Must correspond to a valid 8 characters SWIFT code

    Reference: https://api.bnm.gov.my/portal#operation/BRLatest
    """
    def base_rate(self, bank_codes=None, rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/base-rate')
        
        # Append additional arguments to the url if present
        if bank_codes:
            # Validate if its a valid swift code
            if bank_codes in self.bank_codes:
                req_url = "{}/{}".format(req_url, bank_codes)
            else:
                # To-DO: Handle the exception for invalid params value
                raise ValueError("Wrong Swift Code")
        
        res = self._send_get_request(req_url)
        
        return self._return_response(res, rtype)
    
    """
    Get Daily FX Turnover

    Optional Parameters:
        
        date : string<date>
            Date with format as defined by RFC 3339, section 5.6 (YYYY-MM-DD)
        year: int
            Year in format 'YYYYY'. Must be after year 2000
        month: int
            Month in numeric format. [1...12]

    Reference: https://api.bnm.gov.my/portal#tag/Daily-FX-Turnover
    """
    def daily_fx_turnover(self, date=None, year=None, month=None, rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/fx-turn-over')
        
        # Append additional arguments to the url if present
        """
        - By Date (/date/{date})
        - By Month and Year (/year/{year}/month/{month})
        """
        
        res = self._send_get_request(req_url)
        
        return self._return_response(res, rtype)

    """
    Get Exchange Rates

    Optional Parameters:
        
        quote: dict{session : string, quote: string}
            session: string, 4 characters
                A snapshot of the exchange rate daily at 0900, 1130, 1200 and 1700 intervals
                Defaults to '1130'
                Valid values: ['0900', '1130', '1200', '1700']
            quote: string, 2 characters
                Base currency (Ringgit or foreign currency) as the denominator for the exchange rate
                Defaults to 'rm'
                Valid values: ['rm','fx']

        currency_code: string
            3-characters currency code based on ISO4217 standard

        date : string<date>
            Date with format as defined by RFC 3339, section 5.6 (YYYY-MM-DD)
        year: int
            Year in format 'YYYYY'. Must be after year 2000
        month: int
            Month in numeric format. [1...12]

    Reference: https://api.bnm.gov.my/portal#operation/ERLatest
    """
    def exchange_rate(self, quote={"session":"1130", "quote":"rm"}, currency_code=None, date=None, 
                      year=None, month=None,rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/exchange-rate')
        
        # Append additional arguments to the url if present
        """
        - Latest
        - Latest by Currency
        - By Currency and Date
        - By Currency and Month and Year
        """
        
        res = self._send_get_request(req_url, quote)
        
        return self._return_response(res, rtype)
    
    """
    Get Financial Consumer Alert

    Optional Parameters:
        
        search_query : string
            Must be < 50 characters

    Reference: https://api.bnm.gov.my/portal#tag/Financial-Consumer-Alert
    """
    def consumer_alert(self, search_query="", rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/consumer-alert')
        
        # Append additional arguments to the url path if present
        if (len(search_query) > 0) & (len(search_query) < 50):
            req_url = "{}/{}".format(req_url, search_query)
        
        res = self._send_get_request(req_url)
        
        return self._return_response(res, rtype)
    
    """
    Get InterBank Swaps

    Optional Parameters:
        
        date : string<date>
            Date with format as defined by RFC 3339, section 5.6 (YYYY-MM-DD)
        year: int
            Year in format 'YYYYY'. Must be after year 2000
        month: int
            Month in numeric format. [1...12]

    Reference: https://api.bnm.gov.my/portal#tag/Daily-FX-Turnover
    """
    def interbank_swap(self, date=None, year=None, month=None, rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/interbank-swap')
        
        # Append additional arguments to the url if present
        """
        - By Date (/date/{date})
        - By Month and Year (/year/{year}/month/{month})
        """
        
        res = self._send_get_request(req_url)
        
        return self._return_response(res, rtype)
    
    """
    Get Interest Rates

    Optional Parameters:
        product : string
            Provide selection of interbank rates or volumes from three choices; money market operations, 
            interbank or overall
            Defaults to 'money_market_operations'
            Valid values : 'money_market_operations', 'interbank', 'overall'

        date : string<date>
            Date with format as defined by RFC 3339, section 5.6 (YYYY-MM-DD)
        year: int
            Year in format 'YYYYY'. Must be after year 2000
        month: int
            Month in numeric format. [1...12]

    Reference: https://api.bnm.gov.my/portal#tag/Interest-Rate
    """
    def interest_rate(self, product="money_market_operations", date=None, year=None, month=None, rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/interest-rate')
        
        # Append additional arguments to the url if present
        """
        - By Date (/date/{date})
        - By Month and Year (/year/{year}/month/{month})
        """
        
        res = self._send_get_request(req_url, {"product":product})
        
        return self._return_response(res, rtype)

    """
    Get Interest Volume

    Optional Parameters:
        product : string
            Provide selection of interbank rates or volumes from three choices; money market operations, 
            interbank or overall
            Defaults to 'money_market_operations'
            Valid values : 'money_market_operations', 'interbank', 'overall'

        date : string<date>
            Date with format as defined by RFC 3339, section 5.6 (YYYY-MM-DD)
        year: int
            Year in format 'YYYYY'. Must be after year 2000
        month: int
            Month in numeric format. [1...12]

    Reference: https://api.bnm.gov.my/portal#tag/Interest-Rate
    """
    def interest_volume(self, product="money_market_operations", date=None, year=None, month=None, rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/interest-volume')
        
        # Append additional arguments to the url if present
        """
        - By Date (/date/{date})
        - By Month and Year (/year/{year}/month/{month})
        """
        
        res = self._send_get_request(req_url, {"product":product})
        
        return self._return_response(res, rtype)