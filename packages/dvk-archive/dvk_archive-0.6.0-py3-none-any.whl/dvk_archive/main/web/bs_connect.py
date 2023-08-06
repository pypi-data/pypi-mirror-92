#!/usr/bin/env python3

from bs4 import BeautifulSoup
from io import BytesIO
from json import loads
from os.path import abspath, exists
from requests import exceptions
from requests import Session
from shutil import copyfileobj
from urllib.error import HTTPError

def get_headers() -> dict:
    """
    Return headers to use when making a URL connection.
    """
    headers = {
        "User-Agent":
        "Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Accept-Language":
        "en-US,en;q=0.5"}
    return headers

def basic_connect(url:str=None, encoding:str="utf-8", data:dict=None) -> str:
    """
    Connects to a URL and returns the HTML source.
    Doesn't work with JavaScript

    :param url: URL to retrieve, defaults to None
    :type url: str, optional
    :param encoding: Text encoding to use, defaults to "utf-8"
    :type encoding: str, optional
    :param data: Request payload for post requests, defaults to None
    :type data: str, optional
    :return: HTML source
    :rtype: str
    """
    ## RETURN NONE IF URL IS INVALID
    if url is None or url == "":
        return None
    session = Session()
    headers = get_headers()
    try:
        ## SEND REQUEST
        if data is None:
            ## SEND GET REQUEST IF THERE IS NO POST DATA
            request = session.get(url, headers=headers)
        else:
            ## SEND POST REQUEST IF POST DATA IS PROVIDED
            request = session.post(url, data=data)
        ## SET ENCODING
        if encoding is None:
            request.encoding = request.apparent_encoding
        else:
            request.encoding = encoding
        return request.text
    except:
        return None
    return None

def bs_connect(url:str=None, encoding:str="utf-8", data:dict=None) -> BeautifulSoup:
    """
    Connects to a URL and returns a BeautifulSoup object.
    Doesn't work with JavaScript

    :param url: URL to retrieve, defaults to None
    :type url: str, optional
    :param encoding: Text encoding to use, defaults to "utf-8"
    :type encoding: str, optional
    :param data: Request payload for post requests, defaults to None
    :type data: str, optional
    :return: BeautifulSoup object of the URL page
    :rtype: str
    """
    html = basic_connect(url, encoding, data)
    if html is None or html == "":
        return None
    return BeautifulSoup(html, features="lxml")

def json_connect(url:str=None, encoding:str="utf-8", data:dict=None) -> dict:
    """
    Connects to a URL and returns a dict with JSON data.

    :param url: URL to retrieve, defaults to None
    :type url: str, optional
    :param encoding: Text encoding to use, defaults to "utf-8"
    :type encoding: str, optional
    :param data: Request payload for post requests, defaults to None
    :type data: str, optional
    :return: Dictionary with JSON data
    :rtype: dict
    """
    html = basic_connect(url, encoding, data)
    ## RETURN NONE IF RETURNED DATA IS NONE OR INVALID
    if html is None or html == "":
        return None
    try:
        ## CONVERT TO JSON
        json = loads(html)
        return json
    except:
        return None

def download(url:str=None, file_path:str=None):
    """
    Downloads a file from given URL to given file.

    :param url: Given URL, defaults to None
    :type url: str, optional
    :param file_path: Given file path, defaults to None
    :type file_path: str, optional
    """
    if (url is not None and file_path is not None):
        file = abspath(file_path)
        # SAVE FILE
        try:
            session = Session()
            headers = get_headers()
            response = session.get(url, headers=headers)
            byte_obj = BytesIO(response.content)
            byte_obj.seek(0)
            with open(file, "wb") as f:
                copyfileobj(byte_obj, f)
        except (HTTPError,
                exceptions.ConnectionError,
                exceptions.MissingSchema,
                ConnectionResetError):
            print("Failed to download:" + url)
