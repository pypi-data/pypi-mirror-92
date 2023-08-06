#!/usr/bin/env python3

from _functools import cmp_to_key
from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.processing.string_compare import compare_alphanum
from dvk_archive.main.processing.string_compare import compare_strings
from tqdm import tqdm
from typing import List
from os import listdir, walk
from os.path import abspath, exists, isdir, join


def get_directories(directory:str=None, only_dvk:bool=True) -> List[str]:
    """
    Returns a list of sub-directories inside a given directory.
    If specified, only returns directories that contain DVK files.
    Includes the given directory.

    :param directory: Directory to search, defaults to None
    :type directory: str, optional
    :param only_dvk: Whether ot only include directories with DVKs, defaults to True
    :type only_dvk: bool, optional
    :return: Sub-directories of the given directory
    :rtype: list[str]
    """
    ## RETURN EMPTY LIST IF GIVEN DIRECTORY IS INVALID
    if directory is None:
        return []
    path = abspath(directory)
    if not exists(path) or not isdir(path):
        return []
    ## GET ALL DIRECTORIES AND SUBDIRECTORIES
    dirs = []
    for p in walk(path):
        dirs.append(abspath(p[0]))
    ## IF SET TO ONLY RETURN DIRECTORIES WITH DVK FILES,
    ## FILTER OUT DIRECTORIES WITHOUT DVK FILES
    if only_dvk:
        i = 0
        while i < len(dirs):
            dvk_dirs = listdir(dirs[i])
            delete = True
            for file in dvk_dirs:
                if file.endswith(".dvk"):
                    delete = False
                    break
            if delete:
                del dirs[i]
                i = i - 1
            ##INCREMENT COUNTER
            i = i + 1
    return dirs

class DvkHandler:

    def __init__(self, directory:str=None):
        """
        Initializes the DvkHandler object.
        Loads dvks from a given directory if specified.

        :param directory: Directory from which to load DVKs, defaults to None
        :type directory: str, optional
        """
        self.dvks = []
        if directory is not None:
            self.read_dvks(directory)
    
    def read_dvks(self, directory:str=None):
        """
        Reads all the DVK files in a given directory and stores them in a list.

        :param directory: Directory from which to load DVKs, defaults to None
        :type directory: str, optional
        """
        self.dvks = []
        if directory is not None:
            ## GET LIST OF DIRECTORIES CONTAINING DVK FILES
            dirs = get_directories(abspath(directory))
            ## LOAD LIST OF DVK FILES
            print("Reading DVK files:")
            for path in tqdm(dirs):
                for file in listdir(path):
                    if file.endswith(".dvk"):
                        dvk = Dvk(abspath(join(path, file)))
                        self.dvks.append(dvk)

    def sort_dvks(self, sort_type:str=None):
        """
        Sorts all currently loaded DVK objects in the Dvk list.

        :param sort_type: Sort type ("t" = Time, "a" = alphabetical), defaults to None
        :type sort_type: str, optional
        """
        print("Sorting DVK files...")
        if sort_type is not None and self.get_size() > 0:
            if sort_type == "t":
                comparator = cmp_to_key(self.compare_time)
            else:
                comparator = cmp_to_key(self.compare_alpha)
            self.dvks = sorted(self.dvks, key=comparator)

    def compare_time(self, x:Dvk=None, y:Dvk=None) -> int:
        """
        Compare two Dvk objects by their publication time.

        :param x: 1st Dvk object, defaults to None
        :type x: Dvk, optional
        :param y: 2nd Dvk object, defaults to None
        :type y: Dvk, optional
        :return: Which Dvk should come first
        :rtype: int
        """
        ## RETURN 0 IF EITHER DVK IS NONE
        if x is None or y is None:
            return 0
        ## COMPARE BY TIME
        result = compare_strings(x.get_time(), y.get_time())
        ## IF TIMES ARE THE SAME, COMPARE BY TITLE
        if result == 0:
            result = compare_alphanum(x.get_title(), y.get_title())
        return result

    def compare_alpha(self, x:Dvk=None, y:Dvk=None) -> int:
        """
        Compare two Dvk objects alphabetically by title.

        :param x: 1st Dvk object, defaults to None
        :type x: Dvk, optional
        :param y: 2nd Dvk object, defaults to None
        :type y: Dvk, optional
        :return: Which Dvk should come first
        :rtype: int
        """
        ## RETURN 0 IF EITHER DVK IS NONE
        if x is None or y is None:
            return 0
        ## COMPARE BY TITLE
        result = compare_alphanum(x.get_title(), y.get_title())
        ## IF TITLES ARE THE SAME, COMPARE BY TIME
        if result == 0:
            result = compare_strings(x.get_time(), y.get_time())
        return result

    def get_size(self) -> int:
        """
        Gets size of the DVK list.

        :return: Size of the DVK list
        :rtype: int
        """
        return len(self.dvks)

    def get_dvk(self, index:int=0) -> Dvk:
        """
        Returns a Dvk object based on the given index.

        :param index: Index of the Dvk to return, defaults to 0
        :type index: int, optional
        :return: Dvk object from Dvk list
        :rtype: Dvk
        """
        return self.dvks[index]
