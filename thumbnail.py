#! python3
import os
import copy
import re
import logging as log
#import tkinter as tk
from PIL import Image

# Debug
# -------------------------------------------------
log.basicConfig(level=log.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s')

"""
# Class
# -------------------------------------------------
class GUIFrame(tk.Frame):
    def __init__(self):
        self.num = 999
"""     

# 0:
# -------------------------------------------------

year = 20
quarter = 2
source_image_dir = './img/' + str(year) + '/'
thumbnail_image_dir = './img/tmb/' + str(year) + '/'
html_dir = './html/' + str(year) + 'Q'+ str(quarter) + '.html'

log.debug('source_image_dir: ' + source_image_dir)
log.debug('thumbnail_image_dir: ' + thumbnail_image_dir)
log.debug('html_dir: ' + html_dir)


# 1: リスト作成
# -------------------------------------------------

# ファイルリスト取得
source_image_list = os.listdir(source_image_dir)
thumbnail_image_list = os.listdir(thumbnail_image_dir)

# jpg,pngのリストを作成
match_extension_regex = re.compile(r'\w+\.jpg|\w+\.png', re.I)
jpg_png_list = match_extension_regex.findall(str(source_image_list))

# jpg,pngのリストから、128KB以上かつ480*360px以上のファイルリストを作成
large_image_list = list(range(0))
for i in range(len(jpg_png_list)):
    if os.path.getsize(source_image_dir + jpg_png_list[i]) > 128000:
        tmp_img_obj = Image.open(source_image_dir + jpg_png_list[i])
        if (tmp_img_obj.width * tmp_img_obj.height) > 172800: # == 480*360
            large_image_list.append(jpg_png_list[i])

# 重量級画像かつサムネイル未整備のリストを作成
candidate_list = list(range(0))
for i in range(len(large_image_list)):
    tmp_name = large_image_list[i].split('.')[0]
    if not any(s.startswith(r'tmb_' + tmp_name) for s in thumbnail_image_list):
        candidate_list.append(large_image_list[i])

log.debug('candidate_list: ' + str(candidate_list))


# 2: サムネイル画像作成・保存
# -------------------------------------------------

# 候補リストに基づいて画像を読む
for i in range(len(candidate_list)):
    image_obj = Image.open(source_image_dir + candidate_list[i])
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
    image_obj.save(thumbnail_image_dir + 'tmb_' + tmp_name + '.jpg', quality=100)
    log.debug('tmp_name: ' + thumbnail_image_dir + 'tmb_' + tmp_name + '.jpg')


# 3: html向けの文字列リストを作成
# -------------------------------------------------

source_image_list.sort(reverse=True)

# このクオーターに属するものを抽出する（ひとまずこれで…
# 普通に算出できるようになったので、以下要修正！！！

if quarter == 1:
    date_code = (str(year) + '01', str(year) + '02', str(year) + '03')
elif quarter == 2:
    date_code = (str(year) + '04', str(year) + '05', str(year) + '06')
elif quarter == 3:
    date_code = (str(year) + '07', str(year) + '08', str(year) + '09')
elif quarter == 4:
    date_code = (str(year) + '10', str(year) + '11', str(year) + '12')

log.debug('date_code: ' + str(date_code))

# 名前リストを作成
image_name_list = list(range(0))
for i in range(len(source_image_list)):
    tmp_file_name = source_image_list[i].split('.')[0]
    if tmp_file_name.startswith(date_code):
        image_name_list.append(tmp_file_name)

log.debug('image_name_list: ' + str(image_name_list))

# サムネイルリストを最新の状態に更新する
thumbnail_image_list = os.listdir(thumbnail_image_dir)

# htmlに入れたい文字列のリストを取得
add_list = list(range(0))
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
        add_list[i] = r'        <section><p>' + image_name_list[i] + r'</p><a href=".' + source_image_dir + source_image_list[i] + r'"><img src=".' + thumbnail_image_dir + add_list[i] + r'"></a></section>'
    else:
        add_list[i] = r'        <section><p>' + image_name_list[i] + r'</p><a href=".' + source_image_dir + source_image_list[i] + r'"><img src=".' + source_image_dir + add_list[i] + r'"></a></section>'

html_article = '\n'.join(add_list)
html_article += '\n    '

log.debug('html_article: ' + str(html_article))


# 5: htmlに反映
# -------------------------------------------------

# htmlファイルの読み込み
html_file = open(html_dir, 'r', encoding='utf-8')
html_content = html_file.read()

#
html_regex_A = re.compile(r'<!DOCTYPE html>.*<article class="log_images">\n', re.DOTALL)
html_regex_B = re.compile(r'</article>.*</html>', re.DOTALL)

html_mo_A = html_regex_A.search(html_content)
html_mo_B = html_regex_B.search(html_content)

updated_html = html_mo_A.group() + html_article + html_mo_B.group()


# 6: html 上書き保存
# -------------------------------------------------

target_file = open(html_dir, 'w', encoding='utf-8')

target_file.write(updated_html)
target_file.close()

log.debug('FINISH')


'''
# GUI test
# -------------------------------------------------

# TKあんまり良くないな…

window = tk.Tk()
window.title("L.A.P. | Log Assets Processor (GUI test)")
window.geometry("482x482")
window.grid_columnconfigure(0, weight=1, pad=16)
window.grid_columnconfigure(1, weight=2, pad=16)
window.grid_rowconfigure(0, pad=8)
window.grid_rowconfigure(1, pad=8)
window.grid_rowconfigure(2, pad=8)
window.grid_rowconfigure(3, pad=8)
window.grid_rowconfigure(4, pad=8)
window.grid_rowconfigure(5, pad=8)
window.grid_rowconfigure(6, pad=8)

# -----------------------
label_year = tk.Label(text=str(year))
label_year.grid(row=0, column=0)

entry_year_target = tk.Entry()
entry_year_target.insert(tk.END, str(year))
entry_year_target.grid(row=0, column=1)

# -----------------------
label_year = tk.Label(text=str(quarter))
label_year.grid(row=1, column=0)

entry_year_target = tk.Entry()
entry_year_target.insert(tk.END, str(quarter))
entry_year_target.grid(row=1, column=1)

# -----------------------
tk.Label(text='Source Image DIR:').grid(row=2, column=0)
tk.Label(text=source_image_dir).grid(row=2, column=1)

tk.Label(text='Thumbnail Image DIR:').grid(row=3, column=0)
tk.Label(text=thumbnail_image_dir).grid(row=3, column=1)

tk.Label(text='Target HTML DIR:').grid(row=4, column=0)
tk.Label(text=html_dir).grid(row=4, column=1)

tk.Label(text='Candidate Image List:').grid(row=5, column=0)
tk_candidate_image_list = tk.Text(height=str(len(candidate_list)), width=30, wrap=tk.CHAR)
tk_candidate_image_list.insert(tk.END, '\n'.join(candidate_list))
tk_candidate_image_list.grid(row=5, column=1)

# -----------------------
tk.Label(text='Update').grid(row=6, column=0)
tk.Button(text="GO").grid(ipadx=50, row=6, column=1)

# -----------------------
window.mainloop()

# TODO: GIF
# -------------------------------------------------

# gifのリストを作成
match_extension_regex = re.compile(r'\w+\.gif', re.I)
gif_list = match_extension_regex.findall(str(source_image_list))

# gifかつ256KB以上のリストを作成
large_gif_list = list(range(0))
for i in range(len(gif_list)):
    if os.path.getsize(source_image_dir + gif_list[i]) > 512000:
        large_gif_list.append(gif_list[i])

print('- large_gif_list: ' + str(large_gif_list))
'''