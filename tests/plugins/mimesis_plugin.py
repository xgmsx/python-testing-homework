import random

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field

FAKER_SEED_MAGIC_NUMBER = 32


@pytest.fixture(scope='session')
def faker_seed() -> int:
    """Seed generation fixture."""
    return random.Random().getrandbits(FAKER_SEED_MAGIC_NUMBER)


@pytest.fixture(scope='session')
def mf(faker_seed: int) -> 'Field':
    """Mimesis faker fixture."""
    return Field(locale=Locale.RU, seed=faker_seed)
