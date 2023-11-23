import qrcode
import cv2
from collections import deque
import random
from PIL import Image
import numpy as np



def getQrCode(d, name, num):
    data = d
    bs = 1
    bd = 1

    qr = qrcode.QRCode(
        version=None,  
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=bs,
        border=bd,
    )
    qr.add_data(data)
    qr.make(fit=True)
    # 獲得 QR Code 二維陣列
    matrix = qr.get_matrix()
    def is_valid(x, y):
        return 0 <= x < len(matrix) and 0 <= y < len(matrix[0])
    
    points = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # 上, 下, 左, 右
    queue = deque()
    queue.append((bd, bd))
    queue.append((bd, len(matrix) - 1 - bd))
    queue.append((len(matrix[0]) - 1 - bd, bd))
    # 測試中心點變白
    # 左上角中心點
    queue.append((4, 4))
    # 左下角
    queue.append((len(matrix) - 4 - 1, 4))
    # 右上角
    queue.append((4, len(matrix) - 4 - 1))
    while queue:
        x, y = queue.popleft()
        
        
        if matrix[x][y] == 1:
            matrix[x][y] = 0
            points.append((x, y))
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if is_valid(new_x, new_y) and matrix[new_x][new_y] == 1:
                    queue.append((new_x, new_y))
    
    num_to_remove = int(num * len(points))
    items_to_remove = random.sample(points, num_to_remove)
    points = [item for item in points if item not in items_to_remove]

    for x, y in points:
        matrix[x][y] = 1
    
    matrix = [[int(value) for value in row] for row in matrix]

    # 定位點 up down
    matrix[bd][bd + 3] = 1
    matrix[bd][len(matrix) - bd - 3 - 1] = 1
    matrix[bd + 6][bd + 3] = 1
    matrix[bd + 6][len(matrix) - bd - 3 - 1] = 1
    matrix[len(matrix) - 1 - bd][bd + 3] = 1
    matrix[len(matrix) - 1 - bd - 6][bd + 3] = 1

    # 定位點 left right
    matrix[bd + 3][bd] = 1
    matrix[bd + 3][bd + 6] = 1
    matrix[len(matrix) - bd - 3 - 1][bd] = 1
    matrix[len(matrix) - bd - 3 - 1][bd + 6] = 1
    matrix[bd + 3][len(matrix) - bd - 1] = 1
    matrix[bd + 3][len(matrix) - bd - 6 - 1] = 1

    
    
    # 測試中心點變白
    # 左上角中心點
    queue.append((4, 4))
    # 左下角
    queue.append((len(matrix) - 4 - 1, 4))
    # 右上角
    queue.append((4, len(matrix) - 4 - 1))
    # while queue:
    #     x, y = queue.popleft()
        
        
    #     if matrix[x][y] == 1:
    #         matrix[x][y] = 0
    #         points.append((x, y))
    #         for dx, dy in directions:
    #             new_x, new_y = x + dx, y + dy
    #             if is_valid(new_x, new_y) and matrix[new_x][new_y] == 1:
    #                 queue.append((new_x, new_y))
    
    queue.append((4, 4))
    # 左下角
    queue.append((len(matrix) - 4 - 1, 4))
    # 右上角
    queue.append((4, len(matrix) - 4 - 1))
    while queue:
        x, y = queue.popleft()
        matrix[x][y] = 1
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            matrix[new_x][new_y] = 1
    
    t = np.array(matrix)
    t = np.where(t > 0, 0, 255)
    t = t.astype(np.uint8)
    img = Image.fromarray(t)
    img = img.resize((len(t) * 50, len(t) * 50), Image.NEAREST)

    img.save(name)

    return matrix




def makeCornerImage(input_path, save_path):
    # corner 為圓角弧度，越大越圓
    img = cv2.imread(input_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(50, 50))

    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    o_to_closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    c_to_opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
    cv2.imwrite(save_path, o_to_closing)


photo_name = "random80.png"

if __name__ == '__main__':
    getQrCode("https://reurl.cc/dmOgE2", photo_name, 0.8)
    makeCornerImage(photo_name, photo_name)
