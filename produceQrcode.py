import qrcode
from PIL import Image

# 创建QR码对象
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# 输入要生成QR码的数据
data = "Hello, QR Code!"

# 添加数据到QR码
qr.add_data(data)
qr.make(fit=True)

# 创建一个PIL图像对象
img = qr.make_image(fill_color="black", back_color="white")

# 将图像转换为黑白图像（1位像素）
img = img.convert("1")

# 获取图像的像素数据
img_array = list(img.getdata())

# 将图像数据转换为二维数组
width, height = img.size
array_2d = [img_array[i * width:(i + 1) * width] for i in range(height)]

print(array_2d)
