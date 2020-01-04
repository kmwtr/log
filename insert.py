#! python3

import os, re

# 0:
# -------------------------------------------------
year = '20'
quarter = 'Q1'
html_path = './html/' + year + quarter + '.html'
img_dir = './img/' + year

# 1: html
# -------------------------------------------------
html_file = open(html_path, 'r', encoding='utf-8')
html_file_content = html_file.read()

"""
match_pattern = r'(\d{6}\w*.\w{3})"'
imagefile_regex = re.compile(match_pattern)

html_mo = imagefile_regex.findall(html_file_content)
"""

# 2: image
# -------------------------------------------------
imagefile_list = os.listdir(img_dir)

# 3: molding
# -------------------------------------------------
"""
html_mo = set(html_mo)
imagefile_list = set(imagefile_list)
add_list = imagefile_list - html_mo

add_list = list(add_list)
"""

imagefile_list.sort(reverse=True)

for i in range(len(imagefile_list)):
    file_name = imagefile_list[i].split('.')
    imagefile_list[i] = r'        <section><p>' + file_name[0] + r'</p><img src=".' + img_dir + r'/' + imagefile_list[i] + r'"></section>'

html_article = '\n'.join(imagefile_list)
html_article += '\n    '

# 4: composit
# -------------------------------------------------
html_regex_A = re.compile(r'<!DOCTYPE html>.*<article class="log_images">\n', re.DOTALL)
html_regex_B = re.compile(r'</article>.*</html>', re.DOTALL)

html_mo_A = html_regex_A.search(html_file_content)
html_mo_B = html_regex_B.search(html_file_content)

updated_html = html_mo_A.group() + html_article + html_mo_B.group()

#print(updated_html)

# 5: 
# -------------------------------------------------

target_file = open(html_path, 'w', encoding='utf-8')

target_file.write(updated_html)
target_file.close()

print('OK.')