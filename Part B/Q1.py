fibonacci = lambda n: (lambda f: [f(f, i) for i in range(n)])(lambda self, x, a=0, b=1: a if x == 0 else b if x == 1 else self(self, x - 1, b, a + b))

# Generate the first 10 Fibonacci numbers
print(fibonacci(20))