from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm.decl_api import declarative_base
import datetime
from typing import List, Optional

Base = declarative_base()

class Work(Base):
    __tablename__ = 'Work'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    genre: Mapped[str] = mapped_column(String(255))

    url: Mapped[str] = mapped_column(String(255), unique=True)
    complete_url: Mapped[str] = mapped_column(Text)
    url_hash: Mapped[str] = mapped_column(String(255), index=True)

    cover_url: Mapped[str] = mapped_column(String(400))
    complete_cover_url: Mapped[str] = mapped_column(Text)
    cover_url_hash: Mapped[str] = mapped_column(String(255), index=True)
    cover_is_downloaded: Mapped[bool] = mapped_column(default=False)
    cover_local_path: Mapped[Optional[str]] = mapped_column(String(500))
    cover_hash: Mapped[Optional[str]] = mapped_column(String(256), index=True)

    work_type: Mapped[str] = mapped_column(String(255))
    language: Mapped[str] = mapped_column(String(255))

    total_chapters: Mapped[int] = mapped_column(default=0)
    is_completed: Mapped[bool] = mapped_column(default=False)

    chapters: Mapped[List['Chapter']] = relationship('Chapter', back_populates='work', cascade='all, delete-orphan')
    panels: Mapped[List['Panel']] = relationship('Panel', back_populates='work', cascade='all, delete-orphan')

    added_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True))

    def __repr__(self):
        return f'Work(id={self.id}, title={self.title}, author={self.author}, description={self.description}, genre={self.genre}, \
              url={self.url}, cover_url={self.cover_url}, cover_local_path={self.cover_local_path}, total_chapters={self.total_chapters}, \
              is_completed={self.is_completed}, chapters={self.chapters}, added_at={self.added_at}, updated_at={self.updated_at})'


class Chapter(Base):
    __tablename__ = 'Chapter'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(400))
    url: Mapped[str] = mapped_column(String(400), index=True)
    complete_url: Mapped[str] = mapped_column(Text)
    url_hash: Mapped[str] = mapped_column(String(255), index=True)

    work_id: Mapped[int] = mapped_column(ForeignKey('Work.id'))
    work: Mapped['Work'] = relationship('Work', back_populates='chapters')

    order: Mapped[int] = mapped_column(default=0)

    panels: Mapped[List['Panel']] = relationship('Panel', back_populates='chapter', cascade='all, delete-orphan')

    added_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True))

    content: Mapped[Optional[str]] = mapped_column(Text)

    def __repr__(self):
        return f'Chapter(id={self.id}, title={self.title}, url={self.url}, work_id={self.work_id}, work={self.work}, order={self.order}, \
                panels={self.panels}, added_at={self.added_at}, updated_at={self.updated_at}, content={self.content})'


class Panel(Base):
    __tablename__ = 'Panel'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(600), index=True)
    complete_url: Mapped[str] = mapped_column(Text)
    url_hash: Mapped[str] = mapped_column(String(255), index=True)
    order: Mapped[int] = mapped_column(default=0)

    work_id: Mapped[int] = mapped_column(ForeignKey('Work.id'))
    work: Mapped['Work'] = relationship('Work', back_populates='panels')

    chapter_id: Mapped[int] = mapped_column(ForeignKey('Chapter.id'))
    chapter: Mapped['Chapter'] = relationship('Chapter', back_populates='panels')

    added_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True))

    is_credits: Mapped[bool] = mapped_column(default=False)

    is_downloaded: Mapped[bool] = mapped_column(default=False)
    local_path: Mapped[Optional[str]] = mapped_column(String(600))

    hash: Mapped[Optional[str]] = mapped_column(String(255), index=True)

    def __repr__(self):
        return f'Panel(id={self.id}, url={self.url}, order={self.order}, chapter_id={self.chapter_id}, chapter={self.chapter}, \
                added_at={self.added_at}, updated_at={self.updated_at}, is_credits={self.is_credits}, is_downloaded={self.is_downloaded}, \
                local_path={self.local_path}, work_id={self.work_id}, work={self.work})'
