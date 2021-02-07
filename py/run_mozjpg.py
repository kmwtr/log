#! python3
import logging as log
import os
import sys
import subprocess

import debug_config

def run_mozjpg(file_path: str, output_dir: str):
    log.debug('-> run_mozjpg()')

    # 圧縮、中間ファイルとして出力
    cp = subprocess.run(['cjpeg-static', '-quality', '90', '-outfile', 'intermediate_img.jpg', file_path], encoding='utf-8', stdout=subprocess.PIPE)
    print(cp)

    # Exif 等メタデータを削除、最終ファイル出力
    cp = subprocess.run(['jpegtran-static', '-copy', 'none', '-outfile', 'final.jpg', output_dir + 'intermediate_img.jpg'], encoding='utf-8', stdout=subprocess.PIPE)
    print(cp)

    # 中間ファイル削除
    ## しごと

# -------------------------------------------------

if __name__ == '__main__':
    run_mozjpg('IMG_20201106_082741.png', '')
    #os.system('PAUSE')