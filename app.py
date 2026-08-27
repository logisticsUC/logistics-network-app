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
    現状と改善案を整理し、コストを比較・評価する卒業研究用アプリです。
    """
)

# 機密情報に関する注意
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
    placeholder="例：工場 → 物流センター → 委託加工先 → 物流センター",
)

st.subheader("検討する改善案")

improved_network = st.text_area(
    "改善後の物流の流れを入力してください",
    placeholder="例：工場 → 委託加工先 → 物流センター",
)

improvement_reason = st.text_area(
    "なぜこの改善を検討していますか？",
    placeholder="例：中間輸送を削減し、物流費とリードタイムを低減するため",
)


# ==========================================
# STEP 2：基本条件
# ==========================================

st.header("2．基本条件")

monthly_quantity = st.number_input(
    "月間数量（個）",
    min_value=0,
    value=100000,
    step=1000,
)


# ==========================================
# STEP 3：現行案と改善案のコスト入力
# ==========================================

st.header("3．コスト条件の入力")

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
# STEP 4：コスト変化の理由
# ==========================================

st.header("4．コスト変化の理由")

st.write(
    "改善によって各コストが変化する理由を整理してください。"
)

transport_reason = st.text_area(
    "物流費が変化する理由",
    placeholder="例：中間拠点を削減し、輸送回数が減るため",
)

processing_reason = st.text_area(
    "加工費が変化する理由",
    placeholder="例：委託加工先を変更することで加工単価が上昇するため",
)

storage_reason = st.text_area(
    "保管費が変化する理由",
    placeholder="例：保管拠点を集約し、倉庫使用量が減るため",
)


# ==========================================
# コスト計算
# ==========================================

# 月間加工費
current_processing = (
    monthly_quantity * current_processing_unit
)

improved_processing = (
    monthly_quantity * improved_processing_unit
)

# 月間総コスト
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

# 年間総コスト
current_annual_total = (
    current_monthly_total * 12
)

improved_annual_total = (
    improved_monthly_total * 12
)

# 年間削減額
annual_difference = (
    current_annual_total
    - improved_annual_total
)


# ==========================================
# STEP 5：比較結果
# ==========================================

st.header("5．コスト比較結果")

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
)


# ==========================================
# 年間削減額
# ==========================================

st.subheader("改善効果")

st.metric(
    "改善案による年間削減額",
    f"{annual_difference:,.0f}円",
)


# ==========================================
# グラフ
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
# 注意事項
# ==========================================

st.caption(
    "本アプリは卒業研究用の試作版です。"
    "実際の投資判断を保証するものではありません。"
)
