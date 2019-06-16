from bisect import bisect_left
import sys
import heapq

def add_remove_plus_truth(heap,elem):
    """Adds/removes the element. Returns True if removes, False otherwise."""

    # this must be slow
    if elem in heap:
        heap.remove(elem)
        # restore heapq??
        return True

    heap.push(elem)
    return False


def ulam_sequence(n,X):
    """Constructs all terms up to X of U(1,n)."""

    ulam_seq = [1,n]
    unique_seq = heapq.heapify([n + 1])
    non_unique_set = set()

    largest_elem = n + 1

    while (largest_elem <= X):
        smallest_unique = unique_seq[0]

        for elem in ulam_seq:
            u = smallest_unique + elem

            #Look in non_unique_set to see if u is in there
            if (u not in non_unique_set):
                if add_remove_plus_truth(unique_seq, u):

                    #If already in unique_set, add to non_unique_set
                    non_unique_set.add(u)

        largest_elem = unique_seq[0]
        if largest_elem <= X:
            ulam_seq.append(largest_elem)
            unique_seq.heappop()


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

