import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) == 1:        
        corpus  = crawl("corpus1")
        corpus =  {'1': {'2'}, '2': {'3', '1'}, '3': {'4', '5', '2'}, '4': {'1', '2'}, '5': set()} 
    elif len(sys.argv) == 2:
        corpus = crawl(sys.argv[1])
    else:
        sys.exit("Usage: python pagerank.py corpus")

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
    # raise NotImplementedError
    linked_pages = corpus.get(page, set()) # 如果 page 在 corpus 中不存在，则返回一个默认值 set()（一个空集合）
    num_links = len(linked_pages)
    num_pages = len(corpus)
    probability_distribution = {}
    if num_links == 0:
        for p in corpus:
            probability_distribution[p] = 1/num_pages
    else:
        for p in corpus:
            if p in linked_pages:
                probability_distribution[p] = damping_factor/num_links + (1 - damping_factor)/num_pages
            else:
                probability_distribution[p] = (1 - damping_factor)/num_pages
        total_prob = sum(probability_distribution.values())
        if total_prob != 1:
            probability_distribution = {page: prob/total_prob for page, prob in probability_distribution.items()}

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # raise NotImplementedError
    page_count = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))
    for _ in range(n):
        page_count[current_page] += 1
        probability_disctribution = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
            population = list(probability_disctribution.keys()),
            weights = list(probability_disctribution.values()),
            k = 1 # 只选一个，避免创建大列表
            )[0] # random.choices() 返回的是一个列表，所以加上 [0] 取出第一个元素。

    pagerank = {page: count/n for page, count in page_count.items()}
    return pagerank 

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # raise NotImplementedError
    num_pages = len(corpus)
    pagerank = {page: 1/num_pages for page in corpus}
    num_links = {page: len(links) for page, links in corpus.items()}

    while True:
        new_pagerank = {}
        for p in corpus:
            new_pagerank[p] = (1-damping_factor)/num_pages
            for i, linked_pages in corpus.items():
                if p in linked_pages:
                    new_pagerank[p] += damping_factor*pagerank[i]/num_links[i]
                if num_links[i] == 0:
                    new_pagerank[p] += damping_factor*pagerank[i]/num_pages
        errors = {page: abs(pagerank[page] - new_pagerank[page]) for page in corpus}
        if all(error < 0.001 for error in errors.values()):
            break
        else:
            pagerank = new_pagerank
    return pagerank
if __name__ == "__main__":
    main()
