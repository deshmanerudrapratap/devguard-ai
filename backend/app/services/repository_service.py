from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import ConflictError, NotFoundError
from app.models.repository import Repository, utcnow
from app.schemas.repository import RepositoryCreate, RepositoryUpdate


def list_repositories(db: Session) -> list[Repository]:
    stmt = select(Repository).order_by(Repository.created_at.desc())
    return list(db.scalars(stmt).all())


def get_repository(db: Session, repository_id: int) -> Repository:
    repo = db.get(Repository, repository_id)
    if repo is None:
        raise NotFoundError(f"Repository {repository_id} was not found.")
    return repo


def create_repository(db: Session, payload: RepositoryCreate) -> Repository:
    repo = Repository(
        name=payload.name.strip(),
        local_path=payload.local_path,
        remote_url=payload.remote_url,
        description=(payload.description or "").strip() or None,
    )
    db.add(repo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError(f"A repository named '{payload.name.strip()}' is already registered.") from None
    db.refresh(repo)
    return repo


def update_repository(db: Session, repository_id: int, payload: RepositoryUpdate) -> Repository:
    repo = get_repository(db, repository_id)
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        if isinstance(value, str):
            value = value.strip() or None
        setattr(repo, key, value)
    repo.updated_at = utcnow()
    db.commit()
    db.refresh(repo)
    return repo


def delete_repository(db: Session, repository_id: int) -> None:
    repo = get_repository(db, repository_id)
    db.delete(repo)
    db.commit()
