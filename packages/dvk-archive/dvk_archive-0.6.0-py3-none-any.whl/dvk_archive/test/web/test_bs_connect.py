#!/usr/bin/env/ python3

from os import stat
from os.path import abspath, exists, join
from dvk_archive.test.temp_dir import get_test_dir
from dvk_archive.main.web.bs_connect import bs_connect
from dvk_archive.main.web.bs_connect import basic_connect
from dvk_archive.main.web.bs_connect import download
from dvk_archive.main.web.bs_connect import json_connect

def test_basic_connect():
    """
    Tests the basic_connect function
    """
    ## TEST GETTING HTML PAGE
    url = "http://pythonscraping.com/exercises/exercise1.html"
    html = basic_connect(url)
    assert html is not None
    assert html.startswith("<html>\n<head>\n<title>A Useful Page</title>")
    ## TEST GETTING INVALID HTML PAGE
    assert basic_connect() is None
    assert basic_connect(None) is None
    assert basic_connect("") is None
    assert basic_connect("asdfghjkl") is None

def test_bs_connect():
    """
    Tests the bs_connect function.
    """
    ## TEST GETTING BEAUTIFULSOUP FROM PAGE
    url = "http://pythonscraping.com/exercises/exercise1.html"
    bs = bs_connect(url)
    assert bs is not None
    assert bs.find("h1").get_text() == "An Interesting Title"
    assert bs.find("title").get_text() == "A Useful Page"
    ## TEST GETTING INVALID PAGE
    assert bs_connect() is None
    assert bs_connect(None) is None
    assert bs_connect("") is None
    assert bs_connect("qwertyuiop") is None

def test_json_connect():
    ## TEST LOADING PAGE AS A JSON OBJECT
    json = json_connect("http://echo.jsontest.com/key/value/json/test")
    assert json["json"] == "test"
    assert json["key"] == "value"
    ## TEST LOADING AN INVALID PAGE
    json = json_connect("asdfghjkl")
    assert json is None
    json = json_connect(None)
    assert json is None

def test_download():
    """
    Tests the download function.
    """
    ## TEST DOWNLOADING A GIVEN FILE
    test_dir = get_test_dir()
    file = abspath(join(test_dir, "image.jpg"))
    url = "http://www.pythonscraping.com/img/gifts/img6.jpg"
    download(url, file)
    assert exists(file)
    assert stat(file).st_size == 39785
    ## TEST DOWNLOADING WITH INVALID PARAMETERS
    file = join(test_dir, "invalid.jpg")
    download(None, None)
    assert not exists(file)
    download(None, file)
    assert not exists(file)
    download("asdfasdf", file)
    assert not exists(file)
    download(url, None)
    assert not exists(file)

def all_tests():
    """
    Runs all tests for the bs_connect module.
    """
    test_basic_connect()
    test_bs_connect()
    test_json_connect()
    test_download()

