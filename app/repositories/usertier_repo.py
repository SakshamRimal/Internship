from app.repositories.base import BaseRepository
from app.db.models.user import UserTiers


class UserTierRepo(BaseRepository):

    # get a single tier by its id
    def get_tier_by_id(self , tier_id: int) -> UserTiers:
        tier = self.session.query(UserTiers).filter_by(tier_id=tier_id).first()
        return tier

    # get all the fixed tiers
    def get_all_tiers(self) -> list[UserTiers]:
        tiers = self.session.query(UserTiers).all()
        return tiers