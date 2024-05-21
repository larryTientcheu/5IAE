import joblib
import numpy as np
import pandas as pd


def make_predictions(model_path, encoder_path, inputs):
    model = joblib.load_model(model_path)
    encoder = joblib.load_encoder(encoder_path)

    for input in inputs:
        input_df = pd.DataFrame([input])

    categorical_features = ["AIRLINE", "ORIGIN_AIRPORT", "DESTINATION_AIRPORT"]

    for feature in categorical_features:
        input_df[feature] = encoder[feature].transform(input_df[feature])

    input_df["SCHEDULED_DEPARTURE_HOUR"] = pd.to_datetime(
        input_df["SCHEDULED_DEPARTURE"]
    ).dt.hour
    input_df["SCHEDULED_DEPARTURE_MINUTE"] = pd.to_datetime(
        input_df["SCHEDULED_DEPARTURE"]
    ).dt.minute
    input_df["SCHEDULED_DEPARTURE_DAY_OF_WEEK"] = pd.to_datetime(
        input_df["SCHEDULED_DEPARTURE"]
    ).dt.dayofweek
    input_df["SCHEDULED_DEPARTURE_MONTH"] = pd.to_datetime(
        input_df["SCHEDULED_DEPARTURE"]
    ).dt.month

    # Drop the original datetime columns
    input_df = input_df.drop(["SCHEDULED_DEPARTURE"], axis=1)

    input_df = input_df[
        [
            "AIRLINE",
            "ORIGIN_AIRPORT",
            "DESTINATION_AIRPORT",
            "SCHEDULED_DEPARTURE_HOUR",
            "SCHEDULED_DEPARTURE_MINUTE",
            "SCHEDULED_DEPARTURE_DAY_OF_WEEK",
            "SCHEDULED_DEPARTURE_MONTH",
        ]
    ]

    predictions = model.predict(input_df)

    return predictions
