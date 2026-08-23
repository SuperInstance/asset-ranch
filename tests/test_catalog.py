import json, os, subprocess, sys, tempfile, unittest

CAT = os.path.join(os.path.dirname(__file__), "..", "scripts", "catalog.py")

def run(*args):
    return subprocess.run([sys.executable, CAT, *args], capture_output=True, text=True)

class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        open(os.path.join(self.d, "a.png"), "w").write("x")

    def test_add_pending_and_review(self):
        r = run("add", "--dir", self.d, "--file", "a.png", "--prompt", "p",
                "--model", "m", "--lane", "cloud-free")
        self.assertEqual(r.returncode, 0, r.stderr)
        aid = r.stdout.strip()
        m = json.load(open(os.path.join(self.d, "manifest.json")))
        self.assertEqual(m["assets"][0]["verdict"], "pending")
        r = run("review", aid, "--dir", self.d, "--verdict", "approve", "--note", "clean")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("approved", r.stdout)
        m = json.load(open(os.path.join(self.d, "manifest.json")))
        self.assertEqual(m["assets"][0]["verdict"], "approved")
        self.assertEqual(m["assets"][0]["note"], "clean")

    def test_no_double_flip_without_force(self):
        aid = run("add", "--dir", self.d, "--file", "a.png", "--prompt", "p",
                  "--model", "m", "--lane", "local").stdout.strip()
        run("review", aid, "--dir", self.d, "--verdict", "approve")
        r = run("review", aid, "--dir", self.d, "--verdict", "reject")
        self.assertNotEqual(r.returncode, 0)

    def test_missing_file_rejected(self):
        r = run("add", "--dir", self.d, "--file", "nope.png", "--prompt", "p",
                "--model", "m", "--lane", "local")
        self.assertNotEqual(r.returncode, 0)

if __name__ == "__main__":
    unittest.main()
