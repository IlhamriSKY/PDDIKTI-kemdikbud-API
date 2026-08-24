"""Minimal quickstart for pddiktipy.

The upstream API sits behind Cloudflare, so you must provide clearance. Pick the
option that fits your setup (see the README "Cloudflare access" section):

    # A. Easiest on your own machine (requires: pip install "pddiktipy[auto]")
    #    Open https://pddikti.kemdiktisaintek.go.id once, pass the check, then:
    client = api(auto_cookie=True)

    # B. Paste cf_clearance + User-Agent from your browser's DevTools:
    client = api(cf_clearance="...", user_agent="Mozilla/5.0 ...")

    # C. Point at your own Cloudflare-solving proxy:
    client = api(base_url="http://localhost:8080/api")

Run:  python examples/quickstart.py
"""
from pddiktipy import api


def main() -> None:
    """Run a few representative queries against the live API."""
    with api(auto_cookie=True) as client:
        # Aggregate counts
        print("Universities:", client.get_pt_count())
        print("Students    :", client.get_mahasiswa_count())

        # Combined search (payload is AES-decrypted transparently)
        results = client.search_all("Universitas Diponegoro")
        students = (results or {}).get("data", {}).get("mahasiswa", [])
        if students:
            first = students[0]
            print("Example     :", first["nama"], "-", first["nama_pt"])


if __name__ == "__main__":
    main()
