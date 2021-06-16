class RandomAccessQueue:
    array = empty array of length 8
    head_pointer = 0
    tail_pointer = 0

    def pushright(x):
        array[tail_pointer] = x
        tail_pointer++
        if (tail_pointer == array.length):
            new_array = empty array of length (array.length * 2)
            for (int i=0; i<tail_pointer-head_pointer; i++) {
                new_array[i] = array[head_pointer+i]
            }
            array = new_array
            tail_pointer -= head_pointer
            head_pointer = 0
    
    def popleft():
        if (head_pointer >= tail_pointer):
            throw Exception("The queue is empty")
            # or return null
        else:
            x = array[head_pointer]
            head_pointer++
            return x
    
    def element_at(i):
        index = head_pointer+i
        if (index >= tail_pointer):
            throw Exception("Index out of bounds")
            # or return null
        else:
            return array[index]
