from typer.testing import CliRunner
from chirrup import __version__, cli

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"chirrup v{__version__}\n" in result.stdout
