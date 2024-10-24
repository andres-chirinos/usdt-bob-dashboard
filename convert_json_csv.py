import pandas as pd
from datetime import datetime
import collect, json

# Nombre del archivo CSV de entrada
input_csv_filename = "data/usdt_bob_prices.csv"

def json_set(x):
    if type(x)!=str:
        return None
    try:
        return eval(x)
    except Exception as err:
        print(err)

def process_csv(file_path):
    # Leer el archivo CSV
    df = pd.read_csv(file_path)

    # Eliminar columnas no deseadas
    columns_to_remove = ["index"]
    df.drop(columns=columns_to_remove, inplace=True)

    # Redondear los valores a 5 decimales
    int_columns = ["timestamp", "buyerRegDaysLimit", "monthOrderCount"]

    decimal_columns = [
        "priceFloatingRatio",
        "rateFloatingRatio",
        "currencyRate",
        "price",
        "initAmount",
        "surplusAmount",
        "tradableQuantity",
        "amountAfterEditing",
        "maxSingleTransAmount",
        "minSingleTransAmount",
        "payTimeLimit",
        "dynamicMaxSingleTransAmount",
        "minSingleTransQuantity",
        "maxSingleTransQuantity",
        "dynamicMaxSingleTransQuantity",
        "commissionRate",
        "monthFinishRate",
        "positiveRate",
    ]

    df[decimal_columns] = df[decimal_columns].map(
        lambda x: round(float(x), 5) if pd.notnull(x) else x
    )

    df[int_columns] = df[int_columns].fillna(0).map(lambda x: int(x))


    # Aplicar la función collect.listing a cada fila de las columnas relevantes
    df["tradeMethodCommissionRates"] = df["tradeMethodCommissionRates"].apply(
        lambda x: collect.listing(json_set(x), "paymentMethod", "commissionRate")
    )
    df["tradeMethods"] = df["tradeMethods"].apply(
        lambda x: collect.listing(json_set(x), "identifier","payType")
    )
    df["badges"] = df["badges"].apply(
        lambda x: collect.listing(json_set(x))
    )

    # Reordenar las columnas en el DataFrame
    column_order = [
        'timestamp', 'advNo', 'classify', 'tradeType', 'advStatus', 'priceType',
        'priceFloatingRatio', 'rateFloatingRatio', 'currencyRate', 'price',
        'initAmount', 'surplusAmount', 'tradableQuantity', 'amountAfterEditing',
        'maxSingleTransAmount', 'minSingleTransAmount', 'buyerKycLimit',
        'buyerRegDaysLimit', 'buyerBtcPositionLimit', 'payTimeLimit', 'tradeMethods',
        'takerAdditionalKycRequired', 'isTradable', 'dynamicMaxSingleTransAmount',
        'minSingleTransQuantity', 'maxSingleTransQuantity', 'dynamicMaxSingleTransQuantity',
        'commissionRate', 'tradeMethodCommissionRates', 'isSafePayment', 'userNo',
        'monthOrderCount', 'monthFinishRate', 'positiveRate', 'userType', 'userGrade',
        'userIdentity', 'badges', 'isBlocked', 'activeTimeInSecond'
    ]
    df = df[column_order]

    # Guardar los datos procesados en un nuevo archivo CSV
    #collect.append_or_create("data/processed_usdt_bob_prices.csv", df)
    collect.append_or_create("data/binance_usdt_bob_offers.csv", df)

    return df

if __name__ == "__main__":
    df = process_csv(input_csv_filename)
    aggregated_df = collect.aggregate_data(df)
    #print(aggregated_df.head())
