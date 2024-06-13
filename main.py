from fastapi import FastAPI, UploadFile,Form,Response,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
# 유효하지 않은 계정정보에 대한 에러처리를 하는 문법
from fastapi_login.exceptions import InvalidCredentialsException
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
# 	로그인
# -----------------------------------
# base64를 통해 인코딩된 패스워드를 디코딩 가능
# -> 이 시크릿키를 노출시키면 언제든지 jwt를 해석할 수 있음
SECRET = "super-coding"
# LoginManager(시크릿키, 토큰이 어디서 발급될거냐)
manager = LoginManager(SECRET,'/login')

@manager.user_loader()

# user가 존재하는지 확인
# 액세스토큰 형식을 정해서 보내줬기때문에
# 그 형식대로 id값을 넘겨줘야함
def query_user(data):
  WHERE_STATEMENTS = f'id="{data}"'
  if type(data) == dict:
    WHERE_STATEMENTS = f'''id="{data['id']}"'''
  # 특정컬럼을 조회하려면 컬럼명도 같이 가져와야됨
  # 컬럼명도 같이 가져오는 문법
  con.row_factory = sqlite3.Row
  cur = con.cursor()
  # id가 같으면 모든 정보들을 가져옴
  user = cur.execute(f"""
                    SELECT * from users WHERE {WHERE_STATEMENTS}
                    """).fetchone()
  return user

@app.post('/login')
# 회원가입시 입력한 아이디와 패스워드 정보가 넘어옴
def login(id:Annotated[str,Form()],
					password:Annotated[str,Form()]):
  user = query_user(id)
  if not user:
    # raise : 파이썬에서 에러메시지
    raise InvalidCredentialsException
		# POST http://127.0.0.1:8000/login 401 (Unauthorized)
		# 인과되지않은 유저 라는 에러메시지 출력
		# => 401을 자동으로 생성해서 내려줌
  # elif => 파이썬에서 else if
  # 유저의 패스워드 정보와 받아온 패스워드 정보가 같지 않으면
  elif password != user['password']:
    raise InvalidCredentialsException
		# => 200을 자동으로 생성해서 내려줌
  
  # manager가 액세스토큰을 만들어줌
  # 액세스토큰(JWT) : 토큰안에 인코딩을 해서 데이터를 넣어줌
	# JWT방식 : 서버가 토큰이 맞는지 아닌지만 검증을 하고, 토큰을 파헤쳐보면 유저정보가 들어있음
	# -> 세션방식 : db를 조회해서 유저정보가 존재하는지 아닌지 검증할 필요가 없음
  access_token = manager.create_access_token(data={
    # sub라는 객체에 유저정보를 담아서 내려줌
		'sub': {
			'id':user['id'],
			'name':user['name'],
			'email':user['email']
		}
	})
  
  return {'access_token':access_token}


# -----------------------------------
# 	회원가입
# -----------------------------------
@app.post("/signup")
def signup(id:Annotated[str,Form()],
					password:Annotated[str,Form()],
					name:Annotated[str,Form()],
					email:Annotated[str,Form()]):
  # DB에 저장
  cur.execute(f"""
              INSERT INTO users(id,name,email,password)
              VALUES ('{id}', '{name}', '{email}', '{password}')
              """)
  # input password 타입으로 비밀번호를 가렸어도 터미널에서는 다 볼수있음
  # print 주석처리 안하면 오류남
  # print(id, password)
  con.commit()
  return "200"
# 200이라는 응답이 떨어졌기 때문에 비밀번호를 저장하시겠습니까? 알림창 뜸

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
                insertAt:Annotated[int,Form()],
                # 유저인증이 됐을때만 글쓰기 가능
                # user=Depends(manager)
                ):
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
# user에 의존적일수있게 추가
# -> 유저가 인증된 상태에서만 응답을 내려줌
async def get_items(user=Depends(manager)):
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
  # media_type='image/*' -> 모든 이미지타입 (배포시 파이썬 버전문제 오류 해결)
  return Response(content=bytes.fromhex(image_bytes), media_type='image/*')


# 이 아래에 작성하면 위에서 처리되고 아래 있는 코드는 실행안됨
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")