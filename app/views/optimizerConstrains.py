from pydantic import BaseModel

class OptimizerConstrains(BaseModel):
    weeks: int
    must_have: list[int]
    cant_have: list[int]