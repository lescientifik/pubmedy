# Pubmedy
A lightweight Biopython-based interface to NCBI's Entrez API, created to speed up systematic literature reviews.


## Installation:

```bash
pip install git+https://github.com/lescientifik/pubmedy.git
```

If you want to install it in dev mode:

```bash
pip install -e git+https://github.com/lescientifik/pubmedy.git#egg=pubmedy
```

Or simpler, in the directory of your choice:

```bash
git clone https://github.com/lescientifik/pubmedy.git
cd pubmedy
pip install -e .
```

## Usage:

```
usage: pubmedy [-h] --email EMAIL -s SEARCH -o OUTFILE

A CLI to query the Pubmed API and save the results. At the end, you get back 2
files:a logfile to keep track of your query and a csv file

optional arguments:
  -h, --help            show this help message and exit
  --email EMAIL         Your email address.
  -s SEARCH, --search SEARCH
                        Your search query. You should use the online Pubmed
                        website to build it more easily and copy-paste here
  -o OUTFILE, --outfile OUTFILE
                        The outfile. Don't include the file extension, this
                        will be generated for you

```

Note that your email adress is only used iff you do anything that bothers the Entrez managers, so they can contact you!
