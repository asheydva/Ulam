from sage.rings.polynomial.polynomial_ring import PolynomialRing_commutative
class NonStandardRing(PolynomialRing_commutative):
    def __init__(self,names):
        if len(names) > 1:
            raise ValueError("Too many variables.")
        PolynomialRing_commutative.__init__(self, ZZ, names)
        
    def __repr__(self):
        return("Nonstandard Ring U(1,%s)" % self.gens())
    
class ArithmeticSequence:
    def __init__(self,start,end, ring, check = True):
        if check:
            if (start not in ring) or (end not in ring):
                raise ValueError("Endpoints do not lie in the given ring.")
        
            if start > end:
                raise ValueError("Start of interval larger than end of interval.")
        
        self.initial = start
        self.final = end
        self.base_ring = ring
        
    def __repr__(self):
        if self.is_singleton():
            return("Singleton %s in %s" % (self.initial, self.base_ring))
        return("Sequence of elements in %s with endpoints %s and %s" % (self.base_ring, self.initial, self.final))
        
    def __contains__(self, elem):
        if elem not in self.base_ring:
            return False
        
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
        if seq2.final >= self.initial - 1:
            if seq2.initial <= self.final - 1:
                return True
            
        if self.final >= seq2.initial - 1:
            if self.initial <= seq2.final - 1:
                return True
            
        return False
        
    def __add__(self, seq2):
        if self.intersects(seq2):
            raise ValueError("Only addition of non-intersecting sequences is defined.")
            
        representation_dictionary = {"One representation":[], "Multiple representations":[]}
        
        if self.is_singleton() or seq2.is_singleton():
            representation_dictionary["One representation"] = [ArithmeticSequence(self.initial + seq2.initial, self.final + seq2.final, self.base_ring)]
            
        else:
            start = self.initial + seq2.initial
            end = self.final + seq2.final
            
            if start < end - 2:
                representation_dictionary["One representation"] = [ArithmeticSequence(start, start + 1, self.base_ring), ArithmeticSequence(end - 1, end, self.base_ring)]
                
                if start <= end - 4:
                    representation_dictionary["Multiple representations"] = [ArithmeticSequence(start + 2, end - 2, self.base_ring)]
                
            else:
                representation_dictionary["One representation"] = [ArithmeticSequence(start, end, self.base_ring)]
                
                
        return representation_dictionary
    
    def union(self, seq2, check = True, span = False):
        if check:    
            if not self.initial in seq2.base_ring:
                raise ValueError("Sequences not defined over the same ring.")
                
        if not span:
            if not self.intersects(seq2):
                raise ValueError("Only union of intersecting sequences is defined---consider using span.")
                
        start = min(self.initial, seq2.initial)
        end = max(self.final, seq2.final)
        
        return ArithmeticSequence(start, end, self.base_ring)
    
    def intersection(self, other):
        if self.intersects(other):
            start = max(self.initial, other.initial)
            end = min(self.final, other.final)
            
            return ArithmeticSequence(start, end, self.base_ring)
            
        return []
    
    def complement(self, seq2):
        sequences_not_cut_out = []
        
        if self.initial < seq2.initial:
            sequences_not_cut_out.append(ArithmeticSequence(self.initial, min(self.final, seq2.initial - 1), self.base_ring))
            
        if self.final > seq2.final:
            sequences_not_cut_out.append(ArithmeticSequence(max(self.initial, seq2.final + 1),self.final, self.base_ring))
            
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
        return ArithmeticSequence(self.final + 1, self.final + 1, self.base_ring, False)
    
    def add_to_itself(self):
        representation_dictionary = {"One representation":[], "Multiple representations":[]}
        if self.is_singleton():
            return representation_dictionary
        
        a = self.initial
        b = self.final
        
        if b == a + 1:
            representation_dictionary["One representation"] = [ArithmeticSequence(2*a + 1,2*a + 1,self.base_ring)]
            return representation_dictionary
            
        if b == a + 2:
            representation_dictionary["One representation"] = [ArithmeticSequence(2*a + 1, 2*a + 3, self.base_ring)]
            return representation_dictionary
        
        representation_dictionary["One representation"] = [ArithmeticSequence(2*a + 1, 2*a + 2, self.base_ring), ArithmeticSequence(2*b - 2, 2*b - 1, self.base_ring)]
        representation_dictionary["Multiple representations"] = [ArithmeticSequence(2*a + 3, 2*b - 3, self.base_ring)]
        return representation_dictionary
    
from bisect import bisect_left
from bisect import bisect_right

class DisjointSequences:
    def __init__(self, disjoint_seq_list, ring, check_disjoint = True, presorted = False):
        self.base_ring = ring
        
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
        O.<w> = self.base_ring
        
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
            return infinity
        
    def union(self, other, seq_pair = "proxy", starting_index = 0):
        if seq_pair == "proxy":
            return self.union(other, [list(self.sequence_list), list(other.sequence_list)])
        
        [seq_list1, seq_list2] = seq_pair
        
        if seq_list2 == []:
            return DisjointSequences(seq_list1, self.base_ring, False, True)
        
        seq_to_merge = seq_list2.pop(0)
        
        i_left = bisect_left(seq_list1, seq_to_merge, starting_index)
        starting_index = i_left
        
        if i_left != 0:
            if seq_list1[i_left - 1].next_to(seq_to_merge):
                seq_to_merge = seq_list1[i_left - 1].union(seq_to_merge, False, True)
                i_left -= 1
        
        i_right = bisect_right(seq_list1, seq_to_merge.next_singleton(), starting_index)
        
        if i_right == 0:
            seq_list1.insert(0, seq_to_merge)
            return self.union(other, [seq_list1, seq_list2], starting_index)
            
        if seq_list1[i_right - 1].next_to(seq_to_merge):
            seq_to_merge = seq_list1[i_right - 1].union(seq_to_merge, False, True)
        
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
            return DisjointSequences(seq_list1, self.base_ring, False, True)
        
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
    
O.<w> = NonStandardRing()
class NonStandardUlamSequence:
    def __init__(self):
        O.<w> = NonStandardRing()
        self.base_ring = O
        self.largest_constant_computed = 2*w
        
        seq1 = ArithmeticSequence(1,1,O,False)
        seq2 = ArithmeticSequence(w,2*w,O,False)
        
        self.ulam_list = DisjointSequences([seq1, seq2],O, False, True)
        self.one_representation_list = DisjointSequences([],O, False, True)
        self.multiple_representation_list = DisjointSequences([],O, False, True)
        
    def __repr__(self):
        return("Nonstandard Ulam sequence U(1,w)")
        
    def extend_one_sequence(self):
        O.<w> = self.base_ring
        ulam_length = len(self.ulam_list.sequence_list)
        
        for i in range(ulam_length):
            if i == ulam_length - 1:
                seq2 = ((self.ulam_list).sequence_list)[-1]
                representation_dictionary = seq2.add_to_itself()

            else:
                seq1 = ((self.ulam_list).sequence_list)[i]
                seq2 = ((self.ulam_list).sequence_list)[-1]
                representation_dictionary = seq1 + seq2
            
            one_representation_partial_list = DisjointSequences(representation_dictionary["One representation"], O)
            new_one_representation_list = one_representation_partial_list.symmetric_difference(self.one_representation_list)
            new_one_representation_list = new_one_representation_list.complement(self.ulam_list)

            new_multiple_representation_list1 = self.one_representation_list.complement(new_one_representation_list)
            new_multiple_representation_list2 = one_representation_partial_list.complement(new_one_representation_list)
            new_multiple_representation_list3 = DisjointSequences(representation_dictionary["Multiple representations"], O)

            new_multiple_representation_list = self.multiple_representation_list.union(new_multiple_representation_list1)
            new_multiple_representation_list = new_multiple_representation_list.union(new_multiple_representation_list2)
            new_multiple_representation_list = new_multiple_representation_list.union(new_multiple_representation_list3)

            new_one_representation_list = new_one_representation_list.complement(self.multiple_representation_list)
            
            self.one_representation_list = new_one_representation_list
            self.multiple_representation_list = new_multiple_representation_list
            
        minimal_sequence = (self.one_representation_list).sequence_list.pop(0)
        a = minimal_sequence.initial
        b = minimal_sequence.final
        
        if a == b:
            if (self.one_representation_list).sequence_list == []:
                one_rep_bound = a + 2 * w
            else:
                one_rep_bound = (self.one_representation_list).sequence_list[0].initial
            
            multiple_rep_bound = self.multiple_representation_list.find_smallest_larger_interval_startpoint(a)
            if (multiple_rep_bound == infinity):
                multiple_rep_bound = a + 2 * w
                
            trivial_bound = a + w
            
            if trivial_bound < min(one_rep_bound, multiple_rep_bound):
                new_seq = ArithmeticSequence(a, a + w - 1, O)
                self.ulam_list = self.ulam_list.union(DisjointSequences([new_seq], O))
                
            else:
                if one_rep_bound < multiple_rep_bound:
                    new_seq = ArithmeticSequence(a, one_rep_bound - 1, O)
                    new_seq2 = ArithmeticSequence(one_rep_bound, one_rep_bound, O)

                    seqs_to_cut_out = DisjointSequences([new_seq2], O)

                    self.ulam_list = self.ulam_list.union(DisjointSequences([new_seq], O))
                    self.one_representation_list = self.one_representation_list.complement(seqs_to_cut_out)
                    self.multiple_representation_list = self.multiple_representation_list.union(seqs_to_cut_out)

                else:
                    new_seq = ArithmeticSequence(a, multiple_rep_bound - 1, O)
                    self.ulam_list = self.ulam_list.union(DisjointSequences([new_seq], O))
        else:
            new_seq = ArithmeticSequence(a, a, O)
            new_seq2 = ArithmeticSequence(a + 1, a + 1, O)
            self.ulam_list = self.ulam_list.union(DisjointSequences([new_seq], O))
            self.multiple_representation_list = self.multiple_representation_list.union(DisjointSequences([new_seq2], O))

            if b > a + 1:
                new_seq3 = ArithmeticSequence(a + 2, b, self.base_ring)
                self.one_representation_list = self.one_representation_list.union(DisjointSequences([new_seq3], O))
                
        self.largest_constant_computed = self.ulam_list.sequence_list[-1].final
                
    def coeff_up_to(self, bound):
        if bound >= self.largest_constant_computed:
            while self.ulam_list.sequence_list[-1].final < bound:
                self.extend_one_sequence()

        seq = ArithmeticSequence(bound + 1, max(bound, self.largest_constant_computed) + 1, self.base_ring)
        return self.ulam_list.complement(DisjointSequences([seq], base_ring))