from PIL import Image

def image_to_matrix(image_path):
    img = Image.open(image_path).convert('L')  # 将图像转换为灰度
    width, height = img.size
    matrix = []

    for y in range(height):
        row = []
        for x in range(width):
            pixel = img.getpixel((x, y))
            if pixel == 255:  # 白色像素
                row.append(0)  # 可通行
            else:  # 黑色像素
                row.append(1)  # 障碍物
        matrix.append(row)

    return matrix

# 使用示例
image_path = 'map.png'
matrix = image_to_matrix(image_path)
