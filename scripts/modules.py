"""Modules"""

from time import sleep
from datetime import (
    datetime,
    timezone,
    timedelta
)
from pymongo import MongoClient
from pandas import DataFrame
import requests


def list_probe():
    """List probes currently online"""
    locations = []
    dest = "https://api.globalping.io/v1/probes"
    head = {
        "User-Agent": "ping.amia.work (https://github.com/Amia33/Globalping)",
        "Accept-Encoding": "gzip",
        "Accept": "application/json"
    }
    resp = requests.get(url=dest, headers=head, timeout=15)
    probes = resp.json()
    for probe in probes:
        magic = {
            "magic": probe["location"]["country"] + "+" + probe["location"]["city"]
        }
        if magic not in locations:
            locations.append(magic)
    return locations


def create_measurement(targets, locations):
    """Create a measurement"""
    measurement_ids = []
    dest = "https://api.globalping.io/v1/measurements"
    head = {
        "User-Agent": "ping.amia.work (https://github.com/Amia33/Globalping)",
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "type": "ping",
        "target": "",
        "locations": "",
        "measurementOptions": {
            "packets": 16
        }
    }
    for target in targets:
        if measurement_ids:
            locations = measurement_ids[0]
        data["target"] = target
        data["locations"] = locations
        resp = requests.post(url=dest, headers=head, json=data, timeout=15)
        measurement_id = resp.json()["id"]
        measurement_ids.append(measurement_id)
    return measurement_ids


def get_measurement(measurement_ids):
    """Get a measurement by ID"""
    measurements = []
    head = {
        "User-Agent": "ping.amia.work (https://github.com/Amia33/Globalping)",
        "Accept-Encoding": "gzip",
        "Accept": "application/json"
    }
    for measurement_id in measurement_ids:
        dest = "https://api.globalping.io/v1/measurements/" + measurement_id
        resp = requests.get(url=dest, headers=head, timeout=15)
        measurement = resp.json()
        while measurement["status"] == "in-progress":
            sleep(0.5)
            resp = requests.get(url=dest, headers=head, timeout=15)
            measurement = resp.json()
        filtered_results = []
        for result in measurement["results"]:
            if result["result"]["status"] != "finished":
                continue
            if not result["result"]["timings"]:
                continue
            filtered_results.append(result)
        measurement["results"] = filtered_results
        measurements.append(measurement)
    return measurements


def connect(conn_str):
    """Connect to MongoDB Atlas"""
    client = MongoClient(conn_str)["globalping"]
    return client


def write_probe_id(measurements, client):
    "Write probe id"
    for measurement in measurements:
        current_probes = DataFrame(client["probes"].find())
        upload = []
        try:
            new_probe = current_probes["_id"].tolist()[-1] + 1
        except KeyError:
            new_probe = 1
        for result in measurement["results"]:
            try:
                search_probes = current_probes.loc[
                    (current_probes["region"] == result["probe"]["region"]) &
                    (current_probes["country"] == result["probe"]["country"]) &
                    (current_probes["city"] == result["probe"]["city"]) &
                    (current_probes["asn"] == result["probe"]["asn"]) &
                    (current_probes["network"] == result["probe"]["network"]) &
                    (current_probes["latitude"] == result["probe"]["latitude"]) &
                    (current_probes["longitude"] ==
                     result["probe"]["longitude"])
                ]
            except KeyError:
                create_probe = True
            else:
                create_probe = search_probes.empty
            finally:
                if create_probe is True:
                    probe_id = new_probe
                    probe_data = {
                        "_id": probe_id,
                        "region": result["probe"]["region"],
                        "country": result["probe"]["country"],
                        "city": result["probe"]["city"],
                        "asn": result["probe"]["asn"],
                        "network": result["probe"]["network"],
                        "latitude": result["probe"]["latitude"],
                        "longitude": result["probe"]["longitude"],
                    }
                    upload.append(probe_data)
                    new_probe += 1
                else:
                    probe_id = search_probes["_id"].tolist()[0]
            result["probe"] = probe_id
        if upload:
            client["probes"].insert_many(upload)
    return measurements


def write_measurement(probes_written, client):
    """Write measurement"""
    upload = []
    colle = "measurements-" + datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for measurement in probes_written:
        created_time = datetime.strptime(
            measurement["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
        updated_time = datetime.strptime(
            measurement["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
        duration = (updated_time - created_time).total_seconds()
        probe_ids = []
        for result in measurement["results"]:
            probe_ids.append(result["probe"])
        measurement_data = {
            "_id": measurement["id"],
            "target": measurement["target"],
            "duration": duration,
            "probe_ids": probe_ids
        }
        upload.append(measurement_data)
    client[colle].insert_many(upload)


def write_result(probes_written, client):
    """Write result"""
    upload = []
    colle = "results-" + datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for measurement in probes_written:
        for result in measurement["results"]:
            rtts = []
            for packet in result["result"]["timings"]:
                rtts.append(packet["rtt"])
            result_data = {
                "_id": measurement["id"] + "-" + str(result["probe"]),
                "timings": {
                    "min": result["result"]["stats"]["min"],
                    "max": result["result"]["stats"]["max"],
                    "total": round(sum(rtts), 3)
                },
                "packets": {
                    "total": result["result"]["stats"]["total"],
                    "rcv": result["result"]["stats"]["rcv"]
                }
            }
            upload.append(result_data)
    client[colle].insert_many(upload)
