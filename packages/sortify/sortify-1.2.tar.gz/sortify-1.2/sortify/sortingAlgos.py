class Sort:
    @staticmethod
    def bubble(array, reverse = False):
        """Performs bubble sort on the input array.
        Args-
            array (list/iterable): The array that you want to sort
            reverse (bool): True to sort the array in decsending order, else False
        Returns-
            sortedArray (list/iterable): The array after sorting
        """
        n = len(array)
        if reverse:
            for i in range(n):
                sorted = True
                for j in range(n-1-i):
                    if array[j] < array[j+1]:
                        array[j], array[j+1] = array[j+1], array[j]
                        sorted = False
                if sorted:
                    break
        else:
            for i in range(n):
                for j in range(n-1-i):
                    if array[j] > array[j+1]:
                        array[j], array[j+1] = array[j+1], array[j]
                        sorted = False
                if sorted:
                    break
        return array 



    @staticmethod
    def selection(array, reverse = False):
        """Performs selection sort on the input array.
        Args-
            array (list/iterable): The array that you want to sort
            reverse (bool): True to sort the array in decsending order, else False
        Returns:
            sortedArray (list/iterable): The array after sorting
        """
        n = len(array)
        if reverse:
            while n:
                smallest_val_index = 0
                for i in range(n):
                    if array[i] < array[smallest_val_index]:
                        smallest_val_index = i  
                array[i], array[smallest_val_index] = array[smallest_val_index], array[i] 
                n -= 1
        else:
            while n:    
                largest_val_index = 0
                for i in range(n):
                    if array[i] > array[largest_val_index]:
                        largest_val_index = i  
                array[i], array[largest_val_index] = array[largest_val_index], array[i] 
                n -= 1
  
        return array 
    

    @staticmethod
    def insertion(array, reverse = False):
        """Performs insertion sort on the input array.
        Args:
            array (list/iterable)- The array that you want to sort
            reverse (bool)- True to sort the array in decsending order, else False
        Returns:
            sortedArray (list/iterable)- The array after sorting
        """
        n = len(array)
        if reverse:    
            for i in range(1,n):
                key_item = array[i] # item that we need to insert at the appropriate posn
                j = i-1 

                while j >= 0 and array[j] < key_item: # looping through the sorted subarray backwards to check if the items are smaller than the key item 
                    array[j+1] = array[j] # if subarray item is smaller than the key item, moving it to the right
                    j -= 1 
                
                array[j+1] = key_item # inserting the key item at its appropriate place

        else:
            for i in range(1,n):
                key_item = array[i] # item that we need to insert at the appropriate posn
                j = i-1 # assumed position of key item; also the position upto which we assume the array is sorted

                while j >= 0 and array[j] > key_item: #looping through the sorted subarray backwards to check if the items are greater than the key item 
                    array[j+1] = array[j] # if subarray item is greater than the key item, moving it to the right
                    j -= 1 
                
                array[j+1] = key_item # inserting the key item at its appropriate place

        return array
    
    @staticmethod
    def quick(array, reverse = False):
        """Performs quick sort on the input array.
        Args-
            array (list/iterable): The array that you want to sort
            reverse (bool): True to sort the array in decsending order, else False
        Returns:
            sortedArray (list/iterable)- The array after sorting
        """
        # base case for recursion
        n = len(array)
        if n < 2:
            return array
        
        pivot = array[(n-1)//2] # selecting the middle element as the pivot
        
        left, right, same = [], [], [] # creating three empty arrays 

        if reverse:
            for element in array: # iterating through the array placing the elements in the correct position
                if element > pivot:
                    left.append(element) 
                elif element < pivot:
                    right.append(element)
                else:
                    same.append(element)
        else:
            for element in array: # iterating through the array placing the elements in the correct position
                if element < pivot:
                    left.append(element) 
                elif element > pivot:
                    right.append(element)
                else:
                    same.append(element)

        return Sort.quick(left, reverse) + same + Sort.quick(right, reverse) # using recursion for further sorting

    
    
    # helper method for merge sort
    @staticmethod
    def mergeList(left, right, reverse):
        
        sorted = [] # we need to add elements from left and right array in a way after the merge is complete, we get a sorted merge
        
        len_left = len(left)
        len_right = len(right)
        
        left_index = right_index = 0

        if reverse: # for sorting in reverse order (largest to smallest)
            while len(sorted) < len_left + len_right:
                if left_index < len_left and right_index < len_right:
                    if left[left_index] >= right[right_index]:
                        sorted.append(left[left_index])
                        left_index += 1  
                    else:
                        sorted.append(right[right_index])
                        right_index += 1
                if left_index == len_left:
                    sorted += right[right_index:]
                    break
                elif right_index == len_right:
                    sorted += left[left_index:]
                    break
        else: # for sorting in ascending order (smallest to largest)
            while len(sorted) < len_left + len_right:
                if left_index < len_left and right_index < len_right:
                    if left[left_index] <= right[right_index]:
                        sorted.append(left[left_index])
                        left_index += 1
                    else:
                        sorted.append(right[right_index])
                        right_index += 1
                
                if left_index == len_left:
                    sorted += right[right_index:]
                    break
                elif right_index == len_right:
                    sorted += left[left_index:]
                    break     
        return sorted
    
    @staticmethod
    def merge(array, reverse = False):
        """Performs merge sort on the input array.
        Args:
            array (list/iterable): The array that you want to sort
            reverse (bool): True to sort the array in decsending order, else False
        Returns:
            sortedArray (list/iterable): The array after sorting
        """
        # base case for recursion
        n = len(array)
        if n < 2:
            return array

        mid_index = n // 2 # selecting the mid index to split the array at
        
        left = Sort.merge(array[ : mid_index], reverse) # performing recursive splits on the left array 
        right = Sort.merge(array[mid_index : ], reverse) # performing recursive splits on the right array

        return Sort.mergeList(left, right, reverse) # finally merging the splits while sorting

