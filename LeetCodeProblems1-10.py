# Problems from LeetCode.com

# Problem 1:
def twoSum(nums, target):
    """return the indices of the input such that the elements at those indices sum to target"""
    numbers_we_need = {}
    for i in range(len(nums)):
        if nums[i] in numbers_we_need:
            return [numbers_we_need[nums[i]], i]
        numbers_we_need[target - nums[i]] = i
    return False

# Problem 2:
# given two non-empty linked lists, representing two non negative integers (stored in reverse order) e.g. 4->5->6 =
# 654. Add the two numbers and return it in the form of a linked list (also in reverse order)
class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next
    def getValue(self):
        return self.val
    def getNext(self):
        return self.next
    def setNext(self, newNext):
        self.next = newNext

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        new_node.setNext(self.head)
        self.head = new_node

    def insertSorted(self, value):
        new_node = Node(value)

        current = self.head
        previous = None
        while current:
            if current.getValue() >= value or current.getValue() == None:
                break
            else:
                previous = current
                current = current.getNext()
        if not previous:
            new_node.setNext(self.head)
            self.head = new_node
        else:
            previous.setNext(new_node)
            new_node.setNext(current)

    def size(self):
        head = self.head
        count = 0
        while head:
            count += 1
            head = head.getNext()
        return count

    def search(self, target):
        head = self.head
        found = False
        while head and not found:
            if head.getValue() == target:
                found = True
            else:  head = head.getNext()
        if not found:
            return False
        return True

    def delete(self, data):
        current = self.head
        previous = None
        found = False
        while current and not found:
            if current.getValue() == data:
                found = True
            else:
                previous = current
                current = current.getNext()
        if not found:
            return False
        if not previous:
            self.head = current.getNext()
        else:  previous.setNext(current.getNext())
        return True

    def compareString(self, otherLL):
        l1 = self.head
        l2 = otherLL.head
        while l1 or l2:
            if l1 and not l2:
                return 1
            elif l2 and not l1:
                return -1
            if l1.getValue() > l2.getValue():
                return 1
            elif l1.getValue() < l2.getValue():
                return -1
            l1, l2 = l1.getNext(), l2.getNext()
        return 0

    def merge(self, otherLL):
        firstHead = self.head
        secondHead = otherLL.head
        while firstHead and secondHead:
            # save next pointers
            first_next = firstHead.getNext()
            second_next = secondHead.getNext()

            # point list 2 node to next node in list 1. point current list 1 node to current list 2 node
            secondHead.setNext(first_next)
            firstHead.setNext(secondHead)

            # update current pointers for next iteration
            firstHead = first_next
            secondHead = second_next

        otherLL.head = secondHead
        return

    def __str__(self):
        head = self.head
        string = ''
        while head:
            string += str(head.getValue()) + '->'
            head = head.getNext()
        return string


def addTwoLinkedLists(l1, l2):
    """two linked lists will be given, they represent a number in reverse. return the sum of the numbers also
      in the form of a linked list, also reversed"""
    numbers_to_add = []

    # looping though both linked lists to retrieve numbers
    for each in (l1, l2):
        string = ''
        head = each
        while head:
            string += str(head.val)
            head = head.next
        numbers_to_add.append(int(string[::-1]))

    # add numbers and create linked list of sum
    sum_ = sum(numbers_to_add)
    string_sum = str(sum_)
    previous_node = None
    for number in string_sum:
        newNode = Node(number)
        if previous_node:
            newNode.next = previous_node
        previous_node = newNode
    return newNode

# Problem 3:
# Longest substring without repeating characters
