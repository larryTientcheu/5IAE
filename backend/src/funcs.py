def format_input(airline, departure, origin, destination):
    single_input = {
        "AIRLINE": airline,
        "SCHEDULED_DEPARTURE": departure,
        "ORIGIN_AIRPORT": origin,
        "DESTINATION_AIRPORT": destination,
    }
    return single_input
