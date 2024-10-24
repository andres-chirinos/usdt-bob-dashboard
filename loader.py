import pandas as pd
import pytz
from datetime import datetime

data_csv_filename = "data/usdt_bob_prices.csv"
output_csv_filename = "data/usdt_bob_aggregated.csv"

# Función para cargar y verificar los datos
def load_and_verify_data(file_path):
    # Cargar los datos
    trade_df = pd.read_csv(file_path)

    # Verificar las columnas presentes en el DataFrame
    required_columns = ["timestamp", "price", "tradeType", "tradableQuantity", "monthOrderCount"]
    for col in required_columns:
        if col not in trade_df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Convertir el índice de timestamp a fechas en la zona horaria GMT-4
    gmt_minus_4 = pytz.timezone('Etc/GMT-4')
    trade_df['timestamp'] = pd.to_datetime(trade_df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert(gmt_minus_4)

    return trade_df

# Función para calcular precios OHLC y volumen
def calculate_ohlc(df, freq):
    ohlc_df = df.resample(freq, on='timestamp').agg(
        open=('price', 'first'),
        high=('price', 'max'),
        low=('price', 'min'),
        close=('price', 'last'),
        volume=('tradableQuantity', 'sum')
    ).reset_index()
    return ohlc_df

# Función para agrupar y exportar los datos
def aggregate_and_export_data(input_file, output_file, freq):
    # Cargar y verificar los datos
    trade_df = load_and_verify_data(input_file)

    # Calcular el primer cuartil de monthOrderCount
    q1 = trade_df['monthOrderCount'].quantile(0.25)

    print(trade_df.describe())
    # Filtrar las ofertas que se encuentren por encima del primer cuartil
    trade_df = trade_df[trade_df['monthOrderCount'] > q1]

    # Separar los datos de compra y venta
    buy_df = trade_df.query("tradeType == 'BUY'")
    sell_df = trade_df.query("tradeType == 'SELL'")

    # Calcular precios OHLC y volumen
    buy_ohlc_df = calculate_ohlc(buy_df, freq)
    sell_ohlc_df = calculate_ohlc(sell_df, freq)

    # Guardar los datos agregados en un archivo CSV
    buy_ohlc_df.to_csv(f"{output_file}_buy.csv", index=False)
    sell_ohlc_df.to_csv(f"{output_file}_sell.csv", index=False)

    print(f"Data aggregated and written to {output_file}_buy.csv and {output_file}_sell.csv")

if __name__ == "__main__":
    # Agrupar y exportar los datos por día
    aggregate_and_export_data(data_csv_filename, output_csv_filename, 'D')