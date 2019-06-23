# RangeList class


class RangeList:
    """
    hold and manage sequences of integer ranges
    """

    def __init__(self, n1, n2):
        assert n1 < n2, "bad input"
        self.__ranges = [[n1,n1], [n2,n2]]

    def __iter__(self):
        for r in self.__ranges:
            for n in range(r[0], r[1]+1):
                yield n

    def __repr__(self):
        ret = ""
        for range in self.__ranges:
            if range[0] == range[1]:
                ret = ret + str(range[0]) + "\n"
            else:
                ret = ret + str(range[0]) + "," + str(range[1]) + "\n"
        return ret

    def max(self):
        """
        return max number in the sequence
        """
        return self.__ranges[-1][-1]

    def appendRange(self, n1, n2):
        assert n1 <= n2, "range not in order"
        assert n1 > self.max()+1, "overlapping ranges not implemented yet"
        self.__ranges.append([n1, n2])

    def append(self, n):
        m = self.max()
        if n == m+1:
            # grow the last range
            self.__ranges[-1][1] = n
        elif n > m+1:
            # make new range
            self.__ranges.append([n, n])
        else:
            raise "bad input"

if __name__== "__main__":
    rl = RangeList(1,4)
    rl.append(5)
    rl.appendRange(7,8)
    rl.append(11)
    rl.append(12)
    rl.append(13)

    print(rl)

    for n in rl:
        print(n)
