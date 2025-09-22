# 医療情報RAG PoC デモ

このツールは、**厚労省・学会などホワイトリストに登録された信頼できるサイトのみを根拠に**、日本語で質問に答えることができます。  
回答は **「結論 / 根拠 / 注意点 / 出典」** の形式で表示され、出典URLを必ず確認できます。  

⚠️ 本ツールは診断・治療を目的としたものではなく、情報提供のみを目的としています。

---

## 🚀 デモURL
👉 [Streamlit Cloudでデモを見る](https://medicalragdemo-9x87xea88vfrzmepesvhjr.streamlit.app/)

---

## 🛠️ 使用技術
- **Google Custom Search API**  
  → ホワイトリストのURLのみを対象に検索
  https://cse.google.com/cse?cx=a348500516c4940fb
- **OpenAI GPT-4o-mini**  
  → 検索結果を日本語で要約・整形（幻覚防止ルールを適用）  
- **Streamlit**  
  → ブラウザから直接アクセス可能なシンプルなUI  
- **Secrets管理**  
  → APIキーは `.env` や Streamlit Cloud の Secrets に安全に保存

<img width="416" height="660" alt="Image" src="https://github.com/user-attachments/assets/d8d37a5d-0ab7-4904-9488-6672318754db" />

---

## 💡 使い方
1. テキストボックスに質問を入力（例: `2型糖尿病の降圧目標は？`）  
2. 数秒で「結論 / 根拠 / 注意点 / 出典」が表示されます  
3. 出典URLをクリックして一次情報を確認できます
<img width="739" height="471" alt="Image" src="https://github.com/user-attachments/assets/135a5574-1de3-4a6c-8a42-cc2ae0429bb5" />


---

## 🅿️ ポイント
- 情報源を絞り込んでいるため、出典がないものについては該当なしと表示される
<img width="740" height="529" alt="Image" src="https://github.com/user-attachments/assets/455f5f05-a977-4b9f-af5e-5cb70fe02f94" />


---

## 📌 デモ用シナリオ例
- 「2型糖尿病の降圧目標は？」  
- 「インフルエンザの検査タイミングと隔離期間」  
