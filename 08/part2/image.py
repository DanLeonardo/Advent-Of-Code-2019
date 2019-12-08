input_file = './input.txt'
test1_file = './test1.txt'

width, height = 25, 6

# Read all pixels in a single array
pixels = []
with open(input_file) as file:
    pixels = file.readline()
    pixels = [int(pixel) for pixel in pixels.rstrip('\n')]

num_pixels = width * height
num_layers = int(len(pixels) / num_pixels)

# Break pixels down into layers
layers = []
for layer in range(0,num_layers):
    layers.append([])
    for pixel in range(0,num_pixels):
        layers[layer].append(pixels[num_pixels*layer+pixel])
    # print(layers[layer])

final_image = []
for i in range(0, num_pixels):
    for layer in layers:
        if layer[i] != 2:
            final_image.append(layer[i])
            break

print(final_image)

with open('./message.txt', 'w') as write_file:
    for pixel in final_image:
        write_file.write(str(pixel))
    # for row in range(0,height):
    #     for column in range(0,width):
    #         pixel = final_image[row*width+column]
    #         write_file.write(str(pixel))
    #     write_file.write('\n')
