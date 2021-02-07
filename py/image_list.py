#! python3
import os
import re
import logging as log

import debug_config
from load_settings import load_settings

def image_list(dir_settings: dict) -> dict:
    log.debug('-> image_list()')

    # ファイルリスト取得
    source_image_list       = os.listdir(dir_settings['src_img_dir'])
    thumbnail_image_list    = os.listdir(dir_settings['tmb_img_dir'])

    log.debug('source_image_list:    ' + str(source_image_list))
    log.debug('thumbnail_image_list: ' + str(thumbnail_image_list))

    # とりあえず
    for i in range(len(source_image_list)):
        if ' ' in source_image_list[i]:
            log.error('画像ファイル名にスペースが含まれています。ルール通り命名されたファイルしか処理できません。: ' + source_image_list[i])
            return None

    # jpg, png のリストを作成
    match_extension_regex = re.compile(r'\w+\.jpg|\w+\.png', re.I)
    jpg_png_list = match_extension_regex.findall(str(source_image_list))
    
    # gif のリストを作成
    match_extension_regex = re.compile(r'\w+\.gif', re.I)
    gif_list = match_extension_regex.findall(str(source_image_list))

    # 大きい jpg, png, gif のリストを作成
    img_threshold_byte = 128000 # 閾値 for jpg, png
    gif_threshold_byte = 512000 # 閾値 for gif
    large_image_list = []   # 大きい jpg, png のリスト
    large_gif_list = []     # 大きい gif のリスト

    for i in range(len(jpg_png_list)):
        if os.path.getsize(dir_settings['src_img_dir'] + jpg_png_list[i]) > img_threshold_byte:
            large_image_list.append(jpg_png_list[i])

    for i in range(len(gif_list)):
        if os.path.getsize(dir_settings['src_img_dir'] + gif_list[i]) > gif_threshold_byte:
            large_gif_list.append(gif_list[i])

    log.debug('large_image_list:     ' + str(large_image_list))
    log.debug('large_gif_list:       ' + str(large_gif_list))

    # サムネイルを持たない大きい jpg, png リスト
    candidate_img_list = []
    for i in range(len(large_image_list)):
        tmp_name = large_image_list[i].split('.')[0]
        if not any(s.startswith(r'tmb_' + tmp_name) for s in thumbnail_image_list):
            candidate_img_list.append(large_image_list[i])

    log.debug('candidate_img_list:   ' + str(candidate_img_list))

    # サムネイルを持たない大きい gif リスト
    candidate_gif_list = []
    for i in range(len(large_gif_list)):
        tmp_name = large_gif_list[i].split('.')[0]
        if not any(s.startswith(r'tmb_' + tmp_name) for s in thumbnail_image_list):
            candidate_gif_list.append(large_gif_list[i])

    log.debug('candidate_gif_list:   ' + str(candidate_gif_list))

    image_list_dict = {'source_image_list': source_image_list, 'thumbnail_image_list': thumbnail_image_list, 'large_image_list':large_image_list, 'large_gif_list': large_gif_list, 'candidate_img_list': candidate_img_list, 'candidate_gif_list': candidate_gif_list}
    return image_list_dict


# -------------------------------------------------

if __name__ == '__main__':
    image_list(load_settings())
    #os.system('PAUSE')