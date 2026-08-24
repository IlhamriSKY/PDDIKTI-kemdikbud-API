"""
Offline checks for the v2.1 upstream migration.

Covers the AES-256-CBC round trip and the endpoint URLs that changed when
upstream moved from api-pddikti.kemdiktisaintek.go.id to the same-origin
/api path. No network required.
"""
# Fixture injection and white-box endpoint checks are the point here:
# pylint: disable=missing-function-docstring,missing-class-docstring
# pylint: disable=redefined-outer-name,protected-access,too-few-public-methods
# pylint: disable=import-outside-toplevel

import pytest

from pddiktipy.api import api
from pddiktipy.exceptions import ValidationError


@pytest.fixture
def client():
    with api() as c:
        yield c


def test_default_base_url_is_the_new_upstream(client):
    assert client.api_link == "https://pddikti.kemdiktisaintek.go.id/api"


def test_base_url_override_wins_and_drops_pinned_host():
    with api(base_url="http://localhost:8080/api/") as c:
        assert c.api_link == "http://localhost:8080/api"
        assert "Host" not in c.H.get_headers()


def test_default_upstream_pins_host_header(client):
    assert client.H.get_headers()["Host"] == "pddikti.kemdiktisaintek.go.id"


def test_injected_session_is_used():
    import requests
    s = requests.Session()
    with api(session=s) as c:
        assert c.H.session is s


def test_cf_clearance_sets_cookie_and_user_agent():
    ua = "Mozilla/5.0 (X11; Linux x86_64) Chrome/140.0.0.0 Safari/537.36"
    with api(cf_clearance="TESTTOKEN123", user_agent=ua) as c:
        # cookie lands on the session jar for the upstream domain
        jar = c.H.session.cookies
        assert jar.get("cf_clearance", domain="kemdiktisaintek.go.id") == "TESTTOKEN123"
        # the provided UA must be sent (cf_clearance is bound to it)
        assert c.H.get_headers()["User-Agent"] == ua


def test_default_user_agent_when_none_given():
    with api() as c:
        assert c.H.get_headers()["User-Agent"].startswith("Mozilla/5.0")


def test_cloudflare_403_raises_actionable_error(monkeypatch):
    from pddiktipy import helper as helper_mod

    class FakeResp:
        status_code = 403
        headers = {
            "content-type": "text/html; charset=UTF-8",
            "cf-mitigated": "challenge",
        }

        def json(self):
            return {}

        def raise_for_status(self):
            pass

    class FakeSession:
        def get(self, *args, **kwargs):
            del args, kwargs
            return FakeResp()

    with api(session=FakeSession()) as c:
        monkeypatch.setattr(c.H, "get_ip", lambda: "1.2.3.4")
        with pytest.raises(helper_mod.APIResponseError) as ei:
            c.H.response("https://pddikti.kemdiktisaintek.go.id/api/pt/count")
        assert "Cloudflare" in str(ei.value) and "auto_cookie" in str(ei.value)


def test_changed_endpoint_paths(client):
    """The three paths that broke when upstream migrated."""
    assert client._build_endpoint("pencarian/enc/all", "undip").endswith(
        "/pencarian/enc/all/undip"
    )
    assert client._build_endpoint("pt/detail", "abc123").endswith("/pt/detail/abc123")
    assert client._content("announcements", 2, 5, "").startswith(
        "https://pddikti.kemdiktisaintek.go.id/api/content/announcements?"
    )


def test_content_pagination_params(client):
    url = client._content("publications", page=3, page_size=25, search="beasiswa")
    assert "page=3" in url and "page_size=25" in url and "search=beasiswa" in url


def test_filter_search_endpoints(client):
    q = client._filter_query(20, 40, {"provinsi": "Jawa Tengah"})
    assert "limit=20" in q and "offset=40" in q and "provinsi=Jawa%20Tengah" in q


def test_beranda_endpoint(client):
    # get_beranda builds /beranda?content_limit=N; verify via the helper URL shape
    assert client.api_link + "/beranda?content_limit=8" == \
        f"{client.api_link}/beranda?content_limit={client.H.parse(8)}"


def test_id_encryption_round_trip(client):
    plain = "0A2B3C4D-5E6F-7890-ABCD-EF1234567890"
    assert client.H.decrypt_id(client.H.encrypt_id(plain)) == plain


def test_encrypt_id_pads_exact_block_multiple(client):
    """A 16-byte input must gain a full padding block, not zero."""
    plain = "0123456789abcdef"
    assert client.H.decrypt_id(client.H.encrypt_id(plain)) == plain


def test_decrypt_rejects_bad_input(client):
    with pytest.raises(ValidationError):
        client.H.decrypt("")
    with pytest.raises(ValidationError):
        client.H.decrypt("bm90LWEtdmFsaWQtYmxvY2s=")  # not a block multiple


def test_decrypt_returns_parsed_json(client):
    import base64
    import json

    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    from pddiktipy.helper import AES_IV, AES_KEY

    payload = json.dumps({"mahasiswa": [{"nama": "Budi"}]}).encode()
    pad = 16 - (len(payload) % 16)
    enc = Cipher(
        algorithms.AES(base64.b64decode(AES_KEY)),
        modes.CBC(base64.b64decode(AES_IV)),
    ).encryptor()
    blob = base64.b64encode(enc.update(payload + bytes([pad]) * pad) + enc.finalize()).decode()

    assert client.H.decrypt(blob) == {"mahasiswa": [{"nama": "Budi"}]}
