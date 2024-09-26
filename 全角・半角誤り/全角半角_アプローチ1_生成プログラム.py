import docx
import re

def word_file_processing(file_path):
    doc = docx.Document(file_path)
    for para in doc.paragraphs:
        for run in para.runs:
            text = run.text
            text = text.replace(' ', '　')  # 半角スペースを全角スペースに置き換え
            text = re.sub(r'([a-zA-Z0-9\.,:;\'\"\\-])', lambda x: x.group().lower() if x.group().lower() in ['a-z', '0-9', '.,:;\'\"\\-'] else '', text)  # 英数字、記号を半角に変換
            text = re.sub(r'([<>])', lambda x: x.group().lower() if x.group().lower() in ['a-z', '0-9', '.,:;\'\"\\-'] else '', text)  # 桁数字を半角に変換
            text = re.sub(r'([a-zA-Z0-9])', lambda x: x.group().upper() if x.group().lower() in ['a-z', '0-9'] else '', text)  # 桁数字を半角に変換
            text = re.sub(r'([a-zA-Z0-9])', lambda x: x.group().lower() if x.group().lower() in ['a-z', '0-9'] else '', text)  # 桁数字を半角に変換
            para.text = text

    doc.save(file_path)

word_file_processing('全角・半角誤り/data/【全角・半角誤りデータ】崩壊熱除去機能喪失_本文.docx')