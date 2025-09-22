import streamlit as st
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

# .env の読み込み
load_dotenv()

# 環境変数からキーを取得
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def search_whitelist(query, top_k=3):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": GOOGLE_API_KEY, "cx": GOOGLE_CX, "q": query}
    res = requests.get(url, params=params).json()
    return res.get("items", [])[:top_k]


def answer_with_sources(query):
    results = search_whitelist(query)
    if not results:
        return "検索結果が見つかりませんでした。"

    snippets = "\n".join(
        [f"[{i+1}] {item['title']} - {item['snippet']} (URL: {item['link']})"
         for i, item in enumerate(results)]
    )

    prompt = f"""
質問: {query}

以下の検索結果をもとに、必ず次の形式で日本語で答えてください。
- 結論：
- 根拠：（短い引用＋脚注番号）
- 注意点：
- 出典：（番号付きでURL一覧）

検索結果:
{snippets}
"""

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return completion.choices[0].message.content

# UI部分
st.title("医療情報RAG PoC（デモ）")
st.warning("⚠️ 本ツールは診断・治療を目的とするものではありません（情報提供のみ）")

query = st.text_input("質問を入力してください（例: 2型糖尿病の降圧目標は？）")

if query:
    with st.spinner("検索中..."):
        answer = answer_with_sources(query)
        st.markdown(answer)
