from functools import reduce

count_palindromes = lambda lists: list(map(lambda sublist: len(list(filter(lambda s: s == s[::-1], sublist))), lists))
lists_of_strings = [["level", "test", "madam"], ["not", "a", "palindrome"], ["wow", "civic", "noon"]]
result = count_palindromes(lists_of_strings)
print(result)  # Output: [2, 0, 3]