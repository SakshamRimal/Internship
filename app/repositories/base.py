from sqlalchemy.orm import Session


class BaseRepository:
    # no need to rewrite the code for repository it will
    def __init__(self, session: Session) -> None:
        self.session = session

