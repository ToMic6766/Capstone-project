from PIL import Image
from io import BytesIO
import glob
import os

# 현재 경로와 저장 경로를 설정
path = os.path.dirname(os.path.realpath(__file__)) # 현재 경로
save_path = "./reducing_images" # 저장 경로
os.chdir(path)
print("path is : " + path) # 경로 확인용 출력문

#save 경로에 있는 모든 파일을 삭제한다.
[os.remove(f) for f in glob.glob(save_path + "*jpg")]

# 배열 선언
image_list_png = []
image_list_jpg = []

# png 파일 불러오기 + 모든 jpg 파일 삭제
read_files_png = glob.glob("./images/*.png") # 해당 폴더에 있는 모든 png 사진들을 불러온다.
read_files_png.sort()
print(read_files_png) 
print(len(read_files_png))

# png 파일들명 추출
image_list = os.listdir("./images")
image_list.sort()
print(image_list)
print(len(image_list))

search = ".png"
for i, word in enumerate(image_list):
    if search in word:
        image_list_png.append(word.strip(search))

search = ".kpg"
print(image_list_png)
print(len(image_list_png))
print(image_list)
print(len(image_list))

#png to jpg
cnt2 = 0
for f in read_files_png:
    img = Image.open(f).convert("RGB")
    img.save("./images" + image_list_png[cnt2] + ".jpg", "jpeg")
    cnt2 += 1

# jpg 파일 resizing
read_files_jpg = glob.glob("./images/*.jpg")
read_files_jpg.sort()

# jpg 파일명 추출
image_list = os.listdir("./images")
image_list.sort()
print(image_list)
print(len(image_list))

for i, word in enumerate(image_list):
    if search in word:
        image_list_jpg.append(word.strip(search))
print(image_list_jpg)
print(len(image_list_jpg))

cnt = 0

for f in read_files_jpg:
    print(f)
    img = Image.open(f)
    buffer = BytesIO()
    img.save(buffer, "jpeg", quality = 70)
    buffer.seek(0)
    with open(save_path + image_list_jpg[cnt] + "_resize.jpg", "wb") as nfile:
        nfile.write(buffer.getvalue())
        cnt += 1
