from pydantic import BaseModel
from typing import List, Dict

class UsageByDay(BaseModel):
    date: str
    count: int

class ActiveUser(BaseModel):
    email: str
    count: int

class AnalyticsStats(BaseModel):
    total_users: int
    total_addon_usage: int
    usage_by_day: List[UsageByDay]
    most_active_users: List[ActiveUser]
