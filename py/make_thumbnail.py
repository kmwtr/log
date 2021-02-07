#! python3
import os
import subprocess
from PIL import Image
import logging as log

import debug_config

from load_settings import load_settings
from image_list import image_list

def make_thumbnail(image_lists: dict, dirs_list: dict):
    log.debug('-> make_thumbnail()')

    # jpg, png をサムネイル処理する
    candidate_img_list = image_lists['candidate_img_list']

    for i in range(len(candidate_img_list)):
        # 候補リストに基づいて jpg, png を読む
        image_obj = Image.open(dirs_list['src_img_dir'] + candidate_img_list[i])
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
    
        # 一旦pngとして出力
        tmp_name = candidate_img_list[i].split('.')[0]
        tmp_path = dirs_list['tmb_img_dir'] + 'tmb_' + tmp_name + '.png'
        image_obj.save(tmp_path)
        #image_obj.save(dirs_list['tmb_img_dir'] + 'tmb_' + tmp_name + '.jpg', quality=95) # jpgの場合

        log.debug('saved_tmp-tmb: ' + 'tmb_' + tmp_name + '.png')
        
        # mozjpg を呼び出してjpgに圧縮する
        log.debug('-> run_mozjpg()')
        
        output_path = dirs_list['tmb_img_dir'] + 'tmb_' + tmp_name + '.jpg'

        # 圧縮、中間ファイルとして出力
        cp = subprocess.run(['cjpeg-static', '-quality', '90', '-outfile', dirs_list['tmb_img_dir'] + 'intermediate_img.jpg', tmp_path], encoding='utf-8', stdout=subprocess.PIPE)
        print(cp)

        # Exif 等メタデータを削除、最終ファイル出力
        cp = subprocess.run(['jpegtran-static', '-copy', 'none', '-optimize', '-outfile', output_path, dirs_list['tmb_img_dir'] + 'intermediate_img.jpg'], encoding='utf-8', stdout=subprocess.PIPE)
        print(cp)

        log.debug('saved_tmb: ' + 'tmb_' + tmp_name + '.jpg')

        # 中間ファイル削除
        os.remove(dirs_list['tmb_img_dir'] + 'intermediate_img.jpg')
    
    
    # gif をサムネイル処理する
    candidate_gif_list = image_lists['candidate_gif_list']

    for i in range(len(candidate_gif_list)):
        print('Hello')


# -------------------------------------------------

if __name__ == '__main__':
    dirs_list = load_settings()
    make_thumbnail(image_list(dirs_list), dirs_list)
    #os.system('PAUSE')