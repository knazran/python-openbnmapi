# Open BNM API

This is an unofficial Python wrapper for the Bank Negara Malaysia Open API. (https://api.bnm.gov.my/portal)

Currently supports the following endpoints:
- Base Rates/BLR
- Daily FX Turnover
- Exchange Rates
- Financial Consumer Alert
- Interbank Swap
- Interest Rate
- Interest Volume

### To - Do

Implement the following endpoints
- Islamic Interbank Rate
- Kijang Emas
- Overnight Policy Rate (OPR)
- Renminbi
- USD/MYR Interbank Intraday Rate
- Kuala Lumpur USD/MYR Reference Rate

Implement 
- support for date, year, month argument for relevant endpoints
- More proper error handling
- More robust input validation (Is this a valid bank code, currency code etc)
- Cache mechanism 
- Pandas dataframe support

