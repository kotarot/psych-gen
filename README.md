# Psych sheet generator

Psych sheet generator for WCA competitions.


## Requirements

Following python version and some python libraries are required:

* Python 2.7
* Jinja2
* BeautifulSoup4

*Python 2.7.10* and *Jinja2 2.8* are recommended version because I have developed and tested with them.


## Usage

1. Fill *your-competition.txt* with the competition information
([sample file](sample/tohoku-2015.txt) is in *sample/* directory).
1. Fill *your-competition.csv* with the entry list
([sample file](sample/tohoku-2015.csv) is in *sample/* directory).
If you specify `auto` argument, only events list is needed.
1. Run `python generate.py --output path-to-psych.html your-competition`,
and you will soon get psych sheets in your *path-to-psych.html*

For example, run `python generate.py --output sample/tohoku-2015.html sample/tohoku-2015` or `python generate.py --output sample/tohoku-2015.html --auto 93 sample/tohoku-2015` (93 is JRCA eid for Tohoku 2015),
and you will get psych sheets for [Tohoku Open 2015](https://worldcubeassociation.org/results/c.php?i=TohokuOpen2015)
as *sample/tohoku-2015.html*
(*sample/tohoku-2015.txt* and *sample/tohoku-2015.csv* are sample data for that competition).

The sample psych sheets looks like this:
[Psych sheets for Tohoku Open 2015](http://www.terabo.net/psych-sheet/tohoku-2015.html)


## Notes

* You need only Python and some related libraries, you do not need any Web server or MySQL.
* Event format in any *your-competition.csv* only accepts the following terms: 333, 444, 555, 222, 333bf, 333oh, 333fm, 333ft, minx, pyram, sq1, clock, skewb, 666, 777, 444bf, 555bf, 333mbf


## Future works

See [issues](https://github.com/kotarot/psych-gen/issues).

