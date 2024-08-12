prime_desc = lambda nums: sorted([x for x in nums if x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1))], reverse=True)
nums = [10, 7, 4, 3, 11, 13, 17, 18]
print(prime_desc(nums))