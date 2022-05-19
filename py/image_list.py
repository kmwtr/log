#! python3
import os
import re
import logging as log
from PIL import Image

import debug_config
from load_settings import load_settings

# --------------------------------------------------------------------

def file_list_maker(file_extension: str, source_image_list: list) -> list:
    log.debug('-> file_list_maker()')

    match_extension_regex = re.compile(file_extension, re.I)
    return match_extension_regex.findall(str(source_image_list))

def large_file_searcher(file_list: list, threshold_byte: int, dir_settings: dict, resolution_threshold: int) -> list:
    log.debug('-> large_file_searcher()')

    large_file_list = []   # 大きい jpg, png のリスト

    for i in range(len(file_list)):
        if os.path.getsize(dir_settings['src_img_dir'] + file_list[i]) > threshold_byte:
            large_file_list.append(file_list[i])
        elif resolution_threshold != 0:
            # resolution_threshold が有効数字であれば解像度も確認する
            tmp_obj = Image.open(dir_settings['src_img_dir'] + file_list[i])
            tmp_reso = tmp_obj.width * tmp_obj.height
            # ファイルサイズが小さくても解像度が大きければリストに入れる
            if tmp_reso >= resolution_threshold:
                large_file_list.append(file_list[i])

    return large_file_list

def processing_candidate_maker(large_file_list: list, thumbnail_image_list: list) -> list:
    log.debug('-> processing_candidate_maker()')

    candidate_list = []
    for i in range(len(large_file_list)):
        tmp_name = large_file_list[i].split('.')[0]
        if not any(s.startswith(r'tmb_' + tmp_name) for s in thumbnail_image_list):
            candidate_list.append(large_file_list[i])
    
    return candidate_list

# --------------------------------------------------------------------

def image_list(dir_settings: dict) -> dict:
    log.debug('-> image_list()')

    # ファイルリスト取得
    source_image_list       = os.listdir(dir_settings['src_img_dir'])
    thumbnail_image_list    = os.listdir(dir_settings['tmb_img_dir'])

    log.debug('source_image_list:    \n' + str(source_image_list))
    log.debug('thumbnail_image_list: \n' + str(thumbnail_image_list))

    # とりあえず
    for i in range(len(source_image_list)):
        if ' ' in source_image_list[i]:
            log.error('画像ファイル名にスペースが含まれています。ルール通り命名されたファイルしか処理できません。: ' + source_image_list[i])
            return None

    # jpg, png, gif, mp4 のリストを作成
    jpg_png_list    = file_list_maker(r'\w+\.jpg|\w+\.png', source_image_list)
    gif_list        = file_list_maker(r'\w+\.gif', source_image_list)
    mp4_list        = file_list_maker(r'\w+\.mp4', source_image_list)

    # 大きい jpg, png, gif, mp4 のリストを作成
    large_img_list = large_file_searcher(jpg_png_list, 128000, dir_settings, 0)
    large_gif_list = large_file_searcher(gif_list, 512000, dir_settings, 43200) # 240 * 180 を超える場合
    large_mp4_list = large_file_searcher(mp4_list, 512000, dir_settings, 0)

    log.debug('large_img_list: \n' + str(large_img_list))
    log.debug('large_gif_list: \n' + str(large_gif_list))
    log.debug('large_mp4_list: \n' + str(large_mp4_list))

    # サムネイルを持たない大きい jpg, png, gif, mp4 リストを作成
    candidate_img_list = processing_candidate_maker(large_img_list, thumbnail_image_list)
    candidate_gif_list = processing_candidate_maker(large_gif_list, thumbnail_image_list)
    candidate_mp4_list = processing_candidate_maker(large_mp4_list, thumbnail_image_list)

    log.debug('candidate_img_list: \n' + str(candidate_img_list))
    log.debug('candidate_gif_list: \n' + str(candidate_gif_list))
    log.debug('candidate_mp4_list: \n' + str(candidate_mp4_list))

    image_lists_dict = {
        'source_image_list':    source_image_list, 
        'thumbnail_image_list': thumbnail_image_list, 
        'large_img_list':       large_img_list, 
        'large_gif_list':       large_gif_list, 
        'large_mp4_list':       large_mp4_list, 
        'candidate_img_list':   candidate_img_list, 
        'candidate_gif_list':   candidate_gif_list,
        'candidate_mp4_list':   candidate_mp4_list,
        }
    
    #log.debug('image_lists_dict: \n' + str(image_lists_dict))

    return image_lists_dict

# --------------------------------------------------------------------

if __name__ == '__main__':
    image_list(load_settings())
    #os.system('PAUSE')