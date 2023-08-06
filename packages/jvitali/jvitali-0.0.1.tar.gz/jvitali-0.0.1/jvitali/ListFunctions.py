
# from https://pypi.org/project/TinyMath/#modal-close

class ListFunctions:

    # matching 2 lists and their columns
    def colMatch(self, list1, list2, print=False):
        elementsInList1NotInList2 = []
        elementsInList2NotInList1 = []

        for elt in list1:
            if elt not in list2:
                elementsInList1NotInList2.append(elt)
        for elt in list2:
            if elt not in list1:
                elementsInList2NotInList1.append(elt)

        if print==True:
            print("Shape of list 1: " + str(list1.shape))
            print("Shape of list 2: " + str(list2.shape))
            print("Columns in first list not in second list: " + elementsInList1NotInList2)
            print("Columns in second list not in first list: " + elementsInList2NotInList1)

        return elementsInList1NotInList2, elementsInList2NotInList1



