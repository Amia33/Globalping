"""Yearly"""

from os import (
    getenv,
    makedirs
)
from modules import (
    connect,
    gendates_yearly,
    output_yearly_report
)

targets = getenv("TARGETS").split(",")
conn_str = getenv("CONN_STR")

makedirs("results/source/_posts/yearly", exist_ok=True)
client = connect(conn_str)
dates = gendates_yearly()
output_yearly_report(targets, client, dates)
