import pytest
from unittest.mock import MagicMock

from . import views as user_views
from . import serializers as user_serializers


class FakeUser:
    def __init__(self, email="u@example.com", is_active=True):
        self.email = email
        self.is_active = is_active


class FakeRefresh:
    def __init__(self, token_str="refresh"):
        self._token = token_str
        self.access_token = MagicMock()
        # access_token string representation
        self.access_token.__str__.return_value = "access_token_str"

    def __str__(self):
        return self._token

    @classmethod
    def for_user(cls, user):
        return cls("refresh_for_user")


def make_request(data):
    req = MagicMock()
    req.data = data
    return req


def test_login_missing_fields():
    req = make_request({})
    resp = user_views.login_view(req)
    assert resp.status_code == 400
    assert "error" in resp.data


def test_login_success(monkeypatch):
    # patch authenticate to return active user
    monkeypatch.setattr(user_views, "authenticate", lambda username, password: FakeUser(email=username, is_active=True))
    # patch RefreshToken.for_user to return fake refresh with tokens
    monkeypatch.setattr(user_views, "RefreshToken", FakeRefresh)
    # patch UserSerializer to return object with .data
    monkeypatch.setattr(user_views, "UserSerializer", lambda user: MagicMock(data={"email": user.email}))

    req = make_request({"email": "ok@example.com", "password": "pw"})
    resp = user_views.login_view(req)
    assert resp.status_code == 200
    assert "access" in resp.data and "refresh" in resp.data and "user" in resp.data
    assert resp.data["user"]["email"] == "ok@example.com"


def test_login_inactive(monkeypatch):
    monkeypatch.setattr(user_views, "authenticate", lambda username, password: FakeUser(email=username, is_active=False))
    req = make_request({"email": "inactive@example.com", "password": "pw"})
    resp = user_views.login_view(req)
    assert resp.status_code == 401
    assert "error" in resp.data


def test_login_wrong_credentials(monkeypatch):
    monkeypatch.setattr(user_views, "authenticate", lambda username, password: None)
    req = make_request({"email": "noone@example.com", "password": "pw"})
    resp = user_views.login_view(req)
    assert resp.status_code == 401
    assert "error" in resp.data


def test_refresh_missing_token():
    req = make_request({})
    resp = user_views.refresh_token(req)
    assert resp.status_code == 400
    assert "error" in resp.data


def test_refresh_success(monkeypatch):
    # make RefreshToken(token) return object with access_token
    monkeypatch.setattr(user_views, "RefreshToken", FakeRefresh)
    req = make_request({"refresh": "valid_refresh"})
    resp = user_views.refresh_token(req)
    assert resp.status_code == 200
    assert resp.data.get("access") == "access_token_str"


def test_refresh_invalid_token(monkeypatch):
    class BadRefresh:
        def __init__(self, token):
            raise Exception("bad token")

    monkeypatch.setattr(user_views, "RefreshToken", BadRefresh)
    req = make_request({"refresh": "bad"})
    resp = user_views.refresh_token(req)
    assert resp.status_code == 401
    assert "error" in resp.data


def test_register_invalid(monkeypatch):
    # Patch serializer class in serializers module so inner import in view picks it up
    class FakeSerializerInvalid:
        def __init__(self, data=None):
            self.data = data
            self.errors = {"email": ["error"]}
        def is_valid(self):
            return False

    monkeypatch.setattr(user_serializers, "UserRegistrationSerializer", FakeSerializerInvalid, raising=False)

    req = make_request({"email": "x@x.com", "password": "p", "password_confirm": "p"})
    resp = user_views.register_view(req)
    assert resp.status_code == 400
    assert resp.data == {"email": ["error"]}


def test_register_success(monkeypatch):
    # Fake serializer that validates and saves a user
    class FakeSerializerValid:
        def __init__(self, data=None):
            self.data = data
        def is_valid(self):
            return True
        def save(self):
            return FakeUser(email=self.data.get("email"))

    monkeypatch.setattr(user_serializers, "UserRegistrationSerializer", FakeSerializerValid, raising=False)
    # patch RefreshToken.for_user
    monkeypatch.setattr(user_views, "RefreshToken", FakeRefresh)
    # patch UserSerializer to provide .data
    monkeypatch.setattr(user_views, "UserSerializer", lambda user: MagicMock(data={"email": user.email}))

    req = make_request({"email": "new@example.com", "password": "Abc12345!", "password_confirm": "Abc12345!"})
    resp = user_views.register_view(req)
    assert resp.status_code == 201
    assert "access" in resp.data and "refresh" in resp.data and "user" in resp.data
    assert resp.data["user"]["email"] == "new@example.com"