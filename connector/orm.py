import sqlalchemy as sa
from typing import List
from typing import Optional
from sqlalchemy import String
from sqlalchemy import DATETIME
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Text

class Base(DeclarativeBase):
    __abstract__ = True
    pass

class Work(Base):
    __tablename__ = 'Work'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    genre: Mapped[str] = mapped_column(String(255))

    url: Mapped[str] = mapped_column(String(255), unique=True)
    cover_url: Mapped[str] = mapped_column(String(400))
    cover_is_downloaded: Mapped[bool] = mapped_column(default=False)
    cover_local_path: Mapped[Optional[str]] = mapped_column(String(255))

    work_type: Mapped[str] = mapped_column(String(255))
    language: Mapped[str] = mapped_column(String(255))

    total_chapters: Mapped[int] = mapped_column(default=0)
    is_completed: Mapped[bool] = mapped_column(default=False)

    chapters: Mapped[List['Chapter']] = relationship(back_populates='Chapter', cascade='all, delete-orphan')
    panels: Mapped[List['Panel']] = relationship(back_populates='Panel', cascade='all, delete-orphan')
    
    added_at = mapped_column(DATETIME(True), server_default=func.now())
    updated_at = mapped_column(DATETIME(True))


    def __repr__(self):
        return f'Work(id={self.id}, title={self.title}, author={self.author}, description={self.description}, genre={self.genre}, \
              url={self.url}, cover_url={self.cover_url}, cover_local_path={self.cover_local_path}, total_chapters={self.total_chapters}, \
              is_completed={self.is_completed}, chapters={self.chapters}, added_at={self.added_at}, updated_at={self.updated_at})'
    
    pass

class Chapter(Base):
    __tablename__ = 'Chapter'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(400))
    url: Mapped[str] = mapped_column(String(400), index=True)

    work_id: Mapped[int] = mapped_column(sa.ForeignKey('Work.id'))
    work: Mapped['Work'] = relationship('Work', back_populates='chapters')

    order: Mapped[int] = mapped_column(default=0)

    panels: Mapped[List['Panel']] = relationship(back_populates='Panel', cascade='all, delete-orphan')

    added_at = mapped_column(DATETIME(True), server_default=func.now())
    updated_at = mapped_column(DATETIME(True))
    
    # content, its assumed that its a long sting
    content: Mapped[Optional[str]] = mapped_column(Text)

    def __repr__(self):
        return f'Chapter(id={self.id}, title={self.title}, url={self.url}, work_id={self.work_id}, work={self.work}, order={self.order}, \
                panels={self.panels}, added_at={self.added_at}, updated_at={self.updated_at}, content={self.content})'
    
    pass

class Panel(Base):
    __tablename__ = 'Panel'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(600), index=True)
    complete_url: Mapped[str] = mapped_column(Text)
    order: Mapped[int] = mapped_column(default=0)

    work_id: Mapped[int] = mapped_column(sa.ForeignKey('Work.id'))
    work: Mapped['Work'] = relationship('Work')

    chapter_id: Mapped[int] = mapped_column(sa.ForeignKey('Chapter.id'))
    chapter: Mapped['Chapter'] = relationship('Chapter', back_populates='panels')

    added_at = mapped_column(DATETIME(True), server_default=func.now())
    updated_at = mapped_column(DATETIME(True))

    is_credits: Mapped[bool] = mapped_column(default=False)

    is_downloaded: Mapped[bool] = mapped_column(default=False)
    local_path: Mapped[Optional[str]] = mapped_column(String(400))

    hash: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    
    def __repr__(self):
        return f'Panel(id={self.id}, url={self.url}, order={self.order}, chapter_id={self.chapter_id}, chapter={self.chapter}, \
                added_at={self.added_at}, updated_at={self.updated_at}, is_credits={self.is_credits}, is_downloaded={self.is_downloaded}, \
                local_path={self.local_path}), work_id={self.work_id}, work={self.work}'
    
    pass