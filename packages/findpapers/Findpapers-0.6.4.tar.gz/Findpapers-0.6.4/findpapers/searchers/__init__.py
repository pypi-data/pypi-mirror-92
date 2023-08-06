import findpapers.searchers.scopus_searcher as scopus_searcher
import findpapers.searchers.ieee_searcher as ieee_searcher
import findpapers.searchers.pubmed_searcher as pubmed_searcher
import findpapers.searchers.arxiv_searcher as arxiv_searcher
import findpapers.searchers.acm_searcher as acm_searcher
import findpapers.searchers.medrxiv_searcher as medrxiv_searcher
import findpapers.searchers.biorxiv_searcher as biorxiv_searcher


AVAILABLE_DATABASES = [
    scopus_searcher.DATABASE_LABEL,
    ieee_searcher.DATABASE_LABEL,
    pubmed_searcher.DATABASE_LABEL,
    arxiv_searcher.DATABASE_LABEL,
    acm_searcher.DATABASE_LABEL,
    medrxiv_searcher.DATABASE_LABEL,
    biorxiv_searcher.DATABASE_LABEL,
]
