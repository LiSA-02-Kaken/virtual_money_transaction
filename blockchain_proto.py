import hashlib
from datetime import datetime
class Block:

    def __init__(self,  data, previous_hash):
      self.timestamp =  datetime.now()
      self.data = data
      self.previous_hash = previous_hash
      self.hash = self.calc_hash()
      self.next = None


    def calc_hash(self):
        hash_str = "We are going to encode this string of data!".encode('utf-8')
        return hashlib.sha256(hash_str).hexdigest()

class Blockchain:

    def __init__(self):
        self.head = None
        self.next = None

    def add_block(self, data):

        if self.head == None:
            self.head = Block(data,0)

        else:
            current = self.head

          # loop to the last node of the linkedlist
            while current.next:
                current = current.next

            # stores the previous has for the next block
            previous_hash = current.hash
            current.next = Block(data, previous_hash)

      

    def print_blockchain(self):

        if self.head == None:
            print("The blockchain is empty")
            return

        else:
            current = self.head
            while current:
                print("Timestamp:", current.timestamp)
                print("Data:", current.data)
                print("Hash:", current.hash)
                print("Previous hash:", current.previous_hash)
                print("--------------->")

                current = current.next

bitcoin = Blockchain()

bitcoin.add_block("block 1")
bitcoin.add_block("block 2")
bitcoin
bitcoin.add_block("block 3")
bitcoin.print_blockchain()