class Heap:
    #MIN & MAX HEAP Class
    def __init__(self,option='MIN'):
        self.heap = [-1]
        self.option = option

    def insert(self,e):
        self.heap.append(e)
        idx = len(self.heap) - 1
        if self.option == 'MIN':
            #Move up the Heap untill a smaller element is found
            while idx > 1 and self.heap[idx >> 1] > self.heap[idx]:
                self.heap[idx >> 1] , self.heap[idx] = self.heap[idx] , self.heap[idx >> 1]
                idx >>= 1
        elif self.option == 'MAX':
            # Move up the Heap untill a larger element is found
            while idx > 1 and self.heap[idx >> 1] < self.heap[idx]:
                self.heap[idx >> 1], self.heap[idx] = self.heap[idx], self.heap[idx >> 1]
                idx >>= 1

    def heapify(self):

        heap_len = len(self.heap) - 1
        def the_heapify(idx):
            while 1:
                l = idx << 1
                r = (idx << 1) + 1
                the_element = self.heap[idx]
                the_idx = idx

                if self.option == 'MIN':
                    if l <= heap_len and self.heap[l] < the_element:
                        the_element = self.heap[l]
                        the_idx = l
                    if r <= heap_len and self.heap[r] < the_element:
                        the_element = self.heap[r]
                        the_idx = r
                    if the_idx == idx:
                        return
                else:
                    if l <= heap_len and self.heap[l] > the_element:
                        the_element = self.heap[l]
                        the_idx = l
                    if r <= heap_len and self.heap[r] > the_element:
                        the_element = self.heap[r]
                        the_idx = r
                    if the_idx == idx:
                        return
                self.heap[idx], self.heap[the_idx] = self.heap[the_idx], self.heap[idx]
                idx = the_idx

        the_heapify(1)

    def get_heap_top(self):

        if len(self.heap) == 1:
            return None

        if len(self.heap) == 2:
            e = self.heap[1]
            self.heap = [-1]
            return e

        e = self.heap[1]
        self.heap[1] = self.heap[len(self.heap) - 1]
        self.heap = self.heap[:-1]
        self.heapify()

        return e

    def hprint(self):
        print '[]' if len(self.heap) == 1 else self.heap[1:]

    def get(self , i):
        return self.heap[i] if len(self.heap) > 1 else None

    def get_len(self):
        return len(self.heap) - 1 if len(self.heap) > 1 else 0


n = int(raw_input().strip())
a = []
a_i = 0
hmax = Heap(option='MAX')
hmin = Heap(option='MIN')
for a_i in xrange(n):
    a_t = int(raw_input().strip())
    a.append(a_t)
    if len(a) == 1:
        print float(a[0])
    elif len(a) == 2:
        print float(a[0] + a[1]) / 2
        if a[0] > a[1] :
            hmax.insert(a[1])
            hmin.insert(a[0])
        else:
            hmax.insert(a[0])
            hmin.insert(a[1])
    else:
            if a_t > hmax.get(1):
                hmin.insert(a_t)
            else:
                hmax.insert(a_t)

            l_min = hmin.get_len()
            l_max = hmax.get_len()
            if l_min == l_max:
                print float(hmin.get(1) + hmax.get(1)) / 2
            else:
                if abs(l_min - l_max) > 1:
                    if l_min > l_max:
                        e= hmin.get_heap_top()
                        hmax.insert(e)
                    else:
                        e = hmax.get_heap_top()
                        hmin.insert(e)
                    print float(hmin.get(1) + hmax.get(1)) / 2
                else:
                    if l_min > l_max:
                        print float(hmin.get(1))
                    else:
                        print float(hmax.get(1))
