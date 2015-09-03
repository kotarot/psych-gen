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
and put it in _WCA_export/_ directory. Note: This step will be automated in a future version.
1. Fill _your-competition.txt_ with the competition information
([sample file](sample/tohoku-2015.txt) is in _sample/_ directory).
1. Fill _your-competition.csv_ with the entry list
([sample file](sample/tohoku-2015.csv) is in _sample/_ directory).
1. Run `generate.py --output path-to-psych.html your-competition`,
and you will soon get psych sheets in your _path-to-psych.html_

For example, run `generate.py --output tohoku-2015.html tohoku-2015`,
and you will get psych sheets for [Tohoku Open 2015](https://worldcubeassociation.org/results/c.php?i=TohokuOpen2015)
(_sample/tohoku-2015.txt_ and _sample/tohoku-2015.csv_ are sample data for that competition).

The sample psych sheets looks like this:
[Psych sheets for Tohoku Open 2015](http://www.terabo.net/psych-sheet/tohoku-2015.html)


## Notes

* You need only Python and some related libraries, you do not need any Web server or MySQL.
* Event format in any _your-competition.csv_ only accepts the following terms: 333, 444, 555, 222, 333bf, 333oh, 333fm, 333ft, minx, pyram, sq1, clock, skewb, 666, 777, 444bf, 555bf, 333mbf


## Future works

See [issues](https://github.com/kotarot/psych-gen/issues).

