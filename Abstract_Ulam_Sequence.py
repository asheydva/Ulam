from math import ceil
from bisect import bisect_left
from bisect import bisect_right

INFINITY = float("inf")

#If guess is ever above this bound, print relevant non-standard integers being compared.
UPDATE_BOUND = INFINITY

class NonStandardInteger():
    """Non-standard integer a*n + b of a non-standard ring."""

    def __init__(self, a, b, ring):
        self.non_st_part = a
        self.st_part = b
        self.non_st_ring = ring

    def __repr__(self):
        return str((self.non_st_part, self.st_part))

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        a = self.st_part
        b = self.non_st_part
        c = other.st_part
        d = other.non_st_part

        if b == d:
            return a == c

        #Finds any n for which conclusion of a + bn = c + dn is different
        if (c - a) % (b - d) == 0:
            self.non_st_ring.update_exclusions((c - a)/(b - d))

        return False

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        """Returns whether self < other. Finds smallest n such that this can be standardized."""
        a = self.st_part
        b = self.non_st_part
        c = other.st_part
        d = other.non_st_part

        if b == d:
            return a < c

        #Finds smallest n such that a + bn < c + dn.
        guess = ceil(float(c - a)/float(b - d))

        if guess > UPDATE_BOUND:
            print (self,other,guess)

        self.non_st_ring.update_guess(guess)

        return b < d

    def less_than_wo_guess(self, other):
        """Returns whether self < other, without updating standardization."""
        a = self.st_part
        b = self.non_st_part
        c = other.st_part
        d = other.non_st_part

        if b == d:
            return a < c

        return b < d

    def __le__(self, other):
        """Returns whether self <= other. Finds smallest n such that this can be standardized."""
        a = self.st_part
        b = self.non_st_part
        c = other.st_part
        d = other.non_st_part

        if b == d:
            return a <= c

        #Finds smallest n such that a + bn <= c + dn.
        guess = ceil(float(c - a)/float(b - d))

        if guess > UPDATE_BOUND:
            print (self,other,guess)

        self.non_st_ring.update_guess(guess)

        return b < d

    def __gt__(self, other):
        """Returns whether self > other. Finds smallest n such that this can be standardized."""
        c = self.st_part
        d = self.non_st_part
        a = other.st_part
        b = other.non_st_part

        if b == d:
            return a < c

        #Finds smallest n such that a + bn < c + dn.
        guess = ceil(float(c - a)/float(b - d))

        if guess > UPDATE_BOUND:
            print (self,other,guess)

        self.non_st_ring.update_guess(guess)

        return b < d

    def __ge__(self, other):
        """Returns whether self >= other. Finds smallest n such that this can be standardized."""
        c = self.st_part
        d = self.non_st_part
        a = other.st_part
        b = other.non_st_part

        if b == d:
            return a <= c

        #Finds smallest n such that a + bn <= c + dn.
        guess = ceil(float(c - a)/float(b - d))

        if guess > UPDATE_BOUND:
            print (self,other,guess)

        self.non_st_ring.update_guess(guess)

        return b < d

    def next(self, n = 1):
        """Returns the next non-standard integer n away."""
        return NonStandardInteger(self.non_st_part, self.st_part + n, self.non_st_ring)

    def previous(self, n = 1):
        """Returns the previous non-standard integer n away."""
        return NonStandardInteger(self.non_st_part, self.st_part - n, self.non_st_ring)

    def __add__(self, other):
        return NonStandardInteger(self.non_st_part + other.non_st_part, self.st_part + other.st_part, self.non_st_ring)

    def __sub__(self, other):
        return NonStandardInteger(self.non_st_part - other.non_st_part, self.st_part - other.st_part, self.non_st_ring)

    def __rmul__(self, other):
        """"Used to scale a non-standard integer by an integer."""
        return NonStandardInteger(self.non_st_part * other, self.st_part * other, self.non_st_ring)


class NonStandardRing():
    """Class to keep track of results of inequalities of non-standard integers."""
    def __init__(self):
        self.minimal_guess = 1 #guesses minimal n needed to make all inequalities <, > valid.
        self.exclusions_set = set([]) #keeps track of all n that make != inequalities work.

    def __repr__(self):
        return("Nonstandard Ring Z[N]; standardized for " + self.print_all_exclusions())

    def update_guess(self, guess):
        self.minimal_guess = max(int(guess), self.minimal_guess)

    def update_exclusions(self, exclusion):
        self.exclusions_set.add(exclusion)

    def reset_all_exclusions(self):
        self.minimal_guess = 4
        self.exclusions_set = set([])

    def print_all_exclusions(self):
        """Prints a string describing all obstacles to standardization."""
        ex_list = list(self.exclusions_set)
        list.sort(ex_list)
        i = bisect_right(ex_list,self.minimal_guess)
        ex_list = ex_list[i:]
        self.exclusions_set = set(ex_list)

        if len(ex_list) == 0:
            return "N >= " + str(self.minimal_guess)

        init_str = "N >= " + str(self.minimal_guess) + " and N != "
        ex_str = str(ex_list[0])

        for i in range(1,len(ex_list)):
            ex_str = ex_str + ", " + str(ex_list[i])

        return init_str + ex_str

class ArithmeticSequence:
    """Sequence of consecutive non-standard integers between start and end."""
    def __init__(self, start, end):
        #Do not remove this comparison: it ensures the standardization is valid.
        if start > end:
            print(start,end)
            raise ValueError("Start of interval larger than end of interval.")

        self.initial = start
        self.final = end

    def __repr__(self):
        if self.is_singleton():
            return("Singleton " + str(self.initial))
        return("Sequence of elements with endpoints %s and %s" % (self.initial, self.final))

    def __contains__(self, elem):
        """Specifies whether the non-standard integer elem is in the sequence."""
        if elem >= self.initial:
            if elem <= self.final:
                return True

        return False

    def is_singleton(self):
        """Specifies whether the sequence consists of just a single element."""
        return self.initial == self.final

    def __eq__(self, other):
        if self.initial != other.initial:
            return False

        if self.final != other.final:
            return False

        return True

    def intersects(self, other):
        """Returns whether two sequences intersect each other."""
        if other.final >= self.initial:
            if other.initial <= self.final:
                return True

        if self.final >= other.initial:
            if self.initial <= other.final:
                return True

        return False

    #Define methods that allow addition of sequences. This is Minkowski addition, except only distinct sums are allowed, and we keep track of whether an element has just one representation, or multiple.
    def __add__(self, seq2):
        """Addition for distinct sequences."""
        if self.intersects(seq2):
            raise ValueError("Only addition of non-intersecting sequences is defined.")

        #Representation dictionary keeps track of sums, and whether they can be obtained in just one way, or many.
        representation_dictionary = {"One representation":[], "Multiple representations":[]}

        if self.is_singleton() or seq2.is_singleton():
            #If either sequence is a singleton, addition is just the Minkowski sum.
            representation_dictionary["One representation"] = [ArithmeticSequence(self.initial + seq2.initial, self.final + seq2.final)]

        else:
            #If neither sequence is a singleton, most elements in the middle will have multiple representations.
            start = self.initial + seq2.initial
            end = self.final + seq2.final

            if start < end.previous(2):
                representation_dictionary["One representation"] = [ArithmeticSequence(start, start.next()), ArithmeticSequence(end.previous(), end)]

                if start <= end.previous(4):
                    representation_dictionary["Multiple representations"] = [ArithmeticSequence(start.next(2), end.previous(2))]

            else:
                representation_dictionary["One representation"] = [ArithmeticSequence(start, end)]


        return representation_dictionary

    def add_to_itself(self):
        """Addition of a sequence with itself."""

        #Representation dictionary keeps track of sums, and whether they can be obtained in just one way, or many.
        representation_dictionary = {"One representation":[], "Multiple representations":[]}

        #Have special cases if sequence is short.
        if self.is_singleton():
            return representation_dictionary

        a = self.initial
        b = self.final

        if b == a.next():
            x = (2*a).next()
            representation_dictionary["One representation"] = [ArithmeticSequence(x,x)]
            return representation_dictionary

        if b == a.next(2):
            x = (2*a).next()
            y = x.next(2)

            representation_dictionary["One representation"] = [ArithmeticSequence(x, y)]
            return representation_dictionary

        #From here, all sequences are long.

        #Rough order of new endpoints.
        x = 2*a
        y = 2*b

        representation_dictionary["One representation"] = [ArithmeticSequence(x.next(), x.next(2)), ArithmeticSequence(y.previous(2), y.previous())]
        representation_dictionary["Multiple representations"] = [ArithmeticSequence(x.next(3), y.previous(3))]
        return representation_dictionary

    def span(self, other):
        """Finds the smallest sequence that contains both self and other."""
        start = min(self.initial, other.initial)
        end = max(self.final, other.final)

        return ArithmeticSequence(start, end)

    def intersection(self, other):
        """Finds the intersection of two sequences."""
        if self.intersects(other):
            start = max(self.initial, other.initial)
            end = min(self.final, other.final)

            return ArithmeticSequence(start, end)

        return []

    def cut_out(self, other):
        """Removes any elements of other from self. This is a list of as many as two sequences."""

        #Keeps track of sequences in the complement
        sequences_not_cut_out = []

        if self.initial < other.initial:
            sequences_not_cut_out.append(ArithmeticSequence(self.initial, min(self.final, other.initial.previous())))

        if self.final > other.final:
            sequences_not_cut_out.append(ArithmeticSequence(max(self.initial, other.final.next()),self.final))

        return sequences_not_cut_out


    def next_singleton(self):
        """Returns the singleton after this current sequence."""
        return ArithmeticSequence(self.final.next(), self.final.next())

class DisjointSequences:
    """Container of disjoint arithmetic sequences, kept in order."""
    def __init__(self, disjoint_seq_list, check_disjoint = True, presorted = False):

        #If the list of disjoint sequences isn't already sorted, start by sorting it.
        if not presorted:
            disjoint_seq_list = sorted(disjoint_seq_list, key=lambda sequence: sequence.initial)

            #If it is unknown if elements of list are disjoint, check that this is true.
            if check_disjoint:
                num_seq = len(disjoint_seq_list)

                for i in range(num_seq - 1):
                    seq1 = disjoint_seq_list[i]
                    seq2 = disjoint_seq_list[i + 1]

                    if seq1.intersects(seq2):
                        raise ValueError("Inputs must be disjoint sequences.")

        self.sequence_list = disjoint_seq_list

    def __repr__(self):
        return("Increasing sequences: " + str(self.sequence_list))

    def formal_print(self):
        """Gives a more easily readable print-out of the coefficients."""
        formal_list = []

        for seq in self.sequence_list:
            a = seq.initial
            b = seq.final

            if a == b:
                formal_list.append(a)
            else:
                formal_list.append([a,b])

        return formal_list

    def comparable_print(self):
        """Gives print-out that is easy to compare with existing list."""
        comparable_list = []

        for seq in self.sequence_list:
            a = seq.initial
            b = seq.final

            comparable_list.append((a,b))

        return comparable_list

    def shuffle_in(self, seq, return_index = False, starting_index = 0):
        """Unions in sequence seq into self. Can also return the last index where shuffling ends."""

        new_seq_list = self.sequence_list[0:]

        #obtain starting and ending points of the list of sequences
        initial_list = [seq.initial for seq in new_seq_list]
        final_list = [seq.final for seq in new_seq_list]

        start = seq.initial
        end = seq.final

        #find indices of sequences to the left and right of seq
        i_initial = bisect_left(final_list, start.previous(), starting_index)
        i_final = bisect_right(initial_list, end.next(), i_initial)

        if i_final == 0:
            #seq is before every sequence in the list

            new_seq_list.insert(0,seq)

        elif i_initial == len(initial_list):
            #seq is after every sequence in the list

            new_seq_list.append(seq)

        else:

            #Define sequences at the beginning
            start_seq_list = new_seq_list[:i_initial]

            #Define endpoints of sequence that will be in the middle
            new_start = min(start, initial_list[i_initial])
            new_end = max(end, final_list[i_final - 1])

            middle_seq = ArithmeticSequence(new_start, new_end)

            #Define sequences at the end
            end_seq_list = new_seq_list[i_final:]

            new_seq_list = start_seq_list + [middle_seq] + end_seq_list

        ds = DisjointSequences(new_seq_list, False, True)

        if return_index:
            return (ds, i_initial)

        return ds

    def cut_out(self, seq, return_index = False, starting_index = 0):
        """Cuts out any elements of the sequence seq. Can also return the index of the last sequence where cutting occured."""

        new_seq_list = self.sequence_list[0:]

        #obtain starting and ending points of the list of sequences
        initial_list = [seq.initial for seq in new_seq_list]
        final_list = [seq.final for seq in new_seq_list]

        start = seq.initial
        end = seq.final

        #find indices of sequences to the left and right of seq
        i_initial = bisect_left(final_list, start.previous(), starting_index)
        i_final = bisect_right(initial_list, end.next(), i_initial)

        if i_final != 0 and i_initial != len(initial_list):
            #seq isn't before or after every sequence in the list

            #Define sequences at the beginning
            start_seq_list = new_seq_list[:i_initial]

            #Define first sequence being cut
            middle_seq_list = new_seq_list[i_initial].cut_out(seq)

            if i_initial < i_final - 1:
                middle_seq_list = middle_seq_list + new_seq_list[i_final - 1].cut_out(seq)

            #Define sequences at the end
            end_seq_list = new_seq_list[i_final:]

            new_seq_list = start_seq_list + middle_seq_list + end_seq_list

        ds = DisjointSequences(new_seq_list, False, True)

        if return_index:
            return (ds, i_initial)

        return ds

    def select_larger_than(self, elem):
        """Removes all elements smaller than elem."""

        new_seq_list = self.sequence_list[0:]

        #if self is empty, change nothing
        if len(new_seq_list) == 0:
            return DisjointSequences(new_seq_list, False, True)

        #if the bound is too small, change nothing
        if elem < new_seq_list[0].initial:
            return DisjointSequences(new_seq_list, False, True)

        #if the bound is too large, cut out everything
        if elem >= new_seq_list[-1].final:
            return DisjointSequences([], False, True)

        #otherwise, find the index of the smallest interval that intersects the bound
        initial_list = [seq.initial for seq in new_seq_list]
        i = bisect_right(initial_list, elem)

        #find the last sequence that might intersect the bound, and the list of everything after that
        last_cut_seq = new_seq_list[i - 1]
        uncut_seq_list = new_seq_list[i:]

        #if the last sequence really does intersect the bound, cut it accordingly
        if last_cut_seq.final > elem:
            uncut_seq_list = [ArithmeticSequence(elem.next(), last_cut_seq.final)] + uncut_seq_list

        return DisjointSequences(uncut_seq_list, False, True)

    def __add__(self, other):
        """Returns the union of self and other."""

        ds_new = self
        seq_list = other.sequence_list
        i_initial = 0

        for seq in seq_list:
            (ds_new, i_initial) = ds_new.shuffle_in(seq, True, i_initial)

        return ds_new

    def __sub__(self, other):
        """Removes all elements of other from self."""

        ds_new = self
        seq_list = other.sequence_list
        i_initial = 0

        for seq in seq_list:
            (ds_new, i_initial) = ds_new.cut_out(seq, True, i_initial)

        return ds_new

    def symmetric_difference(self, other):
        """Returns the symmetric difference of self and other."""

        diff_1 = self - other
        diff_2 = other - self

        return diff_1 + diff_2


class NonStandardUlamSequence:
    """Ulam sequence over non-standard integers in the ring R."""
    def __init__(self,R,ulam_data = []):
        self.base_ring = R

        if ulam_data == []:

            one = NonStandardInteger(0,1,R)
            n = NonStandardInteger(1,0,R)

            #Keeps track of largest coefficients that have been computed.
            self.largest_constant_computed = 2*n + one

            #First two sequences of the Ulam sequence
            seq1 = ArithmeticSequence(one,one)
            seq2 = ArithmeticSequence(n,2*n)

            #Disjoint sequences for the Ulam sequence
            self.ulam_ds = DisjointSequences([seq1, seq2], False, True)

            #Disjoint sequences larger than the largest computed with one representation
            self.one_rep_ds = DisjointSequences([], False, True)

            #Disjoint sequences larger than the largest computed with >1 representation
            self.multiple_rep_ds = DisjointSequences([], False, True)

        else:
            #if data for specifying the sequence is provided, use that instead
            [self.ulam_ds, self.one_rep_ds, self.multiple_rep_ds] = ulam_data

            self.largest_constant_computed = (self.ulam_ds.sequence_list[-1].final).next()
        
    def __repr__(self):
        return("Nonstandard Ulam sequence U(1,N) computed up to " + str(self.largest_constant_computed))

    def extend_one_sequence(self):
        """Computes the next block of the Ulam sequence."""

        ulam_length = len(self.ulam_ds.sequence_list)

        #Add every block in the Ulam sequence to the last block to be added
        #No need to consider adding 1, as this is handled on the previous iteration
        for i in range(1,ulam_length):
            if i == ulam_length - 1:
                #Addition of the last block to itself handled separately
                seq2 = ((self.ulam_ds).sequence_list)[-1]
                representation_dictionary = seq2.add_to_itself()

            else:
                seq1 = ((self.ulam_ds).sequence_list)[i]
                seq2 = ((self.ulam_ds).sequence_list)[-1]
                representation_dictionary = seq1 + seq2

            #store results as disjoint sequences
            one_rep_ds_guess = DisjointSequences(representation_dictionary["One representation"], False, True)
            multiple_rep_ds_guess = DisjointSequences(representation_dictionary["Multiple representations"], False, True)

            #remove anything too small
            one_rep_ds_guess = one_rep_ds_guess.select_larger_than(self.largest_constant_computed)
            multiple_rep_ds_guess = multiple_rep_ds_guess.select_larger_than(self.largest_constant_computed)

            #take the symmetric difference of existing one rep sequences and the new ones
            new_one_rep_ds = one_rep_ds_guess.symmetric_difference(self.one_rep_ds)

            #everything cut out in the previous step should go into the multiple rep disjoint sequences (this can be more efficient)
            new_multiple_rep_ds = one_rep_ds_guess - new_one_rep_ds

            #add on to the new multiple rep repository everything just computed to have multiple reps
            new_multiple_rep_ds = new_multiple_rep_ds + multiple_rep_ds_guess

            #add on to the new multiple rep repository all of the previously found multiple rep elements
            self.multiple_rep_ds = new_multiple_rep_ds + self.multiple_rep_ds

            #cut out everything with multiple reps from the one rep repository
            self.one_rep_ds = new_one_rep_ds - self.multiple_rep_ds


        #the smallest sequence from one_rep_ds is our guess for the new Ulam block
        minimal_sequence = (self.one_rep_ds).sequence_list[0]
        a = minimal_sequence.initial
        b = minimal_sequence.final

        #cut out everything from multiple_rep_ds smaller than a
        self.multiple_rep_ds = self.multiple_rep_ds.select_larger_than(a)

        n = NonStandardInteger(1,0,self.base_ring)

        if a == b:
            #By adding +1, we get a sequence, until we hit something in either one_rep_ds or multiple_rep_ds

            #if a > n is in Ulam, then a + n is not, which gives a worst case bound
            trivial_bound = a + n

            #compute bound coming from one_rep_ds
            one_rep_list = (self.one_rep_ds).sequence_list
            if len(one_rep_list) == 1:
                #if one_rep_ds only has one block, default to trivial bound
                one_rep_bound = trivial_bound

            else:
                #if there is something else there, choose the smallest
                one_rep_bound = one_rep_list[1].initial

            #compute bound coming from multiple_rep_ds
            multiple_rep_list = self.multiple_rep_ds.sequence_list
            if multiple_rep_list == []:
                #if one_rep_ds is empty, default to trivial bound
                multiple_rep_bound = trivial_bound

            else:
                #if there is something there, choose the smallest
                multiple_rep_bound = multiple_rep_list[0].initial

            #actual bound is the smallest among these
            bound = min(trivial_bound, one_rep_bound)
            bound = min(bound, multiple_rep_bound)

            #the block to add to Ulam has everything from a to bound - 1
            new_seq = ArithmeticSequence(a, bound.previous())
            self.ulam_ds.sequence_list.append(new_seq)

            #cut out everything from one_rep <= bound
            self.one_rep_ds = self.one_rep_ds.select_larger_than(bound)

        else:
            #By adding +1, the next element after a already has two representations
            #Thus, the next block in Ulam is a singleton
            new_seq = ArithmeticSequence(a, a)
            self.ulam_ds.sequence_list.append(new_seq)

            #cut out everything from one_rep and multiple_rep <= a + 1
            self.one_rep_ds = self.one_rep_ds.select_larger_than(a.next())
            self.multiple_rep_ds = self.multiple_rep_ds.select_larger_than(a.next())

        self.largest_constant_computed = (self.ulam_ds.sequence_list[-1].final).next()

    def coeff_up_to(self, bound):
        if self.largest_constant_computed.less_than_wo_guess(bound):
            while self.ulam_ds.sequence_list[-1].final.less_than_wo_guess(bound):
                self.extend_one_sequence()

        return self.ulam_ds

def import_ds(filename, ring):
    f = open(filename, "r")

    seq_list = []

    for line in f:
        ((a0,b0),(a1,b1)) = eval(line)
        start = NonStandardInteger(a0,b0,ring)
        end = NonStandardInteger(a1, b1, ring)

        seq = ArithmeticSequence(start, end)
        seq_list.append(seq)

    f.close()

    return DisjointSequences(seq_list, False, True)

R = NonStandardRing()
n = NonStandardInteger(1,0,R)
one = NonStandardInteger(0,1,R)

ulam_ds = import_ds("Ulam_Coeff.txt",R)
one_rep_ds = import_ds("Ulam_One_Rep.txt",R)
multiple_rep_ds = import_ds("Ulam_Multiple_Rep.txt",R)

U = NonStandardUlamSequence(R, [ulam_ds, one_rep_ds, multiple_rep_ds])

def UlamCoefficients(C):
    """Prints all Ulam coefficients up to C."""
    return U.coeff_up_to(C * n).comparable_print()

def write_all_Ulam_data_up_to(C):
    """Writes files with all of the important Ulam data."""

    exclusions_file = open("Exclusions_Data.txt","a")

    while U.ulam_ds.sequence_list[-1].final.less_than_wo_guess(C*n):
        U.extend_one_sequence()
        exclusions_file.write(str(U.largest_constant_computed) + ": " + R.print_all_exclusions())
        exclusions_file.write("\n")
        R.reset_all_exclusions()

    exclusions_file.close()

    ulam_file = open("Ulam_Coeff.txt","a")
    for seq in U.ulam_ds.sequence_list:
        initial = seq.initial
        final = seq.final
        ulam_file.write(str((initial, final)))
        ulam_file.write("\n")

    ulam_file.close()

    one_rep_file = open("Ulam_One_Rep.txt","w")
    for seq in U.one_rep_ds.sequence_list:
        initial = seq.initial
        final = seq.final
        one_rep_file.write(str((initial, final)))
        one_rep_file.write("\n")

    one_rep_file.close()

    multiple_rep_file = open("Ulam_Multiple_Rep.txt","w")
    for seq in U.multiple_rep_ds.sequence_list:
        initial = seq.initial
        final = seq.final
        multiple_rep_file.write(str((initial, final)))
        multiple_rep_file.write("\n")

    multiple_rep_file.close()

    return "All data written."


if __name__ == "__main__":
    import sys, os

    C = 10
    if len(sys.argv) > 1:
        C = int(sys.argv.pop(1))
    # if len(sys.argv) > 1:
    #     fileName = sys.argv.pop(1)
    #     if os.path.exists(fileName):
    #         os.remove(fileName)
    #     file = open(fileName, 'w+')

    if 1:
        print(UlamCoefficients(C))






