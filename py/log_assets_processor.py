#! python3
import os
import copy
import re
import logging as log
from PIL import Image
import yaml

# Debug Setting
# -------------------------------------------------

log.basicConfig(level=log.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s')

# 0: 設定のロード
# -------------------------------------------------

file = open("lap_settings.yaml", "r", encoding='utf-8')
data = yaml.load(file)

year        = data["Year"]
quarter     = data["Quarter"]

base_dir    = str(data["Base DIR"])
src_img_dir = base_dir + str(data["Source Image DIR"]) + '/' + str(year) + '/'
tmb_img_dir = base_dir + str(data["Thumbnail Image DIR"]) + '/' + str(year) + '/'
html_dir    = base_dir + str(data["Target HTML DIR"]) + '/' + str(year) + 'Q'+ str(quarter) + '.html'

log.debug('base_dir: ' + base_dir)
log.debug('src_img_dir: ' + src_img_dir)
log.debug('tmb_img_dir: ' + tmb_img_dir)
log.debug('html_dir:    ' + html_dir)

# 1: リスト作成
# -------------------------------------------------

# ファイルリスト取得
source_image_list       = os.listdir(src_img_dir)
thumbnail_image_list    = os.listdir(tmb_img_dir)

# jpg, png のリストを作成
match_extension_regex = re.compile(r'\w+\.jpg|\w+\.png', re.I)
jpg_png_list = match_extension_regex.findall(str(source_image_list))

# jpg, png のリストから、128KB以上のファイルリストを作成
large_image_list = []
for i in range(len(jpg_png_list)):
    if os.path.getsize(src_img_dir + jpg_png_list[i]) > 128000:
        large_image_list.append(jpg_png_list[i])

# 重量級画像かつサムネイル未整備のリストを作成
candidate_list = []
for i in range(len(large_image_list)):
    tmp_name = large_image_list[i].split('.')[0]
    if not any(s.startswith(r'tmb_' + tmp_name) for s in thumbnail_image_list):
        candidate_list.append(large_image_list[i])

log.debug('candidate_list: ' + str(candidate_list))

# 2: サムネイル画像作成・保存
# -------------------------------------------------

# 候補リストに基づいて画像を読む
for i in range(len(candidate_list)):
    image_obj = Image.open(src_img_dir + candidate_list[i])
    image_obj = image_obj.convert('RGB') # 必要???
    # アスペクト比によって別処理
    pixel_width = image_obj.width
    pixel_height = image_obj.height
    if pixel_width > pixel_height:
        # 横長ならそのままリサイズ
        image_obj.thumbnail((480, 360), Image.LANCZOS)
    else:
        # 縦長なら正方形にクリッピングしてリサイズ
        image_obj = image_obj.crop((0, (pixel_height - pixel_width)/2, pixel_width, pixel_width + (pixel_height - pixel_width)/2))
        image_obj.thumbnail((360, 360), Image.LANCZOS)
    
    tmp_name = candidate_list[i].split('.')[0]
    image_obj.save(tmb_img_dir + 'tmb_' + tmp_name + '.jpg', quality=95)
    log.debug('saved_tmb: ' + tmb_img_dir + 'tmb_' + tmp_name + '.jpg')


# 3: html向けの文字列リストを作成
# -------------------------------------------------

source_image_list.sort(reverse=True)

# このクオーターに属するものを抽出する（ひとまずこれで…

base_num = int((quarter-1) * 3)
date_code = (
    str(year) + str(base_num + 1).zfill(2), 
    str(year) + str(base_num + 2).zfill(2), 
    str(year) + str(base_num + 3).zfill(2)
    )

log.debug('date_code: ' + str(date_code))

# 名前リストを作成
image_name_list = []
for i in range(len(source_image_list)):
    tmp_file_name = source_image_list[i].split('.')[0]
    if tmp_file_name.startswith(date_code):
        image_name_list.append(tmp_file_name)

log.debug('image_name_list: ' + str(image_name_list))

# サムネイルリストを最新の状態に更新
thumbnail_image_list = os.listdir(tmb_img_dir)

# htmlに入れたい文字列のリストを取得（差分ではなく毎回まとめて成形する）
add_list = []
for i in range(len(image_name_list)):
    if any( s.startswith(r'tmb_' + image_name_list[i]) for s in thumbnail_image_list):
        add_list.append(r'tmb_' + image_name_list[i] + r'.jpg')
    else:
        add_list.append(source_image_list[i])

log.debug('add_list: ' + str(add_list))


# 4: html形式の文字列に成形
# -------------------------------------------------

# ひどい　後で直す
for i in range(len(image_name_list)):
    if add_list[i].startswith(r'tmb_'):
        add_list[i] = r'            <section><p>' + image_name_list[i] + r'</p><a href="' + src_img_dir.replace(base_dir, '..') + source_image_list[i] + r'"><img src="' + tmb_img_dir.replace(base_dir, '..') + add_list[i] + r'"></a></section>'
    else:
        add_list[i] = r'            <section><p>' + image_name_list[i] + r'</p><a href="' + src_img_dir.replace(base_dir, '..') + source_image_list[i] + r'"><img src="' + src_img_dir.replace(base_dir, '..') + add_list[i] + r'"></a></section>'

html_article = '\n'.join(add_list)
html_article += '\n        '

log.debug('html_article: \n' + str(html_article))


# 5: htmlに反映
# -------------------------------------------------

# htmlファイルの読み込み
html_file = open(html_dir, 'r', encoding='utf-8')
html_content = html_file.read()

#
html_regex_A = re.compile(r'<!DOCTYPE html>.*<article class="log_images">\n', re.DOTALL)
html_regex_B = re.compile(r'</article class="log_images">.*</html>', re.DOTALL)

html_mo_A = html_regex_A.search(html_content)
html_mo_B = html_regex_B.search(html_content)

updated_html = html_mo_A.group() + html_article + html_mo_B.group()


# 6: html 上書き保存
# -------------------------------------------------

target_file = open(html_dir, 'w', encoding='utf-8')

target_file.write(updated_html)
target_file.close()

log.debug('FINISH')


# 画像の命名規則を間違うと色々やばいことが起こる