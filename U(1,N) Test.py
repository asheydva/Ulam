from bisect import bisect_left
from bisect import insort_left
import heapq

EPSILON = 2.5
B = 0.139

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

def linear_model(n,C):
    """Calculate coefficients for U(1,n), U(1,n + 1) up to size C."""

    seq1 = ulam_sequence(n, (C + 1)*n + 0.2 * (C + 1) + 3)
    seq2 = ulam_sequence(n + 1, (C + 1)*(n + 1) + 0.2 * (C + 1) + 3)

    coeff_list = []
    len1 = len(seq1)
    len2 = len(seq2)

    while (len1 > 1) and (len2 > 1):
        start1 = seq1[0]
        start2 = seq2[0]

        m = (start2 - start1)

        if m > C:
            break
        
        p = start1 - m * n

        try:
            while (len1 > 1) and (seq1[1] == seq1[0] + 1):
                seq1.pop(0)
                len1 = len(seq1)

        except IndexError:
            len1 = len(seq1)

        try:
            while (len2 > 1) and (seq2[1] == seq2[0] + 1):
                seq2.pop(0)
                len12 = len(seq2)

        except IndexError:
            len2 = len(seq2)

        if (len1 > 1) and (len2 > 1):
            end1 = seq1.pop(0)
            end2 = seq2.pop(0)

            k = end2 - end1
            r = end1 - k * n

            coeff_list.append(((m,p),(k,r)))

    return coeff_list

def store_model(filename,model):
    file = open(filename + ".txt","w")

    for item in model:
        file.write(str(item) + "\n")

    file.close()
        
def ulam_sequence_expected(model, n):
    """Returns the sequence U(1,n) predicted by the model."""

    seq = []

    for term in model:
        (m, p) = term[0]
        (k, r) = term[1]

        start = m * n + p
        end = k * n + r

        for u in range(start, end + 1):
            seq.append(u)

    return seq

def test_N_correctness(N, C):
    """Tests whether N can be used in the weak rigidity theorem for the given value of C."""

    model = linear_model(N, C)

    for item in model:
        (m, p) = item[0]
        (k, r) = item[1]

        if abs(p - m * B) > EPSILON:
            assert 1 == 0

        if abs(r - k * B) > EPSILON:
            assert 1 == 0

    N_0 = int(4*(1 + EPSILON) - B) + 1

    if N_0 <= N + 1:
        
        return (True, model[-1])

    (k,r) = model[-1][1]

    for n in range(N + 2, N_0 + 1):
        seq_expected = ulam_sequence_expected(model, n)
        seq_actual = ulam_sequence(n, k * n + r)

        if seq_expected != seq_actual:
            return (False, n, model[-1])

    return (True, model[-1])
