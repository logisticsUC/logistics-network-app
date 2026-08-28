import streamlit as st
import pandas as pd


# ==========================================
# ページの基本設定
# ==========================================

st.set_page_config(
    page_title="物流ネットワーク評価アプリ",
    page_icon="🚚",
    layout="wide",
)


# ==========================================
# タイトル
# ==========================================

st.title("🚚 物流ネットワーク評価アプリ")

st.write(
    """
    製造業の物流ネットワークについて、
    現状と改善案を整理し、コスト・物流条件・リスクの観点から
    改善案を評価する卒業研究用アプリです。
    """
)

st.warning(
    "会社名、取引先名、実際の原価などの機密情報は入力せず、"
    "匿名化または架空のデータを使用してください。"
)


# ==========================================
# STEP 1：改善テーマの設定
# ==========================================

st.header("1．改善テーマの設定")

improvement_theme = st.selectbox(
    "今回、どのような物流改善を検討しますか？",
    [
        "物流拠点の変更",
        "委託加工先の変更",
        "輸送ルートの変更",
        "保管場所の変更",
        "その他の物流改善",
    ],
)


st.subheader("現在の物流ネットワーク")

current_network = st.text_area(
    "現在の物流の流れを入力してください",
    placeholder="例：工場 → 物流センター → 委託加工先 → 物流センター → 顧客",
)


st.subheader("検討する改善案")

improved_network = st.text_area(
    "改善後の物流の流れを入力してください",
    placeholder="例：工場 → 委託加工先 → 物流センター → 顧客",
)


improvement_reason = st.text_area(
    "この改善を検討している理由",
    placeholder="例：中間輸送を削減し、物流費とリードタイムを低減するため",
)


st.divider()


# ==========================================
# STEP 2：現在の物流状況
# ==========================================

st.header("2．現在の物流状況")

st.write(
    "現在の物流ネットワークについて、基本的な物流条件を入力してください。"
)


col1, col2 = st.columns(2)


with col1:

    monthly_quantity = st.number_input(
        "月間取扱数量（個）",
        min_value=0,
        value=100000,
        step=1000,
    )

    current_distance = st.number_input(
        "現在の輸送距離（km）",
        min_value=0,
        value=300,
        step=10,
    )


with col2:

    current_frequency = st.number_input(
        "現在の月間輸送回数（回）",
        min_value=0,
        value=20,
        step=1,
    )

    current_leadtime = st.number_input(
        "現在のリードタイム（日）",
        min_value=0.0,
        value=5.0,
        step=0.5,
    )


st.divider()


# ==========================================
# STEP 3：改善後の物流条件
# ==========================================

st.header("3．改善後の物流条件")

st.write(
    "改善を実施した場合の物流条件を入力してください。"
)


col1, col2 = st.columns(2)


with col1:

    improved_distance = st.number_input(
        "改善後の輸送距離（km）",
        min_value=0,
        value=180,
        step=10,
    )


with col2:

    improved_frequency = st.number_input(
        "改善後の月間輸送回数（回）",
        min_value=0,
        value=12,
        step=1,
    )

    improved_leadtime = st.number_input(
        "改善後のリードタイム（日）",
        min_value=0.0,
        value=3.0,
        step=0.5,
    )


# ==========================================
# 物流条件の改善効果
# ==========================================

st.subheader("物流条件の改善効果")


distance_difference = (
    current_distance - improved_distance
)

frequency_difference = (
    current_frequency - improved_frequency
)

leadtime_difference = (
    current_leadtime - improved_leadtime
)


if current_distance > 0:

    distance_reduction_rate = (
        distance_difference / current_distance
    ) * 100

else:

    distance_reduction_rate = 0


if current_frequency > 0:

    frequency_reduction_rate = (
        frequency_difference / current_frequency
    ) * 100

else:

    frequency_reduction_rate = 0


if current_leadtime > 0:

    leadtime_reduction_rate = (
        leadtime_difference / current_leadtime
    ) * 100

else:

    leadtime_reduction_rate = 0


result_col1, result_col2, result_col3 = st.columns(3)


with result_col1:

    st.metric(
        "輸送距離",
        f"{improved_distance:,} km",
        delta=f"{distance_difference:,.0f} km",
    )


with result_col2:

    st.metric(
        "月間輸送回数",
        f"{improved_frequency:,} 回",
        delta=f"{frequency_difference:,.0f} 回",
    )


with result_col3:

    st.metric(
        "リードタイム",
        f"{improved_leadtime:,.1f} 日",
        delta=f"{leadtime_difference:,.1f} 日",
    )


st.divider()


# ==========================================
# STEP 4：改善テーマ別チェックリスト
# ==========================================

st.header("4．改善時の確認項目")

st.write(
    """
    選択した改善テーマに応じて、
    コストだけでは判断しにくい品質・供給・BCPなどの観点を確認します。
    """
)


evaluation_options = [
    "選択してください",
    "改善する",
    "変わらない",
    "悪化する",
    "不明",
]


# ==========================================
# テーマ別の質問設定
# ==========================================

checklists = {

    "委託加工先の変更": [

        (
            "品質",
            "新しい委託加工先への変更によって、品質の安定性はどう変化しますか？"
        ),

        (
            "供給安定性",
            "必要数量を安定して生産できる供給能力はどう変化しますか？"
        ),

        (
            "供給安定性",
            "原材料不足や設備停止を含む供給リスクはどう変化しますか？"
        ),

        (
            "BCP",
            "災害やトラブル発生時のBCP対応力はどう変化しますか？"
        ),

        (
            "切替リスク",
            "委託加工先の切替や立上げに伴うリスクはどう変化しますか？"
        ),

        (
            "品質",
            "品質確認や承認に必要な負荷はどう変化しますか？"
        ),

        (
            "在庫",
            "切替時に必要となる在庫量はどう変化しますか？"
        ),

    ],


    "物流拠点の変更": [

        (
            "物流効率",
            "需要地までの輸送効率はどう変化しますか？"
        ),

        (
            "在庫",
            "拠点変更によって必要在庫量はどう変化しますか？"
        ),

        (
            "供給安定性",
            "新しい物流拠点の保管・出荷能力は十分ですか？"
        ),

        (
            "BCP",
            "災害発生時の代替拠点確保などBCP対応力はどう変化しますか？"
        ),

        (
            "切替リスク",
            "拠点移転や切替に伴う業務負荷・リスクはどう変化しますか？"
        ),

        (
            "品質",
            "保管環境や荷扱いによる品質リスクはどう変化しますか？"
        ),

    ],


    "輸送ルートの変更": [

        (
            "物流効率",
            "輸送距離や輸送時間は改善しますか？"
        ),

        (
            "供給安定性",
            "交通障害などによる輸送停止リスクはどう変化しますか？"
        ),

        (
            "品質",
            "輸送方法の変更による製品品質への影響はありますか？"
        ),

        (
            "BCP",
            "災害や道路寸断時の代替輸送ルートは確保できますか？"
        ),

        (
            "在庫",
            "輸送頻度の変更によって必要在庫量はどう変化しますか？"
        ),

        (
            "物流効率",
            "積載効率や輸送車両の使用効率はどう変化しますか？"
        ),

    ],


    "保管場所の変更": [

        (
            "在庫",
            "保管能力や必要在庫量はどう変化しますか？"
        ),

        (
            "品質",
            "温度・湿度・荷扱いなど保管品質への影響はありますか？"
        ),

        (
            "物流効率",
            "工場や顧客までの輸送効率はどう変化しますか？"
        ),

        (
            "供給安定性",
            "入出庫能力や作業人員の確保に問題はありませんか？"
        ),

        (
            "BCP",
            "災害発生時の在庫確保や代替倉庫への対応力はどう変化しますか？"
        ),

        (
            "切替リスク",
            "在庫移動や倉庫切替に伴うリスクはどう変化しますか？"
        ),

    ],


    "その他の物流改善": [

        (
            "物流効率",
            "今回の改善によって物流効率はどう変化しますか？"
        ),

        (
            "品質",
            "製品品質への影響はありますか？"
        ),

        (
            "供給安定性",
            "安定供給への影響はありますか？"
        ),

        (
            "BCP",
            "BCP上のリスクはどう変化しますか？"
        ),

        (
            "在庫",
            "必要在庫量への影響はありますか？"
        ),

        (
            "切替リスク",
            "改善実施時の切替リスクはありますか？"
        ),

    ],

}


selected_questions = checklists[improvement_theme]


st.info(
    f"「{improvement_theme}」で確認しておきたい項目を表示しています。"
)


evaluation_results = []


for index, question_data in enumerate(selected_questions):

    category = question_data[0]
    question = question_data[1]

    answer = st.selectbox(
        f"{index + 1}．【{category}】{question}",
        evaluation_options,
        key=f"evaluation_{improvement_theme}_{index}",
    )

    evaluation_results.append(
        {
            "分類": category,
            "確認項目": question,
            "評価": answer,
        }
    )


st.divider()


# ==========================================
# STEP 5：コスト条件の入力
# ==========================================

st.header("5．コスト条件の入力")

st.write(
    "現行案と改善案について、月間コストを入力してください。"
)


col1, col2 = st.columns(2)


# -------------------------
# 現行案
# -------------------------

with col1:

    st.subheader("🔵 現行案")

    current_transport = st.number_input(
        "現行案：月間物流費（円）",
        min_value=0,
        value=1000000,
        step=10000,
    )

    current_processing_unit = st.number_input(
        "現行案：加工単価（円／個）",
        min_value=0.0,
        value=50.0,
        step=1.0,
    )

    current_storage = st.number_input(
        "現行案：月間保管費（円）",
        min_value=0,
        value=200000,
        step=10000,
    )


# -------------------------
# 改善案
# -------------------------

with col2:

    st.subheader("🟢 改善案")

    improved_transport = st.number_input(
        "改善案：月間物流費（円）",
        min_value=0,
        value=600000,
        step=10000,
    )

    improved_processing_unit = st.number_input(
        "改善案：加工単価（円／個）",
        min_value=0.0,
        value=52.0,
        step=1.0,
    )

    improved_storage = st.number_input(
        "改善案：月間保管費（円）",
        min_value=0,
        value=150000,
        step=10000,
    )


# ==========================================
# コスト計算
# ==========================================

current_processing = (
    monthly_quantity * current_processing_unit
)

improved_processing = (
    monthly_quantity * improved_processing_unit
)


current_monthly_total = (
    current_transport
    + current_processing
    + current_storage
)

improved_monthly_total = (
    improved_transport
    + improved_processing
    + improved_storage
)


current_annual_total = (
    current_monthly_total * 12
)

improved_annual_total = (
    improved_monthly_total * 12
)


monthly_difference = (
    current_monthly_total
    - improved_monthly_total
)

annual_difference = (
    current_annual_total
    - improved_annual_total
)


if current_annual_total > 0:

    annual_reduction_rate = (
        annual_difference / current_annual_total
    ) * 100

else:

    annual_reduction_rate = 0


st.divider()


# ==========================================
# STEP 6：コスト・リスク評価
# ==========================================

st.header("6．コスト・リスク評価")


# ==========================================
# コスト比較
# ==========================================

st.subheader("💰 コスト比較")


result_df = pd.DataFrame(
    {
        "項目": [
            "月間物流費",
            "月間加工費",
            "月間保管費",
            "月間総コスト",
            "年間総コスト",
        ],

        "現行案": [
            current_transport,
            current_processing,
            current_storage,
            current_monthly_total,
            current_annual_total,
        ],

        "改善案": [
            improved_transport,
            improved_processing,
            improved_storage,
            improved_monthly_total,
            improved_annual_total,
        ],

    }
)


st.dataframe(
    result_df,
    use_container_width=True,
    hide_index=True,
)


cost_col1, cost_col2, cost_col3 = st.columns(3)


with cost_col1:

    st.metric(
        "月間コスト差額",
        f"{monthly_difference:,.0f} 円",
    )


with cost_col2:

    st.metric(
        "年間コスト差額",
        f"{annual_difference:,.0f} 円",
    )


with cost_col3:

    st.metric(
        "年間コスト変化率",
        f"{annual_reduction_rate:,.1f} %",
    )


# ==========================================
# 年間総コストグラフ
# ==========================================

st.subheader("年間総コスト比較")


chart_df = pd.DataFrame(
    {
        "年間総コスト": [
            current_annual_total,
            improved_annual_total,
        ]
    },

    index=[
        "現行案",
        "改善案",
    ],
)


st.bar_chart(chart_df)


# ==========================================
# 定性評価
# ==========================================

st.subheader("🔍 コスト以外の評価")


evaluation_df = pd.DataFrame(
    evaluation_results
)


st.dataframe(
    evaluation_df,
    use_container_width=True,
    hide_index=True,
)


# ==========================================
# 回答数を集計
# ==========================================

improved_count = 0
unchanged_count = 0
worsened_count = 0
unknown_count = 0
unselected_count = 0


for result in evaluation_results:

    if result["評価"] == "改善する":

        improved_count += 1

    elif result["評価"] == "変わらない":

        unchanged_count += 1

    elif result["評価"] == "悪化する":

        worsened_count += 1

    elif result["評価"] == "不明":

        unknown_count += 1

    else:

        unselected_count += 1


risk_col1, risk_col2, risk_col3, risk_col4 = st.columns(4)


with risk_col1:

    st.metric(
        "改善",
        f"{improved_count} 項目",
    )


with risk_col2:

    st.metric(
        "変化なし",
        f"{unchanged_count} 項目",
    )


with risk_col3:

    st.metric(
        "悪化",
        f"{worsened_count} 項目",
    )


with risk_col4:

    st.metric(
        "不明・未確認",
        f"{unknown_count + unselected_count} 項目",
    )


# ==========================================
# 注意が必要な項目
# ==========================================

st.subheader("⚠️ 注意・確認が必要な項目")


attention_items = []


for result in evaluation_results:

    if result["評価"] in [
        "悪化する",
        "不明",
        "選択してください",
    ]:

        attention_items.append(result)


if len(attention_items) == 0:

    st.success(
        "現在の入力では、明確な懸念項目はありません。"
    )

else:

    for item in attention_items:

        st.warning(
            f"【{item['分類']}】"
            f"{item['確認項目']} "
            f"→ 評価：{item['評価']}"
        )


st.divider()


# ==========================================
# STEP 7：総合評価
# ==========================================

st.header("7．改善案の総合評価")

st.write(
    "これまで入力した物流条件・コスト・リスクをまとめて確認します。"
)


# ==========================================
# 改善テーマ
# ==========================================

st.subheader("改善概要")

st.write(
    f"**改善テーマ：** {improvement_theme}"
)


if current_network:

    st.write(
        f"**現在：** {current_network}"
    )


if improved_network:

    st.write(
        f"**改善後：** {improved_network}"
    )


if improvement_reason:

    st.write(
        f"**改善を検討する理由：** {improvement_reason}"
    )


# ==========================================
# 物流改善結果
# ==========================================

st.subheader("🚚 物流条件の変化")


summary_col1, summary_col2, summary_col3 = st.columns(3)


with summary_col1:

    st.metric(
        "輸送距離",
        f"{current_distance:,} → {improved_distance:,} km",
        delta=f"{distance_difference:,.0f} km",
    )


with summary_col2:

    st.metric(
        "輸送回数",
        f"{current_frequency:,} → {improved_frequency:,} 回",
        delta=f"{frequency_difference:,.0f} 回",
    )


with summary_col3:

    st.metric(
        "リードタイム",
        f"{current_leadtime:,.1f} → {improved_leadtime:,.1f} 日",
        delta=f"{leadtime_difference:,.1f} 日",
    )


# ==========================================
# コスト改善結果
# ==========================================

st.subheader("💰 コスト評価")


if annual_difference > 0:

    st.success(
        f"改善案では年間約 {annual_difference:,.0f} 円の"
        f"コスト削減が見込まれます。"
    )

elif annual_difference < 0:

    st.warning(
        f"改善案では年間約 {abs(annual_difference):,.0f} 円の"
        f"コスト増加が見込まれます。"
    )

else:

    st.info(
        "現行案と改善案の年間総コストは同額です。"
    )


# ==========================================
# リスク評価結果
# ==========================================

st.subheader("🛡️ リスク・懸念事項")


if worsened_count == 0 and unknown_count == 0 and unselected_count == 0:

    st.success(
        "入力された評価では、悪化または未確認となっている項目はありません。"
    )

else:

    st.warning(
        f"悪化：{worsened_count}項目 ／ "
        f"不明・未確認：{unknown_count + unselected_count}項目"
    )


# ==========================================
# 総合コメント
# ==========================================

st.subheader("📋 総合コメント")


if unselected_count > 0:

    st.warning(
        "まだ回答していない確認項目があります。"
        "総合判断の前にチェックリストを確認してください。"
    )


elif annual_difference > 0 and worsened_count == 0 and unknown_count == 0:

    st.success(
        "コスト面で改善効果があり、"
        "現在の入力では大きなリスク悪化も確認されていません。"
        "実施条件や詳細内容を確認したうえで、"
        "改善案を検討する価値があります。"
    )


elif annual_difference > 0 and (
    worsened_count > 0 or unknown_count > 0
):

    st.warning(
        "コスト面では改善効果があります。"
        "一方で、悪化または未確認となっている項目があります。"
        "コスト効果だけで判断せず、"
        "注意項目を確認したうえで改善案を検討してください。"
    )


elif annual_difference <= 0 and improved_count > 0:

    st.info(
        "コスト削減効果は確認できませんが、"
        "物流条件や品質・供給など他の項目で改善効果がある可能性があります。"
        "コスト以外のメリットも含めて判断してください。"
    )


else:

    st.warning(
        "現在の入力では改善効果が限定的です。"
        "改善条件やコスト条件を再確認してください。"
    )


# ==========================================
# 注意事項
# ==========================================

st.divider()

st.caption(
    "本アプリは卒業研究用の試作版です。"
    "表示される評価は入力された情報に基づく検討支援であり、"
    "実際の投資・物流変更などの意思決定を保証するものではありません。"
)
