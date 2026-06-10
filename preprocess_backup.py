import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

SEQ_LENGTH = 12

def load_data():
    train = pd.read_csv("data/raw/revenue/train.csv")
    stores = pd.read_csv("data/raw/revenue/stores.csv")

    return train, stores

def preprocess_data(train, stores):
    df = train.merge(stores, on="Store", how="left")

    df["Date"] = pd.to_datetime(df["Date"])

    df = df.sort_values(["Store", "Date"])

    df["Weekly_Sales"] = df["Weekly_Sales"].fillna(0)

    df["Type"] = df["Type"].map({
        "A": 0,
        "B": 1,
        "C": 2
    })

    df["IsHoliday"] = df["IsHoliday"].astype(int)

    df["Month"] = df["Date"].dt.month

    return df

def create_sequences(df, seq_length=SEQ_LENGTH):

    all_x = []
    all_y = []

    scaler = MinMaxScaler(feature_range=(0, 1))

    for store_id in df["Store"].unique()[:10]:

        store_df = (
            df[df["Store"] == store_id]
            .sort_values("Date")
            .copy()
        )

        sales = (
            store_df["Weekly_Sales"]
            .values
            .reshape(-1, 1)
        )

        sales_scaled = scaler.fit_transform(sales)

        for i in range(
            len(sales_scaled) - seq_length
        ):

            all_x.append(
                sales_scaled[i:i + seq_length]
            )

            all_y.append(
                sales_scaled[i + seq_length]
            )

    X = np.array(
        all_x,
        dtype=np.float32
    )

    y = np.array(
        all_y,
        dtype=np.float32
    )

    return X, y, scaler

if __name__ == "__main__":
    train, stores = load_data()

    df = preprocess_data(train, stores)

    X, y, scaler = create_sequences(df)

    print("Sequence shape:", X.shape)
    print("Target shape:", y.shape)