
import pytest
import pydantic
from propan.test.rabbit import build_message

from main import healthcheck

def test_publish(test_broker):
    msg = build_message({ "msg": "ping" }, queue="ping")
    with pytest.raises(pydantic.ValidationError):
        await healthcheck(msg, reraise_exc=True)