# -*- coding: utf-8 -*-
"""
Calc-Insight-Kit 项目批量运行入口
支持分层批量执行、全局统一运行
"""
import os
import sys
import subprocess
from calc_insight_kit.config import RUN_KID_MODE, RUN_MIDDLE_MODE, RUN_UNIVERSITY_MODE

def run_all_demos():
    base_path = os.path.abspath('.')
    layer_config = [
        ('kid', RUN_KID_MODE),
        ('middle', RUN_MIDDLE_MODE),
        ('university', RUN_UNIVERSITY_MODE)
    ]

    for layer_name, is_run in layer_config:
        if not is_run:
            print(f'\n【{layer_name.upper()}层】已关闭运行，跳过')
            continue
        
        print(f'\n===== 开始运行【{layer_name.upper()}】全部示例 =====')
        demo_dir = os.path.join(base_path, 'examples', layer_name)
        if not os.path.exists(demo_dir):
            continue
        
        file_list = sorted([f for f in os.listdir(demo_dir) if f.endswith('.py') and f.startswith(tuple(f'{i:02d}' for i in range(1,10)))])
        for file in file_list:
            file_path = os.path.join(demo_dir, file)
            print(f'运行: {file}')
            subprocess.run([sys.executable, file_path], cwd=base_path)
    
    print('\n✅ 所有开启层级的示例运行完成！')

if __name__ == '__main__':
    run_all_demos()
