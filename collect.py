import requests
import csv, json
from datetime import datetime

url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
csv_filename = "usdt_bob_prices.csv"


def get(asset: str = "USDT", trade_type: str = "SELL"):
    payload = {
        "asset": asset,
        "fiat": "BOB",
        "tradeType": trade_type,
        "transAmount": "",
        "page": 1,
        "rows": 10,
        "payTypes": [],
        "publisherType": None,
    }

    all_data = []
    while True:
        response = requests.post(url, json=payload)
        data = response.json()

        if not data["data"]:
            break

        all_data.extend(data["data"])
        payload["page"] += 1

    # Fecha actual para el registro
    now = int(datetime.now().timestamp())

    # Escribe los datos en un archivo CSV
    with open(csv_filename, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Escribir encabezados si el archivo está vacío
        if file.tell() == 0:
            headers = (
                ["index", "timestamp"]
                + list(all_data[0]["adv"].keys())
                + list(all_data[0]["advertiser"].keys())
            )
            writer.writerow(headers)

        index = 1
        for adv in all_data:
            row = (
                [index, now]
                + list(adv["adv"].values())
                + list(adv["advertiser"].values())
            )
            writer.writerow(row)
            index += 1

    print(f"Data written to {csv_filename}")


if __name__ == "__main__":
    get(trade_type="SELL")
    get(trade_type="BUY")
