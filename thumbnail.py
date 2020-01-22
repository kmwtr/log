#! python3

import copy, os, re, PIL.Image
# from PIL import Image

# 0:
# -------------------------------------------------

year = '20'
quarter = 'Q1'
source_image_dir = './img/' + year + '/'
thumbnail_image_dir = './img/tmb/' + year + '/'

print('- source_image_dir: ' + source_image_dir)
print('- thumbnail_image_dir: ' + thumbnail_image_dir)


# 1: リスト作成
# -------------------------------------------------

# ファイルリスト取得
source_image_list = os.listdir(source_image_dir)
thumbnail_image_list =  os.listdir(thumbnail_image_dir)

# jpg,pngのリストを作成
match_extension_regex = re.compile(r'\w+\.jpg|\w+\.png', re.I)
jpg_png_list = match_extension_regex.findall(str(source_image_list))

# jpg,pngかつ128KB以上のリストを作成
large_image_list = list(range(0))
for i in range(len(jpg_png_list)):
    if os.path.getsize(source_image_dir + jpg_png_list[i]) > 128000:
        large_image_list.append(jpg_png_list[i])

# 一旦ファイル名のみ取得
compare_list = list(range(0))
for i in range(len(large_image_list)):
    file_name = large_image_list[i].split('.')
    compare_list.append(file_name[0])

# jpg,png,128KB以上かつサムネイルが未整備のリストを作成
candidate_list = list(range(0))
for i in range(len(compare_list)):
    if not any( s.startswith(r'tmb_' + compare_list[i] + r'.') for s in thumbnail_image_list):
        candidate_list.append(large_image_list[i])

print('- candidate_list: ' + str(candidate_list))


# 3: サムネイル画像作成・保存
# -------------------------------------------------

# 候補リストに基づいて画像を読む
for i in range(len(candidate_list)):
    image_obj = PIL.Image.open(source_image_dir + candidate_list[i])
    image_obj = image_obj.convert('RGB')
    # アスペクト比によって別処理
    pixel_width = image_obj.width
    pixel_height = image_obj.height
    if pixel_width > pixel_height:
        # 横長ならそのままリサイズ
        image_obj.thumbnail((480, 360), PIL.Image.LANCZOS)
    else:
        # 縦長なら正方形にクリッピングしてリサイズ
        image_obj = image_obj.crop((0, (pixel_height - pixel_width)/2, pixel_width, pixel_width + (pixel_height - pixel_width)/2))
        image_obj.thumbnail((360, 360), PIL.Image.LANCZOS)
        
    image_obj.save(thumbnail_image_dir + 'tmb_' + compare_list[i] + '.jpg', quality=100)


# TODO: GIF
# -------------------------------------------------

