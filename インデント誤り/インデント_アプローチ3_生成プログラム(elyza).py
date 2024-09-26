import xml.etree.ElementTree as ET
import re
import logging
import sys

logging.basicConfig(level=logging.INFO)

namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# ステップ1: 名前空間の設定
root = ET.parse('用語誤り/xml/word/document.xml').getroot()
root.nsmap.update(namespace)

# ステップ2: xml形式の処理対象ファイル読み取り
if not ET.parse('用語誤り/xml/word/document.xml').getroot():
    logging.error("File 'document.xml' not found.")
    sys.exit(1)

# ステップ3: 要素の抽出
p_elements = root.findall('.//{w:p}', namespaces=namespace)
for p_element in p_elements:
    r_elements = p_element.findall('.//{w:r}', namespaces=namespace)
    for r_element in r_elements:
        t_elements = r_element.findall('.//{w:t}', namespaces=namespace)
        ind_elements = p_element.findall('.//{w:ind}', namespaces=namespace)
        for t_element, ind_element in zip(t_elements, ind_elements):
            logging.info(f"Text: {t_element.text}, Indent: {ind_element.get()}")

# ステップ4: 項目番号形式を修正するルールの作成
def fix_formatting(p_element):
    for r_element in p_element.findall('.//{w:r}', namespaces=namespace):
        t_element = r_element.find('.//{w:t}', namespaces=namespace)
        text = t_element.text
        if re.match(r'\d+\.\d+\.\d+\.\d+|(\(\d+\))|([a-zA-Z].*)', text):
            text = re.sub(r'\s', '', text)
            if re.match(r'\(\d+\)', text):
                text = re.sub(r'\(\d+\)', lambda m: f"({m.group(0).lstrip()})", text)
            elif re.match(r'[a-zA-Z].*', text):
                text = re.sub(r'([a-zA-Z].*)', lambda m: f"{m.group(0).lstrip()}.", text)
            t_element.text = text

# ステップ5: 項目番号の連番を修正するルールの作成
def fix_numbering(p_element):
    for r_element in p_element.findall('.//{w:r}', namespaces=namespace):
        t_element = r_element.find('.//{w:t}', namespaces=namespace)
        text = t_element.text
        if re.match(r'\d+\.\d+\.\d+\.\d+|(\(\d+\))|([a-zA-Z].*)', text):
            parts = text.split('.')
            if len(parts) > 1:
                prefix = parts[0]
                suffix = '.'.join(parts[1:])
                if re.match(r'\(\d+\)', suffix):
                    suffix = re.sub(r'\(\d+\)', lambda m: f"({m.group(0).lstrip()})", suffix)
                elif re.match(r'[a-zA-Z].*', suffix):
                    suffix = re.sub(r'([a-zA-Z].*)', lambda m: f"{m.group(0).lstrip()}.", suffix)
                t_element.text = f"{prefix}.{suffix}"

# ステップ6: 項目番号のインデントを修正するルールの作成
def fix_indent(p_element):
    for r_element in p_element.findall('.//{w:r}', namespaces=namespace):
        t_element = r_element.find('.//{w:t}', namespaces=namespace)
        text = t_element.text
        if re.match(r'\d+\.\d+\.\d+\.\d+|(\(\d+\))|([a-zA-Z].*)', text):
            parts = text.split('.')
            if len(parts) > 1:
                prefix = parts[0]
                suffix = '.'.join(parts[1:])
                if re.match(r'\(\d+\)', suffix):
                    suffix = re.sub(r'\(\d+\)', lambda m: f"({m.group(0).lstrip()})", suffix)
                elif re.match(r'[a-zA-Z].*', suffix):
                    suffix = re.sub(r'([a-zA-Z].*)', lambda m: f"{m.group(0).lstrip()}.", suffix)
                t_element.text = f"{prefix}.{suffix}"

# ステップ7: 作成したルールの適用
for p_element in p_elements:
    fix_formatting(p_element)
    fix_numbering(p_element)
    fix_indent(p_element)

# 変更内容を元のxmlファイルに上書き
ET.parse('用語誤り/xml/word/document.xml').write('用語誤り/xml/word/document.xml')