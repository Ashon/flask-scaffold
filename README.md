---
marp: true
---

# Flask Application Ecosystem

`Flask-script`, `Flask-migrate`, `Flask-smorest` 소개

---

좋은 웹 애플리케이션 프로젝트 시작할 때, 생각해야 할 점들

- 서비스의 품질 (당연히 중요함)
  - DB 설계
  - 빠른 코드
  - 안전한 테스트코드
  - 성능 좋은 서버
  - 오케스트레이션

---

하지만, 품질은 단순히 서비스 코드가 잘 짜여지고 배치되는 것 만으로는 만족되지 않음.

- 운영도구는 어떻게?
  > 운영을 인터페이스가 제공되어야 함.
- DB관리는 어떻게?
  > 데이터베이스의 스키마, 버전 관리가 필요함.
- 거버넌스 (설계, API 스키마, 추상화 등)
  > 오래가는 프로젝트를 위해서는 좋은 설계에 대한 고민들이 필요함.
  > **하자 많은 집에서 살고싶지 않다.**

그 밖에도 달성해야 할 문제들이 있지만,
이번에는 위 세가지 부분에 대해서만 다룬다.

---

3가지 문제들을 다루기 위한 Flask ecosystem

- `Flask-script`: 운영도구를 쉽게 만든다.
- `Flask-migrate`: DB 버전관리를 쉽게 만든다.
- `Flask-smorest`: RESTful API 작성을 쉽게 만든다.

---

### Structure

``` sh
.
|- app/
|
|  # pip package 정의, 설정
|- setup.py  # optional: pypi로 올릴게 아니라면 굳이...
|- setup.cfg
|
|  # 패키지 의존성 관리
|- requirements.txt
|- requirements-dev.txt
|
|  # 애플리케이션 컨테이너 빌드 설정
|- Dockerfile
|
|  # 개발에 필요한 서비스 의존성 정의
|- docker-compose.yml
|
|  # CI/CD를 위한 테스트 자동화 스크립트
|- Jenkinsfile
|- ...
```

---

### Structure(Domain based)

- App 별로 디렉토리가 구분됨.
- Pluggable App에 적합한 형태
- 의존성 관리가 힘들 수 있음

``` sh
.
|- app/
   |- wsgi.py
   |
   |- users/
   |  |- models.py
   |  |- views.py
   |
   |- orders/
      |- models.py
      |- views.py
```

---

### Structure(Layer based)

- 레이어별로 디렉토리가 구분됨.
- 복잡한 모델들을 관리할 때 용이함.
  - 같은 레이어 안에서의 의존성을 한곳에서 관리
- 계층에서 발생하는 문제들을 따로 풀기가 수월함.

``` sh
.
|- app/
   |- wsgi.py
   |
   |- models/
   |  |- user.py
   |  |- order.py
   |
   |- views/
      |- user.py
      |- order.py
```

---

### Flask-script

Flask 애플리케이션의 관리를 위한 CLI확장을 작성할 수 있는 도구

``` sh
.
|- app/
   |- wsgi.py
   |- manage.py # manage script
```

---

### Flask-script

```python
# file: app/manage.py
from flask_script import Manager
from wsgi import app


manager = Manager(app)


@manager.command
def hello():
    print('world')


if __name__ == '__main__':
    manager.run()
```

---

### Flask-script

`hello` 실행

``` sh
$ ./app/manage.py hello
world
```

---

### Flask-script

manage 스크립트를 이용해 애플리케이션 컨텍스트를 초기화하고 여러 작업들을 수행가능함.

``` python
@manager.command
def create_superuser(username, password):
    """ 서비스의 superuser를 생성한다.
    """

    user = User(
        username=username, password=password,
        is_superuser=True)
    user.save()
```

``` sh
# username=admin password=adminpass
$ ./app/manage.py create_superuser admin adminpass
```

---

### Flask-migrate

Flask 애플리케이션의 DB 마이그레이션 관리 도구.

`SQLAlchemy`와 `Alembic`을 이용해 ORM과 DB 마이그레이션 관리를 도와준다.

- `Sqlalchemy`: ORM 라이브러리
- `Alembic`: Sqlalchemy로 작성되는 ORM에 대한 DB 형상을 관리해 주는 라이브러리

---

### Flask-migrate + Flask-script

``` python
from flask_script import Manager
from flask_migrate import MigrateCommand

from wsgi import app


manager = Manager(app)

# flask-migration 관련 관리 커맨드들이 db 커맨드 컬렉션으로 등록된다.
manager.add_command('db', MigrateCommand)

...
```

---

### Flask-migrate + Flask-script

``` sh
./app/manage.py db
usage: Perform database migrations

Perform database migrations

positional arguments:
  {init,revision,migrate,edit,merge,upgrade,downgrade,show,history,heads,branches,current,stamp}
    init                Creates a new migration repository
    revision            Create a new revision file.
    migrate             Alias for 'revision --autogenerate'
    edit                Edit current revision.
    merge               Merge two revisions together. Creates a new migration file
    upgrade             Upgrade to a later version
    downgrade           Revert to a previous version
    show                Show the revision denoted by the given symbol.
    history             List changeset scripts in chronological order.
    heads               Show current available heads in the script directory
    branches            Show current branch points
    current             Display the current revision for each database.
    stamp               'stamp' the revision table with the given revision; don't run any migrations

optional arguments:
  -?, --help            show this help message and exit
```

---

### Flask-migrate: Migration script 관리 시나리오

1. ORM class로 User 모델을 정의한다.
  > 새로운 모델 정의
2. 생성된 ORM클래스들에 대한 마이그레이션 스크립트를 자동 생성한다.
  > DB 변경사항에 대한 스키마 트랜지션 준비
3. DB에 마이그레이션을 반영한다.
  > DB에 변경된 사항 반영

---

### Flask-migrate: Migration script 관리

1. ORM class로 User 모델을 정의한다.

```python
# file: app/models/user.py

class User(db.Model):
    uuid = db.Column(db.String(36), default=generate_uuid, primary_key=True)

    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

### Flask-migrate: Migration script 관리

2. 생성된 ORM클래스들에 대한 마이그레이션 스크립트를 자동 생성한다.

```sh
# 프로젝트에서 최초로 마이그레이션을 준비하는 경우 init으로 초기화 해 주어야 한다.
$ ./app/manage.py db init

# User model migration script를 작성한다.
$ ./app/manage.py db migrate
```

`migrations` 디렉토리가 생성되고, 그 안에 정의한 ORM 클래스에 대한 DB 트랜지션 스크립트가 생성됨.

```sh
$ tree migrations
migrations/
|- ...
|- versions
   |- 690e0cb4cd10_.py  # 비어있는 DB에 User모델스키마를 반영하는 스크립트.
```

---

### Flask-migrate: Migration script 관리

2. 생성된 ORM클래스들에 대한 마이그레이션 스크립트를 자동 생성한다.

```sh
# 생성된 migration 스크립트를 DB에 적용한다.
$ ./app/manage.py db upgrade

# 이밖에도 과거 버전들을 하나로 merge한다거나 하는 좋은 기능들을 많이 가지고 있음.
```

**!!주의사항!!**

- 마이그레이션 코드는 반드시 프로젝트에 포함되고 버전 관리가 되어야 한다.
  - 스키마가 망가진다거나, 업그레이드가 정상적으로 되지 않을 수 있음.
  - 서비스에 큰 영향을 초래할 수 있으므로 잘 관리해야 한다.
  - 이 부분을 잘 관리하려면 Backward migration에 대한 준비도 잘 해 놓아야 한다.

---

### Flask-smorest

Flask 애플리케이션에서 관리되는 데이터들을 스키마로 정의하고, `RESTful API` 작성을
보다 쉽게 만들어주는 라이브러리

- `marshmallow`: serialization 라이브러리
  python object들을 다양한 자료형으로 변환하기 쉽게 해 준다.
- OAS(OpenAPI Specification)에 맞춰 API 문서가 자동생성되도록 도와준다.

---

### Flask-smorest: API작성 시나리오

1. API 스키마 정의 (Schema)
2. Endpoint 정의 (Blueprint)

---

### Flask-smorest: API작성 시나리오

1. API 스키마 정의 (Schema)

아까 정의한 ORM. 이런 모델이 있다고 할 때...

```python
class User(db.Model):
    uuid = db.Column(db.String(36), default=generate_uuid, primary_key=True)

    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

### Flask-smorest: API작성 시나리오

1. API 스키마 정의 (Schema)

``` python
# file: app/schema/user.py
import marshmallow as ma


class UserSchema(ma.Schema):
    uuid = ma.fields.UUID(required=True, description='사용자 오브젝트 UUID')
    email = ma.fields.Email(required=True, description='사용자 이메일 주소')
```

---

### Flask-smorest: API작성 시나리오

2. Endpoint 정의 (Blueprint)

여기서는 `FBV(function based view)`로 view가 정의되는 시나리오를 설명한다.
`CBV(Class Based View)`는 공식 문서를 참고한다.

---

``` python
# file: app/views/user.py
from flask_smorest import Blueprint

from models.user import User
from schema.user import UserSchema


blueprint = Blueprint(
    'User API', 'user', url_prefix='/users',
    description='사용자 정보 API'
)


@blueprint.route('')
@blueprint.arguments(UserSchema(many=True))
def get_users():
    """사용자 리스트 조회

    모든 사용자 리스트를 조회한다.
    """

    users = User.query.all()
    return users
```

---

``` python
# file: app/wsgi.py
from flask import Flask

import settings
from core.app import create_app

from views.user import blueprint as user_bp
# from views.blabla import blueprint as blabla_bp


# blueprint를 추가한다.
routes = [user_bp, ]

# app factory 형태로 flask app을 빌드한다.
app = create_app(__name__, settings, routes)
```
