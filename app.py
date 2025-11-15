#「app.py」にコードを記述してください。
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

# APIキーが設定されていない場合の警告
if not OPENAI_API_KEY:
    st.error("環境変数 OPENAI_API_KEY が設定されていません。.env ファイルを確認してください。")
    st.stop()

st.title("専門家LLMアプリ")
st.write("このアプリは、入力テキストに基づいて異なる専門家として振る舞うLLMを利用しています。ラジオボタンで専門家の種類を選択し、テキストを入力して送信してください。LLMが選択した専門家として回答します。")

def get_expert_response(input_text: str, expert_type: str) -> str:
    """入力テキストと専門家の種類に基づいて、LLMからの回答を取得する。"""
    try:
        # LLMの初期化
        llm = ChatOpenAI(temperature=0, api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")

        # 専門家の種類に応じたシステムメッセージの設定
        if expert_type == "医療専門家":
            system_message = SystemMessage(content="あなたは医療専門家です。患者の質問に対して正確で丁寧に回答してください。医学的根拠のない診断は行わないでください。")
        elif expert_type == "法律専門家":
            system_message = SystemMessage(content="あなたは法律専門家です。法律に関する質問に対して明確で正確に回答してください。")
        else:
            system_message = SystemMessage(content="あなたは一般的な知識を持つアシスタントです。")

        # ユーザーメッセージの作成
        human_message = HumanMessage(content=input_text)

        # チャットメッセージのリストを作成
        messages = [system_message, human_message]

        # LLMにメッセージを渡して回答を取得
        response = llm(messages)

        return response.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# ラジオボタンで専門家の種類を選択
expert_type = st.radio("専門家の種類を選択してください:", ("医療専門家", "法律専門家"))

# テキスト入力フォーム
input_text = st.text_input("質問を入力してください:")

# 送信ボタン
if st.button("送信"):
    if input_text.strip():
        with st.spinner("回答を生成中..."):
            # LLMからの回答を取得
            answer = get_expert_response(input_text, expert_type)
            # 回答を表示
            st.write("LLMの回答:")
            st.write(answer)
    else:
        st.warning("質問を入力してください。")