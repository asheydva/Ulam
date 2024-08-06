import sys, os
from sortedcontainers import SortedSet

# the algorithm was adopted from the paper by Philip Gibbs, see https://vixra.org/pdf/1508.0085v2.pdf

# defaults
n = 2
X = 13 # 1000
fileName = None
skip_launch_args = True

only_brute_force = False ###

# global data
lamda = 2.44344296778474
tolerance = 0.0001
ulam_seq = [1]
ulam_set = set(ulam_seq)

# residue(1) is 0.4092585802837928 - don't add to range sets
low_range_set = SortedSet()
high_range_set = SortedSet()

def residue(u):
    ''' residue is in [0, 1] '''
    return u % lamda / lamda

def register_ulam(u, res = None):
    ''' adds u to sets and list '''
    if res is None:
        res = residue(u) 
    ulam_seq.append(u)
    ulam_set.add(u)

    # sets are sorted by res, then u
    if res < 0.8/2:
        low_range_set.add((res, u))
    elif res > 0.24/2 + 0.5:
        high_range_set.add((res, u))


def is_ulam_brute_force(u_cand):
    found_sum = 0
    addend = 0
    for cur_u in reversed(ulam_seq):
        other_u = u_cand - cur_u
        if other_u >= cur_u:
            break # done with u_cand
        if other_u not in ulam_set:
            continue
        
        found_sum += 1
        if found_sum > 1:
            # not unique
            break

        addend = cur_u # will use it if u_cand turns out to be Ulam
    return found_sum == 1, addend


def is_ulam_by_residue(u_cand, cand_res):
    ''' use Gibbs aglorithm '''
    found_sum = 0
    addend = 0

    # iterate low range from smallest up
    threshold = cand_res/2 + tolerance
    for (cur_res, cur_u) in low_range_set.irange(maximum=(threshold,0)):
        other_u = u_cand - cur_u
        if other_u == cur_u:
            continue # can't use the same number twice
        if other_u == addend:
            continue # this is the same pair as before
        if other_u not in ulam_set:
            continue
        
        found_sum += 1
        if found_sum > 1:
            # not unique
            return False, addend

        addend = cur_u # will use it if u_cand turns out to be Ulam


    # now iterate high range from largest down.
    # from Gibbs: 2 * (1.0 - rdi) <= (1.0 - rd0)
    threshold = cand_res/2 + 0.5 - tolerance
    for (cur_res, cur_u) in high_range_set.irange(minimum=(threshold,0), reverse=True):
        other_u = u_cand - cur_u
        if other_u == cur_u:
            continue # can't use the same number twice
        if other_u == addend:
            continue # this is the same pair as before
        if other_u not in ulam_set:
            continue
        
        found_sum += 1
        if found_sum > 1:
            # not unique
            return False, addend

        addend = cur_u # will use it if u_cand turns out to be Ulam
            
    return found_sum == 1, addend




def ulam_sequence(n, X, file = None, print_addends = False):
    """Constructs all terms up to X of U(1,n)."""

    register_ulam(n)
    u_cand = n

    while (True):
        u_cand += 1
        if u_cand > X:
            break
        
        if only_brute_force:
            res = None
            use_brute_force = True
        else:
            res = residue(u_cand)
            # use brute for low and high ends of residue
            use_brute_force = res < 0.24 - tolerance or res > 0.8 + tolerance

        is_ulam = False
        if use_brute_force:
            is_ulam, addend = is_ulam_brute_force(u_cand)
        else:
            is_ulam, addend = is_ulam_by_residue(u_cand, res)


        if is_ulam:
            # register next Ulam number
            register_ulam(u_cand, res)

            if file:
                addend_str = ''
                if print_addends:
                    smaller_addend = min(addend, u_cand - addend)
                    addend_str = ' ' + str(smaller_addend)
                file.write(str(u_cand) + addend_str + '\n')
                # file.write(str(residue(u_cand)) + '\n')

    print('low_range_set size:', len(low_range_set))
    # print(low_range_set)
    # print
    print('high_range_set size:', len(high_range_set))
    # print(high_range_set)
    # print
    print('ulam_seq size:', len(ulam_seq))
    print

    return ulam_seq

if not skip_launch_args:
    if len(sys.argv) > 1:
        n = int(sys.argv.pop(1))
    if len(sys.argv) > 1:
        X = int(sys.argv.pop(1))
    if len(sys.argv) > 1:
        fileName = sys.argv.pop(1)

# print("ulam_sequence("+str(n)+","+str(X)+")", ulam_sequence(n,X))
if fileName:
    if os.path.exists(fileName):
        os.remove(fileName)
    file = open(fileName, 'w+')

    if 1:
        # print inside the method with addends
        ulam_sequence(n, X, file, True)
    else:
        for n in ulam_sequence(n,X):
            file.write(str(n) + '\n')

    file.close()

elif 0:
    # do profiling
    import cProfile
    X = 1000*1000
    print('ulam_sequence', n,X)
    # cProfile.run('print(ulam_sequence(n,X))')
    cProfile.run('ulam_sequence(n,X)')
else:
    # just print to screen
    print(ulam_sequence(n,X))
