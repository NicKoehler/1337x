import argparse
from .py_1337x import Search1337x

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

parser = argparse.ArgumentParser(description="Finds torrents on 1337x")
parser.add_argument("query", type=str, help="Enter a query to search")
parser.add_argument(
    "-c",
    "--category",
    type=str,
    help=f'< {" | ".join(CATEGORIES.keys())} >',
)
parser.add_argument(
    "-s", "--sort", type=str, help=f'< {" | ".join(SORT["ASC"].keys())} >'
)
parser.add_argument(
    "-t", "--sort-type", type=str, help="< ASC | DESC >", default="DESC"
)

parser.add_argument(
    "-d", "--no-download", action='store_true', help="Don't download torrent, only print magnets"
)

args = parser.parse_args()

query = args.query
sort_type = args.sort_type.upper()
no_download = args.no_download

category = CATEGORIES.get(args.category.upper()) if args.category else None
sort = SORT[sort_type].get(args.sort.upper()) if args.sort else None

Search1337x().search(query, category, sort, no_download)
