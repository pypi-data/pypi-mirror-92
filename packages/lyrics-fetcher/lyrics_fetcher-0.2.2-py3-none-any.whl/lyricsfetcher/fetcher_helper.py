import lyricsgenius
import subprocess
import os
import re


class Fetcher:
    def __init__(self):
        """
        Initializes required variables.
        NOTE: token availability is only checked when required
        """
        # specifying the absolute path for finding the correct files later
        absdir = os.path.abspath(__file__)
        self.filedir = "/".join(absdir.split("/")[:-1])

        # registering the default directory for output
        self.lyrics_directory = self.get_out_dir()

        # registering the token
        self.token = self.check_token()

    def set_out_dir(self, new_out_dir):
        """
        Sets output lyrics directory to specified directory

        Args:
            new_out_dir (string): new output directory path
        """
        # removing potential backslashes from specified path since they are not required and break the function
        # four backslashes required for regex escaping
        new_out_dir = re.sub('\\\\', '', new_out_dir)

        # replacing the root dir sign "~" by the hardcoded equivalent to prevent breaking
        new_out_dir = re.sub(
            "~", "/".join(os.getcwd().split('/')[:3]), new_out_dir)

        if str(new_out_dir)[-1] != "/":
            new_out_dir = f"{new_out_dir}/"

        if os.path.isdir(new_out_dir):
            os.remove(f"{self.filedir}/outdir.conf")
            with open(f"{self.filedir}/outdir.conf", "w+") as outdirfile:
                outdirfile.write(new_out_dir)
        else:
            print("Directory does not exist. The output directory remains unchanged.")

        self.get_out_dir()  # to refresh self.lyrics_directory variable
        print(f"Output directory set to {self.lyrics_directory}")

    def get_out_dir(self):
        """
        returns the currently set lyrics output directory

        Returns:
            self.lyrics_directory [string]: currently set output directory
        """
        with open(f"{self.filedir}/outdir.conf", "r") as outdirfile:
            self.lyrics_directory = outdirfile.readline()
        return self.lyrics_directory

    def set_token(self, newtoken):
        """
        Set a new token. Can overwrite current token if necessary. Overwrite requires user confirmation

        Args:
            newtoken (string): token to set
        """
        # checking whether the user has set their genius API token
        self.check_token()
        if not os.path.isfile(f"{self.filedir}/genius_token.conf"):
            with open(f"{self.filedir}/genius_token.conf", "w+") as tokenfile:
                tokenfile.write(newtoken)
            self.check_token  # loading in new token as self.token
            print(f"Token set to {newtoken}")
        else:
            overwrite = input(
                f"Token is currently {self.token}\noverwrite existing genius_token.conf file to contain {newtoken}? [y/n]: ")
            if str(overwrite.lower().strip()) == "y":
                os.remove(f"{self.filedir}/genius_token.conf")
                # recursively calling this function again to write the .conf file
                self.set_token(newtoken)
            else:
                exit()

    def check_token(self):
        """
        Checks whether a token is saved and loads it into variable called self.token when present

        Returns:
            self.token [string/Nonetype]: token (unencrypted)
        """
        try:
            with open(f"{self.filedir}/genius_token.conf", "r") as tokenfile:
                self.token = tokenfile.readline()
            if self.token[-2:] == "/n":
                self.token = self.token[:-2]

        except FileNotFoundError:  # if the file does not exist
            self.token = None

        return self.token

    def get_settings(self):
        """returns current settings
        """
        self.check_token  # checking the newest version of the token
        print(f"Current token: {self.token}")
        print(f"Current output directory: {self.get_out_dir()}")
        if self.token == None or self.token == "empty":
            self.print_warning()

    def print_warning(self):
        """prints warning when no token is set
        """
        print("\nGenius API token not yet set.\nMake sure to use fetch_lyrics set token 'XXX' where XXX is your Genius API token.\nWithout doing so, this function will not work.\n")

    def fetch(self, args):
        """
        attempts to fetch the lyrics from Genius, and calls the appropriate next fuctions if specicied.
        Prints error message if lyrics for a given prompt are not found

        Args:
            args (dict): all specified arguments from the CLI, received from the lyricsfetcher.py script
        """
        # check for the token again, if no token is found, quit the process
        self.token = self.check_token()
        if self.token == None or self.token.rstrip() == "empty":
            self.print_warning()
            quit()
        else:
            # Initializing the lyricsgenius Genius object
            self.genius = lyricsgenius.Genius(self.token)

        # extracting required information for the specified arguments
        self.artist_kw = args["<artist>"]
        self.song_kw = args["<song_title>"]

        try:
            # try finding the lyrics for the specified arguments on Genius and saving it to a variable called self.lyrics
            song = self.genius.search_song(
                title=self.song_kw, artist=self.artist_kw)
            self.lyrics = song.lyrics

            # checking if the lyrics should be printed and/or copied in adition to being displayed
            if args["--print"]:
                self.print_to_file()
            if args["--copy"]:
                self.copy_to_clipboard()

            # printing the lyrics as output on the command line
            print(self.lyrics)

        except Exception:  # if no lyris are found:
            print(
                f"No lyrics found for prompt {self.artist_kw} - {self.song_kw}.")

    def print_to_file(self):
        """
        Prints found lyrics to a .txt file in specified output directory called '[Artist] - [Song title].txt'
        """
        # note that the self.lyrics_directory alreadh has a trailing slash
        filepath = f"{self.lyrics_directory}{self.artist_kw} - {self.song_kw} lyrics.txt"
        with open(filepath, 'w+') as outfile:
            outfile.write(self.lyrics)

    def copy_to_clipboard(self):
        """
        Copies found lyris to (MacOS) clipboard. Compatibility of other OS' under investigation
        """
        process = subprocess.Popen(
            'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(self.lyrics.encode('utf-8'))
