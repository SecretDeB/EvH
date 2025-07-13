import hashlib
import math

from bitarray import bitarray

size_div = 1


class BloomFilter(object):
    def __init__(self, items_count, fp_prob, static_allocation=True, init_hash_count=1, bf_fixed_size=600,
                 hash_function="SHA256"):
        '''
        items_count : int
            Number of items expected to be stored in bloom filter
        fp_prob : float
            False Positive probability in decimal
        '''

        self.fp_prob = fp_prob
        self.hash_function = hash_function
        self.reset_hash(hash_function)

        if static_allocation is True:
            self.size = bf_fixed_size
            if items_count==0:
                self.size = 0
            else:
                self.hash_count = self.get_hash_count(self.size, items_count)
        else:
            self.size = self.get_size(items_count, fp_prob)
            self.hash_count = self.get_hash_count(self.size, items_count)

        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)
        # print("Number of hash function:" + str(self.size))

    def reset_hash(self, hash_function="SHA256"):
        match hash_function:
            case "SHA1":
                self.sha = hashlib.sha1()
            case "SHA256":
                self.sha = hashlib.sha256()
            case "SHA512":
                self.sha = hashlib.sha512()
            case _:
                print("Enter valid hash function.")

    def get_bit_array(self):
        return self.bit_array

    def add(self, item, flag):
        '''
        Add an item in the filter
        '''

        # print(F"ADD: item = {item.encode('utf-8')}")
        if flag:
            self.reset_hash(self.hash_function)
            self.sha.update(item.encode('utf-8'))
            # print("Pk key:"+str(int(self.sha.hexdigest(),16)))
        else:
            self.sha.update(item.encode('utf-8'))
            # print("Updated value:" + str(int(self.sha.hexdigest(), 16)))
            snapshot = self.sha.copy()
            for i in range(self.hash_count):
                self.sha.update(str(i).encode('utf-8'))
                digest = int(self.sha.hexdigest(), base=16) % self.size
                # print("digest:" + str(digest))
                self.bit_array[digest] = True
                self.sha = snapshot.copy()

    def display(self):
        '''
                Display the bloom filter bits
        '''
        for i in range(self.size):
            if self.bit_array[i]==1:
                # print(str(i)+":"+str(self.bit_array[i]) + " ", end="")
                print(str(i) + ",", end="")
        print()

    def check(self, item, flag):
        '''
        Check for existence of an item in filter
        '''
        if flag:
            self.reset_hash(self.hash_function)
            self.sha.update(item.encode('utf-8'))

            snapshot_undo = self.sha.copy()
            self.sha.update(item.encode('utf-8'))
        # print(F"CHECK: item = {item.encode('utf-8')}")
        if flag:
            snapshot = self.sha.copy()
            for i in range(self.hash_count):
                self.sha.update(str(i).encode('utf-8'))
                digest = int(self.sha.hexdigest(), base=16) % self.size
                if self.bit_array[digest] == False:
                    self.sha = snapshot_undo.copy()
                    return False
                self.sha = snapshot.copy()
        return True

    def get(self, snapshot=None, item=None, flag=None):
        '''
        Check for existence of an item in filter
        '''
        if flag:
            self.reset_hash(self.hash_function)
            self.sha.update(item.encode('utf-8'))
            # print("Pk key:" + str(int(self.sha.hexdigest(), 16)))
            return -1, self.sha
        else:
            snapshot.update(str(item).encode('utf-8'))
            snapshot_= snapshot.copy()
            # print("Updated value:" + str(int(snapshot_.hexdigest(), 16)))
            for i in range(self.hash_count):
                snapshot.update(str(i).encode('utf-8'))
                digest = int(snapshot.hexdigest(), base=16) % self.size
                if self.bit_array[digest] == False:
                    return 0, None
                # print("digest:" + str(digest))
                snapshot = snapshot_.copy()
        return 1, snapshot_

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
        return int(k)

    def get_load_factor(self):
        '''
        counts the number of one's comparing to bit array size
        '''
        count = self.bit_array.count(1)
        return count / self.size
