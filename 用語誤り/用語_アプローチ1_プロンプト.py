import sys
import os

# 現在のファイルパスを取得(用語誤りディレクトリ内で本プログラムを実行するために使用)
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

    ①「とき」と「時」の校閲
    テキストから「とき」または「時」を含む部分を抽出し、それぞれの語の使用文脈に基づき修正を行ってください。
    - 「とき」が文脈内で時点を意味する場合には「時」に修正してください。
    - 「時」が文脈内で条件を示す場合には「とき」に修正してください。

    ②「ほか」を意味する語の校閲
    テキストから「他」「外」を含む部分を抽出し、複合語ではなく単独で用いられている場合には「ほか」に修正してください。

    回答：
    """
)

# プロンプトの内容を踏まえ、生成AIがコマンドライン上にプログラムを生成する
answer = result.split("回答：")[-1].strip()
print("-"*10 + "判定結果" + "-"*10)
print(answer)
