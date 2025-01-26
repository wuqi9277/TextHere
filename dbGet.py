from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped,Session
from typing import Optional
from sqlalchemy import String,Boolean,create_engine,select
from random import choice

class Base(DeclarativeBase):
    pass

class main_table(Base):
    __tablename__ = 'main_table'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[Optional[str]] = mapped_column(String,unique=True)
    sentences : Mapped[str] = mapped_column(String)
    is_uesd : Mapped[bool] = mapped_column(Boolean,default=False)

engine = create_engine("sqlite:///dataBase.db",echo=True)

# Base.metadata.create_all(engine)

session = Session(engine)
stmt = (select(main_table).where(main_table.is_uesd == False))
result = session.scalars(stmt)
whole_id_list = []
for i in result:
    whole_id_list.append(i.id)
result.close()
selected_id = choice(whole_id_list)
sentences_stmt = (select(main_table).where(main_table.id == selected_id))
sentences_stmt_result = session.scalars(sentences_stmt).one_or_none()
if sentences_stmt_result == None :
    states_msg = 'all sentences has been selected !'
#
sentences = sentences_stmt_result.sentences
id = sentences_stmt_result.id
name = sentences_stmt_result.name
#
sentences_stmt_result.is_uesd = True
print(sentences)
session.commit()
session.flush()
session.close()