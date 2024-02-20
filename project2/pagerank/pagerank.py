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

    print (pages)
    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Total number of pages
    Num = len(corpus)

    random_page = (1 - damping_factor)/Num
    distrib = {}
    for i in corpus:
        distrib[i] = random_page

    for i in corpus[page]:
        linked_from_page = len(corpus[page])
        links = linked_from_page if (linked_from_page > 0) else Num
        distrib[i] += damping_factor * (1/links)
    

    return distrib




def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    random_page, _ = random.choice(list(corpus.items()))


    print ('****',random_page)
    sample = transition_model(corpus, random_page, damping_factor)

    distrib_model = sample.copy()

    for i in range(n):
        x = random.choices(list(sample.keys()), list(sample.values()), k=1)
        sample = transition_model(corpus, x[0], damping_factor)
        for p in distrib_model:
            distrib_model[p] += sample[p]

    for p in distrib_model:
        distrib_model[p] = distrib_model[p] / n

        


    return distrib_model

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    """
    print (corpus)
    # Total number of pages
    Num = len(corpus)
    distrib = {}
    for i in corpus:
        distrib[i] = 1 / Num
    
    print (distrib)

    new_distrib = {}

    while True:
        for p in corpus:
            new = (1 - damping_factor) / Num 
            for p1 in corpus[p]:
                p1 = distrib[p1] / len(corpus[p1])
            p1 *= damping_factor
            new_distrib[p] += p1

    return new_distrib

    """
    distrib = {}
    threshold = 0.0005
    N = len(corpus)
    for key in corpus:
        distrib[key] = 1 / N

    while True:
        count = 0
        for key in corpus:
            new = (1 - damping_factor) / N
            sigma = 0
            for page in corpus:
                if key in corpus[page]:
                    num_links = len(corpus[page])
                    sigma = sigma + distrib[page] / num_links
            sigma = damping_factor * sigma
            new += sigma
            if abs(distrib[key] - new) < threshold:
                count += 1
            distrib[key] = new 
        if count == N:
            break
    
    return distrib

if __name__ == "__main__":
    main()
