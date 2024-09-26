import xml.etree.ElementTree as ET
import xml.dom.minidom
import re

# ステップ1: ファイルの読み込み
data_dir = '用語誤り/data'
xml_file = 'input.xml'
word_file = '用語誤り/data/【用語誤りデータ(55個)】第12条_まとめ資料_本文.docx'

# 解凍してxmlファイルを生成
import zipfile
with zipfile.ZipFile(word_file) as zip_file:
    zip_file.extractall(data_dir)

# ステップ2: 情報の抽出
xml_tree = ET.parse(f'{data_dir}/{xml_file}').getroot()
text = xml_tree.text

# ステップ3: 修正ルールの作成
def fix_rule1(text):
    return re.sub(r'とき|時', lambda m: m.group().lower() == 'とき' and '時' or 'とき', text)

def fix_rule2(text):
    return re.sub(r'他|外', lambda m: m.group().lower() == 'ほか' and 'ほか' or '他', text)

# ステップ4: 処理分岐判定
def is_rule1(text):
    return re.search(r'とき|時', text)

def is_rule2(text):
    return re.search(r'他|外', text)

# ステップ5: 作成したルールの適用
def apply_rule(text):
    if is_rule1(text):
        return fix_rule1(text)
    elif is_rule2(text):
        return fix_rule2(text)
    return text

# ステップ6: ファイル出力
new_text = apply_rule(text)
dom = xml.dom.minidom.parseString(new_text)
xml_tree = ET.fromstring(dom.toxml())
ET.SubElement(xml_tree, 'new_text').text = new_text
ET.save(f'{data_dir}/{xml_file}')

print("Processing complete.")