from ..utils.database import Base
from .timestamptmixin import TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Numeric, CheckConstraint #Column застарілий стиль в sqlalchemy, починаючи з версії sqlalchemy 2.0 використовують Mapped, mapped_column


class Users(Base, TimestampMixin):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(25), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    # check comment about connection next by code
    events: Mapped[list["Events"]] = relationship(back_populates="creator") 
    event_users: Mapped[list["EventUsers"]] = relationship(back_populates="user")
    paid: Mapped[list["Items"]] = relationship(back_populates="paid_by_user")
    user_consumers: Mapped[list["ItemConsumers"]] = relationship(back_populates="user")
    from_debts: Mapped[list["Debts"]] = relationship(back_populates="from_user", foreign_keys="[Debts.from_user_id]")
    to_debts: Mapped[list["Debts"]] = relationship(back_populates="to_user",  foreign_keys="[Debts.to_user_id]")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
    
class Events(Base, TimestampMixin):
    __tablename__ = "events"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    # one-to-many(user-event)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False  )
    creator: Mapped["Users"] = relationship(back_populates="events") 
    # check comment about connection next by code
    event_users: Mapped[list["EventUsers"]] = relationship(back_populates="event")
    items: Mapped[list["Items"]] = relationship(back_populates="event")
    debt: Mapped[list["Debts"]] = relationship(back_populates="event")
        
    def __repr__(self):
        return f"<Event(name='{self.name}', created_by={self.created_by})>"
    
class EventUsers(Base):
    __tablename__ = "event_users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # one-to-many(user-event_users)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["Users"] = relationship(back_populates="event_users")
    # one-to-many(events-event_users)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))
    event: Mapped["Events"] = relationship(back_populates="event_users")
    
    def __repr__(self):
        return f"<EventUser(user_id={self.user_id}, event_id={self.event_id})>"
    
class Items(Base):
    __tablename__ = "items"
    __table_args__ = (
        CheckConstraint('price_per_unit >= 0', name='check_price_positive'),
        CheckConstraint('count_product >= 0', name='check_count_positive'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    price_per_unit: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    count_product: Mapped[int] = mapped_column(Integer, nullable=False)
    # one-to-mane(event-item)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))
    event: Mapped["Events"] = relationship(back_populates="items")
    # one to many(user-item)
    paid_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    paid_by_user: Mapped["Users"] = relationship(back_populates="paid")
    
    item_consumers: Mapped[list["ItemConsumers"]] = relationship(back_populates="item")
    
    def __repr__(self):
        return f"<Item(name='{self.name}', price={self.price_per_unit}, count={self.count_product})>"
    
class ItemConsumers (Base):
    __tablename__ = "item_consumers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # one-to-many(item-Item_consumers)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"))
    item: Mapped["Items"] = relationship(back_populates="item_consumers")
    # one-to-many(user-Item_consumers)   
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["Users"] = relationship(back_populates="user_consumers")  

    def __repr__(self):
        return f"<ItemConsumer(item_id={self.item_id}, user_id={self.user_id})>"  
    
class Debts(Base):
    __tablename__ = "debts"    

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))
    event: Mapped["Events"] = relationship(back_populates="debt")
    
    from_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    from_user: Mapped["Users"] = relationship(back_populates="from_debts", foreign_keys="[Debts.from_user_id]")
    
    to_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    to_user: Mapped["Users"] = relationship(back_populates="to_debts", foreign_keys="[Debts.to_user_id]")
    
    def __repr__(self):
        return f"<Debt(from={self.from_user_id}, to={self.to_user_id}, amount={self.amount})>"
    