input_file = './input.txt'
test1_file = './test1.txt'

width, height = 25, 6

pixels = []
with open(input_file) as file:
    pixels = file.readline()
    pixels = [int(pixel) for pixel in pixels.rstrip('\n')]

num_pixels = width * height
num_layers = int(len(pixels) / num_pixels)

layers = []
for layer in range(0,num_layers):
    layers.append([])
    for pixel in range(0,num_pixels):
        layers[layer].append(pixels[num_pixels*layer+pixel])

fewest_0 = -1
fewest_0_layer = -1

for layer in layers:
    num_0 = 0
    for pixel in layer:
        if pixel == 0:
            num_0 += 1

    if fewest_0 == -1 or num_0 < fewest_0:
        fewest_0 = num_0
        fewest_0_layer = layer

num_1 = 0
num_2 = 0
for pixel in fewest_0_layer:
    if pixel == 1:
        num_1 += 1
    elif pixel == 2:
        num_2 += 1

print(num_1 * num_2)
