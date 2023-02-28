import random

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field


@pytest.fixture(scope="session")
def faker_seed() -> int:
    return random.Random().getrandbits(32)


@pytest.fixture(scope="session")
def mf(faker_seed: int) -> 'Field':
    return Field(locale=Locale.RU, seed=faker_seed)
