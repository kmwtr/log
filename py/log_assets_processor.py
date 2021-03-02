#! python3
import os
import copy
import re
import logging as log
from PIL import Image
import yaml

import debug_config

from load_settings import load_settings
from image_list import image_list
from make_thumbnail import make_image_thumbnail, make_gif_thumbnail

# -------------------------------------------------

settings = load_settings()
image_lists = image_list(settings)

make_image_thumbnail(image_lists, settings)
make_gif_thumbnail(image_lists, settings)


# 以下未整理

# 3: html向けの文字列リストを作成
# -------------------------------------------------

image_lists['source_image_list'].sort(reverse=True)

# このクオーターに属するものを抽出する（ひとまずこれで…
base_num = int((settings['quarter']-1) * 3)
date_code = (
    str(settings['year']) + str(base_num + 1).zfill(2), 
    str(settings['year']) + str(base_num + 2).zfill(2), 
    str(settings['year']) + str(base_num + 3).zfill(2)
    )

log.debug('date_code: ' + str(date_code))

# 今回のクオーター内の名前リストを作成
image_name_list = [] # 名前のみ
this_quarter_img_file_list = [] # 拡張子含むファイル名
for i in range(len(image_lists['source_image_list'])):
    tmp_file_name = image_lists['source_image_list'][i].split('.')[0]
    if tmp_file_name.startswith(date_code):
        image_name_list.append(tmp_file_name)
        this_quarter_img_file_list.append(image_lists['source_image_list'][i])

log.debug('image_name_list: ' + str(image_name_list))
log.debug('this_quarter_img_file_list: ' + str(this_quarter_img_file_list))

# サムネイルリストを最新の状態に更新
image_lists['thumbnail_image_list'] = os.listdir(settings['tmb_img_dir'])

# htmlに入れたい文字列のリストを取得（差分ではなく毎回まとめて成形する）
add_list = []
for i in range(len(image_name_list)):
    if any( s.startswith(r'tmb_' + image_name_list[i]) for s in image_lists['thumbnail_image_list']):
        # とりあえず簡易的にGIFと突き合わせる
        if 'tmb_' + image_name_list[i] + '.gif' in image_lists['thumbnail_image_list']:
            add_list.append(r'tmb_' + image_name_list[i] + r'.gif')
        else:
            add_list.append(r'tmb_' + image_name_list[i] + r'.jpg')
    else:
        add_list.append(this_quarter_img_file_list[i])

log.debug('add_list: ' + str(add_list))

# ここまで問題ない気がするが…。

# 4: html形式の文字列に成形
# -------------------------------------------------

# ひどい　後で直す
for i in range(len(image_name_list)):
    if add_list[i].startswith(r'tmb_'):
        add_list[i] = r'            <section><p>' + image_name_list[i] + r'</p><a href="' + settings['src_img_dir'].replace(settings['base_dir'], '..') + this_quarter_img_file_list[i] + r'"><img src="' + settings['tmb_img_dir'].replace(settings['base_dir'], '..') + add_list[i] + r'"></a></section>'
    else:
        add_list[i] = r'            <section><p>' + image_name_list[i] + r'</p><a href="' + settings['src_img_dir'].replace(settings['base_dir'], '..') + this_quarter_img_file_list[i] + r'"><img src="' + settings['src_img_dir'].replace(settings['base_dir'], '..') + add_list[i] + r'"></a></section>'

html_article = '\n'.join(add_list)
html_article += '\n        '

log.debug('html_article: \n' + str(html_article))


# 5: htmlに反映
# -------------------------------------------------

# htmlファイルの読み込み
html_file = open(settings['html_dir'], 'r', encoding='utf-8')
html_content = html_file.read()

#
html_regex_A = re.compile(r'<!DOCTYPE html>.*<section id="log_images">\n', re.DOTALL)
html_regex_B = re.compile(r'</section>\n    </article>.*</html>', re.DOTALL)

html_mo_A = html_regex_A.search(html_content)
html_mo_B = html_regex_B.search(html_content)

updated_html = html_mo_A.group() + html_article + html_mo_B.group()


# 6: html 上書き保存
# -------------------------------------------------

target_file = open(settings['html_dir'], 'w', encoding='utf-8')

target_file.write(updated_html)
target_file.close()

log.debug('FINISH')

os.system('PAUSE')

# 画像の命名規則を間違うと色々やばいことが起こる