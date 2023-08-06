class Queue:
    def __init__(self, *args):
        self.arr = list(args)

    def size(self):
        return len(self)

    def push(self, element):
        self.arr.append(element)

    def append(self, element):
        self.push(element)

    def pop(self):
        return self.arr.pop(0)

    def get_list(self):
        return self.arr

    def get_array(self):
        return self.arr

    def __getitem__(self, slice):
        return self.arr[slice]

    def __iter__(self):
        return iter(self.arr)

    def __add__(self, lst):
        self.arr.extend(lst)

    def __sub__(self, val):
        for i in range(len(self.arr)):
            self.arr[i] -= val

    def __mul__(self, val, individually=True):
        if individually:
            for i in range(len(self.arr)):
                self.arr[i] *= val
        else:
            self.arr *= val

    def __div__(self, val):
        for i in range(len(self.arr)):
            self.arr[i] /= val

    def __len__(self):
        return len(self.arr)

    def __repr__(self):
        return "[" + ", ".join(list(map(str, self.arr))) + "]"
