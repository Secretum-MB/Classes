# Problem 004
def largestPalindromeProduct():
    def isPalindrome(n):
        n_string = str(n)
        string_divisor = len(n_string) // 2
        if len(n_string) % 2 == 0:
            first_half = n_string[:string_divisor]
        else:
            first_half = n_string[:string_divisor + 1]
        second_half = n_string[string_divisor:]
        if first_half == second_half[::-1]:
            return True
        return False

    largest_product = 999 * 999

    while True:
        while not isPalindrome(largest_product):
            largest_product -= 1

        for i in reversed(range(1, 1000)):
            if largest_product % i == 0:
                first_number = i
                second_number = largest_product / first_number
                if (first_number > 99 and first_number < 1000) and (second_number > 99 and second_number < 1000):
                    return largest_product

        largest_product -= 1
        if largest_product < 10000:
            return False


# Problem 005
def smallestMultiple(n):
    """returns the smalest multiple of all numbers in range from 1 to n"""
    def isPrime(n):
        for i in range(2, int(n)):
            if n % i == 0:
                return False
        return True

    def primeFactors(n):
        """returns list of prime factors of input int input n"""
        prime_factors = []
        next_factor = 2
        while not isPrime(n):
            while n % next_factor == 0:
                prime_factors.append(next_factor)
                n /= next_factor
            else:
                next_factor += 1
                while not isPrime(next_factor):
                    next_factor += 1
        prime_factors.append(int(n))
        return prime_factors

    # store a list of prime factors in separate lists for each number
    list_of_factors_for_each = []
    for i in range(2, n+1):
        list_of_factors_for_each.append(primeFactors(i))

    # use a set to extract unique factors across the entire range
    # we will use these to later get the count in each sublist above of prime factors
    set_of_all_primes = set()
    for i in list_of_factors_for_each:
        for j in i:
            set_of_all_primes.add(j)

    # count frequency of each factor in each sublist above.
    # use factor ^ maximum frequency in determining LCM.
    least_common_multiple_factors = []
    for i in set_of_all_primes:
        current_count_factor = 0
        for j in list_of_factors_for_each:
            if j.count(i) > current_count_factor:
                current_count_factor = j.count(i)
        least_common_multiple_factors.append(i ** current_count_factor)

    smallest_multiple = 1
    for i in least_common_multiple_factors:
        smallest_multiple *= i
    return smallest_multiple


# Problem 006
def foo():
    pass













