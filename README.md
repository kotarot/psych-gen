# Psych sheets generator

Psych sheets generator for WCA competitions.


## Requirements

Following python version and some python libraries are required:

* Python 2.7
* Jinja2

_Python 2.7.10_ and _Jinja2 2.8_ are recommended version because I have developed and tested with them.


## Usage

1. Go to [WCA results export page](https://worldcubeassociation.org/results/misc/export.html),
download the latest __TSV ZIP__ file (i.e., _WCA_exportXXX_YYYYMMDD.tsv.zip_),
and put it in `WCA_export/` directory.
1. Fill `your-competition.txt` with the competition information
([sample file](sample/tohoku-2015.txt) is in `sample/` directory).
1. Fill `your-competition.csv` with the entry list
([sample file](sample/tohoku-2015.csv) is in `sample/` directory).
1. Run `generate.py --output path-to-psych.html your-competition`.
1. You will soon get psych sheets in your `path-to-psych.html`

For example, run `generate.py --output tohoku-2015.html tohoku-2015`,
and you will get psych sheets for [Tohoku Open 2015](https://worldcubeassociation.org/results/c.php?i=TohokuOpen2015)
(`sample/tohoku-2015.txt` and `sample/tohoku-2015.csv` are sample data for that competition).


## Notes

* You need only Python and some related libraries, you do not need any Web server or MySQL.
* Event format in `your-competition.csv` only accepts the following terms: 333, 444, 555, 222, 333bf, 333oh, 333fm, 333ft, minx, pyram, sq1, clock, skewb, 666, 777, 444bf, 555bf, 333mbf


## Future works

See [issues](https://github.com/kotarot/psych-gen/issues).

