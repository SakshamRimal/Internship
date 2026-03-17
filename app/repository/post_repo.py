from sqlmodel import select, Session
from app.models.post_model import Posts
from app.schemas import post_schema


# Note: If your DB driver is async, use AsyncSession and add 'await'
async def get_post_repo(session: Session):
    # SQLModel preferred way
    statement = select(Posts)
    results = session.exec(statement)
    return results.all()


async def create_post_repo(session: Session, post: post_schema.PostSchemas):
    # Convert schema to DB model
    new_post = Posts(**post.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


async def get_post_by_id_repo(session: Session, id: int):
    # .get() is the fastest way to find by Primary Key
    return session.get(Posts, id)


async def update_post_repo(session: Session, id: int, post_data: post_schema.PostSchemas):
    # 1. Fetch the existing record
    db_post = session.get(Posts, id)
    if not db_post:
        return None

    # 2. Update the fields
    update_data = post_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)

    # 3. Save
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


async def delete_post_repo(session: Session, id: int):
    db_post = session.get(Posts, id)
    if not db_post:
        return False
    session.delete(db_post)
    session.commit()
    return True