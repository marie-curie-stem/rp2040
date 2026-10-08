import math, time
last = 10000
found = 4             # we start from 11, know 2, 3, 5, 7
def is_prime(number):
    flag_prime = 1
    for divider in range(3, int(math.sqrt(number))+1, 2):
        if number % divider == 0:
            flag_prime = 0
            break
    return flag_prime
if __name__ == "__main__":
    print(f"Prime numbers to {last}")
    start = time.monotonic()
    for number in range(11, last, 2):
        found += is_prime(number)
    end = time.monotonic()
    print(f"This took: {(end - start)} seconds.")
    print(f"I found {found} prime numbers.")
