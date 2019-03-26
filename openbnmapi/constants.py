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