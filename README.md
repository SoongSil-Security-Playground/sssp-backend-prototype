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

- submit_challenge.py
    - 다이나믹 스코어로 바뀌면, 점수계산 다시해야지 ... 
- global_exception_handler.py
    - Python error detail 전체노출 나중 삭제
    - Exception 뜨면 Catch해서 detail과 함께 error 메시지를 전송하도록
        - sqlalchemy_data_error_handler()
    - SQL enum
        - SQL Enum에서 오류뜨면 truncated error 발생하는데 이거 수정하고, {detail:reason} 으로 수정하기 

- auth/*
    - Input validation 작업 

- submit_challenge.py
    - flag validation
    - 무단 플래그 인증 취약점같은거 있는지 확인 ( 띄어쓰기가튼거 등 ) [ 아직 귀찮아서 안함 ㅋ..!! ]
