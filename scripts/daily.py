"""Daily"""

from os import (
    getenv,
    makedirs
)
from modules import (
    connect,
    write_daily,
    drop_colle,
    output_probes,
    output_daily_report
)

targets = getenv("TARGETS").split(",")
conn_str = getenv("CONN_STR")

makedirs("results/source/_posts/daily", exist_ok=True)
client = connect(conn_str)
write_daily(targets, client)
drop_colle(client)
output_probes(client)
output_daily_report(targets, client)
