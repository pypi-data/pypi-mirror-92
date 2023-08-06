import ast
import html
import re
import sys
from importlib._bootstrap import spec_from_loader
from bs4 import BeautifulSoup

import requests


class StackOverflowImporter:
    """ 
    `from stackoverflow import quick_sort` will go through the search results 
    of `[python] quick sort` looking for the largest code block that doesn't 
    syntax error in the highest voted answer from the highest voted question 
    and return it as a module, or raise ImportError if there's no code at all.
    """
    API_URL = "https://api.stackexchange.com"

    @classmethod
    def find_working_code(cls, query):
        urls = cls.fetch_urls(query)
        for url in urls:
            result = cls.fetch_code(url)
            if result != False:
                code, author = result
                return code, author, url
        raise ImportError(f"No good code found in {len(urls)} search results.")

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        spec = spec_from_loader(fullname, cls, origin='hell')
        spec.__license__ = "CC BY-SA 3.0"
        code, author, url = cls.find_working_code(spec.name)
        spec._url = url
        spec._code, spec.__author__ = code, author
        return spec

    @classmethod
    def create_module(cls, spec):
        """Create a built-in module"""
        return spec

    @classmethod
    def exec_module(cls, module=None):
        """Exec a built-in module"""
        try:
            exec(module._code, module.__dict__)
        except:
            print(module._url)
            print(module._code)
            raise

    @classmethod
    def get_code(cls, fullname):
        return compile(cls.fetch_code(cls.fetch_url(fullname)), 'StackOverflow.com/' + fullname, 'exec')

    @classmethod
    def get_source(cls, fullname):
        return cls.get_code(fullname)

    @classmethod
    def is_package(cls, fullname):
        return False

    ############################

    @classmethod
    def fetch_urls(cls, query):
        query = query.lower().replace("stackoverflow.", "").replace("_", " ")
        ans = requests.get(cls.API_URL + "/search", {
            "order": "desc",
            "sort": "votes",
            "tagged": "python",
            "site": "stackoverflow",
            "intitle": query,
        }).json()
        if not ans["items"]:
            raise ImportError("Couldn't find any question matching `" + query + "`")
        return map(lambda x: x["link"], ans["items"])

    @classmethod
    def fetch_code(cls, url):
        q = requests.get(url)
        return cls.find_code_in_html(q.text)

    @staticmethod
    def find_code_in_html(s):
        # no more zalgo
        soup = BeautifulSoup(s, "html.parser")
        answers = soup.find_all(id=re.compile("^answer\-"))

        for answer in answers:
            answer.votes = int(answer.find(itemprop="upvoteCount")["data-value"])

        for answer in sorted(answers, key=lambda a: -a.votes): # sort by votes, descending
            codez = map(lambda x: x.get_text(), answer.find_all("pre"))
            for code in sorted(codez, key=lambda x: -len(x)):  # more code is obviously better
                # don't forget attribution
                # this should probably work
                author_url = answer.find("a", href=lambda h: h != None and h.startswith("/users/"))["href"]
                author_link = "https://stackoverflow.com" + author_url
                try:
                    ast.parse(code)
                    return code, author_link  # it compiled! uhm, parsed!
                except:
                    pass
        return False


sys.meta_path.append(StackOverflowImporter())
