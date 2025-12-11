#!/usr/bin/env python3
# white.py
import os
from pathlib import Path
import numpy as np
from PIL import Image

def png_on_white(png_path, out_path=None):
    """单张 PNG → 白底 RGB 数组，可选落盘"""
    rgba = np.array(Image.open(png_path).convert('RGBA'))
    rgb  = rgba[...,:3].astype(np.float32)
    alpha = rgba[...,3:4].astype(np.float32) / 255.0
    composite = (alpha * rgb + (1 - alpha) * 255.0).astype(np.uint8)
    if out_path:
        Image.fromarray(composite).save(out_path)
    return composite

def batch_png_on_white(folder, out_folder=None, ext='.png'):
    """
    读取 folder 下所有 PNG -> 白底
    out_folder:  None  -> 同级 *_white.png
                路径字符串 -> 统一输出目录
    返回 {name: np_array} 字典
    """
    folder = Path(folder)
    if out_folder is None:          # 默认同级加后缀
        out_folder = folder
    else:
        out_folder = Path(out_folder)
        out_folder.mkdir(exist_ok=True)

    results = {}
    for png_file in folder.glob(f'*{ext}'):
        save_path = out_folder / f'{png_file.stem}_white.png'
        arr = png_on_white(png_file, save_path)
        results[png_file.name] = arr
        print(f'saved: {save_path}')
    return results

if __name__ == '__main__':
    for i in range(6):
        out_dir = Path(f'white/{i + 1}')
        out_dir.mkdir(parents=True, exist_ok=True)   # ← 自动建目录
        batch_png_on_white(f'img/{i + 1}', out_dir)