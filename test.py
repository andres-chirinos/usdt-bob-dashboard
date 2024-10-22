import requests
import csv
from datetime import datetime, timedelta

# Configuración de la API de Binance
url = "https://api.binance.com/api/v3/klines"
symbol = "USDTBOB"
interval = "1d"  # Intervalo de 1 día
start_date = "2022-01-01"  # Fecha de inicio
end_date = "2023-01-01"  # Fecha de fin

# Convertir las fechas a timestamps
start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)

# Función para obtener datos históricos
def get_historical_data(symbol, interval, start_timestamp, end_timestamp):
    data = []
    while start_timestamp < end_timestamp:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_timestamp,
            "endTime": end_timestamp,
            "limit": 1000
        }
        response = requests.get(url, params=params)
        response_data = response.json()
        print(response_data)
        if not response_data:
            break
        data.extend(response_data)
        start_timestamp = response_data[-1][0] + 1
    return data

# Obtener los datos históricos
historical_data = get_historical_data(symbol, interval, start_timestamp, end_timestamp)

# Guardar los datos en un archivo CSV
csv_filename = "usdt_bob_historical_prices.csv"
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])
    for entry in historical_data:
        writer.writerow(entry[:6])

print(f"Data written to {csv_filename}")