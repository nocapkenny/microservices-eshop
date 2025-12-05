import pytest
from unittest.mock import MagicMock
from django.core import exceptions as django_exceptions
from rest_framework import serializers as drf_serializers

from . import serializers as user_serializers
from .serializers import UserRegistrationSerializer


class FakeUser:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def test_validate_email_when_unique(monkeypatch):
    ser = UserRegistrationSerializer()
    mock_mgr = MagicMock()
    mock_mgr.filter.return_value.exists.return_value = False
    monkeypatch.setattr(user_serializers.User, "objects", mock_mgr, raising=False)

    out = ser.validate_email("unique@example.com")
    assert out == "unique@example.com"


def test_validate_email_when_exists_raises(monkeypatch):
    ser = UserRegistrationSerializer()
    mock_mgr = MagicMock()
    mock_mgr.filter.return_value.exists.return_value = True
    monkeypatch.setattr(user_serializers.User, "objects", mock_mgr, raising=False)

    with pytest.raises(drf_serializers.ValidationError):
        ser.validate_email("exists@example.com")


def test_validate_password_valid_and_invalid(monkeypatch):
    ser = UserRegistrationSerializer()

    monkeypatch.setattr(user_serializers, "validate_password", lambda v: None)
    assert ser.validate_password("Str0ngP@ssw") == "Str0ngP@ssw"

    def _raise(p):
        raise django_exceptions.ValidationError(["too weak"])
    monkeypatch.setattr(user_serializers, "validate_password", _raise)
    with pytest.raises(drf_serializers.ValidationError) as exc:
        ser.validate_password("weak")
    assert any("too weak" in str(x) for x in exc.value.detail)


def test_validate_passwords_match_and_mismatch():
    ser = UserRegistrationSerializer()
    with pytest.raises(drf_serializers.ValidationError) as exc:
        ser.validate({"password": "a", "password_confirm": "b"})
    assert "password_confirm" in exc.value.detail

    attrs = {"password": "same", "password_confirm": "same", "email": "e@example.com"}
    out = ser.validate(attrs.copy())
    assert out["password"] == "same"
    assert out["password_confirm"] == "same"


def test_create_calls_create_user_and_pops_confirm(monkeypatch):
    ser = UserRegistrationSerializer()
    mock_mgr = MagicMock()
    fake_user = FakeUser(email="u@example.com")
    mock_mgr.create_user.return_value = fake_user
    monkeypatch.setattr(user_serializers.User, "objects", mock_mgr, raising=False)

    validated = {
        "email": "u@example.com",
        "password": "Abc12345!",
        "password_confirm": "Abc12345!",
        "first_name": "F",
        "last_name": "L",
    }

    user = ser.create(validated.copy())
    mock_mgr.create_user.assert_called_once()
    called_kwargs = mock_mgr.create_user.call_args[1]
    assert "password_confirm" not in called_kwargs
    assert called_kwargs["email"] == "u@example.com"
    assert user is fake_user