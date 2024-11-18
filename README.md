# sssp-backend
soongsil security playground Ctf Platform backend

## Framework && Languages
- FastAPI with python3
- React
- Database : MySQL
    - ORM: sqlalchemy

## How to run

```bash
$ docker-compose up -d --build
```

## Todo

- SQL enum
    - SQL Enum에서 오류뜨면 truncated error 발생하는데 이거 수정하고, {detail:reason} 으로 수정하기 
- Error Exception
    - Python error detail 전체노출 나중 삭제

- login / regsiter / logout
    - Input validation 작업 

- Challege Submit
    - flag validation
    - 무단 플래그 인증 취약점같은거 있는지 확인 ( 띄어쓰기가튼거 등 ) [ 아직 귀찮아서 안함 ㅋ..!! ]

- config.py
    - 배포할 떄 env 디폴트값 싹다 지우기 