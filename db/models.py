from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from db.session import Base, engine

class Log(Base):
    __tablename__ = "logs"

    id:Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    timestamp: Mapped[str] = mapped_column(String)
    level: Mapped[str] = mapped_column(String)
    user_id: Mapped[str | None] = mapped_column(String, nullable=True)
    method: Mapped[str] = mapped_column(String)
    endpoint: Mapped[str] = mapped_column(String)
    status_code: Mapped[int] = mapped_column(Integer)
    response_time: Mapped[float] = mapped_column(Float)

Base.metadata.create_all(bind=engine)