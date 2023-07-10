from uuid import UUID
from users.model import User, UserOut, UserIn

users = [
    {
        "id": "58c490d0-2105-48a6-9e75-99836634e5c1",
        "name": "User 1",
        "email": "u1mail@mail.com",
        "password_hash": "$2a$12$7QpRmCf0yZphJS29HdpYYON1aRGGkDNsQxatgUm4Te4cxHOov5bWK",
    },
    {
        "id": "ba44c1f7-1702-4a10-b856-a3d60223835b",
        "email": "u2mail@mail.com",
        "name": "User 2",
        "password_hash": "$2a$12$QBdQzbBpBChZLfkd4o5XCuQZvUast9CvakyFopIPvUunNw4ybtpd2",
    },
    {
        "id": "576d864b-163c-4121-8011-283a58dfde73",
        "name": "User 3",
        "email": "u3mail@mail.com",
        "password_hash": "$2a$12$KCt7kDiHIfDHXLV13NAsL.lQfbhHnOTCzS5gVnFBPi2fXALAyGZly",
    },
]


def user_exist(email: str) -> bool:
    return True if [item for item in users if item.get("email") == email] else False


def get_users() -> list[UserOut]:
    users_out = [
        {"num": i, "user": UserOut(**data)} for i, data in enumerate(users, start=1)
    ]
    return users_out


def get_user_by_email(email: str) -> User | None:
    user = [item for item in users if item.get("email") == email]
    return User(**user[0]) if user else None


def add_user(user: User) -> None:
    users.append(user.model_dump())


def update_user(email: str, user: User) -> UserOut:
    updated_user = [item for item in users if item.get("email") == email]
    updated_user[0].update({"name": user.name})
    updated_user[0].update({"email": user.email})
    updated_user[0].update({"password_hash": user.password_hash})

    return UserOut(**user.model_dump(exclude=["id", "password_hash"]))


def del_user(email: str) -> UserOut:
    deleted_user = [item for item in users if item.get("email") == email]
    user = UserOut(**deleted_user[0])
    users.remove(deleted_user[0])
    return user


if __name__ == "__main__":
    email = "u2mail@mail.com"
    user = get_user_by_email(email=email)
    print(user.model_dump(exclude="id").values())
