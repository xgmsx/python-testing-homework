import random

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field


@pytest.fixture(scope='session')
def faker_seed() -> int:
    """Seed generation fixture."""
    return random.Random().getrandbits(32)  # noqa: WPS432


@pytest.fixture(scope='session')
def mf(faker_seed: int) -> 'Field':
    """Mimesis faker fixture."""
    return Field(locale=Locale.RU, seed=faker_seed)
