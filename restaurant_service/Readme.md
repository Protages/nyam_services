## Run server:
- `uvicorn --port=8002 src.core.main:app --reload`


## Onion Architecture

1. Вся работа с БД содержится в репозиториях, где на каждую таблицу создается 
базовый абстрактный репозиторий, и от этих асбтрактных репозиториев реализуются 
репозитории для работы с конкретной ORM, например:

- Абстрактный - `UserAbcRepo(ABC)` - только список абстрактных методов.
- Конкретный для ORM SQLAlchemy - `UserSQLAlchemyRepo(UserAbcRepo)` - содержит всю работу с БД.


2. На каждую таблицу создается Сервис, который в __init__ принимает класс, 
реализующий абстракный репозиторий этой таблицы (напр. `UserSQLAlchemyRepo(UserAbcRepo)`). 
Сервис вызывает методы репозитория на создание, чтение и т.д., при этом он может делать 
запросы к другим сервисам или к сторонним API, например:

- Сервис - `UserService` - при инициальзации принимает `user_repo: type[UserAbcRepo]` 
и создает его локальный инстансе `self.user_repo: UserAbcRepo = user_repo()`.


3. Роуты (эндпойнты) работают только с Сервисами, получая их через внедрение 
зависимостей - Dependency Injection. Например:

- Эндпойнт на получения юзера:
```
async def get_user(
    id: int, 
    user_service: Annotated[UserService, Dependsuser_service)]
)
```

- Где `user_service`:
```
def user_service():
    return UserService(UserSQLAlchemyRepo)
```

### В чем польза (на мой взгляд)

1. Даже если мы знаем что будем использовать одну ORM (напр. SQLAlchemy) мы можем 
создать несколько репозиториев для нее, каждый из которых будет своим образом выполнять 
запросы. Скажем на этапе MVP мы не могли уделить достаточно времени оптимизации запросов. 
Затем время появилось, и мы можем написать новый репозиторий с уже оптимизированными 
запросами (или написаными в другом стиле (синхронном мб)). 
Затем мы просто меняем старый репозиторий на новый в Dependency Injection.


## Прочее

- Запросы стараюсь писать только через statement 
(создавать объекты stmt для последующего их выполнения в session.execute(stmt)).
- Таблицы объявляются в Декларативный стиле (есть два - Императивный (классический) и Декларативный).