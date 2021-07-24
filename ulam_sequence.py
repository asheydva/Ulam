import sys, os

# defaults
n = 2
X = 1000
file = None


def ulam_sequence(n, X, file = None, print_addends = False):
    """Constructs all terms up to X of U(1,n)."""

    ulam_seq = [1,n]
    ulam_set = set(ulam_seq)
    u_cand = ulam_seq[-1]

    while (True):
        u_cand += 1
        if u_cand > X:
            break
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
        if found_sum == 1:
            # register next Ulam number
            ulam_seq.append(u_cand)
            ulam_set.add(u_cand)
            if file:
                addend_str = ''
                if print_addends:
                    smaller_addend = u_cand - addend
                    addend_str = ' ' + str(smaller_addend)
                file.write(str(u_cand) + addend_str + '\n')

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
    if 1:
        # print inside the method with addends
        ulam_sequence(n, X, file, True)
    else:
        for n in ulam_sequence(n,X):
            file.write(str(n) + '\n')

    file.close()
elif 0:
    import cProfile
    print('ulam_sequence', n,X)
    cProfile.run('print(ulam_sequence(n,X))')
else:
    print(ulam_sequence(n,X))
