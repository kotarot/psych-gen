# Psych sheets generator

Psych sheets generator for WCA competitions.


## Requirements

Following python version and some python libraries are required:

* Python 2.7
* Jinja2

_Python 2.7.10_ and _Jinja2 2.8_ are recommended version because I develop and test with it.


## Usage

1. Go to WCA results export page, download the latest __TSV__ files (WCA_exportXXX_YYYYMMDD.tsv.zip), unzip it, and put `WCA_export_Results.tsv` in the same directory as `generate.py` is.
1. Fill `competitors.txt` with the competitors list (sample data is already written).
1. Fill `events.txt` with the events list (sample data is already written).
1. Run `generate.py`.
1. You will soon get psych sheets in your `psych.html`


## Notes

* You need only Python and some related libraries, you do not need any web server or MySQL.
* Event format in `events.txt` only accepts following terms: 333, 444, 555, 222, 333bf, 333oh, 333fm, 333ft, minx, pyram, sq1, clock, skewb, 666, 777, 444bf, 555bf, 333mbf


## Future works

I will write some here.

