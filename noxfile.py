"""Nox Sessions."""
import tempfile

import nox
from nox.sessions import Session
from typing import Any

locations = "src", "tests", "noxfile.py"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python="3.8")
def tests(session: Session) -> None:
    """Run test suite."""
    args = session.posargs
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "pytest")
    session.run("pytest", *args)


@nox.session(python="3.8")
def black(session: Session) -> None:
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)
