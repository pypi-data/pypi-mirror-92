from PIL import Image

img = Image.open("images_pixel/codemao.jpg").convert("RGB")
width, height = img.size


def adj_pic(img, r, g, b):
    old = 0
    for y in range(height):
        for x in range(width):
            value = list(img.getpixel((x, y)))
            value[0] += r
            value[1] += g
            value[2] += b
            img.putpixel((x, y), tuple(value))
        process = int((y+1)*100 / height)
        if process != old:
            print(f"图片渲染进度：{process}%")
            old = process
    img.show()


adj_pic(img, 20, 15, 0)
