import xml.etree.ElementTree as ET
import re
import xml.dom.minidom

# 名前空間の設定
namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# xmlファイルの読み込み
def read_xml_file(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except FileNotFoundError:
        print("指定されたファイルが見つかりません。")
        return None

# 正規表現のルールの作成
def create_regex_rule(type, pattern):
    if type == 'full_width':
        return re.compile(pattern)
    elif type == 'half_width':
        return re.compile(pattern.replace(r'[^\x20-\x7E\xA1-\xDF\xE0-\u00FF\u0800-\uFFFF]+', ''))

# 文書校閲の処理
def document_processing(xml_file_path):
    doc = read_xml_file(xml_file_path)
    if doc is None:
        return

    for elem in doc.findall('.//{w:p}'):
        for run in elem.findall('.//{w:r}'):
            for text in run.findall('.//{w:t}'):
                text.text = text.text.replace(' ', '')
                if re.search(r'([^\x20-\x7E\xA1-\xDF\xE0-\u00FF\u0800-\uFFFF]+|[^\x20-\x7E\xA1-\xDF\xE0-\u00FF\u0800-\uFFFF]+、|[^\x20-\x7E\xA1-\xDF\xE0-\u00FF\u0800-\uFFFF]+~|[^\x20-\x7E\xA1-\xDF\xE0-\u00FF\u0800-\uFFFF]+：|[^\x20-\x7E\xA1-\xDF\xE0-\u00FF\u0800-\uFFFF]+％|[^\x20-\x7E\xA1-\xDF\xE0-\u00FF\u0800-\uFFFF]+|([^\x20-\x7E\xA1-\xDF\xE0-\u00FF\u0800-\uFFFF]+|[^\x20-\x7E\xA1-\xDF\xE0-\u00FF\u0800-\uFFFF]+、|[^\x20-\x7E\xA1-\xDF\xE0-\u00FF\u0800-\uFFFF]+~|[^\x20-\x7E\xA1-\xDF\xE0-\u00FF\u0800-\uFFFF]+：|[^\x20-\x7E\xA1-\xDF\xE0-\u00FF\u0800-\uFFFF]+％|[^\x20-\x7E\xA1-\xDF\xE0-\u00FF\u0800-\uFFFF]+)') is not None:
                    text.text = text.text.replace(re.escape(text.text), text.text.replace(' ', ''))

    doc.save(xml_file_path)

# 実行
document_processing('全角・半角誤り/xml/word/document.xml')