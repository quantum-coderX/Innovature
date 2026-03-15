#!/usr/bin/env python3
"""Week 7 API smoke tests for public sharing links."""

import time
from datetime import datetime, timedelta, timezone
import requests


BASE_URL = "http://localhost:5000"


def _assert_status(response, expected_codes, label):
    if response.status_code not in expected_codes:
        raise AssertionError(
            f"{label} failed. Expected {expected_codes}, got {response.status_code}. Body: {response.text}"
        )


def _register_and_login(username, password):
    register = requests.post(
        f"{BASE_URL}/auth/register",
        json={"username": username, "password": password},
        timeout=15,
    )
    _assert_status(register, {201, 500}, f"register {username}")

    login = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": username, "password": password},
        timeout=15,
    )
    _assert_status(login, {200}, f"login {username}")
    token = login.json().get("access_token")
    if not token:
        raise AssertionError(f"No access token returned for {username}")
    return token


def _auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def run_week7_tests():
    owner_username = f"week7_owner_{int(time.time())}"
    other_username = f"week7_other_{int(time.time())}"
    password = "Testpass1"

    print("1) Register/login owner and second user")
    owner_token = _register_and_login(owner_username, password)
    other_token = _register_and_login(other_username, password)

    print("2) Create note as owner")
    create_note = requests.post(
        f"{BASE_URL}/notes",
        headers=_auth_headers(owner_token),
        json={"title": "Shared note", "content": "Visible via public token."},
        timeout=15,
    )
    _assert_status(create_note, {201}, "create note")
    note_id = create_note.json()["id"]

    print("3) Create share link without expiration")
    create_share = requests.post(
        f"{BASE_URL}/notes/{note_id}/share",
        headers=_auth_headers(owner_token),
        json={},
        timeout=15,
    )
    _assert_status(create_share, {201}, "create share without expiration")
    share = create_share.json()
    share_id = share["id"]
    token = share["token"]

    print("4) Public access and counter increment")
    public_one = requests.get(f"{BASE_URL}/s/{token}", timeout=15)
    _assert_status(public_one, {200}, "first public access")
    c1 = public_one.json()["share"]["access_count"]

    public_two = requests.get(f"{BASE_URL}/s/{token}", timeout=15)
    _assert_status(public_two, {200}, "second public access")
    c2 = public_two.json()["share"]["access_count"]
    if c2 <= c1:
        raise AssertionError(f"access_count did not increase: {c1} -> {c2}")

    print("5) Non-owner cannot list owner share links")
    non_owner_list = requests.get(
        f"{BASE_URL}/notes/{note_id}/shares",
        headers=_auth_headers(other_token),
        timeout=15,
    )
    _assert_status(non_owner_list, {403, 404}, "non-owner share list")

    print("6) Revoke share and ensure public access fails")
    revoke = requests.patch(
        f"{BASE_URL}/notes/{note_id}/shares/{share_id}",
        headers=_auth_headers(owner_token),
        json={"is_revoked": True},
        timeout=15,
    )
    _assert_status(revoke, {200}, "revoke share")

    revoked_public = requests.get(f"{BASE_URL}/s/{token}", timeout=15)
    _assert_status(revoked_public, {410}, "public access after revoke")

    print("7) Create short-lived share and verify expiration")
    short_lived = (datetime.now(timezone.utc) + timedelta(seconds=15)).isoformat().replace('+00:00', 'Z')
    expired_share = requests.post(
        f"{BASE_URL}/notes/{note_id}/share",
        headers=_auth_headers(owner_token),
        json={"expires_at": short_lived},
        timeout=15,
    )
    _assert_status(expired_share, {201}, "create future-expiry share")
    expired_data = expired_share.json()

    time.sleep(16)

    inactive_public = requests.get(f"{BASE_URL}/s/{expired_data['token']}", timeout=15)
    _assert_status(inactive_public, {410}, "public access for expired share")

    print("All Week 7 sharing tests passed")


if __name__ == "__main__":
    run_week7_tests()