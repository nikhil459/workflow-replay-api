from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class WorkflowRecord(Base):
    __tablename__ = "workflows"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    events: Mapped[list[dict]] = mapped_column(JSON)
