"""
OpenNEM Diff Versions
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

from opennem.api.export.map import StatType
from opennem.core.compat import translate_id_v3_to_v2
from opennem.db import SessionLocal
from opennem.db.models.opennem import NetworkRegion
from opennem.schema.core import BaseModel
from opennem.schema.network import NetworkNEM, NetworkSchema
from opennem.utils.http import http

logger = logging.getLogger("opennem.diff.versions")

BASE_URL_V2 = "https://data.opennem.org.au"
BASE_URL_V3 = "https://data.dev.opennem.org.au"

CUR_YEAR = datetime.now().year


def get_v2_url(
    stat_type: StatType, network_region: str, bucket_size: str = "daily", year: int = CUR_YEAR
) -> str:
    """
    get v2 url

    https://data.opennem.org.au/power/tas1.json
    https://data.opennem.org.au/tas1/energy/daily/2021.json
    https://data.opennem.org.au/tas1/energy/monthly/all.json
    """

    url_components = []

    if stat_type == StatType.power:
        url_components = ["power", network_region.lower()]

    elif stat_type == StatType.energy and bucket_size == "monthly":
        url_components = [network_region.lower(), "energy", bucket_size, "all"]

    elif stat_type == StatType.energy and bucket_size == "daily":
        url_components = [network_region.lower(), "energy", bucket_size, str(year)]

    else:
        raise Exception("Invalid v2 url components")

    url_path = "/".join(url_components)
    url_path += ".json"

    url = urljoin(BASE_URL_V2, url_path)

    return url


def get_v3_url(
    stat_type: StatType, network_region: str, bucket_size: str = "daily", year: int = CUR_YEAR
) -> str:
    """
    Get v3 url

    https://data.dev.opennem.org.au/v3/stats/au/NEM/TAS1/power/7d.json
    https://data.dev.opennem.org.au/v3/stats/au/NEM/TAS1/energy/2021.json
    https://data.dev.opennem.org.au/v3/stats/au/NEM/TAS1/energy/all.json
    """

    url_components = [
        "v3",
        "stats",
        "au",
        "NEM",
        network_region.upper(),
        stat_type.value,
    ]

    if stat_type == StatType.power:
        url_components += [
            "7d",
        ]

    elif stat_type == StatType.energy and bucket_size == "monthly":
        url_components += ["all"]

    elif stat_type == StatType.energy and bucket_size == "daily":
        url_components += [str(year)]

    else:
        raise Exception("Invalid v2 url components")

    url_path = "/".join(url_components)
    url_path += ".json"

    url = urljoin(BASE_URL_V3, url_path)

    return url


def get_url_map(regions: List[str]) -> List[Dict[str, Any]]:
    urls = []

    for region in regions:
        url_set = {
            "v2": get_v2_url(StatType.power, region),
            "v3": get_v3_url(StatType.power, region),
        }
        urls.append(url_set)

        url_set = {
            "v2": get_v2_url(StatType.energy, region),
            "v3": get_v3_url(StatType.energy, region),
        }
        urls.append(url_set)

        url_set = {
            "v2": get_v2_url(StatType.energy, region, "monthly"),
            "v3": get_v3_url(StatType.energy, region, "monthly"),
        }
        urls.append(url_set)

    return urls


def validate_url_map(url_map: List[Dict[str, Any]]) -> bool:
    success = True

    for us in url_map:
        for version in ["v2", "v3"]:
            r = http.get(us[version])

            if not r.ok:
                logger.error("invalid {} url: {}".format(version, us[version]))
                success = False

    return success


def get_network_regions(network: NetworkSchema) -> List[NetworkRegion]:
    """Return regions for a network"""
    s = SessionLocal()
    regions = s.query(NetworkRegion).filter_by(network_id=network.code).all()

    codes = [r.code for r in regions]

    return codes


def get_id_diff(seriesv2: Dict, seriesv3: Dict) -> Optional[List[str]]:
    id2_diffs = sorted([i["id"] for i in seriesv2])
    id3_diffs = sorted([translate_id_v3_to_v2(i["id"]) for i in seriesv3])

    diff = list(set(id2_diffs) - set(id3_diffs))

    if len(diff) < 1:
        return None

    return diff


def get_data_by_id(id: str, series: List[Dict]) -> Optional[Dict]:
    id_s = list(filter(lambda x: x["id"] == id, series))

    if len(id_s) < 1:
        logger.error("Could not find id {} in series".format(id))
        return None

    return id_s.pop()


def run_diff() -> None:
    regions = get_network_regions(NetworkNEM)
    url_map = get_url_map(regions)
    # validate_url_map(url_map)

    network_region = "tas1"

    for network_region in regions:
        v2_power = http.get(get_v2_url(StatType.power, network_region)).json()
        v3_power = http.get(get_v3_url(StatType.power, network_region)).json()["data"]

        if len(v2_power) != len(v3_power):
            logger.info(
                "Series {} for {} is missing ids. v2 has {} v3 has {}".format(
                    StatType.power.value, network_region, len(v2_power), len(v3_power)
                )
            )

        id_diff = get_id_diff(v2_power, v3_power)

        if id_diff:
            for i in id_diff:
                logger.info(
                    "Series {} for {} is missing ids. v3 doesn't have {}".format(
                        StatType.power.value, network_region, i, (v3_power)
                    )
                )


if __name__ == "__main__":
    run_diff()
