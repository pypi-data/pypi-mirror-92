import time


def get_utc_timestamp(is_millisecond=True):
    timestamp = time.time()
    return int(timestamp * 1000) if is_millisecond else timestamp