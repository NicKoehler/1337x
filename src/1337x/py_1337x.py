"""
This module fetches entries from "1337x.to" and opens them with your default torrent client.
Author: NicKoehler

"""

from ast import Raise
import os
import platform
import subprocess
from re import compile
from requests import get
from bs4 import BeautifulSoup as Soup


class Bcolors:
    """
    Class containig the colors to print in the terminal
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Search1337x:
    """
    Helper class used to store constant links and method for searching entries
    """

    # links
    _BASE = "https://1337x.to"
    _NORMAL_SEARCH = _BASE + "/search/{}/{}/"
    _SORT_SEARCH = _BASE + "/sort-search/{}/{}/"
    _CATEGORY_SEARCH = _BASE + "/category-search/{}/{}/"
    _SORT_CATEGORY_SEARCH = _BASE + "/sort-category-search/{}/{}/"

    # categories
    TV = "TV/{}"
    XXX = "XXX/{}"
    GAMES = "Games/{}"
    MUSIC = "Music/{}"
    ANIME = "Anime/{}"
    OTHER = "Other/{}"
    MOVIES = "Movies/{}"
    APPLICATIONS = "Apps/{}"
    DOCUMENTARIES = "Documentaries/{}"

    # sorting
    LEECHERS_DESC = "leechers/desc/{}"
    LEECHERS_ASC = "leechers/asc/{}"
    SEEDERS_DESC = "seeders/desc/{}"
    SEEDERS_ASC = "seeders/asc/{}"
    TIME_DESC = "time/desc/{}"
    TIME_ASC = "time/asc/{}"
    SIZE_DESC = "size/desc/{}"
    SIZE_ASC = "size/asc/{}"

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0",
    }

    def __init__(self):
        self.page = 1
        self.platform = platform.system()

    def search(self, query: str, category: str = None, sort: str = None, no_download: bool = False):
        """
        creates an infinite loop showing the results fetched from the website
        and prompts the user to choose something to download
        """

        while True:

            if category and sort:
                url = self._SORT_CATEGORY_SEARCH.format(
                    query, category.format(sort.format(self.page))
                )

            elif category:
                url = self._CATEGORY_SEARCH.format(
                    query, category.format(self.page)
                )

            elif sort:
                url = self._SORT_SEARCH.format(
                    query, sort.format(self.page)
                )

            else:
                url = self._NORMAL_SEARCH.format(
                    query, self.page
                )
            
            r = get(url, headers=self.HEADERS)

            if r.status_code != 200:
                raise Exception(f"Error: {r.status_code} - {r.reason}")

            r.encoding = "utf-8"
            soup = Soup(r.text, "lxml")
            body = soup.find("tbody")
            pages = soup.find("div", class_="pagination")

            if not body:
                print("No results found")
                break

            if pages:
                pages = pages.find_all("li")

            entries = body.find_all("tr")[::-1]

            titles = {}

            for num, entry in enumerate(entries):

                title, seeds, leechers, date, size, author = entry.find_all(
                    "td"
                )

                title = title.text
                seeds = seeds.text
                leechers = leechers.text
                date = date.text
                size = size.next_element
                author = author.text

                link = f'{self._BASE}{entry.find_all("a")[1].attrs["href"]}'

                idx = len(entries) - num

                titles[idx] = (
                    f"{Bcolors.HEADER}{Bcolors.BOLD}{idx}{Bcolors.ENDC} • "
                    f"{Bcolors.BOLD}{title}{Bcolors.ENDC}\n"
                    f"{' '*(3 + len(str(idx)))}"
                    f"Seeds: {Bcolors.OKGREEN}{seeds}{Bcolors.ENDC} | "
                    f"Leechers: {Bcolors.WARNING}{leechers}{Bcolors.ENDC} | "
                    f"Date: {Bcolors.OKBLUE}{date}{Bcolors.ENDC} | "
                    f"Size: {Bcolors.OKCYAN}{size}{Bcolors.ENDC} | "
                    f"Uploader: {Bcolors.HEADER}{author}{Bcolors.ENDC}\n",
                    link,
                )

            print()

            for i in titles.values():
                print(i[0])

            if pages:
                pages = [
                    int(i.text)
                    for i in filter(lambda x: x.text.isnumeric(), pages)
                ]
                formatted_pages = " • ".join(
                    f"{Bcolors.OKGREEN}{Bcolors.BOLD}{i}{Bcolors.ENDC}"
                    if i == self.page
                    else str(i)
                    for i in pages
                )
                print(f"< prev • {formatted_pages} • next >\n")

            try:
                choices = list(
                    map(
                        lambda x: x.strip().lower(),
                        input("Choose what you want to download > ").split(),
                    )
                )
            except KeyboardInterrupt:
                break

            if all(
                choice.isnumeric() and int(choice) in titles.keys()
                for choice in choices
            ):
                for choice in choices:
                    self.start_download(titles[int(choice)][1], no_download)
                break

            elif any(choice in ["n", "next"] for choice in choices):
                if self.page < max([1, *pages]):
                    self.page += 1
                continue

            elif any(choice in ["p", "prev"] for choice in choices):
                if self.page > 1:
                    self.page -= 1
                continue

            print("Invalid choice")
            break


    def start_download(self, link: str, no_download: bool):
        """
        fetch the magnet from the link and opens it
        """
        soup = Soup(get(link).text, "lxml")
        magnet_link = soup.find("a", href=compile("^magnet:.*"))["href"]
        if no_download:
            print(magnet_link)
        else:
            self.open(magnet_link)

    def open(self, link):
        """
        opens the magnet with the default torrent client
        """

        if self.platform == "Windows":
            os.startfile(link)

        elif self.platform == "Darwin":
            subprocess.call(
                ("open", link),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            subprocess.call(
                ("xdg-open", link),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

CATEGORIES = {
    "TV": Search1337x.TV,
    "XXX": Search1337x.XXX,
    "GAMES": Search1337x.GAMES,
    "MUSIC": Search1337x.MUSIC,
    "ANIME": Search1337x.ANIME,
    "OTHER": Search1337x.OTHER,
    "MOVIES": Search1337x.MOVIES,
    "APPLICATIONS": Search1337x.APPLICATIONS,
    "DOCUMENTARIES": Search1337x.DOCUMENTARIES,
}

SORT = {
    "ASC": {
        "LEECHERS": Search1337x.LEECHERS_ASC,
        "SEEDERS": Search1337x.SEEDERS_ASC,
        "TIME": Search1337x.TIME_ASC,
        "SIZE": Search1337x.SIZE_ASC,
    },
    "DESC": {
        "LEECHERS": Search1337x.LEECHERS_DESC,
        "SEEDERS": Search1337x.SEEDERS_DESC,
        "TIME": Search1337x.TIME_DESC,
        "SIZE": Search1337x.SIZE_DESC,
    },
}