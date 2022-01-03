class Stack:
     def __init__(self) -> None:
         self.items = []

     def is_empty(self) -> bool:
         return self.items == []

     def push(self, item) -> None:
         self.items.insert(0,item)

     def count(self) -> int:
         return len(self.items)

     def pop(self):
         return self.items.pop(0)

     def top(self):
         return self.items[0]

     def size(self) -> int:
         return len(self.items)