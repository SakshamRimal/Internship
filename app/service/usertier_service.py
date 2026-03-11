from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.usertier_repo import UserTierRepo
from app.repositories.user_repo import UserRepository
from app.schemas.usertier_schema import UserTierRead

# this is the service for the repo where we keep the repo in the database and return it here we return the tier like bronze , silver ,platinum etc
class UserTierService:

    def __init__(self, session: Session):
        self._tierRepo = UserTierRepo(session=session)
        self._userRepo = UserRepository(session=session)

    def get_all_tiers(self) -> list[UserTierRead]:
        return self._tierRepo.get_all_tiers()

    # get which tier a specific user belongs to
    def get_user_tier(self, user_id: int) -> UserTierRead:
        user = self._userRepo.get_user_by_id(user_id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
        if not user.tier_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} has no tier assigned")
        tier = self._tierRepo.get_tier_by_id(tier_id=user.tier_id)
        return tier