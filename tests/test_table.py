import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).parents[1]


class GatewayGuideTests(unittest.TestCase):
    def test_matrix_covers_required_gateway_families(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Checked 2026-10-07", text)
        for name in ("LiteLLM", "Portkey", "Bifrost", "Kong", "Envoy", "OpenRouter", "Cloudflare", "ArgoLink"):
            self.assertIn(name, text)
        for column in ("Route / load balance", "Fallback / retry", "Cache", "Budget / rate controls", "Self-host"):
            self.assertIn(column, text)

    def test_sources_have_primary_links(self):
        text = (ROOT / "sources.md").read_text(encoding="utf-8")
        self.assertIn("Checked 2026-10-07", text)
        self.assertGreaterEqual(len(re.findall(r"https://[^) ]+", text)), 10)

    def test_no_unsafe_credentials_or_retired_endpoint(self):
        text = "\n".join(p.read_text(encoding="utf-8") for p in ROOT.rglob("*.md"))
        self.assertNotIn("api." + "argolink.io", text)
        self.assertNotIn("sk-", text.lower())


if __name__ == "__main__":
    unittest.main()
