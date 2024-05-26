from pathlib import Path
import joblib
from joblib import Memory
import pandas as pd

# import time

memory = Memory(Path(__file__).parent / ".cachedir", verbose=0)


# Function to load pickle files
def load_pickles():
    # Configure the path to be the grand parent directory of helpers.py
    path = Path(__file__).parent.parent

    model_path = path / "tmodels/nn_model.pkl"
    label_encoder_path = path / "tmodels/label_encoders.pkl"

    model = joblib.load(model_path)
    encoder = joblib.load(label_encoder_path)
    return model, encoder


# Caching function to reduce model load time
def cached_load():
    loaded = memory.cache(load_pickles)
    return loaded()


def make_prediction(inputs):
    model, encoder = cached_load()  # type: ignore
    input_df = pd.DataFrame([inputs])

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

    prediction = model.predict(input_df)

    return prediction[0][0]


def load_dfs():
    path = Path(__file__).parent
    df_airline = pd.read_pickle(path / "airlines_dataframe")
    df_airports = pd.read_pickle(path / "airports_dataframe")
    return df_airline, df_airports


def format_prompt_response(prompt):
    df_airline, df_airports = load_dfs()

    prompt["airline"] = (
        prompt["airline"]
        + "("
        + df_airline[df_airline["CODE"] == prompt["airline"]]["AIRLINE"].iloc[0]
        + ")"
    )
    prompt["origin_airport"] = (
        prompt["origin_airport"]
        + "("
        + df_airports[df_airports["Airport_Code"] == prompt["origin_airport"]][
            "Airport_Name"
        ].iloc[0]
        + ")"
    )
    prompt["destination_airport"] = (
        prompt["destination_airport"]
        + "("
        + df_airports[df_airports["Airport_Code"] == prompt["destination_airport"]][
            "Airport_Name"
        ].iloc[0]
        + ")"
    )
    return prompt

    # Helper Test function
    # data = {
    #     "AIRLINE": "AS",
    #     "SCHEDULED_DEPARTURE": "2024-12-28 06:23:00",
    #     "ORIGIN_AIRPORT": "HOU",
    #     "DESTINATION_AIRPORT": "BOS",
    # }
    # start = time.time()
    # price = make_prediction(data)
    # end = time.time()
    # print("\nThe function took {:.2f} s to compute.".format(end - start))
    # print("\nThe price is:\n {}".format(price))


# prompt_test = {
#     "price": "660.51324",
#     "airline": "AA",
#     "destination_airport": "MIA",
#     "id": 22,
#     "origin_airport": "LAX",
#     "prompt": "What is the price tests test",
#     "scheduled_departure": "Fri, 24 May 2024 08:00:00 GMT",
#     "success": True,
# }

# print(format_prompt_response(prompt_test))
