def turning_machienes(string):
    parts = string.strip().split('+')
    total_ones = len(parts[0]) + len(parts[1])
    return '1' * total_ones

input_tape = "1+11"
output = turning_machienes(input_tape)
print(output)
