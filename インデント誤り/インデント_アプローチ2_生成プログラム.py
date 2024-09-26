import xml.etree.ElementTree as ET
import re

# ステップ1:ファイルの読み込み
data_dir = 'data'
file_name = 'input.xml'
tree = ET.parse(data_dir + '/' + file_name)
root = tree.getroot()

# ステップ2:情報の抽出
text_info = []
for elem in root.iter():
    if elem.text:
        text_info.append(elem.text)

# ステップ3:項目番号形式を修正するルールの作成
item_number_rule = re.compile(r'(\d+(?:\.\d+)*)(?:\s|$)')
item_number_rule2 = re.compile(r'\(\d+(?:\.\d+)*\)')
item_number_rule3 = re.compile(r'\.\s*')

# ステップ4:項目番号の連番を修正するルールの作成
item_number連番_rule = re.compile(r'\d+(?:\.\d+)*\.\d+(?:\.\d+)*')
item_number連番_rule2 = re.compile(r'\(\d+(?:\.\d+)*\)\.\d+(?:\.\d+)*')
item_number連番_rule3 = re.compile(r'\.\s*')

# ステップ5:項目番号のインデントを修正するルールの作成
indent_rule = re.compile(r'\s*')
indent_rule2 = re.compile(r'\s+')

# ステップ6:作成したルールの適用
for i, text in enumerate(text_info):
    if item_number_rule.match(text):
        text = item_number_rule.sub(lambda match: match.group(0).replace(' ', '\u3000'), text)
    elif item_number_rule2.match(text):
        text = item_number_rule2.sub(lambda match: match.group(0).replace(' ', '\u3000'), text)
    elif item_number_rule3.match(text):
        text = item_number_rule3.sub(lambda match: match.group(0).replace(' ', '\u3000'), text)

    if item_number連番_rule.match(text):
        text = item_number連番_rule.sub(lambda match: match.group(0).replace(' ', '\u3000'), text)
    elif item_number連番_rule2.match(text):
        text = item_number連番_rule2.sub(lambda match: match.group(0).replace(' ', '\u3000'), text)
    elif item_number連番_rule3.match(text):
        text = item_number連番_rule3.sub(lambda match: match.group(0).replace(' ', '\u3000'), text)

    if indent_rule.match(text):
        text = indent_rule.sub(lambda match: '\u3000' + match.group(0), text)
    elif indent_rule2.match(text):
        text = indent_rule2.sub(lambda match: '\u3000\u3000' + match.group(0), text)

    text_info[i] = text

# ステップ7:ハイライト付与
highlight_text = '\u0009'
for i, text in enumerate(text_info):
    if text!= text_info[i-1]:
        text_info[i] = '<font color="yellow">' + text + '</font>' + highlight_text

# ステップ8:ファイル出力
output_file = ET.Element('root')
for i, text in enumerate(text_info):
    elem = ET.Element('text')
    elem.text = text
    output_file.append(elem)

tree = ET.ElementTree(output_file)
tree.write(data_dir + '/' + 'output.xml')