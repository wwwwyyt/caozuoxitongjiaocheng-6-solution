#!/usr/bin/env python3
# img2pdf.py
import os, re
from pathlib import Path
from PIL import Image

def natural_sort_key(name):
    """把 abc123def456 拆成 [abc, 123, def, 456]，实现 1<2<10 的自然排序"""
    return [int(t) if t.isdigit() else t.lower()
            for t in re.split(r'(\d+)', name)]

def imgs_to_pdf(folder, out_pdf='output.pdf', quality=95):
    # 1. 找到目录里常见图片后缀
    exts = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif')
    files = [f for f in os.listdir(folder)
             if f.lower().endswith(exts)]
    if not files:
        raise SystemExit('目录里没有找到图片')
    files.sort(key=natural_sort_key)          # 关键：按编号顺序

    # 2. 统一转成 RGB（PDF 不支持透明通道）
    images = [Image.open(os.path.join(folder, f)).convert('RGB')
              for f in files]

    # 3. 第一张作为“主图”，其余 append
    images[0].save(out_pdf,
                   save_all=True,
                   append_images=images[1:],
                   quality=quality,
                   optimize=True)
    print(f'已生成 {out_pdf}  共 {len(images)} 页')

if __name__ == '__main__':
    for i in range(6):
        out_dir = Path(f'pdf/{i + 1}')
        out_dir.mkdir(parents=True, exist_ok=True)   # 自动建目录
        imgs_to_pdf(f'white/{i + 1}', f"{out_dir}.pdf")
    