from app.database.postgres.model.claim import Claim
from app.database.postgres.repository.base_operation import BaseRepository


class UserRepository(BaseRepository[Claim]):
    pass


claim_repository = UserRepository(Claim)
