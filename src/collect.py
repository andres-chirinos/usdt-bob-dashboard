import requests, os
import pandas as pd
from datetime import datetime

#Const
url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
offers_csv_filename = "data/binance_usdt_bob_offers.csv"
currency_csv_filename = "data/currency_exchange_rates.csv"

#Utils
def listing(json, *objectives):
    if not json:
        return ""
    if not objectives:
        return '|'.join(map(str, json))
    return '|'.join(map(lambda x: ':'.join(str(x[obj]) for obj in objectives if obj in x), json))

def append_or_create(csv_filename,df):
    file_exists = os.path.isfile(csv_filename)
    if file_exists:
        with open(csv_filename, 'r') as f:
            file_empty = len(f.read().strip()) == 0
    else:
        file_empty = True
    
    df.to_csv(csv_filename, mode='a', header=file_empty, index=False)

def add_data_from_csv(df, csv_filename):
    if os.path.isfile(csv_filename):
        temp_df = pd.read_csv(csv_filename)
        df = pd.concat([df, temp_df], ignore_index=True)
    return df

#Obtain
def get_from_binance(asset: str = "USDT"):
    payload = {
        "asset": asset,
        "fiat": "BOB",
        "tradeType": "",
        "page": 1,
        "rows": 10,
        "payTypes": [],
        "countries": [],
        "publisherType": None,
    }

    time = int(datetime.now().timestamp())

    all_data = []
    for trade_type in ["BUY", "SELL"]:
        payload["tradeType"] = trade_type
        payload["page"] = 1  # Reset page number for each trade type
        while True:
            response = requests.post(url, json=payload)
            data = response.json()

            if not data["data"]:
                break

            all_data.extend(data["data"])
            payload["page"] += 1

    df = pd.DataFrame([{
        'timestamp': time,
        'advNo': adv['adv']['advNo'],
        'classify': adv['adv']['classify'],
        'tradeType': adv['adv']['tradeType'],
        'advStatus': adv['adv']['advStatus'],
        'priceType': adv['adv']['priceType'],
        'priceFloatingRatio': round(float(adv['adv']['priceFloatingRatio'] or 0), 5),
        'rateFloatingRatio': round(float(adv['adv']['rateFloatingRatio'] or 0), 5),
        'currencyRate': round(float(adv['adv']['currencyRate'] or 0), 5),
        'price': round(float(adv['adv']['price'] or 0), 5),
        'initAmount': round(float(adv['adv']['initAmount'] or 0), 5),
        'surplusAmount': round(float(adv['adv']['surplusAmount'] or 0), 5),
        'tradableQuantity': round(float(adv['adv']['tradableQuantity'] or 0), 5),
        'amountAfterEditing': round(float(adv['adv']['amountAfterEditing'] or 0), 5),
        'maxSingleTransAmount': round(float(adv['adv']['maxSingleTransAmount'] or 0), 5),
        'minSingleTransAmount': round(float(adv['adv']['minSingleTransAmount'] or 0), 5),
        'buyerKycLimit': adv['adv']['buyerKycLimit'],
        'buyerRegDaysLimit': int(adv['adv']['buyerRegDaysLimit'] or 0),
        'buyerBtcPositionLimit': adv['adv']['buyerBtcPositionLimit'],
        'payTimeLimit': round(float(adv['adv']['payTimeLimit'] or 0), 5),
        'tradeMethods': listing(adv['adv']['tradeMethods'], 'identifier', 'payType'),
        'takerAdditionalKycRequired': adv['adv']['takerAdditionalKycRequired'], 
        'isTradable': adv['adv']['isTradable'],
        'dynamicMaxSingleTransAmount': round(float(adv['adv']['dynamicMaxSingleTransAmount'] or 0), 5),
        'minSingleTransQuantity': round(float(adv['adv']['minSingleTransQuantity'] or 0), 5),
        'maxSingleTransQuantity': round(float(adv['adv']['maxSingleTransQuantity'] or 0), 5),
        'dynamicMaxSingleTransQuantity': round(float(adv['adv']['dynamicMaxSingleTransQuantity'] or 0), 5),
        'commissionRate': round(float(adv['adv']['commissionRate'] or 0), 5),
        'tradeMethodCommissionRates': listing(adv['adv']['tradeMethodCommissionRates'], 'paymentMethod', 'commissionRate'),
        'isSafePayment': adv['adv']['isSafePayment'],
        'userNo': adv['advertiser']['userNo'],
        'monthOrderCount': int(adv['advertiser']['monthOrderCount'] or 0),
        'monthFinishRate': round(float(adv['advertiser']['monthFinishRate'] or 0), 5),
        'positiveRate': round(float(adv['advertiser']['positiveRate'] or 0), 5),
        'userType': adv['advertiser']['userType'],
        'userGrade': adv['advertiser']['userGrade'],
        'userIdentity': adv['advertiser']['userIdentity'],
        'badges': listing(adv['advertiser']['badges']),
        'isBlocked': adv['advertiser']['isBlocked'],
        'activeTimeInSecond': adv['advertiser']['activeTimeInSecond']
    } for adv in all_data])

    append_or_create(offers_csv_filename, df)

    return df

def aggregate_data(df):
    # Agrupar por precio
    grouped_df = df.groupby(['price', 'tradeType','timestamp']).agg(
        advertisers_qty=('price', 'size'),
        available=('tradableQuantity', 'sum')
    ).reset_index()

    # Renombrar columnas
    grouped_df = grouped_df.rename(columns={
        'price': 'price',
        'available': 'available',
        'advertisers_qty': 'advertisers_qty',
        'tradeType': 'type',
        'timestamp': 'timestamp'
    })

    grouped_df['price'] = round(grouped_df['price'],5)
    grouped_df['available'] = round(grouped_df['available'],5)

    # Añadir columnas adicionales
    grouped_df['curr_from'] = grouped_df['type'].apply(lambda x: 'USDT' if x == 'SELL' else 'BOB')
    grouped_df['curr_to'] = grouped_df['type'].apply(lambda x: 'BOB' if x == 'SELL' else 'USDT')
    grouped_df['source'] = 'binance'

    # Reordenar columnas
    grouped_df = grouped_df[['price', 'available', 'advertisers_qty', 'type', 'timestamp', 'curr_from', 'curr_to', 'source']]
    append_or_create(currency_csv_filename, grouped_df)
    return grouped_df

if __name__ == "__main__":
    df = get_from_binance()
    #df = pd.read_csv("data/binance_usdt_bob_offers.csv")
    aggregated_df = aggregate_data(df)