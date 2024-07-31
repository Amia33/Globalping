"""Measure"""

from os import getenv
from modules import (
    list_probe,
    create_measurement,
    get_measurement,
    connect,
    write_probe_id,
    write_measurement,
    write_result
)

targets = getenv("TARGETS").split(",")
conn_str = getenv("CONN_STR")

locations = list_probe()
measurement_ids = create_measurement(targets, locations)
measurements = get_measurement(measurement_ids)
client = connect(conn_str)
probes_written = write_probe_id(measurements, client)
write_measurement(probes_written, client)
write_result(probes_written, client)
