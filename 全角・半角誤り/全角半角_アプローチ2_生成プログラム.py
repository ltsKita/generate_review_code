import xml.etree.ElementTree as ET
import re

# ステップ1: ファイルの読み込み
data_dir = 'data'
xml_file = ET.parse(f'{data_dir}/original.xml')
root = xml_file.getroot()

# ステップ2: 情報の抽出
text = ''
for elem in root.findall('.//text'):
    text += elem.text

# ステップ3: 正規表現ルールの作成
full_angle_regex = re.compile(r'[^\x20-\x7E\xA1-\xDF]')  # 半角文字を全角文字に置換
half_angle_regex = re.compile(r'[^\x20-\x7E\xA1-\xDF]+')  # 全角文字を半角文字に置換

# ステップ4: 正規表現ルールの作成
roman_regex = re.compile(r'[IVXLCDM]+')  # ローマ数字を半角に置換
bracket_regex = re.compile(r'[^\w\s]+')  # 括弧を半角に置換
comma_regex = re.compile(r'[0-9,]+')  # 桁数字を半角に置換

# ステップ5: ルールを用いて対象テキストを取得
for match in full_angle_regex.finditer(text):
    text = text.replace(match.group(), match.group().encode('utf-8').decode('cp932'))

for match in half_angle_regex.finditer(text):
    text = text.replace(match.group(), match.group().encode('utf-8').decode('cp932'))

# ステップ6: ルールを用いて対象テキストを置換
text = roman_regex.sub(lambda match: match.group().encode('utf-8').decode('cp932'), text)
text = bracket_regex.sub(lambda match: match.group().encode('utf-8').decode('cp932'), text)
text = comma_regex.sub(lambda match: match.group().encode('utf-8').decode('cp932'), text)

# ステップ7: ハイライト付与
highlight_text = ''
for elem in root.findall('.//text'):
    elem.text = text.replace(elem.text, f"<span style='background-color: yellow'>{text}</span>")
    highlight_text += elem.text

# ステップ8: ファイル出力
with open(f'{data_dir}/output.xml', 'w') as f:
    f.write(ET.tostring(root, encoding='unicode'))
with open(f'{data_dir}/output.docx', 'w') as f:
    f.write(highlight_text.encode('utf-8'))