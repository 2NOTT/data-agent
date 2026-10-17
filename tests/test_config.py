import os
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

from dotenv import load_dotenv


class ConfigTests(unittest.TestCase):
    def load_config(self, environment):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            env_file = Path(directory) / ".env"
            env_file.write_text(
                "API_KEY=test-file-key\nBASE_URL=https://example.invalid/v1\nMODEL=test-model\n",
                encoding="utf-8",
            )
            with patch.dict(os.environ, environment, clear=True), patch(
                "dotenv.load_dotenv",
                side_effect=lambda _path, **kwargs: load_dotenv(env_file, **kwargs),
            ) as loader:
                config = runpy.run_path(str(root / "app/conf/app_config.py"))["app_config"]
                loader.assert_called_once_with(root / ".env", override=False)
                return config

    def test_loads_project_env(self):
        config = self.load_config({})
        self.assertEqual(config.llm.api_key, "test-file-key")
        self.assertEqual(config.llm.base_url, "https://example.invalid/v1")
        self.assertEqual(config.llm.model_name, "test-model")

    def test_environment_overrides_env_file(self):
        config = self.load_config({"API_KEY": "test-process-key", "MODEL": "process-model"})
        self.assertEqual(config.llm.api_key, "test-process-key")
        self.assertEqual(config.llm.model_name, "process-model")


if __name__ == "__main__":
    unittest.main()
