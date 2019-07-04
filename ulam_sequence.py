import sys, os

# defaults
n = 2
X = 1000
file = None

def add_remove_plus_truth(set,elem):
    """Adds/removes the element. Returns True if removes, False otherwise."""

    if elem in set:
        set.remove(elem)
        return True

    set.add(elem)
    return False


def ulam_sequence(n,X):
    """Constructs all terms up to X of U(1,n)."""

    ulam_seq = [1,n]
    unique_set = set([n + 1])
    non_unique_set = set()

    largest_elem = n + 1

    while (True):
        smallest_unique = min(unique_set) # this takes time

        for elem in ulam_seq:
            u = smallest_unique + elem

            #Look in non_unique_set to see if u is in there
            if (u not in non_unique_set):
                if add_remove_plus_truth(unique_set, u):

                    #If already in unique_set, add to non_unique_set
                    non_unique_set.add(u)

        largest_elem = min(unique_set) # this takes time
        unique_set.remove(largest_elem)

        if largest_elem > X:
            break

        ulam_seq.append(largest_elem)

    return ulam_seq

if len(sys.argv) > 1:
    n = int(sys.argv.pop(1))
if len(sys.argv) > 1:
    X = int(sys.argv.pop(1))
if len(sys.argv) > 1:
    fileName = sys.argv.pop(1)
    if os.path.exists(fileName):
        os.remove(fileName)
    file = open(fileName, 'w+')

# print("ulam_sequence("+str(n)+","+str(X)+")", ulam_sequence(n,X))
if file:
    for n in ulam_sequence(n,X):
        file.write(str(n) + '\n')

    file.close()
elif 0:
    import cProfile
    print('ulam_sequence', n,X)
    cProfile.run('print(ulam_sequence(n,X))')
else:
    print(ulam_sequence(n,X))
