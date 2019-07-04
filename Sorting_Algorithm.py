from random import randint
from bisect import bisect_left
from bisect import bisect_right

SEQ_LIST = [[-3,3],[6,6],[9,14],[16,22]]

initial_list = map(lambda seq: seq[0], SEQ_LIST)
final_list = map(lambda seq: seq[1], SEQ_LIST)


def find_indices(seq):
    initial = seq[0]
    final = seq[1]

    i_initial_1 = bisect_left(final_list, initial - 1)
    i_initial_0 = bisect_left(initial_list, initial, i_initial_1)
    i_final_0 = bisect_right(initial_list, final + 1, i_initial_0)
    i_final_1 = bisect_right(final_list, final, i_initial_1)

    return (i_initial_0, i_initial_1, i_final_0, i_final_1)

def find_indices_c(seq):
    initial = seq[0]
    final = seq[1]

    i_initial_0 = bisect_left(initial_list, initial)
    i_initial_1 = bisect_left(final_list, initial)
    i_final_0 = bisect_right(initial_list, final)
    i_final_1 = bisect_right(final_list, final, i_initial_1)
    
    return (i_initial_0, i_initial_1, i_final_0, i_final_1)

def shuffle_in(seq):
    (i_initial_0, i_initial_1, i_final_0, i_final_1) = find_indices(seq)

    new_seq_list = SEQ_LIST[0:]

    if i_final_0 == 0:
        #seq is before every sequence in the list

        new_seq_list.insert(0,seq)
        return new_seq_list

    if i_initial_1 == len(SEQ_LIST):
        #seq is after every sequence in the list

        new_seq_list.append(seq)
        return new_seq_list

    start = min(seq[0], initial_list[i_initial_1])
    end = max(seq[1], final_list[i_final_0 - 1])

    new_seq_list = new_seq_list[:i_initial_1] + [[start, end]] + new_seq_list[i_final_0:]
    return new_seq_list

def cut_out_basic(seq1, seq2):
    initial = seq1[0]
    final = seq1[1]

    if seq2[0] <= initial:
        if seq2[1] >= final:
            return []

        return [[seq2[1] + 1, final]]

    if seq2[1] >= final:
        return [[initial, seq2[0] - 1]]

    return [[initial, seq2[0] - 1], [seq2[1] + 1, final]]    

def cut_out(seq):
    (i_initial_0, i_initial_1, i_final_0, i_final_1) = find_indices_c(seq)

    new_seq_list = SEQ_LIST[0:]
    
    if i_final_0 == 0:
        #seq is before every sequence in the list
        return new_seq_list

    if i_initial_1 == len(SEQ_LIST):
        #seq is after every sequence in the list
        return new_seq_list

    #sequences prior to anything being cut
    start_seq_list = SEQ_LIST[:i_initial_1]

    #first sequence being cut
    middle_seq_list = cut_out_basic(SEQ_LIST[i_initial_1],seq)

    if i_initial_1 < i_final_0 - 1:
        middle_seq_list = middle_seq_list + cut_out_basic(SEQ_LIST[i_final_0 - 1],seq)

    #sequences after everything cut
    end_seq_list = SEQ_LIST[i_final_0:]

    return start_seq_list + middle_seq_list + end_seq_list

def select_larger_than(elem):
    new_seq_list = SEQ_LIST[0:]

    if elem < new_seq_list[0][0]:
        return new_seq_list

    if elem >= new_seq_list[-1][1]:
        return []

    initial_list = map(lambda seq: seq[0], SEQ_LIST)
    i = bisect_right(initial_list, elem)

    last_cut_seq = new_seq_list[i - 1]

    uncut_seq_list = new_seq_list[i:]

    if last_cut_seq[1] > elem:
        uncut_seq_list = [[elem + 1, last_cut_seq[1]]] + uncut_seq_list

    return uncut_seq_list

def convert_to_int_list(seq_list):
    int_list = []
    for seq in seq_list:
        for i in range(seq[0], seq[1] + 1):
            int_list.append(i)

    return int_list

def select_larger_than_v2(elem):
    int_list = convert_to_int_list(SEQ_LIST)

    i = bisect_left(int_list, elem + 1)
    return int_list[i:]

def test_select():
    for i in range(-5,25):
        int_list_1 = convert_to_int_list(select_larger_than(i))
        int_list_2 = select_larger_than_v2(i)

        if int_list_1 != int_list_2:
            print(i)
            print(int_list_1)
            print(int_list_2)
            assert 1==2

    print "All Correct!"
