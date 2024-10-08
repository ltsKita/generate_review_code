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

    ステップ1:名前空間の設定
    名前空間は以下のものを使用してください。
    namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    名前空間プレフィックスwを、この名前空間URIに対応させて設定します。この設定は、後続の要素検索や操作に必須です。

    ステップ2:xml形式の処理対象ファイル読み取り
    xmlディレクトリの直下、さらにwordディレクトリの直下にあるdocument.xmlファイルを読み取ります。
    lxmlモジュールを使用してXMLをパースし、名前空間を利用できるようにします。
    ファイルが存在しない場合、適切なエラーメッセージを表示してください。

    ステップ3:要素の抽出
    <w:p>要素ごとにテキストを処理します。
    <w:p>要素の子要素に<w:r>要素があり、さらに<w:r>要素の子要素である<w:t>要素を検索し、テキスト情報を取得します。
    この際、名前空間を指定してfindallメソッドを使うことに注意してください。
    抽出したテキストは、ログに出力して確認できるようにしてください。

    ステップ4:正規表現ルールの作成
    以下の要素に対して、全角のものを検出して半角に修正する正規表現の辞書ルールを作成してください。
        ・英数字および記号(ローマ数字,ギリシャ文字,数式文字,「〜,：,％」,『全角小文字アルファベットの直後に用いられ、項目番号として使用されているもの』は除く)
        ・項目番号の一部として使用される括弧(項目番号例：「(1),(ⅰ),(a),(a-1),(a-1-1)」)
        ・桁数字として用いられるカンマ

    ステップ5:正規表現ルールの作成
    以下の要素に対して、半角のものを検出して全角に修正する正規表現の辞書ルールを作成してください。
        ・ローマ数字,ギリシャ文字,数式文字,「〜,：,％」,『全角小文字アルファベットの直後に用いられ、項目番号として使用されているもの』
        ・項目番号ではない箇所で使用されている括弧(項目番号例：「(1),(ⅰ),(a),(a-1),(a-1-1)」)
        ・桁数字以外の箇所で用いられるカンマ

    ステップ6:ルールを用いて対象テキストを取得
    ステップ4,5で作成した正規表現ルールを元に、修正が必要な文章を取得してください。

    ステップ7:ルールを用いて対象テキストを置換
    ステップ6で取得した文章に対して、ステップ4,5で作成した正規表現ルールを用いて元の<w:t>要素のテキストの該当文字列のみを置換してください。

    ステップ8:ハイライト付与
    今回の処理で変更があったテキストは<w:rPr>タグを用いてハイライト(黄色)を付与してしてください。

    それでは各ステップごとの要件を満たすコードをステップバイステップで作成してください。
    回答：
    """
)

# プロンプトの内容を踏まえ、生成AIがコマンドライン上にプログラムを生成する
answer = result.split("回答：")[-1].strip()
print("-"*10 + "判定結果" + "-"*10)
print(answer)
