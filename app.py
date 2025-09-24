import streamlit as st
import requests
from openai import OpenAI
import os
import csv
from datetime import datetime

# APIキー（Secretsから取得）
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
CX = os.environ["GOOGLE_CX"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)
LOG_FILE = "logs.csv"

# --- Google検索 ---
def search_whitelist(query, top_k=3):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": GOOGLE_API_KEY, "cx": CX, "q": query}
    res = requests.get(url, params=params).json()
    return res.get("items", [])[:top_k]

# --- ログ保存 ---
def save_log(query, conclusion, reason, caution, sources, full_answer):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, query, conclusion, reason, caution, "; ".join(sources), full_answer])

# --- 回答生成 ---
def answer_with_sources(query):
    results = search_whitelist(query)
    if not results:
        return "検索結果が見つかりませんでした。", "", "", "", []

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

    answer = completion.choices[0].message.content

    # セクションごとに分割
    conclusion, reason, caution, sources = "", "", "", []
    for line in answer.splitlines():
        if line.startswith("- 結論："):
            conclusion = line.replace("- 結論：", "").strip()
        elif line.startswith("- 根拠："):
            reason = line.replace("- 根拠：", "").strip()
        elif line.startswith("- 注意点："):
            caution = line.replace("- 注意点：", "").strip()
        elif line.startswith("- 出典："):
            pass
        elif line.strip().startswith("http"):
            sources.append(line.strip())

    # ログ保存
    save_log(query, conclusion, reason, caution, sources, answer)

    return answer, conclusion, reason, caution, sources


# --- UI部分 ---
st.title("医療情報RAG PoC")
st.warning("⚠️ 本ツールは情報源を絞り込むことでハレーションを予防し正確性の高い情報収集ができます。ただし、必ずしも正確とは限らないため、医療情報を使用する場合には必ず情報源の確認をしましょう。")

query = st.text_input("質問を入力してください（例: 2型糖尿病の降圧目標は？）")

if query:
    with st.spinner("検索中..."):
        answer, conclusion, reason, caution, sources = answer_with_sources(query)

        st.subheader("📌 回答")
        st.markdown(answer)

        st.subheader("📂 ログ（CSVダウンロード用）")
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            st.download_button(
                label="ログをCSVでダウンロード",
                data=f,
                file_name="logs.csv",
                mime="text/csv"
            )
