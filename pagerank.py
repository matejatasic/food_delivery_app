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
    
    if not corpus[page]:
        probability_for_all = 1 / len(corpus.keys())
        return {key: probability_for_all for key in corpus}

    probability_for_all = 1 - damping_factor  
    additional_probability = probability_for_all / len(corpus.keys())
    probabilities = {key: additional_probability for key in corpus}
    
    number_of_possible_pages = len(corpus[page])

    for possible_page in corpus[page]:
        probabilities[possible_page] += damping_factor / number_of_possible_pages

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    sample_page = None
    times_page_visited = {}

    for i in range(n):
        if not sample_page:
            sample_page = random.choice(list(corpus.keys()))
            times_page_visited[sample_page] = 1
            
            continue
        
        transition_probabilities = transition_model(corpus=corpus, page=sample_page, damping_factor=damping_factor)
        transition_probabilities_keys = [key for key in transition_probabilities.keys()]
        transition_probabilities_values = [value for value in transition_probabilities.values()]
        sample_page = random.choices(
            population=transition_probabilities_keys, 
            weights=transition_probabilities_values, 
            k=1
        )[0]
        times_page_visited[sample_page] = times_page_visited.get(sample_page, 0) + 1
    
    return {key: value / n for key, value in times_page_visited.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    pages = list(corpus.keys())
    number_of_pages = len(pages)
    page_rank = {key: 1 / number_of_pages for key in pages}

    corpus = add_links_to_pages_with_no_links(corpus)

    old_page_rank = {**page_rank}

    while True:
        for page in page_rank:
            probabilities_sum = get_sum_of_probabilities_to_land_on_page(corpus, old_page_rank, page)
            page_rank[page] = (1 - damping_factor)/number_of_pages + damping_factor*probabilities_sum

        if is_difference_small(old_page_rank, page_rank):
            break

        old_page_rank = {**page_rank}

    return old_page_rank


def add_links_to_pages_with_no_links(corpus):
    for page in corpus:
        if corpus[page]:
            continue
        
        corpus[page] = {*corpus.keys()}

    return corpus


def get_sum_of_probabilities_to_land_on_page(corpus, old_page_rank, page):
    probabilities_sum = 0

    for current_page in corpus:
        if not page in corpus[current_page]:
            continue
        
        probabilities_sum += old_page_rank[current_page] / len(corpus[current_page])

    return probabilities_sum


def is_difference_small(old_page_rank, page_rank):
    small_changes = [
        abs(old_page_rank[page] - page_rank[page]) for page in old_page_rank 
        if round(abs(old_page_rank[page] - page_rank[page]), 3) < 0.001
    ]
    
    return len(small_changes) == len(old_page_rank.keys())


if __name__ == "__main__":
    main()
