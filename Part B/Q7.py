def generate_values():
    print('Generating values...')
    yield 1
    yield 2
    yield 3

def square(x):
    print(f'Squaring {x}')
    return x * x
print('Eager evaluation:')
values = list(generate_values())
squared_values = [square(x) for x in values]
print(squared_values)
print('\nLazy evaluation:')
squared_values = [square(x) for x in generate_values()]
print(squared_values)
# Lazy Evaluation processes each piece of data as soon as it's generated, which can be more efficient for large data sets or streams of data.
# In this program it is deomonstrated by only generating the values when preforming the square function as apposed to in "Eager evaluation:" where they are stored in a seperate variable ahead of time