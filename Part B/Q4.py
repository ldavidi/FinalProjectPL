cumulative_operation = lambda operation: lambda sequence: sequence[0] if len(sequence) == 1 else operation(sequence[0], cumulative_operation(operation)(sequence[1:]))
factorial = lambda n: cumulative_operation(lambda x, y: x * y)(list(range(1, n + 1)))

# Example usage:
print(factorial(5))  # Output: 120
exponentiation = lambda base, exp: cumulative_operation(lambda x, y: x * y)([base] * exp)

# Example usage:
print(exponentiation(2, 3))  # Output: 8