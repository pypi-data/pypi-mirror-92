import os

import pytest
from novaposhta.client import Novaposhta

TEST_KEY = os.environ.get('TEST_API_KEY')


@pytest.fixture
def client():
    return Novaposhta(api_key=TEST_KEY)
