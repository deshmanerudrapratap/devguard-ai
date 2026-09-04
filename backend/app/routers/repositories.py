from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.repository import RepositoryCreate, RepositoryRead, RepositoryUpdate
from app.services import repository_service

router = APIRouter(prefix="/repositories", tags=["repositories"])


@router.get("", response_model=list[RepositoryRead])
def list_repositories(db: Session = Depends(get_db)) -> list[RepositoryRead]:
    return [RepositoryRead.model_validate(item) for item in repository_service.list_repositories(db)]


@router.post("", response_model=RepositoryRead, status_code=status.HTTP_201_CREATED)
def register_repository(payload: RepositoryCreate, db: Session = Depends(get_db)) -> RepositoryRead:
    return RepositoryRead.model_validate(repository_service.create_repository(db, payload))


@router.get("/{repository_id}", response_model=RepositoryRead)
def get_repository(repository_id: int, db: Session = Depends(get_db)) -> RepositoryRead:
    return RepositoryRead.model_validate(repository_service.get_repository(db, repository_id))


@router.patch("/{repository_id}", response_model=RepositoryRead)
def update_repository(
    repository_id: int, payload: RepositoryUpdate, db: Session = Depends(get_db)
) -> RepositoryRead:
    return RepositoryRead.model_validate(repository_service.update_repository(db, repository_id, payload))


@router.delete("/{repository_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_repository(repository_id: int, db: Session = Depends(get_db)) -> None:
    repository_service.delete_repository(db, repository_id)
