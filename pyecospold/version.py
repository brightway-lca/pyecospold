"""Version information for lxmlh package."""
import pathlib


def _get_version():
    """Return the version number."""
    versionFile = pathlib.Path(__file__).parent / "VERSION"
    # Read the version number from VERSION file
    with open(versionFile, "r", encoding="UTF-8") as vf:
        # The full version, including alpha/beta/rc tags
        versionList = vf.read().strip().split(".")
    return ".".join(versionList)


__version__ = _get_version()
