from PIL import Image
import os,re

# 打开一个jpg图像文件，注意是当前路径:
im = Image.open('test.jpg')
# im.show()
# 获得图像尺寸:
w, h = im.size
print('Original image size: %sx%s' % (w, h))
# 缩放到50%:
im.thumbnail((w//2, h//2))
print('Resize image to: %sx%s' % (w//2, h//2))
# 把缩放后的图像用jpeg格式保存:
im.save('thumbnail.jpg', 'jpeg')

def makeDictory(path):
    paths = os.path.split(path)
    pa = ''
    for dic in paths:
        pa = os.path.join(pa, dic)
        if(not os.path.exists(pa)):
            os.makedirs(dic)


def resizeimg(path,dpath,width,height,threshold,prefix):
    # grey_im.show()
    makeDictory(dpath)
    for file in os.listdir(path):
        if not os.path.isdir(os.path.join(path,file)):
            try:
                print(file)
                im = Image.open(os.path.join(path,file))
                file=re.sub(r"(\d+)\.",lambda x:f"{x.group(1)}_{prefix}.",file)
                # im.show()
                w, h = im.size
                grey_im = im
                grey_im = grey_im.resize((width,height))
                # grey_im.save(os.path.join('book/ocrimg3/',file))
                grey_im = grey_im.convert('L')
                # grey_im.save(os.path.join('book/ocrimg4/',file))
                threshold = threshold
                table = []
                for i in range(256):
                    if  i <= threshold:
                        table.append(1)
                    else:
                        table.append(0)
                # print(table)
                # 图片二值化
                photo = grey_im.point(table, '1')
                photo.save(os.path.join(dpath,file))
            except Exception as e:
                print(e)
                continue

if __name__ == '__main__':
    # resizeimg(50,50,87)
    # resizeimg(45,45,85)
    # resizeimg(30,30,85)
    for i in range(90,98):
        # resizeimg(30,30,i,i)
        # resizeimg(25,25,i,i)
        # resizeimg(20,25,i,i)
        for j in range(35,75,5):
            for k in range(35,75,5):
                resizeimg("book/ocrimg2/ocrtrue/",'book/ocrimg5/ocr/',j,k,i,f"{j}{k}{i}")

