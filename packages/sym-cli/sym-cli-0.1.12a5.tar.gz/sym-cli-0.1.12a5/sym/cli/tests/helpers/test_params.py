from sym.cli.helpers.config import Config
from sym.cli.helpers.params import get_profile
from sym.cli.tests.helpers.sandbox import Sandbox


def test_profile_aliases(sandbox: Sandbox):
    with sandbox.push_xdg_config_home():
        Config.instance()["org"] = "launchdarkly"
        assert get_profile("intuit_production") is not None
