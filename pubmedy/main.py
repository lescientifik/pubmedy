import argparse
import csv
import logging
import time

from Bio import Entrez

from .extractor import extract_record_infos
from .helpers import config_basicLogger

parser = argparse.ArgumentParser(
    prog="Pubmedy",
    description=f"A CLI to query the Pubmed API and save the results. "
    f"At the end, you get back 2 files:"
    f"a logfile to keep track of your query and a csv file",
)
parser.add_argument(
    "--email",
    required=True,
    help=f"Your email address."
    f"If you do anything that bothers the Entrez managers, they will contact you!",
)
parser.add_argument(
    "-s",
    "--search",
    required=True,
    help=f"Your search query. "
    f"You should use the online Pubmed website to build it more easily and copy-paste here",
)

parser.add_argument(
    "-o",
    "--outfile",
    required=True,
    type=str,
    help="The outfile. Don't include the file extension, this will be generated for you",
)


def main(email: str, search_string: str, output_file: str):
    config_basicLogger(output_file)
    log = logging.getLogger("pubmedy")
    log.info("Querying Pubmed with the following query: %s", search_string)
    Entrez.email = email
    search_handle = Entrez.esearch(db="pubmed", term=search_string, retmax=10_000)
    search_record = Entrez.read(search_handle)
    search_handle.close()
    log.info("Found %s articles", len(search_record["IdList"]))
    if search_record["IdList"]:
        start = time.perf_counter()
        results_handle = Entrez.efetch(
            db="pubmed", id=search_record["IdList"], retmode="xml",
        )
        records = Entrez.read(results_handle)
        log.info("Retrieved records in %s sec", time.perf_counter() - start)
        start = time.perf_counter()
        processed_records = [
            extract_record_infos(record) for record in records["PubmedArticle"]
        ]
        log.info("Record processed in %s sec", time.perf_counter() - start)
        results_handle.close()
        keys = processed_records[0].keys()
        with open(output_file + ".csv", "w") as out_csv:
            dict_writer = csv.DictWriter(out_csv, keys, quoting=csv.QUOTE_ALL)
            dict_writer.writeheader()
            dict_writer.writerows(processed_records)
        log.info("Csv output written at %s", output_file + ".csv")


def cli():
    args = parser.parse_args()
    main(args.email, args.search, args.outfile)


if __name__ == "__main__":
    cli()
