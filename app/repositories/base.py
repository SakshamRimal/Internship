from sqlalchemy.orm import Session


class BaseRepository:
    # no need to rewrite the code for repository it will extend it
    # here we use the session so that we can intherit it in another class and use it whenever we need
    def __init__(self, session: Session) -> None:
        self.session = session

