from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class DeviceStatsRequest(BaseModel):
    device_id: int
    metric_key: str
    start_date: Optional[date] = Field(
        default=None,
        description="The start date for the statistics period. If not provided, statistics will start from the earliest record.",
    )
    stop_date: Optional[date] = Field(
        default=None,
        description="The end date for the statistics period. If not provided but a start_date is, statistics will go up to the latest record.",
    )


class UserStatsRequest(BaseModel):
    user_id: int
    aggregate: bool
    metric_key: str
    start_date: Optional[date] = Field(
        default=None,
        description="The start date for the statistics period. If not provided, statistics will start from the earliest record.",
    )
    stop_date: Optional[date] = Field(
        default=None,
        description="The end date for the statistics period. If not provided but a start_date is, statistics will go up to the latest record.",
    )


class StatsResponse(BaseModel):
    min: float
    max: float
    count: int
    sum: float
    median: float
