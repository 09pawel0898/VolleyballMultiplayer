class Stack:
     def __init__(self):
         self.items = []

     def is_empty(self):
         return self.items == []

     def push(self, item):
         self.items.insert(0,item)

     def count(self):
         return len(self.items)

     def pop(self):
         return self.items.pop(0)

     def top(self):
         return self.items[0]

     def size(self):
         return len(self.items)