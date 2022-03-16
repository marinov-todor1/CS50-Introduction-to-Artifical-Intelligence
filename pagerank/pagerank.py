import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    countLinkedPages = len(corpus[page])
    countCorpusPages = len(corpus.keys())

    # Calculate each corpus page chance
    noDamping = (1 - damping_factor) / countCorpusPages

    # Calculate each linked page chance
    damping = damping_factor / countLinkedPages
    withDamping = damping + noDamping

    result = {}
    # Assign percentile chance for each page, based on linked/not-linked
    for each in corpus.keys():
        if each in corpus[page]:
            result[each] = withDamping
        else:
            result[each] = noDamping

    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # start at a random page
    initial_page = random.choice(list(corpus.keys()))

    # keep track of visited pages
    track_record = {}
    for each in corpus:
        track_record[each] = 0
    latest_page = initial_page

    # select N samples and keep track of each visited page
    for i in range(n):
        possibilities = transition_model(corpus, latest_page, damping_factor)
        keys = list(possibilities.keys())
        values = list(possibilities.values())
        next_page = random.choices(keys, weights=values, k=1)
        track_record[next_page[0]] += 1
        latest_page = next_page[0]

    # divide each result by the number of samples to make the total chance sum up to 1
    for record in track_record:
        track_record[record] /= n

    return track_record


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    ranks = {}
    # set initial rank values to 1/page count
    initial_rank = 1 / len(corpus)
    for each_page in corpus:
        ranks[each_page] = initial_rank

    enough = True

    while enough:
        enough = False
        for page in corpus:
            page_rank = calc_page_rank(corpus, ranks, page)
            summ = page_rank - ranks[page]
            if summ > abs(1):
                enough = True
            ranks[page] = page_rank

    test_sum = 0
    for key, values in ranks.items():
        test_sum += values

    return ranks


def calc_page_rank(corpus, current_ranks, page):

    dSum = 0
    for key, values in corpus.items():
        if page in values:
            prI = current_ranks[key]
            dSum += (prI / len(values))

    first_part = (1 - DAMPING) / len(corpus)
    pageRank = round(first_part + (DAMPING * dSum), 3)
    return pageRank


if __name__ == "__main__":
    main()
