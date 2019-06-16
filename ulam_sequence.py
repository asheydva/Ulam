from bisect import bisect_left
import sys

def add_plus_truth(seq,elem):
    """Adds the elem to seq if not in there and returns whether the element was added or not."""

    #Find the place where we would have to insert the element
    k = bisect_left(seq,elem)

    if (k >= len(seq)):
        seq.insert(k,elem)
        return True

    if (seq[k] == elem):
        return False

    seq.insert(k,elem)
    return False

def remove_plus_truth(seq,elem):
    """Removes the elem to seq if in there and returns whether the element was removed or not."""

    #Find the place where the element would have to be
    k = bisect_left(seq,elem)

    if (k >= len(seq)):
        return False

    if (seq[k] == elem):
        seq.pop(k)
        return True

    return False

def add_remove_plus_truth(seq,elem):
    """Adds/removes the element. Returns True if removes, False otherwise."""

    #Find the place where the element would have to be
    k = bisect_left(seq,elem)

    if (k >= len(seq)):
        seq.insert(k,elem)
        return False

    if (seq[k] == elem):
        seq.pop(k)
        return True

    seq.insert(k,elem)
    return False



def contains(seq,elem):
    """Returns whether seq contains elem"""

    #Find the place where the element would have to be
    k = bisect_left(seq,elem)

    if (k >= len(seq)):
        return False

    if (seq[k] == elem):
        return True

    return False

def ulam_sequence(n,X):
    """Constructs all terms up to X of U(1,n)."""

    ulam_seq = [1,n]
    unique_seq = [n + 1]
    non_unique_seq = []

    largest_elem = n + 1

    while (largest_elem <= X):
        smallest_unique = unique_seq[0]

        for elem in ulam_seq:
            u = smallest_unique + elem

            #Look in non_unique_seq to see if u is in there
            if (not contains(non_unique_seq,u)):
                if add_remove_plus_truth(unique_seq, u):

                    #If already in unique_set, add to non_unique_set
                    add_plus_truth(non_unique_seq,u)

        largest_elem = unique_seq[0]
        if largest_elem <= X:
            ulam_seq.append(largest_elem)
            unique_seq.pop(0)


    return ulam_seq

# defaults
n = 2
X = 1000

if len(sys.argv) > 1:
    n = int(sys.argv.pop(1))
if len(sys.argv) > 1:
    X = int(sys.argv.pop(1))

# print("ulam_sequence("+str(n)+","+str(X)+")", ulam_sequence(n,X))
print(ulam_sequence(n,X))

