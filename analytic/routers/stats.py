from typing import Dict, Union

from fastapi import APIRouter, Body, status

from analysis_worker import *
from routers.models import DeviceStatsRequest, StatsResponse, UserStatsRequest

stats_router = APIRouter()

start_time_default = "1970-01-01T00:00:00Z"
stop_time_default = ""


def _dict_stats_to_statresponce(stats: Dict):
    return StatsResponse(
        min=stats["min"],
        max=stats["max"],
        count=stats["count"],
        sum=stats["sum"],
        median=stats["median"],
    )


@stats_router.post(
    "/device",
    response_model=StatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get statistics by device",
    description="Retrieve statistics for a specific device over a given time period.\
    You need to provide a device statistics request model.",
)
async def get_stats_by_device(
    device: DeviceStatsRequest = Body(
        ...,
        example={
            "device_id": 1,
            "metric_key": "x",
            # can be written in iso format with Z at the end
            # example: 2024-03-16T08:29:02.027960Z
            "start_date": "2000-01-01",
            "stop_date": "2000-01-31",
        },
    )
):
    """
    Retrieves statistics for a specific device.

    - **device_id**: The unique identifier for the device.
    - **metric_key**: The key for the specific metric to retrieve.
    - **start_date**: Optional start date for the statistics period (default is the earliest record).
    - **stop_date**: Optional end date for the statistics period (default is the latest record).
    """
    stats = dev_metrics_by_device_id.delay(
        device.device_id,
        device.metric_key,
        device.start_date if device.start_date is not None else start_time_default,
        device.stop_date if device.stop_date is not None else stop_time_default,
    ).get()
    return _dict_stats_to_statresponce(stats)


@stats_router.post(
    "/user",
    response_model=Union[StatsResponse, Dict[int, StatsResponse]],
    status_code=status.HTTP_200_OK,
    summary="Get statistics by user",
    description="Retrieve statistics for a specific user over a given time period. You can choose to aggregate the data or not. You need to provide a user statistics request model.",
)
async def get_stats_by_user(
    user: UserStatsRequest = Body(
        ...,
        example={
            "user_id": 1,
            "aggregate": True,
            "metric_key": "x",
            # can be written in iso format with Z at the end
            # example: 2024-03-16T08:29:02.027960Z
            "start_date": "2000-01-01",
            "stop_date": "2000-01-31",
        },
    )
):
    """
    Retrieves statistics for a specific user.

    - **user_id**: The unique identifier for the user.
    - **aggregate**: A boolean indicating whether to aggregate the data or not.
    - **metric_key**: The key for the specific metric to retrieve.
    - **start_date**: Optional start date for the statistics period (default is the earliest record).
    - **stop_date**: Optional end date for the statistics period (default is the latest record).
    """
    fun = dev_metrics_by_user_all if user.aggregate else dev_metrics_by_user_foreach
    stats = fun.delay(
        user.user_id,
        user.metric_key,
        user.start_date if user.start_date is not None else start_time_default,
        user.stop_date if user.stop_date is not None else stop_time_default,
    ).get()
    return (
        _dict_stats_to_statresponce(stats)
        if user.aggregate
        else {device: _dict_stats_to_statresponce(stat) for device, stat in stats}
    )
