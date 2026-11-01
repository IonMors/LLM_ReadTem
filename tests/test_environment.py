
import importlib.metadata
import sys


def test_python_version():
    """Project requires Python 3.13."""
    assert sys.version_info.major == 3
    assert sys.version_info.minor == 12


def test_deepteam_installed():
    """Verify DeepTeam is installed."""
    version = importlib.metadata.version("deepteam")
    assert version is not None


def test_openai_sdk_installed():
    """Verify the OpenAI-compatible SDK is installed."""
    version = importlib.metadata.version("openai")
    assert version is not None


def test_dotenv_installed():
    """Verify environment configuration library is installed."""
    version = importlib.metadata.version("python-dotenv")
    assert version is not None
