from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    # щоб updated_at оновлювався, треба щоби ти викликав .commit() після зміни об'єкта. SQLAlchemy автоматично це не робить без session.commit().
    update_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now()
    )
    