import lxml.etree as ET
import re

# 名前空間の設定
namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# xml形式の処理対象ファイル読み取り
word_dir = '用語誤り/xml/word'
file_path = f'{word_dir}/document.xml'

try:
    tree = ET.parse(file_path)
    root = tree.getroot()
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    exit()

# 名前空間を設定
root = ET.default_namespace = namespace

# 要素の抽出
p_elements = root.findall('.//{w:p}', namespaces=namespace)
for p in p_elements:
    r_elements = p.findall('.//{w:r}', namespaces=namespace)
    for r in r_elements:
        t_elements = r.findall('.//{w:t}', namespaces=namespace)
        for t in t_elements:
            text = t.text
            print(text)

            # 修正ルールの作成
            if re.search(r'とき', text):
                if re.search(r'時点', text):
                    text = text.replace('とき', '時')
                else:
                    text = text.replace('時', 'とき')
            elif re.search(r'他', text):
                if re.search(r'ほか', text):
                    text = text.replace('外', 'ほか')
                else:
                    text = text.replace('他', 'ほか')
            t.text = text

            # 処理分岐判定
            if re.search(r'とき|時', text):
                # 「とき」と「時」の修正
                t.addprevious(ET.Element('w:rPr', {'w:color': 'FFD700'}))
            elif re.search(r'他|外', text):
                # 「他」と「外」の修正
                t.addprevious(ET.Element('w:rPr', {'w:color': 'FFD700'}))

# 作成したルールの適用
ET.register_namespace("", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")
root = ET.fromstring(open(file_path, 'r').read())
ET.ElementTree(root).write(file_path)