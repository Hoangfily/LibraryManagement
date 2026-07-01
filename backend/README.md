# Library Management Backend

Backend FastAPI don gian cho he thong Quan ly Thu vien.

## Cai dependencies

```bash
pip install -r requirements.txt
```

## Tao file .env

Copy file `.env.example` thanh `.env` va cap nhat thong tin ket noi MySQL:

```bash
cp .env.example .env
```

Vi du:

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/library_db
SECRET_KEY=change-me
```

## Chay server

```bash
uvicorn app.main:app --reload
```

## Mo Swagger

Truy cap:

```text
http://127.0.0.1:8000/docs
```

## Chia viec goi y

- Nguoi 1: `auth`, `users`, `core`, `database`
- Nguoi 2: `readers`
- Nguoi 3: `documents`, `copies`
- Nguoi 4: `borrows`, `fines`, `reports`
