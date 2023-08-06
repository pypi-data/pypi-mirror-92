# Sortify

## Project Description
---

__sortify__ is a Python package containing implementations of different sorting algorithms. This module is implemented using vanilla Python and does not need any additional dependencies.

## Installation
---

Simply run the following command in the terminal to install sortify:

```
pip install sortify
```

## Usage
---

The following example demonstrates how you can use __sortify__:

```
from sortify import Sort

if __name__ == "__main__":
    arr = [1, 7, 2, 6, 3, 5, 4]
    print(Sort.bubble(arr))
```

This prints the following result:

```
[1, 2, 3, 4, 5, 6, 7]
```

The available sorting methods are:
* Sort.bubble(arr: list, reverse: bool) → Bubble sort
* Sort.insertion(arr: list, reverse: bool) → Insertion sort
* Sort.selection(arr: list, reverse: bool) → Selection sort
* Sort.quick(arr: list, reverse: bool) → Quick sort
* Sort.mergesort(arr: list, reverse: bool) → Merge sort

Here, set the parameter __reverse = True__ to sort the list in descending order. For example:

```
from sortify import Sort

if __name__ == "__main__":
    arr = [1, 7, 2, 6, 3, 5, 4]
    print(Sort.merge(arr, reverse=False))
```

This prints the following result:

```
[7, 6, 5, 4, 3, 2, 1]
```
