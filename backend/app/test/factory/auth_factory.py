from datetime import datetime

from factory import BUILD_STRATEGY, Factory, LazyAttribute
from faker import Faker
from src.domain.model.auth import Auth

fake = Faker()
current_datetime = datetime.utcnow()


class AuthFactory(Factory):
    class Meta:
        strategy = BUILD_STRATEGY
        model = Auth

    id = LazyAttribute(lambda _: fake.uuid4())
    username = LazyAttribute(lambda _: fake.user_name())
    password = LazyAttribute(lambda _: fake.password())
    login_id = LazyAttribute(lambda _: fake.uuid4())
    refresh_token_id = LazyAttribute(lambda _: fake.uuid4())
    created_at = LazyAttribute(lambda _: current_datetime)
    updated_at = LazyAttribute(lambda _: None)
