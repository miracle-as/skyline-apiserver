from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

class UsageReduction(BaseModel):
    id: str = Field(...)
    value: float = Field(...)
    reduction_rate: Optional[float] = Field(...)

class UsageReductionResponse(BaseModel):
    my_servers: List[UsageReduction] = Field(...)
    same_datacenter: List[UsageReduction] = Field(...)
    gec_total: List[UsageReduction] = Field(...)

class UsageDataPoint(BaseModel):
    euro_mix: float = Field(...)
    norway: float = Field(...)
    gec: Optional[float] = Field(...)
    time: str = Field(...)

class UsageResponse(BaseModel):
    data_points: List[UsageDataPoint] = Field(...)