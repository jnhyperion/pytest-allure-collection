import os
import pytest
from pathlib import Path

tests_dir = os.path.abspath(os.path.dirname(__file__))
root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


@pytest.fixture(autouse=True)
def setup_conftest(testdir):
    testdir.makeconftest(
        f"""
        import sys
        import pytest
        sys.path.insert(0, "{root}")
        pytest_plugins = ("pytest_allure_collection")
    """
    )
    yield


@pytest.fixture
def expected_json(request) -> str:
    with open(os.path.join(tests_dir, "json", f"{request.node.name}.json")) as f:
        return f.read()


def test_allure_collect_recursive_folder(testdir, expected_json):
    test_src1 = """
    import allure
    import pytest
    @allure.tag("tag1", "tag2")
    @allure.title("my title")
    @allure.description("description")
    @pytest.mark.Foo
    def test_foo():
        assert 1==1
    
    @allure.tag("tag1", "tag2")
    @allure.title("my title bar")
    @allure.description("description")
    @pytest.mark.Bar
    def test_bar():
        assert 1==1
    """
    test_src2 = """
    import allure
    import pytest
    @allure.tag("tag1", "tag2")
    @allure.title("my title")
    @allure.description("description")
    @pytest.mark.Foo
    def test_foo():
        assert 1==1
    
    @allure.tag("tag1", "tag2")
    @allure.title("my title bar")
    @allure.description("description")
    @pytest.mark.Bar
    def test_bar():
        assert 1==1
    """
    test_src3 = """
    import allure
    import pytest
    @allure.description("description")
    @pytest.mark.Some
    def test_other_folder():
        assert 1==1
    """
    testdir.makepyfile(
        test_foo=test_src1,
        test_bar=test_src2,
    )
    root_folder = str(testdir)
    testdir._pytester._path = Path(testdir.mkdir("foo"))
    testdir.makepyfile(test_some=test_src3)
    testdir.runpytest("--co", "--collect-allure")
    json_out = os.path.join(root_folder, "allure_collection.json")
    assert os.path.exists(json_out)
    with open(json_out) as f:
        actual = f.read()
        assert actual == expected_json


def test_no_allure_marker(testdir, expected_json):
    test_src = """
    def test_foo():
        assert 1 == 1
    """
    testdir.makepyfile(test_src)
    testdir.runpytest("--co", "--collect-allure")
    json_out = os.path.join(str(testdir), "allure_collection.json")
    assert os.path.exists(json_out)
    with open(json_out) as f:
        actual = f.read()
        assert actual == expected_json


def test_non_allure_marker(testdir, expected_json):
    test_src = """
    import pytest
    @pytest.mark.Foo
    def test_foo():
        assert 1 == 1
    """
    testdir.makepyfile(test_src)
    testdir.runpytest("--co", "--collect-allure")
    json_out = os.path.join(str(testdir), "allure_collection.json")
    assert os.path.exists(json_out)
    with open(json_out) as f:
        actual = f.read()
        assert actual == expected_json


def test_non_allure_marker_without_param(testdir):
    test_src = """
    import pytest
    @pytest.mark.Foo
    def test_foo():
        assert 1 == 1
    """
    testdir.makepyfile(test_src)
    testdir.runpytest("--collect-allure")
    json_out = os.path.join(str(testdir), "allure_collection.json")
    assert not os.path.exists(json_out)


def test_non_allure_marker_non_collection_mode(testdir):
    test_src = """
    import pytest
    @pytest.mark.Foo
    def test_foo():
        assert 1 == 1
    """
    testdir.makepyfile(test_src)
    testdir.runpytest("--co")
    json_out = os.path.join(str(testdir), "allure_collection.json")
    assert not os.path.exists(json_out)


def test_help(testdir):
    result = testdir.runpytest(
        "--help",
    )
    result.stdout.fnmatch_lines(["pytest-allure-collection:", "*--collect-allure*"])


def test_with_allure_markers(testdir, expected_json):
    test_src = """
    import allure
    import time
    import pytest
    @allure.link("custom_link", "link", "foo")
    @allure.label("custom_label", "label1", "label2")
    @allure.id("id00000")
    @allure.tag("tag1", "tag2")
    @allure.story("story_label", "Foo")
    @allure.suite("suite_label")
    @allure.feature("feature_label")
    @allure.epic("epic_label")
    @allure.severity("severity_label")
    @allure.sub_suite("sub_suite_label")
    @allure.parent_suite("parent_suite_label")
    @allure.title("my title")
    @allure.description("description")
    @allure.description_html("<b>description</b>")
    @allure.issue("issue_link", "issue_name")
    @allure.testcase("case_link")
    @pytest.mark.Foo
    def test_foo():
        time.sleep(10000)
    """
    testdir.makepyfile(test_src)
    testdir.runpytest("--co", "--collect-allure")
    json_out = os.path.join(str(testdir), "allure_collection.json")
    assert os.path.exists(json_out)
    with open(json_out) as f:
        actual = f.read()
        assert actual == expected_json


def test_multi_cases_with_allure_markers(testdir, expected_json):
    test_src = """
    import allure
    import time
    import pytest
    @allure.link("custom_link", "link", "foo")
    @allure.label("custom_label", "label1", "label2")
    @allure.id("id00000")
    @allure.tag("tag1", "tag2")
    @allure.story("story_label", "Foo")
    @allure.suite("suite_label")
    @allure.feature("feature_label")
    @allure.epic("epic_label")
    @allure.severity("severity_label")
    @allure.sub_suite("sub_suite_label")
    @allure.parent_suite("parent_suite_label")
    @allure.title("my title")
    @allure.description("description")
    @allure.description_html("<b>description</b>")
    @allure.issue("issue_link", "issue_name")
    @allure.testcase("case_link")
    @pytest.mark.Foo
    def test_foo():
        time.sleep(10000)
    @allure.description_html("<b>description</b>")
    @allure.issue("issue_link", "issue_name")
    @allure.testcase("case_link")
    @pytest.mark.Bar
    def test_bar():
        time.sleep(10000)
    @allure.testcase("case_link")
    @pytest.mark.Some
    def test_other():
        time.sleep(10000)
    """
    testdir.makepyfile(test_src)
    testdir.runpytest("--co", "--collect-allure")
    json_out = os.path.join(str(testdir), "allure_collection.json")
    assert os.path.exists(json_out)
    with open(json_out) as f:
        actual = f.read()
        assert actual == expected_json


def test_with_allure_markers_disable_collection(testdir):
    test_src = """
    import allure
    import time
    import pytest
    @allure.link("custom_link", "link", "foo")
    @allure.label("custom_label", "label1", "label2")
    @allure.id("id00000")
    @allure.tag("tag1", "tag2")
    @allure.story("story_label", "Foo")
    @allure.suite("suite_label")
    @allure.feature("feature_label")
    @allure.epic("epic_label")
    @allure.severity("severity_label")
    @allure.sub_suite("sub_suite_label")
    @allure.parent_suite("parent_suite_label")
    @allure.title("my title")
    @allure.description("description")
    @allure.description_html("<b>description</b>")
    @allure.issue("issue_link", "issue_name")
    @allure.testcase("case_link")
    @pytest.mark.Foo
    def test_foo():
        time.sleep(10000)
    """
    testdir.makepyfile(test_src)
    testdir.runpytest("--co")
    json_out = os.path.join(str(testdir), "allure_collection.json")
    assert not os.path.exists(json_out)


def test_with_allure_markers_non_collection_mode(testdir):
    test_src = """
    import allure
    import pytest
    @allure.link("custom_link", "link", "foo")
    @allure.label("custom_label", "label1", "label2")
    @allure.id("id00000")
    @allure.tag("tag1", "tag2")
    @allure.story("story_label", "Foo")
    @allure.suite("suite_label")
    @allure.feature("feature_label")
    @allure.epic("epic_label")
    @allure.severity("severity_label")
    @allure.sub_suite("sub_suite_label")
    @allure.parent_suite("parent_suite_label")
    @allure.title("my title")
    @allure.description("description")
    @allure.description_html("<b>description</b>")
    @allure.issue("issue_link", "issue_name")
    @allure.testcase("case_link")
    @pytest.mark.Foo
    def test_foo():
        assert 1==1
    """
    testdir.makepyfile(test_src)
    testdir.runpytest("--collect-allure")
    json_out = os.path.join(str(testdir), "allure_collection.json")
    assert not os.path.exists(json_out)
