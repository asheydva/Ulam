from math import ceil
from bisect import bisect_left
from bisect import bisect_right

INFINITY = float("inf")

class NonStandardInteger():
    def __init__(self, a, b, ring):          
        self.st_part = a
        self.non_st_part = b
        self.non_st_ring = ring
        
    def __repr__(self):
        return str((self.non_st_part, self.st_part))
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False
            
        if self.st_part != other.st_part:
            return False
        
        if self.non_st_part != other.non_st_part:
            return False
        
        return True
    
    def __ne__(self, other):
        return not self == other
    
    def __lt__(self, other):
        a = self.st_part
        b = self.non_st_part
        c = other.st_part
        d = other.non_st_part
        
        if b == d:
            return a < c
        
        guess = ceil(float(c - a)/float(b - d))
        self.non_st_ring.update(guess)
        
        return b < d
    
    def __le__(self, other):
        a = self.st_part
        b = self.non_st_part
        c = other.st_part
        d = other.non_st_part
        
        if b == d:
            return a <= c
        
        guess = ceil(float(c - a)/float(b - d))
        self.non_st_ring.update(guess)
        
        return b < d
    
    def __gt__(self, other):
        c = self.st_part
        d = self.non_st_part
        a = other.st_part
        b = other.non_st_part
        
        if b == d:
            return a < c
        
        guess = ceil(float(c - a)/float(b - d))
        self.non_st_ring.update(guess)
        
        return b < d
        
    def __ge__(self, other):
        c = self.st_part
        d = self.non_st_part
        a = other.st_part
        b = other.non_st_part
        
        if b == d:
            return a <= c
        
        guess = ceil(float(c - a)/float(b - d))
        self.non_st_ring.update(guess)
        
        return b < d
    
    def next(self, n = 1):
        return NonStandardInteger(self.st_part + n, self.non_st_part, self.non_st_ring)
    
    def previous(self, n = 1):
        return NonStandardInteger(self.st_part - n, self.non_st_part, self.non_st_ring)
    
    def __add__(self, other):
        return NonStandardInteger(self.st_part + other.st_part, self.non_st_part + other.non_st_part, self.non_st_ring)
    
    def __sub__(self, other):
        return NonStandardInteger(self.st_part - other.st_part, self.non_st_part - other.non_st_part, self.non_st_ring)
    
    def __rmul__(self, other):
        return NonStandardInteger(self.st_part * other, self.non_st_part * other, self.non_st_ring)


class NonStandardRing():
    def __init__(self):
        self.minimal_guess = 1
        
    def __repr__(self):
        return("Nonstandard Ring Z[N]")

    def update(self, guess):
        self.minimal_guess = max(int(guess), self.minimal_guess)


class ArithmeticSequence:
    def __init__(self, start, end, check = True):
        if check:
            if start > end:
                raise ValueError("Start of interval larger than end of interval.")
        
        self.initial = start
        self.final = end
        
    def __repr__(self):
        if self.is_singleton():
            return("Singleton " + str(self.initial))
        return("Sequence of elements with endpoints %s and %s" % (self.initial, self.final))
        
    def __contains__(self, elem):
        if elem >= self.initial:
            if elem <= self.final:
                return True
            
        return False
    
    def is_singleton(self):
        return self.initial == self.final
    
    def __eq__(self, seq2):
        if self.initial not in seq2:
            return False
        
        if self.final not in seq2:
            return False
        
        if seq2.initial not in self:
            return False
        
        if seq2.final not in self:
            return False
        
        return True
    
    def __gt__(self, other):
        return self.initial > other.initial
    
    def __lt__(self, other):
        return self.initial < other.initial
    
    def intersects(self, seq2):
        if seq2.final >= self.initial:
            if seq2.initial <= self.final:
                return True
            
        if self.final >= seq2.initial:
            if self.initial <= seq2.final:
                return True
            
        return False
    
    def next_to(self, seq2):
        if seq2.final.next() >= self.initial:
            if seq2.initial.next() <= self.final:
                return True
            
        if self.final.next() >= seq2.initial:
            if self.initial.next() <= seq2.final:
                return True
            
        return False
        
    def __add__(self, seq2):
        if self.intersects(seq2):
            raise ValueError("Only addition of non-intersecting sequences is defined.")
            
        representation_dictionary = {"One representation":[], "Multiple representations":[]}
        
        if self.is_singleton() or seq2.is_singleton():
            representation_dictionary["One representation"] = [ArithmeticSequence(self.initial + seq2.initial, self.final + seq2.final)]
            
        else:
            start = self.initial + seq2.initial
            end = self.final + seq2.final
            
            if start < end.previous(2):
                representation_dictionary["One representation"] = [ArithmeticSequence(start, start.next()), ArithmeticSequence(end.previous(), end)]
                
                if start <= end.previous(4):
                    representation_dictionary["Multiple representations"] = [ArithmeticSequence(start.next(2), end.previous(2))]
                
            else:
                representation_dictionary["One representation"] = [ArithmeticSequence(start, end)]
                
                
        return representation_dictionary
    
    def union(self, seq2):
        start = min(self.initial, seq2.initial)
        end = max(self.final, seq2.final)
        
        return ArithmeticSequence(start, end)
    
    def intersection(self, other):
        if self.intersects(other):
            start = max(self.initial, other.initial)
            end = min(self.final, other.final)
            
            return ArithmeticSequence(start, end)
            
        return []
    
    def complement(self, seq2):
        sequences_not_cut_out = []
        
        if self.initial < seq2.initial:
            sequences_not_cut_out.append(ArithmeticSequence(self.initial, min(self.final, seq2.initial.previous())))
            
        if self.final > seq2.final:
            sequences_not_cut_out.append(ArithmeticSequence(max(self.initial, seq2.final.next()),self.final))
            
        return sequences_not_cut_out
    
    def symmetric_difference(self, other):
        intersecting_seq = self.intersection(other)
        
        if intersecting_seq == []:
            if self.initial < other.initial:
                return [self, other]
            
            return [other, self]
        
        seq_list1 = self.complement(intersecting_seq)
        seq_list2 = other.complement(intersecting_seq)
        
        if self.initial < other.initial:
            return seq_list1 + seq_list2
        
        return seq_list2 + seq_list1
    
    def next_singleton(self):
        return ArithmeticSequence(self.final.next(), self.final.next(), False)
    
    def add_to_itself(self):
        representation_dictionary = {"One representation":[], "Multiple representations":[]}
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
        
        x = 2*a
        y = 2*b
        
        representation_dictionary["One representation"] = [ArithmeticSequence(x.next(), x.next(2)), ArithmeticSequence(y.previous(2), y.previous())]
        representation_dictionary["Multiple representations"] = [ArithmeticSequence(x.next(3), y.previous(3))]
        return representation_dictionary

class DisjointSequences:
    def __init__(self, disjoint_seq_list, check_disjoint = True, presorted = False):
        if not presorted:
            disjoint_seq_list = sorted(disjoint_seq_list, key=lambda sequence: sequence.initial)
            
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
        formal_list = []
        
        for seq in self.sequence_list:
            a = seq.initial
            b = seq.final
            
            if a == b:
                formal_list.append(a)
            else:
                formal_list.append([a,b])
                
        return formal_list
    
    def find_smallest_larger_interval_startpoint(self, elem):
        initial_value_list = map(lambda seq: seq.initial, self.sequence_list)
        
        i = bisect_right(initial_value_list, elem)
        
        if i < len(initial_value_list):
            return initial_value_list[i]
        
        else:
            return INFINITY
        
    def union(self, other, seq_pair = "proxy", starting_index = 0):
        if seq_pair == "proxy":
            return self.union(other, [list(self.sequence_list), list(other.sequence_list)])
        
        [seq_list1, seq_list2] = seq_pair
        
        if seq_list2 == []:
            return DisjointSequences(seq_list1, False, True)
        
        seq_to_merge = seq_list2.pop(0)
        
        i_left = bisect_left(seq_list1, seq_to_merge, starting_index)
        starting_index = i_left
        
        if i_left != 0:
            if seq_list1[i_left - 1].next_to(seq_to_merge):
                seq_to_merge = seq_list1[i_left - 1].union(seq_to_merge)
                i_left -= 1
        
        i_right = bisect_right(seq_list1, seq_to_merge.next_singleton(), starting_index)
        
        if i_right == 0:
            seq_list1.insert(0, seq_to_merge)
            return self.union(other, [seq_list1, seq_list2], starting_index)
            
        if seq_list1[i_right - 1].next_to(seq_to_merge):
            seq_to_merge = seq_list1[i_right - 1].union(seq_to_merge)
        
        if i_left != 0:
            seq_list1 = seq_list1[:i_left] + [seq_to_merge] + seq_list1[i_right:]
            
        else:
            seq_list1 = [seq_to_merge] + seq_list1[i_right:]
            
        return self.union(other, [seq_list1, seq_list2], starting_index)
    
    def complement(self, other, seq_pair = "proxy", starting_index = 0):
        if seq_pair == "proxy":
            return self.complement(other, [list(self.sequence_list), list(other.sequence_list)])
        
        [seq_list1, seq_list2] = seq_pair
        
        if seq_list2 == []:
            return DisjointSequences(seq_list1, False, True)
        
        seq_to_subtract = seq_list2.pop(0)
        
        i_left = bisect_left(seq_list1, seq_to_subtract, starting_index)
        starting_index = i_left
        
        i_right = bisect_right(seq_list1, seq_to_subtract.next_singleton(), starting_index)
        
        if i_left == 0:
            if i_right == 0:
                return self.complement(other, [seq_list1, seq_list2])
            
            if i_right == 1:
                seq_list1 = seq_list1[0].complement(seq_to_subtract) + seq_list1[1:]
                return self.complement(other, [seq_list1, seq_list2], starting_index)
                
            seq_list1 = seq_list1[0].complement(seq_to_subtract) + seq_list1[i_right - 1].complement(seq_to_subtract) + seq_list1[i_right:]
            return self.complement(other, [seq_list1, seq_list2], starting_index)
        
        if i_left == i_right:
            seq_list1 = seq_list1[:i_left - 1] + seq_list1[i_left - 1].complement(seq_to_subtract) + seq_list1[i_left:]
            return self.complement(other, [seq_list1, seq_list2], starting_index)
        
        seq_list1 = seq_list1[:i_left - 1] + seq_list1[i_left - 1].complement(seq_to_subtract) + seq_list1[i_right - 1].complement(seq_to_subtract) + seq_list1[i_right:]
        
        return self.complement(other, [seq_list1, seq_list2], starting_index)
    
    def symmetric_difference(self, other, seq_pair = "proxy", starting_index = 0):
        difference1 = self.complement(other)
        difference2 = other.complement(self)
        
        return difference1.union(difference2)


class NonStandardUlamSequence:
    def __init__(self,R,init_ulam = 0):
        self.base_ring = R

        if init_ulam == 0:
            one = NonStandardInteger(1,0,R)
            w = NonStandardInteger(0,1,R)
            self.largest_constant_computed = 2*w
        
            seq1 = ArithmeticSequence(one,one, False)
            seq2 = ArithmeticSequence(w,2*w, False)
        
            self.ulam_list = DisjointSequences([seq1, seq2], False, True)
            self.one_representation_list = DisjointSequences([], False, True)
            self.multiple_representation_list = DisjointSequences([], False, True)

        else:
            self.ulam_list = init_ulam
            self.largest_constant_computed = init_ulam.sequence_list[-1].final

            raise NotImplementedError
        
    def __repr__(self):
        return("Nonstandard Ulam sequence U(1,N)")
        
    def extend_one_sequence(self):
        ulam_length = len(self.ulam_list.sequence_list)
        
        for i in range(ulam_length):
            if i == ulam_length - 1:
                seq2 = ((self.ulam_list).sequence_list)[-1]
                representation_dictionary = seq2.add_to_itself()

            else:
                seq1 = ((self.ulam_list).sequence_list)[i]
                seq2 = ((self.ulam_list).sequence_list)[-1]
                representation_dictionary = seq1 + seq2
            
            one_representation_partial_list = DisjointSequences(representation_dictionary["One representation"])
            new_one_representation_list = one_representation_partial_list.symmetric_difference(self.one_representation_list)
            new_one_representation_list = new_one_representation_list.complement(self.ulam_list)

            new_multiple_representation_list1 = self.one_representation_list.complement(new_one_representation_list)
            new_multiple_representation_list2 = one_representation_partial_list.complement(new_one_representation_list)
            new_multiple_representation_list3 = DisjointSequences(representation_dictionary["Multiple representations"])

            new_multiple_representation_list = self.multiple_representation_list.union(new_multiple_representation_list1)
            new_multiple_representation_list = new_multiple_representation_list.union(new_multiple_representation_list2)
            new_multiple_representation_list = new_multiple_representation_list.union(new_multiple_representation_list3)

            new_one_representation_list = new_one_representation_list.complement(self.multiple_representation_list)
            
            self.one_representation_list = new_one_representation_list
            self.multiple_representation_list = new_multiple_representation_list
            
        minimal_sequence = (self.one_representation_list).sequence_list.pop(0)
        a = minimal_sequence.initial
        b = minimal_sequence.final

        w = NonStandardInteger(0,1,self.base_ring)
        
        if a == b:
            if (self.one_representation_list).sequence_list == []:
                one_rep_bound = a + 2 * w
            else:
                one_rep_bound = (self.one_representation_list).sequence_list[0].initial
            
            multiple_rep_bound = self.multiple_representation_list.find_smallest_larger_interval_startpoint(a)
            if (multiple_rep_bound == INFINITY):
                multiple_rep_bound = a + 2 * w
                
            trivial_bound = a + w
            
            if trivial_bound < min(one_rep_bound, multiple_rep_bound):
                new_seq = ArithmeticSequence(a, (a + w).previous())
                self.ulam_list = self.ulam_list.union(DisjointSequences([new_seq]))
                
            else:
                if one_rep_bound < multiple_rep_bound:
                    new_seq = ArithmeticSequence(a, one_rep_bound.previous())
                    new_seq2 = ArithmeticSequence(one_rep_bound, one_rep_bound)

                    seqs_to_cut_out = DisjointSequences([new_seq2])

                    self.ulam_list = self.ulam_list.union(DisjointSequences([new_seq]))
                    self.one_representation_list = self.one_representation_list.complement(seqs_to_cut_out)
                    self.multiple_representation_list = self.multiple_representation_list.union(seqs_to_cut_out)

                else:
                    new_seq = ArithmeticSequence(a, multiple_rep_bound.previous())
                    self.ulam_list = self.ulam_list.union(DisjointSequences([new_seq]))
        else:
            new_seq = ArithmeticSequence(a, a)
            new_seq2 = ArithmeticSequence(a.next(), a.next())
            self.ulam_list = self.ulam_list.union(DisjointSequences([new_seq]))
            self.multiple_representation_list = self.multiple_representation_list.union(DisjointSequences([new_seq2]))

            if b > a.next():
                new_seq3 = ArithmeticSequence(a.next(2), b)
                self.one_representation_list = self.one_representation_list.union(DisjointSequences([new_seq3]))
                
        self.largest_constant_computed = self.ulam_list.sequence_list[-1].final
                
    def coeff_up_to(self, bound):
        if bound >= self.largest_constant_computed:
            while self.ulam_list.sequence_list[-1].final < bound:
                self.extend_one_sequence()

        seq = ArithmeticSequence(bound.next(), max(bound, self.largest_constant_computed).next())
        return self.ulam_list.complement(DisjointSequences([seq]))
