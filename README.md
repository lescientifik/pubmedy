# Pubmedy
A lightweight Biopython-based interface to NCBI's Entrez API, created to speed up systematic literature reviews



## Usage:

Pubmedy [-h] --email EMAIL -s SEARCH -o OUTFILE

A CLI to query the Pubmed API and save the results. At the end, you get back 2
files:a logfile to keep track of your query and a csv file

optional arguments:
  -h, --help            show this help message and exit
  --email EMAIL         Your email address.If you do anything that bothers the
                        Entrez managers, they will contact you!
  -s SEARCH, --search SEARCH
                        Your search query. You should use the online Pubmed
                        website to build it more easily and copy-paste here
  -o OUTFILE, --outfile OUTFILE
                        The outfile. Don't include the file extension, this
                        will be generated for you
