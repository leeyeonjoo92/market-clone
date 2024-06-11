from fastapi import FastAPI, UploadFile,Form,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

con = sqlite3.connect("db.db", check_same_thread=False)
# db에서 cursor()란 개념이 있는데
# 특정 인서트 하거나 셀렉트 할때 사용
cur = con.cursor()

# 데이터 배포시 자동으로 테이블을 만들어줌
# 서버가 내려갈때마다 새로 만드는 오류가 있음
# IF NOT EXISTS -> 테이블이 없을때만 생성해주는 조건문
cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
							id INTEGER PRIMARY KEY,
							title TEXT NOT NULL,
							image BLOB,
							price INTEGER NOT NULL,
							description TEXT,
							place TEXT NOT NULL,
							insertAt INTEGER NOT NULL
						);
            """)

app = FastAPI()

# -----------------------------------
# 	데이터 받기
# -----------------------------------
@app.post("/items")
# fast api의 변수 설정법
async def create_item(image:UploadFile,
                # 폼 데이터형식으로 문자열로 옴
                title:Annotated[str,Form()],
                # 폼 데이터형식으로 숫자로 옴
                price:Annotated[int,Form()],
                description:Annotated[str,Form()],
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]):
  # print(image,title,price,description,place)
  # 이미지가 blob타입으로 오기때문에 이미지를 읽을 시간이 필요함
  image_bytes = await image.read()
  # 데이터베이스에 인서트
  # f문자열 : 백틱처럼
  # hex() : 16진법
  # title~place라는 컬럼을 가지고있는 items라는 테이블에 값을 'title'~'place'로 넣겠다
  # price는 숫자니까 따옴표 없어도됨
  cur.execute(f"""
              INSERT INTO
              items(title, image, price, description, place, insertAt)
              VALUES
              ('{title}', '{image_bytes.hex()}', {price}, '{description}', '{place}', '{insertAt}')
              """)
  con.commit()
  # OK라는 메시지니까 200
  return "200"

# -----------------------------------
# 	데이터 내려주기
# -----------------------------------
@app.get("/items")
async def get_items():
  # .fetchall() -> 가져오는거기 때문에 붙여주면 좋음
  # SELECT * from items -> 이렇게 가져오면 컬럼명은 안가져옴
  # 컬럼명도 같이 가져오는 문법
  con.row_factory = sqlite3.Row
  # db를 가져오면서 connection의 현재 위치를 업데이트해줘야 데이터가 제대로 들어옴
  cur = con.cursor()
  # [["id", 1], ["title", "~~~"], ["description", "00000"],...]
  # 이런 배열 형식으로 데이터를 보내게됨
  rows = cur.execute(f"""
                     SELECT * from items;
                     """).fetchall()
  # [id:1, title:"~~~", description:"00000",...]
  # 이런식으로 바꿔서 보내줌
  # 그리고나서 jsonable_encoder 로 json형식으로 바꿔줘야함
  return JSONResponse(jsonable_encoder(dict(row) for row in rows))

# -----------------------------------
# 	이미지 내려주기
# -----------------------------------
# items_id에 맞는 이미지를 보내줌
@app.get("/images/{item_id}")
async def get_image(item_id):
  cur = con.cursor()
  # fetchone -> 하나만 가져옴
  # hex : 16진법으로 가져오게됨
  image_bytes = cur.execute(f"""
                            SELECT image from items WHERE id={item_id}
                            """).fetchone()[0]
  # 16진법으로 된것을 2진법으로 바꿔서 response하곘다
  return Response(content=bytes.fromhex(image_bytes))

# 이 아래에 작성하면 위에서 처리되고 아래 있는 코드는 실행안됨
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")