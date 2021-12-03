"""Simple test module for testing"""
import tests.mockup.cf_19 as data
from pytest import fixture
import datetime


@fixture()
def dataset():
    return data.dataset(
        start_date=datetime.datetime(2020, 1, 1),
        end_date=datetime.datetime(2020, 1, 20),

    )


def test_simple(dataset):
    assert True
