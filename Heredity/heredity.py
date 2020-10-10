import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Loads gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Computes and returns a joint probability
    for combination of arguments provided.
    """
    # Initiate joint probability
    joint_probability = 1
    
    # Calculate joint gene and trait probabilities for parents
    for parent in people: 
        if people[parent]['mother'] != None and people[parent]['father'] != None:
            continue

        # Probability of parent having no copies of the gene
        if parent not in one_gene and parent not in two_genes:
            if parent in have_trait: # And expressing the trait
                joint_probability *= (PROBS["gene"][0]*PROBS["trait"][0][True])
            if parent not in have_trait: # And not expressing the trait
                joint_probability *= (PROBS["gene"][0]*PROBS["trait"][0][False])

        # Probability of parent having one copy of the gene
        if parent in one_gene: 
            if parent in have_trait: # And expressing the trait
                joint_probability *= (PROBS["gene"][1]*PROBS["trait"][1][True])
            if parent not in have_trait: # And not expressing the trait
                joint_probability *= (PROBS["gene"][1]*PROBS["trait"][1][False])
        
        # Probability of parent having two copies of the gene
        if parent in two_genes:
            if parent in have_trait: # And expressing the trait
                joint_probability *= (PROBS["gene"][2]*PROBS["trait"][2][True])
            if parent not in have_trait: # And not expressing the trait
                joint_probability *= (PROBS["gene"][2]*PROBS["trait"][2][False])

    # Calculate joint gene and trait probabilities for children
    for child in people: 
        if people[child]['mother'] == None or people[child]['father'] == None:
            continue
      
        parents = [people[child]['mother'], people[child]['father']]
        
        # Probability of child having no copies of the gene
        if child not in one_gene and child not in two_genes:
            
            # For each parent
            for parent in parents:
                # If parent has no copies of the gene
                if parent not in one_gene and parent not in two_genes:
                    joint_probability *= (1-PROBS["mutation"]) 
                
                # If parent has one copy of the gene
                if parent in one_gene:
                    joint_probability *= ((1-PROBS["mutation"]) + PROBS["mutation"])/2

                # If parent has no copies of the gene
                if parent in two_genes:
                    joint_probability *= PROBS["mutation"]

            # Probability of child expressing the trait
            if child in have_trait: 
                joint_probability *= PROBS["trait"][0][True]
            if child not in have_trait:
                joint_probability *= PROBS["trait"][0][False]

        # Probability of child having one copy of the gene
        if child in one_gene: 
            combination1_probability = 1 # Probability of mother passing on no copies and father passing on one copy
            combination2_probability = 1 # Probability of mother passing on one copy and father passing on no copies

            # For each parent
            for parent in parents:
    
                # If mother has no copies of the gene or father has two copies of the gene
                if (parent == parents[0] and parent not in one_gene and parent not in two_genes) or (parent == parents[1] and parent in two_genes):
                    combination1_probability *= (1-PROBS["mutation"]) 
                    combination2_probability *= PROBS["mutation"]
                
                # If either parent has one copy of the gene
                if parent in one_gene:
                    combination1_probability *= ((1-PROBS["mutation"]) + PROBS["mutation"])/2
                    combination2_probability *= ((1-PROBS["mutation"]) + PROBS["mutation"])/2
                
                # If mother has two copies of the gene or father has no copies of the gene
                if (parent == parents[0] and parent in two_genes) or (parent == parents[1]and parent not in one_gene and parent not in two_genes):
                    combination1_probability *= PROBS["mutation"]
                    combination2_probability *= (1-PROBS["mutation"]) 

            # Joint probability of combination 1 or combination2 occuring
            joint_probability *= (combination1_probability + combination2_probability)

            # Probability of child expressing the trait
            if child in have_trait: 
                joint_probability *= PROBS["trait"][1][True]
            if child not in have_trait:
                joint_probability *= PROBS["trait"][1][False]

        # Probability of child having two copies of the gene
        if child in two_genes:
            
            # For each parent
            for parent in parents:
    
                # If parent has no copies of the gene
                if parent not in one_gene and parent not in two_genes:
                    joint_probability *= PROBS["mutation"]
                
                # If parent has one copy of the gene
                if parent in one_gene:
                    joint_probability *= ((1-PROBS["mutation"]) + PROBS["mutation"])/2

                # If parent has no copies of the gene
                if parent in two_genes:
                    joint_probability *= (1-PROBS["mutation"])

            # Probability of child expressing the trait
            if child in have_trait: 
                joint_probability *= PROBS["trait"][2][True]
            if child not in have_trait:
                joint_probability *= PROBS["trait"][2][False]

    return joint_probability

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Updates "gene" and "trait" distribution `probabilities` 
    for each person using the joint probability `p` 
    for the combination of arguments (`one_gene`, `two_genes`, `have_trait`) provided.
    """
    for person in probabilities: 
        
        # Update probablities for number of genes 
        if person not in one_gene and person not in two_genes:
            probabilities[person]["gene"][0] += p 
        if person in one_gene:
            probabilities[person]["gene"][1] += p 
        if person in two_genes:
            probabilities[person]["gene"][2] += p 


        # Update probabilities for expressing the trait
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        if person not in have_trait:
            probabilities[person]["trait"][False] += p     

def normalize(probabilities):
    """
    Updates `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1).
    """
    for person in probabilities:
        # Normalise probablities for number of genes 
        genes_sum = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
        probabilities[person]["gene"][0] *= (1/genes_sum)
        probabilities[person]["gene"][1] *= (1/genes_sum)
        probabilities[person]["gene"][2] *= (1/genes_sum)

        #Normalise probabilities for expressing the trait
        traits_sum = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        probabilities[person]["trait"][True] *= (1/traits_sum)
        probabilities[person]["trait"][False] *= (1/traits_sum)


if __name__ == "__main__":
    main()
