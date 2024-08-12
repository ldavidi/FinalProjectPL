concatenate = lambda strings: (lambda result='': [result := result + s + (' ' if i < len(strings) - 1 else '') for i, s in enumerate(strings)][-1])()

print(concatenate(["This", "is", "a", "test","will", "it", "work?"]))  # Output: "This is a test"