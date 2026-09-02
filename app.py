import streamlit as st
import pandas as pd
from groq import Groq

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
    現状と改善案を整理し、
    コスト・物流効率・品質・供給安定性・BCPなどの観点から
    改善案を評価する卒業研究用アプリです。
    """
)

st.warning(
    "会社名、取引先名、実際の原価などの機密情報は入力せず、"
    "匿名化または架空のデータを使用してください。"
)

st.divider()


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
    "現在の物流ネットワークについて、基本的な条件を入力してください。"
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

distance_difference = current_distance - improved_distance
frequency_difference = current_frequency - improved_frequency
leadtime_difference = current_leadtime - improved_leadtime

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


st.subheader("物流条件の変化")

result_col1, result_col2, result_col3 = st.columns(3)

with result_col1:

    st.metric(
        "輸送距離",
        f"{current_distance:,} → {improved_distance:,} km",
    )

with result_col2:

    st.metric(
        "月間輸送回数",
        f"{current_frequency:,} → {improved_frequency:,} 回",
    )

with result_col3:

    st.metric(
        "リードタイム",
        f"{current_leadtime:,.1f} → {improved_leadtime:,.1f} 日",
    )

st.divider()


# ==========================================
# STEP 4：改善テーマ別の確認観点
# ==========================================

st.header("4．改善時に確認すべき観点")

st.write(
    """
    選択した改善テーマに応じて、
    見落としやすい確認項目をアプリ側から提示します。
    """
)


# ==========================================
# テーマ別チェックリスト
# ==========================================

checklists = {

    "委託加工先の変更": [

        {
            "category": "品質",
            "question": "新しい委託加工先への変更によって、品質の安定性はどう変化しますか？",
            "check": [
                "品質保証体制や品質管理基準を確認する",
                "過去の品質実績や不良実績を確認する",
                "品質承認や監査が必要か確認する",
            ],
        },

        {
            "category": "供給安定性",
            "question": "必要数量を安定して生産できる供給能力はどう変化しますか？",
            "check": [
                "通常時の生産能力を確認する",
                "繁忙期の最大生産能力を確認する",
                "設備トラブル発生時の対応力を確認する",
            ],
        },

        {
            "category": "供給安定性",
            "question": "原材料不足や設備停止を含む供給リスクはどう変化しますか？",
            "check": [
                "原材料の調達先や調達安定性を確認する",
                "設備停止時の代替設備を確認する",
                "供給停止時の復旧期間を確認する",
            ],
        },

        {
            "category": "BCP",
            "question": "災害やトラブル発生時のBCP対応力はどう変化しますか？",
            "check": [
                "代替生産拠点の有無を確認する",
                "災害時の物流ルートを確認する",
                "特定拠点への依存度を確認する",
            ],
        },

        {
            "category": "在庫",
            "question": "委託加工先変更によって必要在庫量はどう変化しますか？",
            "check": [
                "安全在庫の増減を確認する",
                "切替時に必要な先行在庫を確認する",
                "仕掛品や半製品在庫への影響を確認する",
            ],
        },

        {
            "category": "切替リスク",
            "question": "委託加工先の切替や立上げに伴うリスクはどう変化しますか？",
            "check": [
                "立上げ期間を確認する",
                "品質承認期間を確認する",
                "システムや発注方法の変更有無を確認する",
            ],
        },

    ],


    "物流拠点の変更": [

        {
            "category": "物流効率",
            "question": "物流拠点変更によって輸送効率はどう変化しますか？",
            "check": [
                "主要需要地までの輸送距離を確認する",
                "輸送回数の増減を確認する",
                "積載効率への影響を確認する",
            ],
        },

        {
            "category": "在庫",
            "question": "物流拠点変更によって必要在庫量はどう変化しますか？",
            "check": [
                "安全在庫の増減を確認する",
                "在庫分散・集約による影響を確認する",
                "在庫移動費用を確認する",
            ],
        },

        {
            "category": "供給安定性",
            "question": "新しい物流拠点の保管・出荷能力は十分ですか？",
            "check": [
                "倉庫保管能力を確認する",
                "入出庫能力を確認する",
                "作業人員の確保状況を確認する",
            ],
        },

        {
            "category": "品質",
            "question": "新しい物流拠点によって品質リスクはどう変化しますか？",
            "check": [
                "保管温度や湿度条件を確認する",
                "荷扱い方法を確認する",
                "保管期間の変化を確認する",
            ],
        },

        {
            "category": "BCP",
            "question": "物流拠点変更によってBCP対応力はどう変化しますか？",
            "check": [
                "災害リスクを確認する",
                "代替倉庫の有無を確認する",
                "代替輸送ルートを確認する",
            ],
        },

        {
            "category": "切替リスク",
            "question": "物流拠点切替時のリスクはどう変化しますか？",
            "check": [
                "在庫移動計画を確認する",
                "システム切替の必要性を確認する",
                "切替期間中の供給方法を確認する",
            ],
        },

    ],


    "輸送ルートの変更": [

        {
            "category": "物流効率",
            "question": "輸送ルート変更によって輸送効率はどう変化しますか？",
            "check": [
                "輸送距離を確認する",
                "輸送時間を確認する",
                "積載効率を確認する",
            ],
        },

        {
            "category": "供給安定性",
            "question": "輸送の安定性はどう変化しますか？",
            "check": [
                "渋滞や交通規制の影響を確認する",
                "輸送会社の対応能力を確認する",
                "輸送停止時の代替方法を確認する",
            ],
        },

        {
            "category": "品質",
            "question": "輸送方法の変更による品質への影響はありますか？",
            "check": [
                "振動や衝撃への影響を確認する",
                "温度管理条件を確認する",
                "輸送時間増減による影響を確認する",
            ],
        },

        {
            "category": "BCP",
            "question": "災害発生時の輸送対応力はどう変化しますか？",
            "check": [
                "代替輸送ルートを確認する",
                "別の輸送会社を利用できるか確認する",
                "道路寸断時の代替手段を確認する",
            ],
        },

        {
            "category": "在庫",
            "question": "輸送条件変更によって必要在庫量はどう変化しますか？",
            "check": [
                "安全在庫への影響を確認する",
                "輸送頻度変更による影響を確認する",
                "リードタイム変化による影響を確認する",
            ],
        },

    ],


    "保管場所の変更": [

        {
            "category": "在庫",
            "question": "保管場所変更によって必要在庫量はどう変化しますか？",
            "check": [
                "保管可能数量を確認する",
                "安全在庫への影響を確認する",
                "在庫移動の必要量を確認する",
            ],
        },

        {
            "category": "品質",
            "question": "保管場所変更による品質への影響はありますか？",
            "check": [
                "温度や湿度条件を確認する",
                "保管設備を確認する",
                "荷扱い方法を確認する",
            ],
        },

        {
            "category": "物流効率",
            "question": "新しい保管場所によって輸送効率はどう変化しますか？",
            "check": [
                "工場からの距離を確認する",
                "顧客までの距離を確認する",
                "輸送回数への影響を確認する",
            ],
        },

        {
            "category": "供給安定性",
            "question": "新しい保管場所の運営能力は十分ですか？",
            "check": [
                "入出庫能力を確認する",
                "作業人員を確認する",
                "繁忙期の対応能力を確認する",
            ],
        },

        {
            "category": "BCP",
            "question": "保管場所変更によってBCP対応力はどう変化しますか？",
            "check": [
                "災害リスクを確認する",
                "代替倉庫を確認する",
                "在庫分散の必要性を確認する",
            ],
        },

    ],


    "その他の物流改善": [

        {
            "category": "物流効率",
            "question": "今回の改善によって物流効率はどう変化しますか？",
            "check": [
                "輸送距離への影響を確認する",
                "輸送回数への影響を確認する",
                "リードタイムへの影響を確認する",
            ],
        },

        {
            "category": "品質",
            "question": "製品品質への影響はありますか？",
            "check": [
                "保管・輸送・荷扱いへの影響を確認する",
                "品質保証方法を確認する",
            ],
        },

        {
            "category": "供給安定性",
            "question": "安定供給への影響はありますか？",
            "check": [
                "供給能力を確認する",
                "設備停止時の対応を確認する",
            ],
        },

        {
            "category": "BCP",
            "question": "BCP上のリスクはどう変化しますか？",
            "check": [
                "代替手段の有無を確認する",
                "特定拠点への依存度を確認する",
            ],
        },

        {
            "category": "在庫",
            "question": "必要在庫量への影響はありますか？",
            "check": [
                "安全在庫への影響を確認する",
                "在庫保有期間を確認する",
            ],
        },

    ],

}


selected_questions = checklists[improvement_theme]

st.info(
    f"「{improvement_theme}」を検討する場合は、"
    f"以下の観点も確認してください。"
)

for index, item in enumerate(selected_questions):

    st.markdown(
        f"**{index + 1}．【{item['category']}】{item['question']}**"
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

current_annual_total = current_monthly_total * 12

improved_annual_total = improved_monthly_total * 12

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
# STEP 6：コスト以外の評価
# ==========================================

st.header("6．コスト以外の評価")

st.write(
    """
    STEP4で提示された確認項目について、
    改善後にどのような変化があるか評価してください。
    """
)

evaluation_options = [
    "選択してください",
    "改善する",
    "変わらない",
    "悪化する",
    "不明",
]

evaluation_results = []


for index, item in enumerate(selected_questions):

    st.subheader(
        f"{index + 1}．{item['category']}"
    )

    st.write(
        item["question"]
    )

    answer = st.selectbox(
        "評価を選択してください",
        evaluation_options,
        key=f"evaluation_{improvement_theme}_{index}",
    )

    evaluation_results.append(
        {
            "分類": item["category"],
            "確認項目": item["question"],
            "評価": answer,
        }
    )


    # ======================================
    # 悪化する場合
    # ======================================

    if answer == "悪化する":

        st.warning(
            "⚠️ この項目は悪化する可能性があります。"
            "以下の点を追加で確認してください。"
        )

        for check_item in item["check"]:

            st.write(
                f"・{check_item}"
            )


    # ======================================
    # 不明の場合
    # ======================================

    elif answer == "不明":

        st.warning(
            "❓ 現時点では判断できていません。"
            "以下の情報を確認すると評価しやすくなります。"
        )

        for check_item in item["check"]:

            st.write(
                f"・{check_item}"
            )


    # ======================================
    # 改善する場合
    # ======================================

    elif answer == "改善する":

        st.success(
            "改善効果が期待されています。"
            "改善すると判断した根拠も確認しておきましょう。"
        )

        improvement_basis = st.text_area(
            "改善すると判断した根拠",
            placeholder="例：委託先から設備能力資料を受領し、必要数量を満たすことを確認した",
            key=f"basis_{improvement_theme}_{index}",
        )


    st.write("---")


# ==========================================
# 評価集計
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


st.subheader("定性評価の集計")

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
# 注意項目抽出
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
        "現在の入力では、未確認または悪化している項目はありません。"
    )

else:

    for item in attention_items:

        st.warning(
            f"【{item['分類']}】"
            f"{item['確認項目']} "
            f"→ {item['評価']}"
        )


st.divider()


# ==========================================
# STEP 7：総合評価
# ==========================================

st.header("7．改善案の総合評価")

st.write(
    "物流条件、コスト、品質、供給安定性、BCPなどをまとめて確認します。"
)


# ==========================================
# 改善概要
# ==========================================

st.subheader("📋 改善概要")

st.write(
    f"**改善テーマ：** {improvement_theme}"
)

if current_network:

    st.write(
        f"**現在の物流ネットワーク：** {current_network}"
    )

if improved_network:

    st.write(
        f"**改善後の物流ネットワーク：** {improved_network}"
    )

if improvement_reason:

    st.write(
        f"**改善を検討する理由：** {improvement_reason}"
    )


# ==========================================
# 物流条件
# ==========================================

st.subheader("🚚 物流条件")

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:

    st.metric(
        "輸送距離",
        f"{current_distance:,} → {improved_distance:,} km",
    )

    st.write(
        f"変化率：{distance_reduction_rate:,.1f}%"
    )

with summary_col2:

    st.metric(
        "輸送回数",
        f"{current_frequency:,} → {improved_frequency:,} 回",
    )

    st.write(
        f"変化率：{frequency_reduction_rate:,.1f}%"
    )

with summary_col3:

    st.metric(
        "リードタイム",
        f"{current_leadtime:,.1f} → {improved_leadtime:,.1f} 日",
    )

    st.write(
        f"変化率：{leadtime_reduction_rate:,.1f}%"
    )


# ==========================================
# コスト比較
# ==========================================

st.subheader("💰 コスト評価")

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
# コストグラフ
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
# 定性評価結果
# ==========================================

st.subheader("🛡️ コスト以外の評価結果")

evaluation_df = pd.DataFrame(
    evaluation_results
)

st.dataframe(
    evaluation_df,
    use_container_width=True,
    hide_index=True,
)


# ==========================================
# 総合コメント
# ==========================================

st.subheader("📊 総合コメント")


if unselected_count > 0:

    st.warning(
        f"まだ {unselected_count} 項目が未回答です。"
        "すべての確認項目を評価したうえで総合判断してください。"
    )


elif annual_difference > 0 and worsened_count == 0 and unknown_count == 0:

    st.success(
        f"改善案では年間約 {annual_difference:,.0f} 円の"
        "コスト削減が見込まれます。"
        "また、現在の入力では悪化・不明となっている確認項目はありません。"
        "詳細条件を確認したうえで、改善案を検討する価値があります。"
    )


elif annual_difference > 0 and (
    worsened_count > 0 or unknown_count > 0
):

    st.warning(
        f"改善案では年間約 {annual_difference:,.0f} 円の"
        "コスト削減が見込まれます。"
        f"一方で、悪化が {worsened_count} 項目、"
        f"不明が {unknown_count} 項目あります。"
        "コストだけで判断せず、注意項目を確認したうえで判断してください。"
    )


elif annual_difference <= 0 and improved_count > 0:

    st.info(
        "コスト面では明確な削減効果が確認できません。"
        "ただし、品質・供給安定性・物流条件などで"
        "改善効果がある可能性があります。"
        "コスト以外の効果も含めて総合的に判断してください。"
    )


else:

    st.warning(
        "現在の条件では大きな改善効果が確認できません。"
        "物流条件・コスト条件・リスク評価を再確認してください。"
    )

# ==========================================
# STEP 8：AIによる追加分析
# ==========================================

st.divider()

st.header("8．🤖 AIによる追加分析")

st.write(
    """
    これまで入力した改善内容・物流条件・コスト・リスク評価をもとに、
    AIが追加で確認すべきリスクや検討事項を整理します。
    """
)

st.info(
    "AI分析を実行すると入力内容が外部AIサービスへ送信されます。"
    "会社名・取引先名・実際の原価などの機密情報は入力せず、"
    "匿名化・架空データで利用してください。"
)


# ==========================================
# 定性評価をAI用の文章に変換
# ==========================================

evaluation_text = ""

for result in evaluation_results:
    evaluation_text += (
        f"- {result['分類']}："
        f"{result['確認項目']} "
        f"→ 評価：{result['評価']}\n"
    )


# ==========================================
# AIへの指示文
# ==========================================

ai_prompt = f"""
以下は、物流ネットワーク改善案について
利用者が入力した評価結果です。

【改善テーマ】
{improvement_theme}

【現在の物流ネットワーク】
{current_network}

【改善後の物流ネットワーク】
{improved_network}

【改善を検討している理由】
{improvement_reason}

【月間取扱数量】
{monthly_quantity:,} 個

【物流条件】

輸送距離：
現行 {current_distance:,} km
改善後 {improved_distance:,} km

月間輸送回数：
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
            f"STEP6に未回答の項目が {unselected_count} 件あります。"
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
