"""Test cases fake-uwsgi package"""
import os

import fake_uwsgi


def test_environ():
    """Test the environment values fake_uwsgi should set."""
    assert os.environ.get("INSTALL_PATH") == os.path.abspath(
        os.path.join(fake_uwsgi.__file__, os.pardir)
    )
    assert os.environ.get("APP_RUN_MODE") == "development"


def test_global_variables():
    """Test the global variables set by fake_uwsgi module"""
    assert fake_uwsgi.opt == {"mode": b"development", "vassal-name": b"fake-uwsgi"}

    assert fake_uwsgi.numproc == 4

    assert fake_uwsgi.LOGVAR == dict()


def test_log(capfd):
    """Test the log function of fake_uwsgi"""
    fake_uwsgi.log("This is a test string being printed.")
    out = capfd.readouterr()[0]
    assert out == "This is a test string being printed.\n"


def test_log_var():
    """Test the set and get log variable functions."""

    # When the key is not set, get_logvar should return None
    assert "test" not in fake_uwsgi.LOGVAR
    assert fake_uwsgi.get_logvar("test") is None

    # Set the value and get it
    fake_uwsgi.set_logvar("test", "yahoo")
    assert fake_uwsgi.get_logvar("test") == "yahoo"

    # Providing the key only should set the value to None
    fake_uwsgi.set_logvar("test")
    assert fake_uwsgi.get_logvar("test") is None

    # Add the same key with a different value
    fake_uwsgi.set_logvar(test="montreal")
    assert fake_uwsgi.get_logvar("test") == "montreal"

    # Add multiple keys and update an existing one
    fake_uwsgi.set_logvar(test="ottawa", another_test="toronto")

    assert fake_uwsgi.get_logvar("test") == "ottawa"
    assert fake_uwsgi.get_logvar("another_test") == "toronto"


def test_worker_id():
    """Test the worker_id function in fake_uwsgi"""
    assert fake_uwsgi.worker_id() == 123


def test_workers():
    """Test the workers function in fake_uwsgi"""
    assert isinstance(fake_uwsgi.workers(), list)

    # Each element of the list should be a dict
    for item in fake_uwsgi.workers():
        assert isinstance(item, dict)


def test_total_requests():
    """Test the total_requests function in fake_uwsgi"""
    assert fake_uwsgi.total_requests() == 564
