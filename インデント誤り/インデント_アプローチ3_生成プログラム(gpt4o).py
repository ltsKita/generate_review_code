from lxml import etree
import re

# ステップ1: 名前空間の設定
namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# ステップ2: XMLファイルの読み込み
def load_xml(file_path):
    try:
        tree = etree.parse(file_path)
        return tree
    except FileNotFoundError:
        print("Error: The specified file was not found.")
        return None

file_path = 'インデント誤り/xml/word/document.xml'
tree = load_xml(file_path)
if tree is None:
    exit()

root = tree.getroot()

# ステップ3: 要素の抽出
def extract_elements(root):
    paragraphs = root.findall('.//w:p', namespaces=namespace)
    extracted_data = []
    for p in paragraphs:
        texts = p.findall('.//w:t', namespaces=namespace)
        indent = p.find('.//w:ind', namespaces=namespace)
        ind_value = indent.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left') if indent is not None else None
        para_text = ''.join([t.text for t in texts if t.text])
        extracted_data.append((para_text, ind_value))
        print(f'Text: {para_text}, Indent: {ind_value}')
    return extracted_data

extracted_data = extract_elements(root)

# ステップ4: 項目番号形式を修正するルールの作成
def apply_numbering_rules(text):
    rules = [
        (r'(\d+)\. ', r'\1．　'),  # "1." -> "1．　"
        (r'\((\d+)\)', r'（\1）'),  # "(1)" -> "（1）"
        (r'([a-zA-Z])\. ', r'ａ．'),  # "a." -> "ａ．"
        (r'\((a|b|c)\)', r'（\1）'),  # "(a)" -> "（a）"
        (r'\((a-\d+)\)', r'（\1）')  # "(a-1)" -> "（a-1）"
    ]
    for pattern, replacement in rules:
        text = re.sub(pattern, replacement, text)
    return text

# ステップ5: 項目番号の連番を修正するルールの作成
def fix_sequential_numbering(text):
    pattern = re.compile(r'(\d+)(\.\d+)*')
    matches = pattern.findall(text)
    if matches:
        # 順番が正しいかを確認し、必要に応じて修正する処理を追加する（例として単純に出力）
        # 実際のルールに応じて修正が必要
        print(f'Sequential Numbering Detected: {matches}')
    return text

# ステップ6: 項目番号のインデントを修正するルールの作成
def apply_indent_rules(text, indent_value):
    indent_map = {
        '0': r'\d+\. ',  # "インデント0文字"
        '1': r'\(\d+\)',  # "インデント1文字"
        '2': r'ａ．',  # "インデント2文字"
        '3': r'（a）',  # "インデント3文字"
        '4': r'（a-\d+）',  # "インデント4文字"
        '5': r'（a-\d+-\d+）'  # "インデント5文字"
    }
    for indent, pattern in indent_map.items():
        if re.match(pattern, text) and indent_value != indent:
            print(f'Indent Correction: {text} -> Indent {indent}')
            # 実際の修正処理を追加する必要がある
    return text

# ステップ7: 変更箇所へのハイライト付与
def highlight_changes(p, original_text, new_text):
    if original_text != new_text:
        for r in p.findall('.//w:r', namespaces=namespace):
            t = r.find('.//w:t', namespaces=namespace)
            if t is not None and t.text == original_text:
                # w:rPr要素を追加してハイライトを適用
                highlight = etree.Element('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}highlight', val='yellow')
                rPr = r.find('.//w:rPr', namespaces=namespace)
                if rPr is None:
                    rPr = etree.SubElement(r, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr')
                rPr.append(highlight)
                t.text = new_text

# ルール適用とハイライト処理の統合
for p in root.findall('.//w:p', namespaces=namespace):
    original_text = ''.join([t.text for t in p.findall('.//w:t', namespaces=namespace) if t.text])
    new_text = apply_numbering_rules(original_text)
    new_text = fix_sequential_numbering(new_text)
    indent_value = p.find('.//w:ind', namespaces=namespace)
    if indent_value is not None:
        new_text = apply_indent_rules(new_text, indent_value.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left'))
    highlight_changes(p, original_text, new_text)

# ステップ8: 変更内容をXMLに上書き保存
tree.write(file_path, xml_declaration=True, encoding='utf-8', standalone=False)
print(f"Document saved to {file_path}")
