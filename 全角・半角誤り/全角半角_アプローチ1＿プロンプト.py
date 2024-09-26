import sys
import os

# 現在のファイルパスを取得(全角・半角誤りディレクトリ内で本プログラムを実行するために使用)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from model_download import get_tokenizer_elyza_8b, get_model_elyza_8b
from transformers import pipeline
from langchain_huggingface.llms import HuggingFacePipeline

# 生成AI(elyza 8Bモデル)を使用するための設定を記述
tokenizer_elyza = get_tokenizer_elyza_8b()
model_elyza = get_model_elyza_8b()

pipe_elyza = pipeline(
    "text-generation",
    model=model_elyza,
    tokenizer=tokenizer_elyza,
    device=0
    )
llm_elyza = HuggingFacePipeline(pipeline=pipe_elyza)

# 生成AIにプロンプトを連携
result = llm_elyza(
    """
    指示：
    あなたは優秀なプログラマです。
    以下のテーマについて、word文書を校閲するコードを作成してください。
    まずはdataディレクトリにあるwordファイルを読み取ります。
    そしてそのファイルから必要な情報を抽出し、校閲処理を行なったものを再度wordファイルに書き出す想定です。
    校閲を実行した語にはハイライトを付与してください。

    ①全角から半角への変換
    ・英数字および記号
        原則：英数字および記号は半角で統一
        例外：ローマ数字,ギリシャ文字,数式文字,「〜,：,％」,『全角小文字アルファベットの直後に用いられ、項目番号として使用されているもの』は全角とする
    ・項目番号の一部として使用される括弧
    ・桁数字として用いられるカンマ


    ②半角から全角への変換
    半角から全角への変換
    ・ローマ数字,ギリシャ文字,数式文字,「〜,：,％」,『全角小文字アルファベットの直後に用いられ、項目番号として使用されているもの』
    ・括弧
        原則：括弧は全角で統一
        例外：項目番号の一部として使用される場合は半角とする
    ・カンマ
        原則：カンマは全角で統一
        例外：桁数字として用いられる場合は半角とする

    回答：
    """
)

# プロンプトの内容を踏まえ、生成AIがコマンドライン上にプログラムを生成する
answer = result.split("回答：")[-1].strip()
print("-"*10 + "判定結果" + "-"*10)
print(answer)
