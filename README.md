# Article API

> *Used for Postman Testing & Implement Swagger UI*

## Install & Usage

- *Clone the repository:*
```
git clone https://github.com/erkamesen/ArticleAPI.git
```

- *Change directory:*
```
cd ArticleAPI/
```

- *Install & Activate venv(optional)*
```
python3 -m venv venv
```

```
source venv/bin/activate (macOS - Linux)
.\venv\Scripts\activate (Windows)
```

- *Install dependencies*
```
pip3 install -r requirements.txt
```

- *Migrate*
```
python manage.py migrate
```

- *Run Server*
```
python manage.py runserver
```

**For Swagger UI**
> http://127.0.0.1:8000/api/docs