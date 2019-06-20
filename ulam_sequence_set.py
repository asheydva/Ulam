import sys

def add_remove_plus_truth(seq,elem):
    """Adds/removes the element. Returns True if removes, False otherwise."""

    if elem in seq:
        seq.remove(elem) # TODO: speed up
        return True

    seq.add(elem)
    return False


def ulam_sequence(n,X):
    """Constructs all terms up to X of U(1,n)."""

    ulam_seq = [1,n]
    unique_seq = set([n + 1])
    non_unique_set = set()

    largest_elem = n + 1

    while (True):
        smallest_unique = min(unique_seq)

        for elem in ulam_seq:
            u = smallest_unique + elem

            #Look in non_unique_set to see if u is in there
            if (u not in non_unique_set):
                if add_remove_plus_truth(unique_seq, u):

                    #If already in unique_set, add to non_unique_set
                    non_unique_set.add(u)

        largest_elem = min(unique_seq)
        unique_seq.remove(largest_elem) # TODO: speed up
        
        if largest_elem > X:
            break

        ulam_seq.append(largest_elem)



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

