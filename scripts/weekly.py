"""Weekly"""

from os import (
    getenv,
    makedirs
)
from modules import (
    connect,
    gendates_weekly,
    output_weekly_report
)

targets = getenv("TARGETS").split(",")
conn_str = getenv("CONN_STR")

makedirs("results/source/_posts/weekly", exist_ok=True)
client = connect(conn_str)
dates = gendates_weekly()
output_weekly_report(targets, client, dates)
