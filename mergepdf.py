#!/usr/bin/env python3
# mergepdf.py
from pathlib import Path
from natsort import natsorted          # pip install natsort
from PyPDF2 import PdfMerger           # pip install PyPDF2

def merge_pdfs(folder, out_file='merged.pdf'):
    folder = Path(folder)
    pdf_paths = natsorted(folder.glob('*.pdf'))   # 1. 找 + 2. 自然排序
    if not pdf_paths:
        raise SystemExit('目录里没有找到 PDF')

    merger = PdfMerger()
    for p in pdf_paths:
        merger.append(str(p))           # 3. 逐个追加
        print(f'append: {p.name}')

    merger.write(out_file)              # 4. 输出
    merger.close()
    print(f'已生成 {out_file}  共 {len(pdf_paths)} 份')


if __name__ == '__main__':
    merge_pdfs('pdf', "操作系统教程（第6版）习题解答.pdf")             # 改成你的目录
