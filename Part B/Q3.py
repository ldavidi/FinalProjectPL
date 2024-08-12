cumulative_sum_squares = lambda lists: list(
    map(
        lambda sublist: (  # First lambda: operates on each sublist
            lambda evens: sum(  # Second lambda: calculates the sum of squares
                map(
                    lambda x: x ** 2,  # Third lambda: squares each even number
                    evens
                )
            )
        )(
            list(  # Fourth lambda: filters out even numbers
                filter(
                    lambda x: x % 2 == 0,  # Fifth lambda: checks if the number is even
                    sublist
                )
            )
        ),
        lists
    )
)

# Example usage:
lists_of_numbers = [[1, 2, 3], [4, 5, 6], [7, 8, 9, 10]]
result = cumulative_sum_squares(lists_of_numbers)
print(result)  # Output: [4, 52, 164]
