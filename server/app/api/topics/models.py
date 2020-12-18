# server/app/api/topics/models.py


import datetime
from typing import Dict
import uuid
from flask import current_app
from sqlalchemy.dialects.postgresql import UUID
from app.api.utils import ISO8601DateTime
from db import db


class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True
    )
    subject = db.Column(db.String(128), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        ISO8601DateTime,
        nullable=False,
        default=datetime.datetime.now
    )
    updated_at = db.Column(
        ISO8601DateTime,
        nullable=False,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )
    deleted_at = db.Column(
        ISO8601DateTime,
        nullable=True
    )
    messages = db.relationship("Message")

    def __init__(self, subject, description, created_by, updated_by):
        self.subject = subject
        self.description = description
        self.created_by = created_by
        self.updated_by = updated_by

    def json(self) -> Dict:
        return {
            "id": str(self.id),
            "subject": self.subject,
            "description": self.description,
            "created_by": str(self.created_by),
            "updated_by": str(self.updated_by),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at
        }

    @classmethod
    def find(cls, **kwargs) -> "Topic":
        """Find a database entry that matches given keyword argument."""
        keys = list(kwargs.keys())
        if (
            len(keys) == 1
            and keys[0] in cls.__table__.columns
        ):
            return cls.query.filter_by(**kwargs).first()

    @classmethod
    def find_all(cls, created_by):
        """Find all topics in the database that are not deleted yet."""
        topics = (
            cls.query.filter_by(deleted_at=None, created_by=created_by)
            .order_by(cls.subject.desc())
            .paginate(
                page=current_app.config.get("PAGE_COUNT"),
                per_page=current_app.config.get("POSTS_PER_PAGE"),
                error_out=False
            ).items
        )
        return [topic.json() for topic in topics]

    def insert(self) -> None:
        """Insert into the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Mark a topic as deleted in the database."""
        self.deleted_at = datetime.datetime.now()
        db.session.commit()
