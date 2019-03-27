# Constants added here to make updating/editing parameters easier

#######
# URL #
#######

base_url = "https://api.bnm.gov.my/public"
headers = {
	"Accept" : "application/vnd.BNM.API.v1+json"
}

###########
# BANKING #
###########

# SWIFT codes for supported banks (https://www.swiftcodes.info/malaysia/)
SWIFT_codes = ['BKKBMYKL', 'CIBBMYKL', 'CITIMYKL', 'HLBBMYKL', 'HBMBMYKL', 'ICBKMYKL', 
	          'MBBEMYKL', 'OCBCMYKL', 'PBBEMYKL', 'RHBBMYKL', 'SCBLMYKX', 'UOVBMYKL', 
	          'AIBBMYKL', 'ALSRMYKL', 'AISLMYKL', 'BIMBMYKL', 'BMMBMYKL', 'CTBBMYKL', 
	          'HLIBMYKL', 'HMABMYKL', 'KFHOMYKL', 'MBISMYKL', 'AFBQMYKL', 'OABBMYKL', 
	          'PUIBMYKL', 'RHBAMYKL', 'SCSRMYKK', 'AGOBMYKL', 'BSNAMYK1', 'PHBMMYKL', 
	          'MFBBMYKL', 'ARBKMYKL', 'BKCHMYKL', 'RJHIMYKL', 'BKRMMYKL']

# Other types of instituions
interest_related_products = ["money_market_operations", "interbank", "overall"]

# What times to take snapshots of
exchange_rate_snapshots = ["0900" "1130" "1200" "1700"]

# Currency Codes
currency_codes = ["AFN", "EUR", "ALL", "DZD", "USD", "AOA", "XCD", "ARS", "AMD", "AWG", "AUD", "AZN", "BSD", "BHD", "BDT", "BBD", "BYN", "BZD", "XOF", "BMD", "INR", "BTN", "BOB", "BOV", "BAM", "BWP", "NOK", "BRL", "BND", "BGN", "BIF", "CVE", "KHR", "XAF", "CAD", "KYD", "CLP", "CLF", "CNY", "COP", "COU", "KMF", "CDF", "NZD", "CRC", "HRK", "CUP", "CUC", "ANG", "CZK", "DKK", "DJF", "DOP", "EGP", "SVC", "ERN", "ETB", "FKP", "FJD", "XPF", "GMD", "GEL", "GHS", "GIP", "GTQ", "GBP", "GNF", "GYD", "HTG", "HNL", "HKD", "HUF", "ISK", "IDR", "XDR", "IRR", "IQD", "ILS", "JMD", "JPY", "JOD", "KZT", "KES", "KPW", "KRW", "KWD", "KGS", "LAK", "LBP", "LSL", "ZAR", "LRD", "LYD", "CHF", "MOP", "MKD", "MGA", "MWK", "MYR", "MVR", "MRU", "MUR", "XUA", "MXN", "MXV", "MDL", "MNT", "MAD", "MZN", "MMK", "NAD", "NPR", "NIO", "NGN", "OMR", "PKR", "PAB", "PGK", "PYG", "PEN", "PHP", "PLN", "QAR", "RON", "RUB", "RWF", "SHP", "WST", "STN", "SAR", "RSD", "SCR", "SLL", "SGD", "XSU", "SBD", "SOS", "SSP", "LKR", "SDG", "SRD", "SZL", "SEK", "CHE", "CHW", "SYP", "TWD", "TJS", "TZS", "THB", "TOP", "TTD", "TND", "TRY", "TMT", "UGX", "UAH", "AED", "USN", "UYU", "UYI", "UYW", "UZS", "VUV", "VES", "VND", "YER", "ZMW", "ZWL", "XBA", "XBB", "XBC", "XBD", "XTS", "XXX", "XAU", "XPD", "XPT", "XAG"]