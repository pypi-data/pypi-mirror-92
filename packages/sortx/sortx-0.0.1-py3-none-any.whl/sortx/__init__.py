
class SortX:
    def __init__(self):
        pass

    def smallSort(self, arr):
        smallest = arr[0]
        smallest_index = 0
        for i in range(1, len(arr)):
            if arr[i] < smallest:
                smallest = arr[i]
                smallest_index = i
        return smallest_index

    def bigSort(self, arr):
        biggest = arr[0]
        biggest_index = 0
        for i in range(1, len(arr)):
            if arr[i] > biggest:
                biggest = arr[i]
                biggest_index = i
        return biggest_index

    def selectionSort(self, arr, ascend=True, descend=False):
        """This method sorts the array(arr), and returns anew array sorted"""
        if descend:
            ascend = False
        elif ascend == False:
            descend = True
        newArr = []
        for _ in range(len(arr)):
            if ascend:
                sort_item = self.smallSort(arr)
            else:
                sort_item = self.bigSort(arr)
            newArr.append(arr.pop(sort_item))
        return newArr
