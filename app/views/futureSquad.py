from pydantic import BaseModel
from decimal import Decimal
from app.views.player import PlayerSchema
from app.models.futureSquad import FutureSquad
class FutureSquadSchema(BaseModel):
    id: int | None = None
    plan_id: int | None = None
    gameweek: int | None = None
    estimated_points: Decimal | None = None
    team: list[PlayerSchema] | None = None
    subs: list[PlayerSchema] | None = None
    captain: PlayerSchema | None = None
    @classmethod
    def from_model(cls,model:FutureSquad):
        return cls(
            id=model.id,
            plan_id=model.plan_id,
            gameweek=model.gameweek,
            estimated_points=model.estimatedPoints,
            players=[PlayerSchema.from_model(player) for player in model.team],
            subs=[PlayerSchema.from_model(player) for player in model.subs],
            captain=PlayerSchema.from_model(model.captain)
        )