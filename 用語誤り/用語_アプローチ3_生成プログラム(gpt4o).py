import os
from lxml import etree

# ステップ1: 名前空間の設定
namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# ステップ2: XMLファイルの読み込み
def load_xml_file(xml_dir):
    xml_path = os.path.join(xml_dir, 'word', 'document.xml')
    if not os.path.exists(xml_path):
        raise FileNotFoundError(f"ファイルが見つかりません: {xml_path}")
    tree = etree.parse(xml_path)
    return tree, tree.getroot()

# ステップ3: <w:p>要素の処理とテキスト抽出
def extract_paragraph_text(root):
    paragraphs = root.findall('.//w:p', namespaces=namespace)
    text_data = []
    for para in paragraphs:
        texts = para.findall('.//w:t', namespaces=namespace)
        para_text = ''.join([t.text for t in texts if t.text])
        text_data.append((para, para_text))
    return text_data

# ステップ4: 修正ルールの作成
def apply_correction_rules(para_text):
    modified_text = para_text

    # ①「とき」と「時」の修正
    if 'とき' in para_text or '時' in para_text:
        if "とき" in para_text:
            modified_text = modified_text.replace('とき', '時')  # 文脈によって時に変更
        elif "時" in para_text:
            modified_text = modified_text.replace('時', 'とき')  # 文脈によってときに変更

    # ②「他」と「外」の修正
    if '他' in para_text or '外' in para_text:
        if "他" in para_text:
            modified_text = modified_text.replace('他', 'ほか')  # 文脈によってほかに変更
        elif "外" in para_text:
            modified_text = modified_text.replace('外', 'ほか')  # 文脈によってほかに変更

    return modified_text

# ステップ5: テキストの変更を反映してハイライトを適用
def highlight_changes(paragraph, original_text, modified_text):
    if original_text != modified_text:
        for t in paragraph.findall('.//w:t', namespaces=namespace):
            if t.text in original_text:
                r_element = t.getparent()
                rPr = etree.Element(f"{{{namespace['w']}}}rPr")
                highlight = etree.Element(f"{{{namespace['w']}}}highlight")
                highlight.set(f"{{{namespace['w']}}}val", "yellow")
                rPr.append(highlight)
                r_element.insert(0, rPr)
                t.text = modified_text

# XMLファイルに上書き保存
def save_xml(tree, xml_dir):
    xml_path = os.path.join(xml_dir, 'word', 'document.xml')
    tree.write(xml_path, xml_declaration=True, encoding='UTF-8', standalone='yes')

def main(xml_dir):
    try:
        tree, root = load_xml_file(xml_dir)
        paragraphs_text = extract_paragraph_text(root)

        # すべての段落を処理して修正を適用
        for para, original_text in paragraphs_text:
            modified_text = apply_correction_rules(original_text)
            highlight_changes(para, original_text, modified_text)

        # 修正後のXMLを保存
        save_xml(tree, xml_dir)

        print("文書校閲が完了しました。")
    except FileNotFoundError as e:
        print(str(e))

# 実行例
xml_directory = '用語誤り/xml/'
main(xml_directory)
