import argparse
from .py_1337x import Search1337x, CATEGORIES, SORT

parser = argparse.ArgumentParser(
    prog="1337x",
    description="Finds torrents on 1337x",
    usage="Usage: python -m 1337x <search_term> [options]\nSupports multiple torrent download, e.g. 1 2 3 or 1-3",
)

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
    "-d", "--no-download", action='store_true', help="Only prints and copy to clipboard all magnet links"
)

args = parser.parse_args()

query = args.query
sort_type = args.sort_type.upper()
no_download = args.no_download

category = CATEGORIES.get(args.category.upper()) if args.category else None
sort = SORT[sort_type].get(args.sort.upper()) if args.sort else None

Search1337x().search(query, category, sort, no_download)
