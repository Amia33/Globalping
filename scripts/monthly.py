"""Monthly"""

from os import (
    getenv,
    makedirs
)
from modules import (
    connect,
    gendates_monthly,
    output_monthly_report
)

targets = getenv("TARGETS").split(",")
conn_str = getenv("CONN_STR")

makedirs("results/source/_posts/monthly", exist_ok=True)
client = connect(conn_str)
dates = gendates_monthly()
output_monthly_report(targets, client, dates)
