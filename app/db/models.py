import datetime

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ToDo(Base):  # обязательно наследуем все модели от нашей Base-метатаблицы
    __tablename__ = "todo"  # Указываем как будет называться наша таблица в базе данных (пишется в ед. числе)

    # Строка говорит, что наша колонка будет интом, но уточняет, что ещё и большим интом (актуально для ТГ-ботов),
    # первичным ключом и индексироваться
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    description: Mapped[str]  # Описание, просто строка; если нужно дополнительные условия добавить, то mapped_column
    completed: Mapped[bool] = mapped_column(default=False)  # Задали значение по-умолчанию False
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
