import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    # Rank pages using sampling
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    
    # Rank pages using iteration
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    

def crawl(directory):
    """
    Parses a `directory` of HTML pages and check for links to other pages.
    Returns a dictionary where each key is a page, and the values are
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
    Returns a probability distribution (PD) over which page to visit next,
    given a current page.
    With probability `damping_factor`, chooses a link linked to by `page`. 
    With probability `1 - damping_factor`, chooses a link from all pages in `corpus`.
    """

    # Create dictionary of all html_pages
    pages_PD = dict()

    for html_page in corpus:
        pages_PD.setdefault(html_page, 0)
    
    # Assign a selection probability to each link in page
    if len(corpus[page]) != 0: # Number of links in page is not 0
        for html_page in corpus[page]:
            pages_PD[html_page] += damping_factor/len(corpus[page])
    
    if len(corpus[page]) == 0: # Number of links in page is 0
        for html_page in pages_PD:
            pages_PD[html_page] += damping_factor/len(pages_PD)

    # Assign a probability to randomly choose each page in corpus
    for html_page in pages_PD:
        pages_PD[html_page] += (1-damping_factor)/len(pages_PD)

    return pages_PD

def sample_pagerank(corpus, damping_factor, n):
    """
    Returns PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names and values are
    their estimated PageRank value (between 0 and 1). All
    PageRank values sum to 1.
    """

    # Create dictionary of all html_pages
    ranked_pages = dict()

    for html_page in corpus:
        ranked_pages.setdefault(html_page, 0)

    # Select a random page to start
    sampled_page = random.choice(list(ranked_pages.keys()))
    
    # Sample corpus pages n times 
    for i in range(n):

        # Determine the PD of pages to visit next
        sampled_page_PD = transition_model(corpus, sampled_page, DAMPING)

        # Select a page to visit
        population = list(sampled_page_PD.keys())
        weights = list(sampled_page_PD.values())
        sampled_page = random.choices(population, weights)[0]

        # Record visit in dictionary
        for html_page in ranked_pages: 
            if html_page == sampled_page:
                ranked_pages[html_page] += 1/n

    return ranked_pages

def iterate_pagerank(corpus, damping_factor):
    """
    Returns PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Returns a dictionary where keys are page names and values are
    their estimated PageRank value (between 0 and 1). All
    PageRank values sum to 1.
    """

    # Create dictionary of all html_pages
    ranked_pages = dict()

    # Assign each page an equivalent rank to start with
    for html_page in corpus:
        ranked_pages.setdefault(html_page, 1/len(corpus))
    
    # Repeat until PageRank values converge
    while True: 

        # Create a deepcopy of the dictionary
        old_ranked_pages = copy.deepcopy(ranked_pages)

        # Calculate the probability that the random surfer arrives at each html_page
        for html_page in ranked_pages:
            
            # Probability of choosing page at random
            random_choice = (1-damping_factor)/len(corpus)
            
            # Probability of arriving to page from a link in another page
            link_choice = 0

            for page in corpus:
                if len(corpus[page]) != 0: # If there are links in the  page    
                    for i in range(len(corpus[page])):     
                        if list(corpus[page])[i] == html_page:
                            link_choice += old_ranked_pages[page]/len(corpus[page])

                else: # If there are no links in the page
                    link_choice += old_ranked_pages[page]/len(corpus)
            
            # Total probability of arriving at the page
            ranked_pages[html_page] = random_choice + damping_factor*link_choice

        # Check if the probabilities have converged (change in PageRank values of no more than 0.001)
        converged = 0

        for html_page in ranked_pages:
            if abs(ranked_pages[html_page] - old_ranked_pages[html_page]) <= 0.001:
                converged += 1

        if converged == len(corpus):
            break     
    
    return ranked_pages

if __name__ == "__main__":
    main()