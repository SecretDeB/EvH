import hashlib
import math

from bitarray import bitarray
size_div = 1

class BloomFilter(object):
    def __init__(self, items_count, fp_prob, static_allocation=True, init_hash_count=1, bf_fixed_size=640,
                 hash_function="SHA256"):
        '''
        items_count : int
            Number of items expected to be stored in bloom filter
        fp_prob : float
            False Positive probability in decimal
        '''
        self.fp_prob = fp_prob
        self.search = []

        if static_allocation is True:
            self.size = bf_fixed_size
            self.hash_count = init_hash_count
        else:
            self.size = self.get_size(items_count, fp_prob)
            self.size = int(self.size / size_div)
            self.hash_count = self.get_hash_count(self.size, items_count)


        print(f"Size = {self.size / 8000} KB")


        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

    def get_bit_array(self):
        return self.bit_array

    def add(self, sha, item):
        '''
        Add an item in the filter
        '''
        sha.update(item.encode('utf-8'))
        # print(F"ADD: item = {item.encode('utf-8')}")

        snapshot  = sha.copy()
        # print(self.hash_count)
        # print(f"self.hash_count = {self.hash_count}")
        for i in range(self.hash_count):
            # SHA Hash Function
            sha.update(str(i).encode('utf-8'))
            digest = int(sha.hexdigest(), base=16) % self.size
            self.bit_array[digest] = True
            sha = snapshot.copy()

    def display(self):
        '''
                Display the bloom filter bits
        '''
        for i in range(self.size):
            print(str(self.bit_array[i]) + " ", end="")
        print()

    def check(self, sha, item):
        '''
        Check for existence of an item in filter
        '''
        sha.update(item.encode('utf-8'))
        # print(F"CHECK: item = {item.encode('utf-8')}")
        snapshot  = sha.copy()
        for i in range(self.hash_count):
            sha.update(str(i).encode('utf-8'))
            digest = int(sha.hexdigest(), base=16) % self.size
            if self.bit_array[digest] == False:
                return None
            sha = snapshot.copy()
        return sha

    @classmethod
    def get_size(self, n, p):
        '''
        Return the size of bit array(m) to used using the following formula
        m = -(n_items * lg(p)) / (lg(2)^2)
        n_items : int
            number of items to be stored in filter
        p : float
            False Positive probability in decimal
        '''
        mul = math.log(p)
        div = (math.log(2) ** 2)
        m = -(n * mul) / div

        # print("M:",m)
        return int(m)

    @classmethod
    def get_hash_count(self, m, n):
        '''
        Return the hash function(k) to be used using the following formula
        k = (m/n_items) * lg(2)
        m : int
            size of bit array
        n_items : int
            number of items expected to be stored in filter
        '''
        k = (m / n) * math.log(2)
        k = k / size_div
        print("hash_count:", k)
        return int(k)

    def get_load_factor(self):
        '''
        counts the number of one's comparing to bit array size
        '''
        count = self.bit_array.count(1)
        return count / self.size
