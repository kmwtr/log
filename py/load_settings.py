#! python3
import os
import glob
import yaml
import logging as log

import debug_config

def load_settings() -> dict:
    log.debug('-> load_settings()')

    # 現在のディレクトリ位置
    path = os.getcwd()
    log.debug('cwd_path:    ' + path)
    
    # 設定ファイルの取得（1階層下まで許容）
    yaml_name = 'lap_settings.yaml'

    if not glob.glob(yaml_name):
        yaml_list = glob.glob(path + '/**/' + yaml_name)

        if not yaml_list:
            log.debug('ERROR | No Setting File')
            return
        
        if not len(yaml_list) == 1:
            log.debug('ERROR | There are many Files')
            return
        
        yaml_name = str(yaml_list[0])

    log.debug('yaml_dir:    ' + yaml_name)

    # ファイルのロード
    file = open(yaml_name, "r", encoding='utf-8')
    data = yaml.safe_load(file)

    year        = data["Year"]
    quarter     = data["Quarter"]

    base_dir    = str(data["Base DIR"])
    src_img_dir = base_dir + str(data["Source Image DIR"]) + '/' + str(year) + '/'
    tmb_img_dir = base_dir + str(data["Thumbnail Image DIR"]) + '/' + str(year) + '/'
    html_dir    = base_dir + str(data["Target HTML DIR"]) + '/' + str(year) + 'Q'+ str(quarter) + '.html'
    
    log.debug('base_dir:    ' + base_dir)
    log.debug('src_img_dir: ' + src_img_dir)
    log.debug('tmb_img_dir: ' + tmb_img_dir)
    log.debug('html_dir:    ' + html_dir)

    setting_dict = {'year':year, 'quarter':quarter, 'base_dir':base_dir, 'src_img_dir':src_img_dir, 'tmb_img_dir':tmb_img_dir, 'html_dir':html_dir}
    return setting_dict


# -------------------------------------------------

if __name__ == '__main__':
    load_settings()
    os.system('PAUSE')