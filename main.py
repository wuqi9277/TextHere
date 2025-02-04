from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped,Session
from typing import Optional
from sqlalchemy import String,Boolean,create_engine,select
from random import choice
from ui_main import main_ui
from os import path
from httpx import get as httpx_get
import threading
import json  # 新增JSON模块
import atexit

# 新增：定义配置文件路径
SETTING_FILE = "setting.json"

# 新增：保存设置到JSON文件
def save_settings():
    settings = {
        "states": states,
        "states_msg": states_msg,
        "id": id,
        "name": name,
        "sentences": sentences,
        "sleep_seconds": sleep_seconds,
        "reset_all": reset_all,
        "use_internet_sentences": use_internet_sentences
    }
    with open(SETTING_FILE, "w") as f:
        json.dump(settings, f, indent=2)

# 新增：从JSON文件加载设置
def load_settings():
    global states, states_msg, id, name, sentences, sleep_seconds, reset_all, use_internet_sentences
    try:
        with open(SETTING_FILE, "r") as f:
            settings = json.load(f)
            states = settings.get("states", True)
            states_msg = settings.get("states_msg", None)
            id = settings.get("id", '')
            name = settings.get("name", '')
            sentences = settings.get("sentences", '')
            sleep_seconds = settings.get("sleep_seconds", 10)
            reset_all = settings.get("reset_all", False)
            use_internet_sentences = settings.get("use_internet_sentences", True)
    except FileNotFoundError:
        save_settings()


# global states
states = True
states_msg = None
id = ''
name = ''
sentences = ''
sleep_seconds = 120
reset_all = False
use_internet_sentences = False
load_settings()
atexit.register(save_settings)


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
    try:
        response = httpx_get(url)
        if response.status_code == 200 and response.text != '':
            sentences = response.text
            print(response.text)
        else:
            states = False
            states_msg = 'http get sentences failed !'
    except Exception as e:
        states = False
        states_msg = 'http get sentences failed !'
    name = 'hitokoto'
    id = 'hitokoto'

print(states_msg)

# 设置超时时间（秒）
timeout = sleep_seconds

def reset_is_used():
    with Session(engine) as session:
        session.query(main_table).update({main_table.is_uesd: False})
        session.commit()
        session.flush()
        session.close()



# 启动UI线程并传递超时时间
if reset_all:
    reset_is_used()
    sentences = 'Reset all sentences successfully !'
    thread_ui = threading.Thread(target=main_ui, args=(states, id, name, sentences, timeout))
else:
    thread_ui = threading.Thread(target=main_ui, args=(states, id, name, sentences, timeout))

thread_ui.start()

