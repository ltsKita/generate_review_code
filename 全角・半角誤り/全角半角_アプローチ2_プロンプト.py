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
    xmlファイルに対して、以下の処理を行う文書校閲プログラム作成してください。
    変更内容は元のxmlファイルに上書きする形で反映させてください。

    ステップ1:ファイルの読み込み
    dataディレクトリにあるWordファイルを解凍し、xml形式のファイルを作成します。

    ステップ2:情報の抽出
    xmlファイルからテキストを抽出します。
    正常に抽出できているか確認します。

    ステップ3:正規表現ルールの作成
    以下の要素に対して、全角のものを検出して半角に修正する正規表現ルールを作成してください。
        ・英数字および記号(ローマ数字,ギリシャ文字,数式文字,「〜,：,％」,『全角小文字アルファベットの直後に用いられ、項目番号として使用されているもの』は除く)
        ・項目番号の一部として使用される括弧(項目番号例：「(1),(ⅰ),(a),(a-1),(a-1-1)」)
        ・桁数字として用いられるカンマ

    ステップ4:正規表現ルールの作成
    以下の要素に対して、半角のものを検出して全角に修正する正規表現ルールを作成してください。
        ・ローマ数字,ギリシャ文字,数式文字,「〜,：,％」,『全角小文字アルファベットの直後に用いられ、項目番号として使用されているもの』
        ・項目番号ではない箇所で使用されている括弧(項目番号例：「(1),(ⅰ),(a),(a-1),(a-1-1)」)
        ・桁数字以外の箇所で用いられるカンマ

    ステップ5:ルールを用いて対象テキストを取得
    ステップ3,4で作成した正規表現ルールを元に、修正が必要な文章を取得してください。

    ステップ6:ルールを用いて対象テキストを置換
    ステップ5で取得した文章に対して、ステップ3,4で作成した正規表現ルールを用いて元のテキストの該当文字列のみを置換してください。

    ステップ7:ハイライト付与
    今回の処理で変更があったテキストにはハイライト(黄色)を付与してしてください。

    ステップ8:ファイル出力
    修正後のテキストを確認し、最終的な出力結果を元のxmlファイルに反映します。
    修正を行なったxmlファイルから新しいWordファイルを作成します。

    それでは、ステップバイステップで要件を満たすコードを出力してください。
    回答：
    """
)

# プロンプトの内容を踏まえ、生成AIがコマンドライン上にプログラムを生成する
answer = result.split("回答：")[-1].strip()
print("-"*10 + "判定結果" + "-"*10)
print(answer)
