from __future__ import annotations

import asyncio
import math
import datetime
from dateutil import relativedelta
from asyncio import gather
from functools import reduce
import random
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Header, Query, status

from skyline_apiserver import schemas
from skyline_apiserver.api import deps
from skyline_apiserver.api.wrapper.openstack import OSPort, OSServer, OSVolume, OSVolumeSnapshot
from skyline_apiserver.api.wrapper.skyline import Port, Server, Service, Volume, VolumeSnapshot
from skyline_apiserver.client import utils
from skyline_apiserver.client.openstack import cinder, glance, keystone, neutron, nova
from skyline_apiserver.client.utils import generate_session, get_system_session
from skyline_apiserver.config import CONF
from skyline_apiserver.log import LOG
from skyline_apiserver.types import constants
from skyline_apiserver.utils.roles import assert_system_admin_or_reader, is_system_reader_no_admin

router = APIRouter()

@router.get(
    "/gec/co2_reduction_last_12_months",
    description="CO2 reduction last 12 months",
    responses={
        200: {"model": schemas.UsageReductionResponse},
    },
    response_model=schemas.UsageReductionResponse,
    status_code=status.HTTP_200_OK,
    response_description="OK",
)
async def co2_reduction_last_12_months(
    # profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
) -> schemas.UsageReductionResponse:
    # assert_system_admin_or_reader(
    #     profile=profile,
    #     exception="Not allowed.",
    # )

    response = {
        "my_servers": [
            {
                "id": "euro_mix",
                "value": 366.68,
            },
            {
                "id": "norway",
                "value": 106.32,
                "reduction_rate": 71.00469074,
            },
            {
                "id": "gec",
                "value": 42.64,
                "reduction_rate": 88.37133195,
            },
            {
                "id": "gec_with_contribution",
                "value": -2.24,
                "reduction_rate": 100.61088688,
            },
        ],
        "same_datacenter": [
            {
                "id": "euro_mix",
                "value": 1833.4,
            },
            {
                "id": "norway",
                "value": 531.6,
                "reduction_rate": 71.00469074,
            },
            {
                "id": "gec",
                "value": 213.2,
                "reduction_rate": 88.37133195,
            },
            {
                "id": "gec_with_contribution",
                "value": -11.2,
                "reduction_rate": 100.61088688,
            },
        ],
        "gec_total": [
            {
                "id": "euro_mix",
                "value": 9167,
            },
            {
                "id": "norway",
                "value": 2658,
                "reduction_rate": 71.00469074,
            },
            {
                "id": "gec",
                "value": 1066,
                "reduction_rate": 88.37133195,
            },
            {
                "id": "gec_with_contribution",
                "value": -56,
                "reduction_rate": 100.61088688,
            },
        ],
    }

    return schemas.UsageReductionResponse(**response)

@router.get(
    "/gec/co2_reduction_last_30_days",
    description="CO2 reduction last 30 days",
    responses={
        200: {"model": schemas.UsageReductionResponse},
    },
    response_model=schemas.UsageReductionResponse,
    status_code=status.HTTP_200_OK,
    response_description="OK",
)
async def co2_reduction_last_30_days(
    # profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
) -> schemas.UsageReductionResponse:
    # assert_system_admin_or_reader(
    #     profile=profile,
    #     exception="Not allowed.",
    # )

    response = {
        "my_servers": [
            {
                "id": "euro_mix",
                "value": 30.55666667,
            },
            {
                "id": "norway",
                "value": 8.86,
                "reduction_rate": 71.00469074,
            },
            {
                "id": "gec",
                "value": 3.55333333,
                "reduction_rate": 88.37133195,
            },
            {
                "id": "gec_with_contribution",
                "value": -0.18666667,
                "reduction_rate": 100.61088688,
            },
        ],
        "same_datacenter": [
            {
                "id": "euro_mix",
                "value": 152.78333333,
            },
            {
                "id": "norway",
                "value": 44.3,
                "reduction_rate": 71.00469074,
            },
            {
                "id": "gec",
                "value": 17.76666667,
                "reduction_rate": 88.37133195,
            },
            {
                "id": "gec_with_contribution",
                "value": -0.93333333,
                "reduction_rate": 100.61088688,
            },
        ],
        "gec_total": [
            {
                "id": "euro_mix",
                "value": 763.91666667,
            },
            {
                "id": "norway",
                "value": 221.5,
                "reduction_rate": 71.00469074,
            },
            {
                "id": "gec",
                "value": 88.83333333,
                "reduction_rate": 88.37133195,
            },
            {
                "id": "gec_with_contribution",
                "value": -4.66666667,
                "reduction_rate": 100.61088688,
            },
        ],
    }

    return schemas.UsageReductionResponse(**response)

@router.get(
    "/gec/co2_history",
    description="CO2 history",
    responses={
        200: {"model": schemas.UsageResponse},
    },
    response_model=schemas.UsageResponse,
    status_code=status.HTTP_200_OK,
    response_description="OK",
)
async def co2_history(
    # profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
) -> schemas.UsageResponse:
    # assert_system_admin_or_reader(
    #     profile=profile,
    #     exception="Not allowed.",
    # )

    response = {
        "data_points": [{
            "euro_mix": random.randint(200, 300),
            "norway": random.randint(80, 150),
            "gec": None,
            "time": (datetime.date(2018 + n, 1, 1)).isoformat()
        } for n in range(0, 4)]
    }

    return schemas.UsageResponse(**response)

@router.get(
    "/gec/power_reduction_last_12_months",
    description="Power reduction last 12 months",
    responses={
        200: {"model": schemas.UsageReductionResponse},
    },
    response_model=schemas.UsageReductionResponse,
    status_code=status.HTTP_200_OK,
    response_description="OK",
)
async def power_reduction_last_12_months(
    # profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
) -> schemas.UsageReductionResponse:
    # assert_system_admin_or_reader(
    #     profile=profile,
    #     exception="Not allowed.",
    # )

    response = {
        "my_servers": [
            {
                "id": "euro_mix",
                "value": 1608000,
            },
            {
                "id": "norway",
                "value": 1256000,
                "reduction_rate": 21.89054726,
            },
            {
                "id": "gec",
                "value": 860000,
                "reduction_rate": 46.51741294,
            },
        ],
        "same_datacenter": [
            {
                "id": "euro_mix",
                "value": 8040000,
            },
            {
                "id": "norway",
                "value": 6280000,
                "reduction_rate": 21.89054726,
            },
            {
                "id": "gec",
                "value": 4300000,
                "reduction_rate": 46.51741294,
            },
        ],
        "gec_total": [
            {
                "id": "euro_mix",
                "value": 40200000,
            },
            {
                "id": "norway",
                "value": 31400000,
                "reduction_rate": 21.89054726,
            },
            {
                "id": "gec",
                "value": 21500000,
                "reduction_rate": 46.51741294,
            },
        ],
    }

    return schemas.UsageReductionResponse(**response)

@router.get(
    "/gec/power_reduction_last_30_days",
    description="Power reduction last 30 days",
    responses={
        200: {"model": schemas.UsageReductionResponse},
    },
    response_model=schemas.UsageReductionResponse,
    status_code=status.HTTP_200_OK,
    response_description="OK",
)
async def power_reduction_last_30_days(
    # profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
) -> schemas.UsageReductionResponse:
    # assert_system_admin_or_reader(
    #     profile=profile,
    #     exception="Not allowed.",
    # )

    response = {
        "my_servers": [
            {
                "id": "euro_mix",
                "value": 134000,
            },
            {
                "id": "norway",
                "value": 104666.66666667,
                "reduction_rate": 21.89054726,
            },
            {
                "id": "gec",
                "value": 71666.66666667,
                "reduction_rate": 46.51741294,
            },
        ],
        "same_datacenter": [
            {
                "id": "euro_mix",
                "value": 670000,
            },
            {
                "id": "norway",
                "value": 523333.33333333,
                "reduction_rate": 21.89054726,
            },
            {
                "id": "gec",
                "value": 358333.33333333,
                "reduction_rate": 46.51741294,
            },
        ],
        "gec_total": [
            {
                "id": "euro_mix",
                "value": 3350000,
            },
            {
                "id": "norway",
                "value": 2616666.66666667,
                "reduction_rate": 21.89054726,
            },
            {
                "id": "gec",
                "value": 1791666.66666667,
                "reduction_rate": 46.51741294,
            },
        ],
    }

    return schemas.UsageReductionResponse(**response)

@router.get(
    "/gec/power_history",
    description="Power history",
    responses={
        200: {"model": schemas.UsageResponse},
    },
    response_model=schemas.UsageResponse,
    status_code=status.HTTP_200_OK,
    response_description="OK",
)
async def co2_history(
    # profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
) -> schemas.UsageResponse:
    # assert_system_admin_or_reader(
    #     profile=profile,
    #     exception="Not allowed.",
    # )

    response = {
        "data_points": [{
            "euro_mix": random.randint(200, 300),
            "norway": random.randint(80, 150),
            "gec": None,
            "time": (datetime.date(2018 + n, 1, 1)).isoformat()
        } for n in range(0, 4)]
    }

    return schemas.UsageResponse(**response)

@router.get(
    "/gec/co2_usage",
    description="CO2 usage",
    responses={
        200: {"model": schemas.UsageResponse},
    },
    response_model=schemas.UsageResponse,
    status_code=status.HTTP_200_OK,
    response_description="OK",
)
async def co2_usage(
    # profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
) -> schemas.UsageResponse:
    # assert_system_admin_or_reader(
    #     profile=profile,
    #     exception="Not allowed.",
    # )

    now = datetime.datetime.now()
    response = {
        "data_points": [{
            "euro_mix": random.randint(2000, 2500),
            "norway": random.randint(1500, 2200),
            "gec": random.randint(1200, 1450),
            "time": (now + datetime.timedelta(seconds=30 * n)).astimezone().isoformat()
        } for n in range(0, 200)]
    }

    return schemas.UsageResponse(**response)

@router.get(
    "/gec/power_usage",
    description="Power usage",
    responses={
        200: {"model": schemas.UsageResponse},
    },
    response_model=schemas.UsageResponse,
    status_code=status.HTTP_200_OK,
    response_description="OK",
)
async def power_usage(
    # profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
) -> schemas.UsageResponse:
    # assert_system_admin_or_reader(
    #     profile=profile,
    #     exception="Not allowed.",
    # )

    now = datetime.datetime.now()
    response = {
        "data_points": [{
            "euro_mix": random.randint(2000, 2500),
            "norway": random.randint(1500, 2200),
            "gec": random.randint(1200, 1450),
            "time": (now + datetime.timedelta(seconds=30 * n)).astimezone().isoformat()
        } for n in range(0, 200)]
    }

    return schemas.UsageResponse(**response)
