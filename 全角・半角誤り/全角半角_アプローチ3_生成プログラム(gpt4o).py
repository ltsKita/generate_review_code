import os
import re
from lxml import etree

# ステップ1: 名前空間の設定
namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# ステップ2: xml形式の処理対象ファイル読み取り
xml_file_path = os.path.join('全角・半角誤り/xml', 'word', 'document.xml')
if not os.path.exists(xml_file_path):
    raise FileNotFoundError(f"File not found: {xml_file_path}")

tree = etree.parse(xml_file_path)
root = tree.getroot()

# ステップ3: 要素の抽出
paragraphs = root.findall('.//w:p', namespaces=namespace)

# 正規表現ルールを定義（ステップ4, 5）
full_to_half = {
    'Ａ': 'A', 'Ｂ': 'B', '１': '1', '２': '2', '〜': '~', '：': ':', '％': '%'
    # 他の全角→半角置換ルールをここに追加
}

half_to_full = {
    'A': 'Ａ', 'B': 'Ｂ', '1': '１', '2': '２', '~': '〜', ':': '：', '%': '％'
    # 他の半角→全角置換ルールをここに追加
}

# ステップ6: ルールを用いて対象テキストを取得＆ステップ7: 置換処理
for para in paragraphs:
    runs = para.findall('.//w:r', namespaces=namespace)
    for run in runs:
        text_elements = run.findall('.//w:t', namespaces=namespace)
        for text_element in text_elements:
            original_text = text_element.text
            
            # 置換前のテキストをログに出力
            print(f"Original text: {original_text}")
            
            # 全角→半角置換
            for full_char, half_char in full_to_half.items():
                original_text = re.sub(re.escape(full_char), half_char, original_text)
            
            # 半角→全角置換
            for half_char, full_char in half_to_full.items():
                original_text = re.sub(re.escape(half_char), full_char, original_text)
            
            # ステップ8: ハイライト付与（変更があった場合のみ）
            if original_text != text_element.text:
                text_element.text = original_text
                
                # ハイライトを追加する<w:rPr>タグを作成
                highlight_element = etree.Element(f"{{{namespace['w']}}}highlight")
                highlight_element.set(f"{{{namespace['w']}}}val", "yellow")

                # 既存の<w:rPr>がない場合は追加
                rPr_element = run.find('.//w:rPr', namespaces=namespace)
                if rPr_element is None:
                    rPr_element = etree.Element(f"{{{namespace['w']}}}rPr")
                    run.insert(0, rPr_element)
                
                rPr_element.append(highlight_element)

# ステップ2: 変更をファイルに上書き保存
tree.write(xml_file_path, xml_declaration=True, encoding='UTF-8', standalone="yes")

print("Processing complete.")
