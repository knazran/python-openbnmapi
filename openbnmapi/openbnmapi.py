import json
import requests
import pandas as pd

from datetime import datetime, date

# Local modules
import constants

class OpenBNMAPI:
    
    """
    Initialise the OpenBNMAPy class.

    params:
    
    default_rtype: str
        Accepts either 'json' or 'dataframe'. Sets the default return type of data to either json or
        pandas DataFrame object. Defaults to 'json'.

    """
    def __init__(self, default_rtype = 'json'):
        self.base_url = constants.base_url
        self.headers = constants.headers
        self.default_rtype = default_rtype
        
        self.bank_codes = constants.SWIFT_codes
        
        self.interest_related_products = constants.interest_related_products
        self.exchange_rate_snapshots = constants.exchange_rate_snapshots

    """
    Helper function to send requests. Handles error codes and exceptions too.
    """ 
    def _send_get_request(self, req_url, params={}): 
        # Send request       
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
    Helper function to process date, year, month as additional parameters. 
    This is due to the fact that these arguments are to be processed as url path parameters

    returns: a valid url path parameter. eg: /date/{date} or /year/{year}/month/{month}
    rtype: string

    """
    def _parse_date_args(self, date, year, month):
        # Check is both date and year,month is being filled up. Either one of them can be inputed
        if (date) and (year and month):
            raise ValueError("Either 'date' or 'year, month' is accepted as arguments")
        
        if date:
            try:
                parsed_date = datetime.strptime(date, '%Y-%m-%d')
                print(parsed_date)

                # Only accept date arguments after year 2000 
                if (parsed_date.year > 2000) and (1 <= parsed_date.month <= 12):
                    # Craft return url
                    return_url = "/date/{}".format(date)
                    return return_url
                else:
                    yield ValueError('Year out of range. Please ensure year is more recent than 2000')
     
            except ValueError:
                raise ValueError("Incorrect date format, should be YYYY-MM-DD")
        
        # Check is year and month exists and is of type int
        if (year and month) and (type(year) == int) and (type(month) == int):
            if (year > 2000) and (1 <= month <= 12): # Needs a more elegant check
                # Craft return url
                return_url = "/year/{}/month/{}".format(year,month)
                return return_url
            else:
                raise ValueError("Incorrect year and month format. \
                                  Ensure year is more recent than 2000 and month is in range of [1...12]")
        
        # Default case. Return nothing
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
        args = self._parse_date_args(date, year, month)
        if args:
            req_url = req_url + args
        
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
        
        # Validation args
        if not quote['session'] in self.exchange_rate_snapshots:
            raise ValueError("Invalid exchange rate snapshots. Valid snapshots are: '0900', '1130', '1200', '1700'")
        if not quote['quote'] in ["rm", "fx"]:
            raise ValueError("Invalid quote. Valid quotes are: 'rm' and 'fx'")

        # Append additional arguments to the url if present
        """
        - Latest
        - Latest by Currency
        - By Currency and Date
        - By Currency and Month and Year
        """
        if currency_code:
            currency_code_error =   ("Invalid Currency Code.\n"
                                    "Please ensure your currency is in ISO 4217 standard format.\n"
                                    "Read more here: https://www.iso.org/iso-4217-currency-codes.html")
            
            if not (len(currency_code) == 3) or \
                currency_code not in constants.currency_codes:
                raise ValueError(currency_code_error)

            
            # Append Currency args first
            currency_args = "/{}".format(currency_code)
            req_url = req_url + currency_args

            # Then append date-related args, if present
            args = self._parse_date_args(date, year, month)
            if args:
                req_url = req_url + args
        
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
        args = self._parse_date_args(date, year, month)
        if args:
            req_url = req_url + args
        
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
        args = self._parse_date_args(date, year, month)
        if args:
            req_url = req_url + args
        
        # Handle the args params
        if not product in self.interest_related_products:
            raise ValueError("Invalid product type")

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

    Reference: https://api.bnm.gov.my/portal#tag/Interest-Volume
    """
    def interest_volume(self, product="money_market_operations", date=None, year=None, month=None, rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/interest-volume')
        
        # Append additional arguments to the url if present
        """
        - By Date (/date/{date})
        - By Month and Year (/year/{year}/month/{month})
        """
        args = self._parse_date_args(date, year, month)
        if args:
            req_url = req_url + args
        
        # Handle the args params
        if not product in self.interest_related_products:
            raise ValueError("Invalid product type")

        res = self._send_get_request(req_url, {"product":product})
        
        return self._return_response(res, rtype)

    """
    Get Islamic Interbank Rate

    Optional Parameters:
        
        date : string<date>
            Date with format as defined by RFC 3339, section 5.6 (YYYY-MM-DD)
        year: int
            Year in format 'YYYYY'. Must be after year 2000
        month: int
            Month in numeric format. [1...12]

    Reference: https://api.bnm.gov.my/portal#tag/Islamic-Interbank-Rate
    """
    def islamic_interback_rate(self, date=None, year=None, month=None, rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/islamic-interbank-rate')
        
        # Append additional arguments to the url if present
        """
        - By Date (/date/{date})
        - By Month and Year (/year/{year}/month/{month})
        """
        args = self._parse_date_args(date, year, month)
        if args:
            req_url = req_url + args
        
        res = self._send_get_request(req_url)
        
        return self._return_response(res, rtype)

    """
    Get Kijang Emas

    Optional Parameters:
        
        date : string<date>
            Date with format as defined by RFC 3339, section 5.6 (YYYY-MM-DD)
        year: int
            Year in format 'YYYYY'. Must be after year 2000
        month: int
            Month in numeric format. [1...12]

    Reference: https://api.bnm.gov.my/portal#tag/Kijang-Emas
    """
    def kijang_emas(self, date=None, year=None, month=None, rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/kijang-emas')
        
        # Append additional arguments to the url if present
        """
        - By Date (/date/{date})
        - By Month and Year (/year/{year}/month/{month})
        """
        args = self._parse_date_args(date, year, month)
        if args:
            req_url = req_url + args
        
        res = self._send_get_request(req_url)
        
        return self._return_response(res, rtype)

    """
    Get Overnight Policy Rate (OPR)

    Optional Parameters:
        
        year: int
            Year in format 'YYYYY'. Must be after year 2000

    Reference: https://api.bnm.gov.my/portal#tag/Overnight-Policy-Rate-(OPR)
    """
    def overnight_policy_rate(self, year=None, rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/opr')
        
        # Append additional arguments to the url if present
        """
        - By Year (/year/{year})
        """
        if year:
            if year > 2000:
                args = "/year/{}".format(year)
                req_url = req_url + args
        
        res = self._send_get_request(req_url)
        
        return self._return_response(res, rtype)
    
    """
    Get Renminbi Deposit Acceptance Rate

    Reference: https://api.bnm.gov.my/portal#tag/Renminbi
    """
    def renminbi_deposit_acceptance_rate(self, rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/renminbi-deposit-acceptance-rate')
        
        res = self._send_get_request(req_url)
        
        return self._return_response(res, rtype)
    
    """
    Get Renminbi Deposit Acceptance Rate

    Reference: https://api.bnm.gov.my/portal#tag/Renminbi
    """
    def renminbi_fx_forward_price(self, rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/renminbi-fx-forward-price')
        
        res = self._send_get_request(req_url)
        
        return self._return_response(res, rtype)
    
    """
    Get USD Interbank Intraday Rate

    Optional Parameters:
        
        date : string<date>
            Date with format as defined by RFC 3339, section 5.6 (YYYY-MM-DD)
        year: int
            Year in format 'YYYYY'. Must be after year 2000
        month: int
            Month in numeric format. [1...12]

    Reference: https://api.bnm.gov.my/portal#tag/USDMYR-Interbank-Intraday-Rate
    """
    def usd_interbank_intraday_rate(self, date=None, year=None, month=None, rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/usd-interbank-intraday-rate')
        
        # Append additional arguments to the url if present
        """
        - By Date (/date/{date})
        - By Month and Year (/year/{year}/month/{month})
        """
        args = self._parse_date_args(date, year, month)
        if args:
            req_url = req_url + args
        
        res = self._send_get_request(req_url)
        
        return self._return_response(res, rtype)

    """
    Get KL USD Reference Rate

    Optional Parameters:
        
        date : string<date>
            Date with format as defined by RFC 3339, section 5.6 (YYYY-MM-DD)
        year: int
            Year in format 'YYYYY'. Must be after year 2000
        month: int
            Month in numeric format. [1...12]

    Reference: https://api.bnm.gov.my/portal#tag/Kuala-Lumpur-USDMYR-Reference-Rate
    """
    def kl_usd_reference_rate(self, date=None, year=None, month=None, rtype = 'json'):
        # Form the request url
        req_url = "{}{}".format(self.base_url, '/kl-usd-reference-rate')
        
        # Append additional arguments to the url if present
        """
        - By Date (/date/{date})
        - By Month and Year (/year/{year}/month/{month})
        """
        args = self._parse_date_args(date, year, month)
        if args:
            req_url = req_url + args
        
        res = self._send_get_request(req_url)
        
        return self._return_response(res, rtype)
    
    

    
