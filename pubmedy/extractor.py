import datetime
import unicodedata
from typing import Dict, List, Union

from .helpers import find_email, unique, clean_html

# pylint: disable=redefined-outer-name


def get_abstract_text(record: Dict) -> str:
    try:
        abstract = record["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]
    # get back abstract structures
    except KeyError:
        return ""
    try:
        tags = [elem.attributes["NlmCategory"] for elem in abstract]
    except KeyError:
        tags = ["" for elem in abstract]
    # abstract value for each structure
    values = [str(elem) for elem in abstract]
    # concat them
    full_text = [" : ".join([tag, value]) for tag, value in zip(tags, values)]
    # final concat to get full abstract
    # normalize unicode to remove \xa strings coming from nowhere
    # https://stackoverflow.com/questions/10993612/python-removing-xa0-from-string
    abstract_text = unicodedata.normalize("NFKD", " ".join(full_text))
    return clean_html(abstract_text)


def get_title(record: Dict) -> str:
    title = record["MedlineCitation"]["Article"]["ArticleTitle"]
    title = unicodedata.normalize("NFKD", title)
    return clean_html(title)


def get_pubdate(record: Dict) -> datetime.date:
    try:
        date_comp = record["MedlineCitation"]["Article"]["ArticleDate"][0]
    except IndexError:
        return None
    date = datetime.date(
        int(date_comp["Year"]), int(date_comp["Month"]), int(date_comp["Day"])
    )
    return date


def get_authorlist_attr(record: Dict) -> List:
    try:
        return list(record["MedlineCitation"]["Article"]["AuthorList"])
    except KeyError:
        return []


def get_author_attr(author: Dict) -> str:
    if "LastName" in author:
        if "ForeName" in author:
            return f"{author['LastName']} {author['ForeName']}"
        else:
            return f"{author['LastName']}"
    elif "CollectiveName" in author:
        return f"{author['CollectiveName']}"
    else:
        pass


def get_authors(record: Dict) -> Union[List, None]:
    authors_list = get_authorlist_attr(record)
    if authors_list:
        return [get_author_attr(author) for author in authors_list]


def get_affiliations(record: Dict) -> Union[List, None]:
    authors_list = get_authorlist_attr(record)
    if authors_list:
        affiliations = unique(
            [
                f"{author['AffiliationInfo'][0]['Affiliation']}"
                for author in authors_list
                if author["AffiliationInfo"]
            ]
        )
        return affiliations


def get_contact_email(record: Dict) -> Union[str, None]:
    affiliations = get_affiliations(record)
    if affiliations is not None:
        emails_list = [
            find_email(affiliation)
            for affiliation in affiliations
            if find_email(affiliation) is not None
        ]
        if emails_list:
            return emails_list[0]


def get_pub_types(record: Dict) -> List:
    type_list = record["MedlineCitation"]["Article"]["PublicationTypeList"]
    return [str(type_) for type_ in type_list]


def get_language(record: Dict) -> str:
    language = record["MedlineCitation"]["Article"]["Language"][0]
    return language


def get_journal(record: Dict) -> str:
    journal = record["MedlineCitation"]["Article"]["Journal"]["Title"]
    return journal


def get_id(record: Dict, id_type: str) -> str:
    id_list = [
        str(doi)
        for doi in record["PubmedData"]["ArticleIdList"]
        if doi.attributes["IdType"] == id_type
    ]
    if id_list:
        return id_list[0]


def get_pmid(record: Dict) -> str:
    return get_id(record, "pubmed")


def get_doi(record: Dict) -> str:
    return get_id(record, "doi")


def get_keyword_lists(record: Dict) -> List:
    if record["MedlineCitation"]["KeywordList"]:
        return [str(keyword) for keyword in record["MedlineCitation"]["KeywordList"][0]]
    else:
        return []


def get_mesh_lists():
    pass


# Pubmed Database not clean enough to do it
###########################################

# def get_cited_articles(record: Dict) -> List:
#     if record["PubmedData"]["ReferenceList"]:
#         if "ArticleIdList" in record["PubmedData"]["ReferenceList"][0]["Reference"][0]:
#             return [
#                 str(ref["Reference"][0]["ArticleIdList"][0])
#                 for ref in record["PubmedData"]["ReferenceList"]
#                 if ref
#             ]
#         else:
#             return []
#     else:
#         return []


def extract_record_infos(record: Dict) -> Dict:
    p_record = {
        "Title": get_title(record),
        "Abstract": get_abstract_text(record),
        "Date": get_pubdate(record),
        "Language": get_language(record),
        "Journal": get_journal(record),
        "Type": None,
        "PubTypes": get_pub_types(record),
        "Authors": get_authors(record),
        "Affiliations": get_affiliations(record),
        "keywords": get_keyword_lists(record),
        # "Cites": get_cited_articles(record),
        "Email": get_contact_email(record),
        "Pmid": get_pmid(record),
        "Doi": get_doi(record),
    }
    ptypes = [ptype.lower() for ptype in p_record["PubTypes"]]
    if [x for x in ptypes if "trial" in x]:
        p_record["Type"] = "Trial"
    if [x for x in ptypes if "review" in x]:
        p_record["Type"] = "Review"
    return p_record
