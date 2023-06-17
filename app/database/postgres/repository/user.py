from typing import Optional, List

from sqlalchemy.orm import Session

from app.database.postgres.model.user import User
from app.database.postgres.repository.base_operation import BaseRepository


class UserRepository(BaseRepository[User]):
    # extra queries that can be overwritten
    def get_by_name(self, name: str, db: Session) -> Optional[List[User]]:
        return db.query(self.model).filter(self.model.name == name).all()


user_repository = UserRepository(User)
