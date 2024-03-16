from fastapi import APIRouter

from analysis_worker import *
from routers.models import DeviceStatsRequest, UserStatsRequest

stats_router = APIRouter()

start_time_default = "1970-01-01T00:00:00Z"
stop_time_default = ""


@stats_router.post("/device")
async def get_stats_by_device(device: DeviceStatsRequest):
    stats = dev_metrics_by_device_id.delay(
        device.device_id,
        device.metric_key,
        device.start_date if device.start_date is not None else start_time_default,
        device.stop_date if device.stop_date is not None else stop_time_default,
    )
    return {"result": str(stats.get())}


@stats_router.post("/user")
async def get_stats_by_user(user: UserStatsRequest):
    fun = dev_metrics_by_user_all if user.aggregate else dev_metrics_by_user_foreach
    stats = fun.delay(
        user.user_id,
        user.metric_key,
        user.start_date if user.start_date is not None else start_time_default,
        user.stop_date if user.stop_date is not None else stop_time_default,
    )
    return {"result": str(stats.get())}
