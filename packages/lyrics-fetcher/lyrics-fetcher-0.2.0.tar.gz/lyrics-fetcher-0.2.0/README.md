# fetch_lyrics CLI Function

Custom command-line interface, based on the [lyricgenius](https://pypi.org/project/lyricsgenius/)\* Genius API implementation. Command line flags can be used to automatically copy the found lyrics to the MacOS\* clipboard, and to store the found lyrics as .txt files in a (configurable) directory.

---

## Installation and First Use

```python
pip install lyrics-fetcher
```

For this software to work, a Genius API token is required. These (free) tokens can be found on [the Genius developers website](https://genius.com/developers). More information about the Genius API can be found in [the Genius API documentation](https://docs.genius.com). See the Usage section for information on how to set a token.

---

## Usage

### Fetching Lyrics

```python
fetch_lyrics -[pc] "Queen" "Bohemian Rhapsody"
```

the `-p` flag enables saving of lyrics to a .txt file. By default, this is the current directory from which the command is run. To change the output directory, see the changing settings section.

the `-c` flag enables copying of the found lyrics to the MacOS\* clipboard. This could be useful for manually adding lyrics to ID3 tags.

`--settings`, `--help` and `--version` can also be called for their basic functionality.

### Changing Settings

before the first use, the token should be set. This token will be locally stored (unencrypted). To set the token, use the following command:

``` python
fetch_lyrics set token "TOKEN"
```

where TOKEN is replaced with the token obtained from the Genius developers webpage.

A custom output directory for the output of found lyrics into .txt files can be set using:

```python
fetch_lyrics set outdir "desired/output/directory"
```

Settings are locally stored in .settings files. Note that these are unencrypted, but are never shared or moved.

---

### Use Policy

This software is licensed using [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html).

---

### Disclaimer and Notes

*) Note that compatibility of different dependencies and OS' is not (yet) investigated.

- I am open to improvements/pull requests, but may not have much time to look into them.

- Currently only supports UTF-8 character encoding.
