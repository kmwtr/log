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
thumbnail_image_list = os.listdir(thumbnail_image_dir)

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

# 候補のファイル名のみのリストを作成
candidate_name_list = list(range(0))
for i in range(len(candidate_list)):
    file_name = candidate_list[i].split('.')
    candidate_name_list.append(file_name[0])


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
        
    image_obj.save(thumbnail_image_dir + 'tmb_' + candidate_name_list[i] + '.jpg', quality=100)


# TODO: GIF
# -------------------------------------------------


# 4: html向けの文字列リストを作成
# -------------------------------------------------

source_image_list.sort(reverse=True)

# すべての画像についてファイル名のみ取得
all_compare_list = list(range(0))
for i in range(len(source_image_list)):
    file_name = source_image_list[i].split('.')
    all_compare_list.append(file_name[0])

# サムネイルリストを最新の状態にする
thumbnail_image_list = os.listdir(thumbnail_image_dir)

# htmlに入れたい文字列のリストを取得
add_list = list(range(0))
for i in range(len(all_compare_list)):
    if any( s.startswith(r'tmb_' + all_compare_list[i] + r'.') for s in thumbnail_image_list):
        for j in range(len(thumbnail_image_list)):
            if thumbnail_image_list[j].startswith(r'tmb_' + all_compare_list[i] + r'.'):
                add_list.append(thumbnail_image_list[j])
    else:
        add_list.append(source_image_list[i])


# 4: html形式の文字列に成形
# -------------------------------------------------

# ひどいけどここまできたからとりあえずやっとく。後で全体直す
for i in range(len(all_compare_list)):
    if add_list[i].startswith(r'tmb_'):
        add_list[i] = r'        <section><p>' + all_compare_list[i] + r'</p><a href=".' + source_image_dir + source_image_list[i] + r'"><img src=".' + thumbnail_image_dir + add_list[i] + r'"></a></section>'
    else:
        add_list[i] = r'        <section><p>' + all_compare_list[i] + r'</p><a href=".' + source_image_dir + source_image_list[i] + r'"><img src=".' + source_image_dir + add_list[i] + r'"></a></section>'

html_article = '\n'.join(add_list)
html_article += '\n    '

print(html_article)

# 4: htmlに反映
# -------------------------------------------------

html_dir = './html/' + year + quarter + '.html'

# htmlファイルの読み込み
html_file = open(html_dir, 'r', encoding='utf-8')
html_content = html_file.read()

#
html_regex_A = re.compile(r'<!DOCTYPE html>.*<article class="log_images">\n', re.DOTALL)
html_regex_B = re.compile(r'</article>.*</html>', re.DOTALL)

html_mo_A = html_regex_A.search(html_content)
html_mo_B = html_regex_B.search(html_content)

updated_html = html_mo_A.group() + html_article + html_mo_B.group()


# 5: html 上書き保存
# -------------------------------------------------

target_file = open(html_dir, 'w', encoding='utf-8')

target_file.write(updated_html)
target_file.close()

print('OK.')
