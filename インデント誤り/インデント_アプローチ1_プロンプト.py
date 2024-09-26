import sys
import os

# 現在のファイルパスを取得(インデント誤りディレクトリ内で本プログラムを実行するために使用)
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

    ①
    本文各号については原則以下で統一し、このルールに当てはまらないインデントおよび項目番号を修正してください。
    具体的に行う校閲処理は3点です。
    ・インデント文字数を下記のように統一
    ・項目番号が連番となるように修正
    ・項目番号の表記(括弧、スペース、ハイフン)を下記のように統一
    また、先頭にインデントの文字数を記載しているが、その直後に続くものがそれぞれの項目番号です。
    "インデント0文字"イ，ロ，ハ・・・
    "インデント1文字"(1)，(2)，(3)・・・
    "インデント2文字"(ⅰ)，(ⅱ)，(ⅲ)・・・
    "インデント3文字"ａ．ｂ．ｃ．・・・
    "インデント4文字"(a)，(b)，(c)・・・
    "インデント5文字"(a-1)，(a-2)，(a-3)・・・
    "インデント6文字"(a-1-1)，(a-1-2)，(a-1-3)・・・


    ②
    添付各項については原則以下で統一し、このルールに当てはまらないインデントおよび項目番号を修正してください。
    具体的に行う校閲処理は4点です。
    ・インデント文字数を下記のように統一
    ・項目番号が連番となるように修正
    ・項目番号の表記(括弧、スペース、ハイフン)を下記のように統一
    また、先頭にインデントの文字数を記載しているが、その直後に続くものがそれぞれの項目番号です。
    "インデント0文字"1.␣・・・（全角スペース）
    "インデント0文字"1.1␣・・・（全角スペース）
    "インデント0文字"1.1.1␣・・・（全角スペース）
    "インデント0文字"1.1.1.1␣・・・（全角スペース）
    "インデント1文字"(1)，(2)，(3)␣・・・（半角スペース）
    "インデント2文字"ａ．ｂ．ｃ．・・・（スペースなし（英字及び．は全角））
    "インデント3文字"(a)，(b)，(c)␣・・・（半角スペース）
    "インデント4文字"(a-1)，(a-2)，(a-3) ␣・・・（半角スペース）
    "インデント5文字"(a-1-1)，(a-1-2)，(a-1-3) ␣・・・（半角スペース）


    回答：
    """
)

# プロンプトの内容を踏まえ、生成AIがコマンドライン上にプログラムを生成する
answer = result.split("回答：")[-1].strip()
print("-"*10 + "判定結果" + "-"*10)
print(answer)
