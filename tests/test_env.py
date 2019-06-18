import tempfile
import unittest
import unittest.mock

from tutor import config as tutor_config
from tutor import env
from tutor import exceptions


class EnvTests(unittest.TestCase):
    def test_walk_templates(self):
        templates = list(env.walk_templates("local"))
        self.assertIn("local/docker-compose.yml", templates)

    def test_pathjoin(self):
        self.assertEqual(
            "/tmp/env/target/dummy", env.pathjoin("/tmp", "target", "dummy")
        )
        self.assertEqual("/tmp/env/dummy", env.pathjoin("/tmp", "dummy"))

    def test_render_str(self):
        self.assertEqual(
            "hello world", env.render_str({"name": "world"}, "hello {{ name }}")
        )

    def test_common_domain(self):
        self.assertEqual(
            "mydomain.com",
            env.render_str(
                {"d1": "d1.mydomain.com", "d2": "d2.mydomain.com"},
                "{{ d1|common_domain(d2) }}",
            ),
        )

    def test_render_str_missing_configuration(self):
        self.assertRaises(exceptions.TutorError, env.render_str, {}, "hello {{ name }}")

    def test_render_file(self):
        config = {}
        tutor_config.merge(config, tutor_config.load_defaults())
        config["MYSQL_ROOT_PASSWORD"] = "testpassword"
        rendered = env.render_file(config, "hooks", "mysql-client", "init")
        self.assertIn("testpassword", rendered)

    @unittest.mock.patch.object(tutor_config.fmt, "echo")
    def test_render_file_missing_configuration(self, _):
        self.assertRaises(
            exceptions.TutorError, env.render_file, {}, "local", "docker-compose.yml"
        )

    def test_render_full(self):
        defaults = tutor_config.load_defaults()
        with tempfile.TemporaryDirectory() as root:
            env.render_full(root, defaults)

    def test_render_full_with_https(self):
        defaults = tutor_config.load_defaults()
        defaults["ACTIVATE_HTTPS"] = True
        with tempfile.TemporaryDirectory() as root:
            env.render_full(root, defaults)

    def test_patch(self):
        patches = {"plugin1": "abcd", "plugin2": "efgh"}
        with unittest.mock.patch.object(
            env.plugins, "iter_patches", return_value=patches.items()
        ) as mock_iter_patches:
            rendered = env.render_str({}, '{{ patch("location") }}')
            mock_iter_patches.assert_called_once_with({}, "location")
        self.assertEqual("abcd\nefgh", rendered)

    def test_patch_separator_suffix(self):
        patches = {"plugin1": "abcd", "plugin2": "efgh"}
        with unittest.mock.patch.object(
            env.plugins, "iter_patches", return_value=patches.items()
        ):
            rendered = env.render_str(
                {}, '{{ patch("location", separator=",\n", suffix=",") }}'
            )
        self.assertEqual("abcd,\nefgh,", rendered)
