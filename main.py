from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped,Session
from typing import Optional
from sqlalchemy import String,Boolean,create_engine,select
from random import choice
from ui_main import main_ui
from os import path
from httpx import get as httpx_get
import threading

# global states
states = True
states_msg = None
id = ''
name = ''
sentences = ''
sleep_seconds = 10
reset_all = False
use_internet_sentences = True

# file check (dataBase.db)
if path.exists("dadaBase.db"):
    states = False

# models
class Base(DeclarativeBase):
    pass

class main_table(Base):
    __tablename__ = 'main_table'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[Optional[str]] = mapped_column(String,unique=True)
    sentences : Mapped[str] = mapped_column(String)
    is_uesd : Mapped[bool] = mapped_column(Boolean,default=False)

# crud
engine = create_engine("sqlite:///dataBase.db",echo=True)

# Base.metadata.create_all(engine)

session = Session(engine)
stmt = (select(main_table).where(main_table.is_uesd == False))
result = session.scalars(stmt)
whole_id_list = []
for i in result:
    whole_id_list.append(i.id)
result.close()
if whole_id_list != []:
    selected_id = choice(whole_id_list)
    sentences_stmt = (select(main_table).where(main_table.id == selected_id))
    sentences_stmt_result = session.scalars(sentences_stmt).one_or_none()
    if sentences_stmt_result == None :
        states_msg = 'all sentences has been selected !'
        sentences = ' '
        states = False

    sentences = sentences_stmt_result.sentences
    id = str(sentences_stmt_result.id)
    name = sentences_stmt_result.name

    if use_internet_sentences == False:
        sentences_stmt_result.is_uesd = True

else:
    states = False
    states_msg = 'all sentences have been selected!'
# print(sentences)
session.commit()
session.flush()
session.close()

# sent https get request to get sentences
if use_internet_sentences:
    url = 'https://v1.hitokoto.cn/?c=d&encode=text'
    response = httpx_get(url)
    if response.status_code == 200 and response.text != '':
        sentences = response.text
    else:
        states = False
        states_msg = 'http get sentences failed !'
    name = 'hitokoto'
    id = 'hitokoto'
    print(response.text)

# build ui and taskkill
print(states_msg)

# 设置超时时间（秒）
timeout = sleep_seconds

# if reset_all

def reset_is_used():
    with Session(engine) as session:
        session.query(main_table).update({main_table.is_uesd: False})
        session.commit()
        session.flush()
        session.close()



# 启动UI线程并传递超时时间
thread_ui = threading.Thread(target=main_ui, args=(states, id, name, sentences, timeout))
thread_ui.start()

if reset_all:
    reset_is_used()