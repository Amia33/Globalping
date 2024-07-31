# Amia33/Globalping

Globalping Automation

## Status

|  Task   |         Started          |          Ended           |
| :-----: | :----------------------: | :----------------------: |
| Measure | 2024-07-31T08:18:43.642Z | 2024-07-31T08:19:17.018Z |
|  Daily  | 1970-01-01T00:00:00.000Z | 1970-01-01T00:00:00.000Z |
| Weekly  | 1970-01-01T00:00:00.000Z | 1970-01-01T00:00:00.000Z |
| Monthly | 1970-01-01T00:00:00.000Z | 1970-01-01T00:00:00.000Z |
| Yearly  | 1970-01-01T00:00:00.000Z | 1970-01-01T00:00:00.000Z |

## Workflow

```mermaid
flowchart LR
  GI1 --> |locations|GI2
  GI2 --> GI3  --> GI4 --> MDB1 & MDB2 & MDB3
  GI3 --> |First id|GI2
  MDB1 --> MDB4
  MDB2 --> MDB5
  MDB3 --> H1
  MDB4 & MDB5 --> H2
  subgraph GlobalpingIo
    GI1(list_probes)
    GI2(create_measurement)
    GI3(measurement_ids)
    GI4(get_measurement)
  end
  subgraph MongoDB
    MDB1(results_temp)
    MDB2(measurements_temp)
    MDB3(probes)
    MDB4(results_daily)
    MDB5(measurements_daily)
  end
  subgraph Hexo
    H1(probes.md)
    H2(reports.md)
  end
```
