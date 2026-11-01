現行 {current_frequency:,} 回
改善後 {improved_frequency:,} 回

リードタイム：
現行 {current_leadtime:,.1f} 日
改善後 {improved_leadtime:,.1f} 日

【コスト】

現行年間総コスト：
{current_annual_total:,.0f} 円

改善後年間総コスト：
{improved_annual_total:,.0f} 円

年間コスト差額：
{annual_difference:,.0f} 円

【コスト以外の評価】

{evaluation_text}

上記をもとに、次の5項目について分析してください。

1. 改善案の主なメリット
2. 現在確認できる懸念点・リスク
3. 利用者が見落としている可能性があるリスク
4. 実施前に追加で確認すべき事項
5. 総合コメント

次のルールを必ず守ってください。

・入力されていない情報を事実として断定しない
・分からないことは「確認が必要」とする
・単純にコストが下がるという理由だけで改善案を推奨しない
・品質、供給安定性、在庫、リードタイム、BCP、切替リスクも考慮する
・入力済みの数値計算をやり直す必要はない
・利用者が気づいていない可能性のある観点を積極的に提示する
・最終判断をAIが断定せず、意思決定を支援する
・日本語で分かりやすく回答する
"""


# ==========================================
# AI分析ボタン
# ==========================================

if st.button(
    "🤖 AI分析を実行",
    type="primary",
    use_container_width=True,
):

    if unselected_count > 0:
        st.warning(
            f"STEP5に未回答の項目が {unselected_count} 件あります。"
            "AI分析は可能ですが、すべて回答した方が分析しやすくなります。"
        )

    try:

        # Streamlit SecretsからGroq APIキーを取得
        api_key = st.secrets["GROQ_API_KEY"]

        # Groqに接続
        client = Groq(
            api_key=api_key
        )

        with st.spinner(
            "AIが物流改善案を分析しています..."
        ):

            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "あなたは製造業の物流・サプライチェーン改善を"
                            "支援する専門アドバイザーです。"
                            "改善案を一方的に決定するのではなく、"
                            "利用者の意思決定を支援してください。"
                        ),
                    },
                    {
                        "role": "user",
                        "content": ai_prompt,
                    },
                ],

                temperature=0.3,
            )

        # AIの回答を取得
        ai_result = response.choices[0].message.content

        st.subheader("🤖 AI分析結果")

        st.markdown(ai_result)

        st.caption(
            "AIの回答は補助的な分析です。"
            "実際の改善判断では、現場条件や関係部門による確認が必要です。"
        )


    except KeyError:

        st.error(
            "Groq APIキーが見つかりません。"
            "StreamlitのSecretsに"
            "「GROQ_API_KEY」が登録されているか確認してください。"
        )


    except Exception as e:

        st.error(
            "AI分析中にエラーが発生しました。"
        )

        st.write("エラー内容：")

        st.code(str(e))
        
# ==========================================
# 最終的な注意事項
# ==========================================

st.divider()

st.caption(
    "本アプリは卒業研究用の試作版です。"
    "表示される評価は入力情報に基づく検討支援であり、"
    "実際の投資・物流変更・委託先変更などの意思決定を保証するものではありません。"
)
