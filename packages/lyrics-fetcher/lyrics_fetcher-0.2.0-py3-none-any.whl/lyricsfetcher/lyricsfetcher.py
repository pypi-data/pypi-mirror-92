# -*- coding: utf-8 -*-

"""fetch_lyrics

Usage:
  fetch_lyrics [-pc] <artist> <song_title>
  fetch_lyrics set outdir <full_path_to_dir>
  fetch_lyrics set token <Genius_API_token> 
  fetch_lyrics (--help | --version | --settings)

Options:
  -p --print       Print found lyrics to textfile.
  -c --copy        Copy found lyrics to clipboard.
  -h --help        Show this screen.
  -v --version     Show version.
  --settings       Show current settings
"""

from .docopt import docopt
from .fetcher_helper import Fetcher

__version__ = "0.2.0"


def main():

    # Fix console for windows users
    # import platform
    # if platform.system() == 'Windows':
    #     import win_unicode_console
    #     win_unicode_console.enable()

    args = docopt(__doc__, version=(f'lyrics-fetcher {__version__}'))
    F = Fetcher()

    if args["--settings"]:
        print(f"Current token: {F.get_token()}")
        print(f"Current output directory: {F.get_out_dir()}")
    elif args['set']:
        if args["outdir"]:
            F.set_out_dir(args["<full_path_to_dir>"])
        elif args["token"]:
            F.set_token(args["<Genius_API_token>"])

    elif args["<artist>"] and args["<song_title>"]:
        F.fetch(args)
    else:
        print("Something went wrong, check your input and try again.")

    # Disable windows unicode console anyways
    # if platform.system() == 'Windows':
    #     win_unicode_console.disable()
