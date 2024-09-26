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
    xmlファイルに対して、以下の処理を行う文書校閲プログラム作成してください。
    変更内容は元のxmlファイルに上書きする形で反映させてください。

    ステップ1:ファイルの読み込み
    dataディレクトリにあるWordファイルを解凍し、xml形式のファイルを作成します。

    ステップ2:情報の抽出
    xmlファイルからテキストを抽出します。
    正常に抽出できているか確認します。

    ステップ3:修正ルールの作成
    作成するルールは2点あります。
    ①「とき」と「時」の修正
        ・文脈上、「とき」が時点を意味していると判断できる場合は「時」に修正する。
        ・文脈上、「時」が条件を意味していると判断できる場合は「とき」に修正する。
    ②「他」と「外」の修正
        ・文脈上、「外」を「ほか」と読むのが適切であれば「ほか」に修正する。
        ・文脈上、「他」が「ほか」と読むのが適切であれば「ほか」に修正する。
    
    ステップ4:処理分岐判定
    抽出したテキストが、(「とき」または「時」,「他」または「外」)のいずれを含むか判断してください。
    「とき」または「時」を含む場合には「①「とき」と「時」の修正」のルールを適用します。
    「他」または「外」を含む場合には「②「他」と「外」の修正」のルールを適用します。

    ステップ5:作成したルールの適用
    ステップ4の結果を踏まえてテキストの修正を行なってください。
    今回の処理で変更があったテキストにはハイライト(黄色)を付与してしてください。

    ステップ6:ファイル出力
    修正後のテキストを確認し、最終的な出力結果を元のxmlファイルに反映します。
    修正を行なったxmlファイルから新しいWordファイルを作成します。

    それでは、この要件を全て満たすコードをステップバイステップで作成してください。

    回答：
    """
)

# プロンプトの内容を踏まえ、生成AIがコマンドライン上にプログラムを生成する
answer = result.split("回答：")[-1].strip()
print("-"*10 + "判定結果" + "-"*10)
print(answer)
