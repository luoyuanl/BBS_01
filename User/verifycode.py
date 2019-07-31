from io import BytesIO
from random import randint, sample

from PIL import Image, ImageFont, ImageDraw


class VerifyCode:
    def __init__(self, width=100, height=40, size=4):
        self.width = width
        self.height = height
        self.size = size  # 验证码长度
        self.__code = None  # 保存验证码字符串
        self.pen = None  # 画笔

    @property
    def code(self):  # 获取验证码字符串的方法
        return self.__code

    def output(self):
        # 1 image pen
        im = Image.new('RGB', (self.width, self.height), self.__rand_color(160, 255))
        self.pen = ImageDraw.Draw(im)

        # 2code string
        self.__code = self.rand_string()

        # 3 draw string
        self.__draw_string()
        # 4 point
        self.__disturb_point()
        # 5 line
        self.__draw_line()
        # 6 return图片的二级制
        # im.save('yzm.png','PNG')  #保存图片
        buf = BytesIO()
        im.save(buf, 'PNG')
        res = buf.getvalue()
        buf.close()
        return res

    def __draw_line(self):
        for i in range(5):
            start_point = (randint(1, self.width - 1), randint(1, self.height - 1))
            end_point = (randint(1, self.width - 1), randint(1, self.height - 1))
            self.pen.line([start_point, end_point], fill=self.__rand_color(50, 100))

    def __disturb_point(self):
        for i in range(300):
            x = randint(1, self.width - 1)
            y = randint(1, self.height - 1)
            self.pen.point([(x, y)], fill=self.__rand_color(60, 120))

    def __draw_string(self):
        font1 = ImageFont.truetype('FreeSansBold.ttf', size=20, encoding='utf-8')
        width = (self.width - 20) / self.size
        for i in range(len(self.__code)):
            x = 13 + i * width
            y = randint(5, 20)
            self.pen.text((x, y), self.__code[i], fill='black', font=font1)

    def rand_string(self):
        # 数字验证码
        return str(randint(1000, pow(10, self.size)) - 1)

    def __rand_color(self, low, high):
        return randint(low, high), randint(low, high), randint(low, high)


# if __name__ == "__main__":
#     vc = VerifyCode()
#     vc.output()
#     print(vc.code)
