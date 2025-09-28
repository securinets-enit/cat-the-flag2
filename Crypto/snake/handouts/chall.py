import math
from PIL import Image, ImageDraw

message = 'SecurinetsENIT{test_flag}'
bits = ''.join(format(ord(char), '08b') for char in message)
num_bits = len(bits)
if num_bits == 0:
    exit(1)
n = math.ceil(math.sqrt(num_bits))
grid = [['0'] * n for _ in range(n)]
bit_index = 0
for row in range(n):
    if row % 2 == 0:
        for col in range(n):
            if bit_index < num_bits:
                grid[row][col] = bits[bit_index]
                bit_index += 1
    else:
        for col in range(n - 1, -1, -1):
            if bit_index < num_bits:
                grid[row][col] = bits[bit_index]
                bit_index += 1

cell_size = 10
img_size = n * cell_size
img = Image.new('1', (img_size, img_size), 1)
draw = ImageDraw.Draw(img)

for row in range(n):
    for col in range(n):
        if grid[row][col] == '1':
            x0 = col * cell_size
            y0 = row * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            draw.rectangle([x0, y0, x1, y1], fill=0)

img.save("maze.png")

