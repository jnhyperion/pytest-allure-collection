from .__version__ import __version__
import os
import json
import pytest
import platform
from allure_pytest.utils import (
    ALLURE_DESCRIPTION_MARK,
    ALLURE_DESCRIPTION_HTML_MARK,
    ALLURE_LINK_MARK,
    ALLURE_LABEL_MARK,
)

_OUTPUT_JSON_FILE_NAME = "allure_collection.json"


@pytest.mark.trylast
def pytest_addoption(parser):
    collect_allure_help = "Collect allure markers into output json file, only works in `collect-only` mode."
    group = parser.getgroup("pytest-allure-collection")
    group.addoption("--collect-allure", action="store_true", help=collect_allure_help)


@pytest.mark.trylast
def pytest_collection(session):
    should_collect: bool = getattr(session.config.option, "collect_allure", True)
    if session.config.option.collectonly and should_collect:
        results = []
        for test in session.items:
            file_path, _, method_name = test.location
            file_path = (
                file_path.replace("\\", "/")
                if platform.system().lower() == "windows"
                else file_path
            )
            test_dict = {
                "name": test.name,
                "location": f"{file_path}::{method_name.replace('.', '::')}",
                "markers": {},
            }
            markers = test.iter_markers()
            title = getattr(test._obj, "__allure_display_name__", None)
            if title:
                test_dict["markers"]["allure_title"] = title
            for marker in markers:
                if marker.name in (
                    ALLURE_DESCRIPTION_MARK,
                    ALLURE_DESCRIPTION_HTML_MARK,
                ):
                    test_dict["markers"][f"{marker.name}"] = f"{marker.args[0]}"
                elif marker.name == ALLURE_LINK_MARK:
                    link_type = marker.kwargs["link_type"]
                    test_dict["markers"][f"allure_{link_type}"] = {
                        "url": marker.args[0],
                        "name": marker.kwargs["name"],
                    }
                elif marker.name == ALLURE_LABEL_MARK:
                    label_type = marker.kwargs["label_type"]
                    test_dict["markers"][f"allure_{label_type}"] = list(marker.args)
            results.append(test_dict)
        if results:
            with open(_OUTPUT_JSON_FILE_NAME, "w") as f:
                json.dump(results, f)
            print(
                f"Generate allure collection result json file at: {os.path.join(os.getcwd(), _OUTPUT_JSON_FILE_NAME)}"
            )
