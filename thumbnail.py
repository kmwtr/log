#! python3

import copy, os, re, PIL.Image
# from PIL import Image

# 0:
# -------------------------------------------------

year = '20'
quarter = 'Q1'
source_image_dir = './img/' + year + '/'
thumbnail_image_dir = './img/tmb/' + year + '/'

print('source_image_dir: ' + source_image_dir)
print('thumbnail_image_dir: ' + thumbnail_image_dir + '\n')


# 1: ファイルから集合を作成する
# -------------------------------------------------

# ファイルリスト取得
source_image_list =     os.listdir(source_image_dir)
thumbnail_image_list =  os.listdir(thumbnail_image_dir)

print('source_image_list:\n' + str(source_image_list) + '\n')
print('thumbnail_image_list:\n' + str(thumbnail_image_list) + '\n')

# ファイル名リスト取得
source_name_list =      copy.copy(source_image_list)
thumbnail_name_list =   copy.copy(thumbnail_image_list)

for i in range(len(source_name_list)):
    file_name = source_name_list[i].split('.')
    source_name_list[i] = file_name[0]

for i in range(len(thumbnail_name_list)):
    file_name = thumbnail_name_list[i].split('.')
    thumbnail_name_list[i] = file_name[0].lstrip('tmb_') # サムネイルからプレフィックスを除去（雑）

# 集合を作成
source_s =      set(source_name_list)               # 元画像
thumbnail_s =   set(thumbnail_name_list)            # サムネイル画像
difference_s =  source_s.difference(thumbnail_s)    # 差集合（サムネイル未作成の画像）


# 2: 処理する画像をファイルサイズと拡張子から決定する
# -------------------------------------------------

# jpgとpngのみ取得
match_extension_pattern = r'\w+\.jpg|\w+\.png'
match_extension_regex = re.compile(match_extension_pattern, re.I)
jpg_png_obj = match_extension_regex.findall(str(source_image_list))

# かつファイルサイズが128KB以上あるもの
large_obj = list(range(0))
for i in range(len(jpg_png_obj)):
    if os.path.getsize(source_image_dir + jpg_png_obj[i]) > 128000:
        large_obj.append(jpg_png_obj[i])

# ファイル名のみ抽出
for i in range(len(large_obj)):
    file_name = large_obj[i].split('.')
    large_obj[i] = file_name[0]

# 集合を作成
large_s = set(large_obj)
target_s = large_s.intersection(difference_s) # 積集合(jpg,png,128KB以上,でサムネイル未作成のもの)

# 処理したいファイル名リスト
target_list = list(target_s)
target_list.sort(reverse=False)

print('target_list: ' + str(target_list) + '\n')

# 3: サムネイル画像作成・保存
# -------------------------------------------------

for i in range(len(target_list)):
    #image_source = PIL.Image.open()


# TODO: GIF
# -------------------------------------------------
