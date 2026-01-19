#!/usr/bin/env python3
"""Lightweight CLI to exercise the pybel module."""
import argparse
import textwrap

import pybel

SNIPPET_LEADER = "\n--- book snippet (first 500 chars) ---\n"


def _print_snippet(text, length):
    excerpt = textwrap.shorten(text, width=length, placeholder=" [...] ")
    print(SNIPPET_LEADER + excerpt)


def _handle_browse(args):
    book = pybel.browse(args.hexagon, args.wall, args.shelf, args.volume)
    _print_snippet(book, args.snippet)


def _handle_search(args):
    results = pybel.search(args.query)
    if not results:
        print("No matches were found for the provided query.")
        return

    for index, result in enumerate(results, start=1):
        reference = f"hex={result.hexagon}, wall={result.wall}, shelf={result.shelf}, volume={result.volume}"
        page = result.page or "unknown"
        print(f"{index}. {reference}, page={page}")
        if index >= args.limit:
            break


def _handle_random(args):
    book = pybel.random(args.hexagon_length)
    _print_snippet(book, args.snippet)


def main():
    parser = argparse.ArgumentParser(description="Simple examples for the Library-of-Babel Python API")
    parser.set_defaults(func=lambda _: parser.print_help())

    subparsers = parser.add_subparsers(title="Commands", dest="command")

    browse_parser = subparsers.add_parser("browse", help="fetch a book at a specific address")
    browse_parser.add_argument("hexagon", help="hexagon identifier (letters+digits)")
    browse_parser.add_argument("wall", help="wall number (1-4)")
    browse_parser.add_argument("shelf", help="shelf number (1-5)")
    browse_parser.add_argument("volume", help="volume number (1-32)")
    browse_parser.add_argument("--snippet", type=int, default=500, help="limit the printed snippet length")
    browse_parser.set_defaults(func=_handle_browse)

    search_parser = subparsers.add_parser("search", help="look for a passage across the volumes")
    search_parser.add_argument("query", help="text to search for")
    search_parser.add_argument("--limit", type=int, default=3, help="how many matches to print")
    search_parser.set_defaults(func=_handle_search)

    random_parser = subparsers.add_parser("random", help="pull a random book snippet")
    random_parser.add_argument("--hexagon-length", type=int, default=256, help="length of the random hexagon name")
    random_parser.add_argument("--snippet", type=int, default=500, help="limit the printed snippet length")
    random_parser.set_defaults(func=_handle_random)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
