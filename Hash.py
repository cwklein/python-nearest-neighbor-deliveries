# Hash.py

class ChainingHashTable:
    def __init__(self, initial_capacity=40):
        self.table = []
        self.size = 0
        for i in range(initial_capacity):
            self.table.append([])

    def insert(self, key, value):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for keyValue in bucket_list:
            if keyValue[0] == key:
                keyValue[1] = value
                return True

        newKeyValue = [key, value]
        bucket_list.append(newKeyValue)
        self.size += 1
        return True

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for keyValue in bucket_list:
            if keyValue[0] == key:
                return keyValue[1]  # value
        return None

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for keyValue in bucket_list:
            if keyValue[0] == key:
                self.size -= 1
                bucket_list.remove([keyValue[0], keyValue[1]])
