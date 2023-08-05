import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import SelectItemNotFound
from widgetastic_patternfly4.ouia import ContextSelector

TESTING_PAGE_URL = "https://patternfly-docs-ouia.netlify.app/documentation/react/components/contextselector"  # noqa


@pytest.fixture
def view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-contextselector-ouia']"
        contextselector = ContextSelector("Basic")

    return TestView(browser)


def test_contextselector_is_displayed(view):
    assert view.contextselector.is_displayed


def test_contextselector_items(view):
    assert set(view.contextselector.items) == {
        "My Project",
        "OpenShift Cluster",
        "Production Ansible",
        "AWS",
        "Azure",
        "My Project 2",
        "Production Ansible 2",
        "AWS 2",
        "Azure 2",
    }
    assert view.contextselector.has_item("AWS")
    assert not view.contextselector.has_item("Non existing item")


def test_contextselector_open(view):
    assert not view.contextselector.is_open
    view.contextselector.open()
    assert view.contextselector.is_open
    view.contextselector.close()
    assert not view.contextselector.is_open


def test_contextselector_item_select(view):
    view.contextselector.fill("AWS")
    assert view.contextselector.read() == "AWS"
    assert not view.contextselector.is_open
    with pytest.raises(SelectItemNotFound):
        view.contextselector.fill("Non existing item")
    assert not view.contextselector.is_open
