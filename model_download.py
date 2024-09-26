"""
このファイルでは生成AIモデルのダウンロードと読み込みを行います。
ダウンロードが済んでいない場合はこちらのプログラムを実行してください。
"""
from transformers import AutoModelForCausalLM, AutoTokenizer

# 生成AIのモデル名を指定
model_name_elyza_8b = "elyza/Llama-3-ELYZA-JP-8B"
# モデル格納先ディレクトリを指定
model_dir = "/datadrive/model" 

# トークナイザーとモデルを指定ディレクトリにダウンロード
tokenizer_elyza_8b = AutoTokenizer.from_pretrained(model_name_elyza_8b, cache_dir=model_dir)
model_elyza_8b = AutoModelForCausalLM.from_pretrained(model_name_elyza_8b, cache_dir=model_dir)

def get_tokenizer_elyza_8b():
    # トークナイザーを別ファイルで使用するための関数
    return tokenizer_elyza_8b

def get_model_elyza_8b():
    # モデルを別ファイルで使用するための関数
    return model_elyza_8b