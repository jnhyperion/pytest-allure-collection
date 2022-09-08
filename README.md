pytest-allure-collection
=============
Pytest plugin to collect allure markers without running any tests.

Install
-------
``` sh
$ pip install pytest-allure-collection
```

Example
-------
* test script `test_example.py`
``` python
import allure
import pytest
@allure.tag("tag1", "tag2")
@allure.title("my title")
@allure.description("description")
@pytest.mark.Foo
def test_foo():
    assert 1==1
```
* running command `pytest --co --collect-allure`
* `allure_collection.json` will be generated in current folder
``` json
[
   {
      "name":"test_foo",
      "location":"test_example.py#test_foo#2",
      "markers":{
         "allure_title":"my title",
         "allure_description":"description",
         "allure_tag":[
            "tag1",
            "tag2"
         ]
      }
   }
]
```
Development
-------
``` sh
$ pip install -r requirements-dev.txt
# test
$ invoke test
# lint
$ invoke lint
# reformat code
$ invoke reformat-code
# install
$ invoke install
```