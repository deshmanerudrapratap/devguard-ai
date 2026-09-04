from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class RepositoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    local_path: str | None = Field(default=None, max_length=1024)
    remote_url: str | None = Field(default=None, max_length=1024)
    description: str | None = Field(default=None, max_length=2000)

    @model_validator(mode="after")
    def require_location(self) -> "RepositoryCreate":
        local = (self.local_path or "").strip() or None
        remote = (self.remote_url or "").strip() or None
        object.__setattr__(self, "local_path", local)
        object.__setattr__(self, "remote_url", remote)
        if not local and not remote:
            raise ValueError("Provide a local_path, a remote_url, or both.")
        return self


class RepositoryUpdate(BaseModel):
    local_path: str | None = Field(default=None, max_length=1024)
    remote_url: str | None = Field(default=None, max_length=1024)
    description: str | None = Field(default=None, max_length=2000)


class RepositoryRead(BaseModel):
    id: int
    name: str
    local_path: str | None
    remote_url: str | None
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
