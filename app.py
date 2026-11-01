import hashlib
import html
import json

import pandas as pd
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="LogiScope | 物流ネットワーク評価",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------
# デザイン（外部画像・追加ライブラリ不要）
# ------------------------------------------
CSS = r"""
<style>
:root { --navy:#112544; --blue:#2357ba; --cyan:#11a7c9; --ink:#152843;
        --sub:#61728b; --line:#e1e8f2; --bg:#f3f6fb; --mint:#087d73; }
html, body, [class*="css"] { font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", "Noto Sans JP", sans-serif; }
[data-testid="stAppViewContainer"] { background:var(--bg); }
[data-testid="stMainBlockContainer"] { padding-top: 1.5rem; padding-bottom: 4rem; max-width: 1330px; }
[data-testid="stSidebar"] { background: #12233e; }
[data-testid="stSidebar"] * { color: #e8effb; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#cbd8e9; }
[data-testid="stSidebar"] hr { border-color:#354b67; }
[data-testid="stSidebar"] a { color:#a9d5ff; }
[data-testid="stSidebar"] [data-testid="stAlert"] * { color:inherit; }
/* ヒーロー */
.ls-hero { position:relative; overflow:hidden; border-radius:22px; padding:32px 36px 30px;
  color:#fff; background:linear-gradient(117deg,#10223d 0%,#183967 54%,#155d8f 100%);
  box-shadow:0 15px 35px rgba(13,35,69,.12); margin: 4px 0 24px; }
.ls-hero:before { content:""; position:absolute; height:270px; width:270px; right:-30px; top:-110px;
  border-radius:100%; border:52px solid rgba(102,195,236,.11); }
.ls-hero:after { content:""; position:absolute; height:190px; width:190px; right:170px; bottom:-170px;
  border-radius:100%; border:42px solid rgba(255,255,255,.055); }
.ls-eyebrow {font-size:11px; letter-spacing:2px; color:#9cdbff; font-weight:750; margin-bottom:11px;}
.ls-hero h1 {font-size: clamp(29px,4.4vw,43px); line-height:1.27; letter-spacing:-.9px;
  color:white!important; margin: 0 0 10px; font-weight:820;}
.ls-hero h1 span {color:#86dbff; font-weight:600; font-size:.58em; margin-left:11px;}
.ls-hero p {position:relative; font-size:14px; line-height:1.8; color:#d5e7f8;
  max-width:780px; margin:0 0 18px;}
.ls-pill {display:inline-block; background:rgba(255,255,255,.09); border:1px solid rgba(255,255,255,.18);
  border-radius:100px; padding:5px 12px; font-size:11px; margin-right:7px; margin-top:6px; color:#f0faff;}
/* 見出し */
.ls-section {margin:11px 0 19px;}
.ls-step {font-size:10px;letter-spacing:2px;font-weight:800;color:#176fc0; margin-bottom:7px;}
.ls-section h2 {margin:0 0 4px; font-size:24px; letter-spacing:-.5px; color:#172e4d; font-weight:800;}
.ls-section p {font-size:13px;color:#61728b;line-height:1.7;margin:5px 0;}
.ls-subhead {font-size:14px;font-weight:760;color:#193b65;margin:0 0 13px;}
/* KPIカード */
.ls-kpi {background:white;border:1px solid var(--line);border-radius:16px;padding:19px 20px 17px;
  box-shadow:0 5px 17px rgba(33,58,95,.035);min-height:122px;}
.ls-kpi-label {font-size:12px; color:#65768e; margin-bottom:11px; font-weight:650;}
.ls-kpi-value {font-size:clamp(21px,2.2vw,30px); color:#172d4b; font-weight:800;letter-spacing:-.6px;line-height:1.26;}
.ls-kpi-foot {font-size:11px;color:#8190a3;margin-top:8px;}
.ls-kpi.is-good {border-top:3px solid #19a9a0;}
.ls-kpi.is-warn {border-top:3px solid #e1a34c;}
.ls-kpi.is-blue {border-top:3px solid #2a71d0;}
.ls-kpi.is-good .ls-kpi-value {color:#08796e;}
.ls-kpi.is-warn .ls-kpi-value {color:#ae6b24;}
/* インフォ・概要 */
.ls-banner {background:#e8f3ff;border-left:3px solid #3082d5; padding:12px 16px;
  border-radius:0 10px 10px 0; color:#244b73;font-size:12px;line-height:1.8;margin:7px 0 18px;}
.ls-sidebar-logo {font-size:25px;font-weight:820;letter-spacing:-1px;color:#fff;margin:5px 0 3px;}
.ls-sidebar-txt {font-size:11px;color:#9cacc4!important;line-height:1.8;}
.ls-sidebar-label {font-size:10px;letter-spacing:1px;color:#8ca6ca;font-weight:800;margin:22px 0 10px;}
.ls-sidebar-note {background:#203b5b;border:1px solid #375476;border-radius:10px;
  color:#d9e9f9;font-size:12px;line-height:1.85;padding:13px 14px;}
.ls-sidebar-step {font-size:12px; color:#d4e5f6; padding:8px 0; border-bottom:1px solid #2d405c;}
.ls-footer {border-top:1px solid #dfe7f0;margin-top:34px;padding-top:19px;color:#8693a5;font-size:11px;}
.ls-muted {font-size:12px;color:#60758f;}
.ls-split-title {font-size:12px;font-weight:800;letter-spacing:.5px;margin-bottom:9px;}
.ls-question {font-size:14px; font-weight:700; color:#243e5b; margin-bottom:6px; line-height:1.7;}
.ls-category {font-size:10px;font-weight:750;letter-spacing:.6px;background:#e5effc;
  color:#275e9d; padding:4px 9px;border-radius:50px;display:inline-block;margin-bottom:7px;}
.ls-route {background:#f4f8fd;border:1px dashed #c9d8eb;padding:12px 15px;border-radius:10px;
  font-size:13px;color:#344a62;line-height:1.8;white-space:pre-wrap;}
/* タブ */
.stTabs [data-baseweb="tab-list"] {gap:6px;overflow-x:auto;padding-bottom:5px;border-bottom:1px solid #dde6f0;}
.stTabs [data-baseweb="tab"] {border:1px solid transparent!important;background:#e9eef7!important;
  color:#4a5e79!important;border-radius:10px!important;font-weight:730!important;
  padding:10px 16px!important;height:auto;white-space:nowrap;}
.stTabs [data-baseweb="tab"][aria-selected="true"] {background:#1d477c!important;color:white!important;
  border-color:#1d477c!important;box-shadow:0 4px 9px rgba(20,55,96,.14);}
.stTabs [data-baseweb="tab-highlight"] {display:none;}
.stTabs [data-baseweb="tab-border"] {display:none;}
.stTabs [data-testid="stTabContent"] {padding-top:20px;}
/* 入力やコンテナ */
[data-testid="stVerticalBlockBorderWrapper"] > div {border-radius:16px!important;}
div[data-testid="stNumberInput"] input,div[data-testid="stTextArea"] textarea {
  border-radius:8px!important;}
div[data-testid="stButton"] button[kind="primary"] {background:linear-gradient(100deg,#1f57ab,#168ab9)!important;
  border:0!important;color:white!important;border-radius:10px!important;min-height:46px;
  font-weight:800;box-shadow:0 7px 16px rgba(31,87,171,.18);}
@media (max-width:750px) {
  .ls-hero {padding:24px 20px;border-radius:15px;}
  .ls-hero h1 span {display:block;margin:3px 0 0; font-size:.56em;}
  .ls-section h2 {font-size:21px;}
  .ls-kpi {padding:16px 14px;min-height:105px;}
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def safe(value):
    """画面上に入力内容をHTMLとして埋め込む際にエスケープする。"""
    return html.escape(str(value), quote=True)


def section(no, title, description):
    st.markdown(
        f'<div class="ls-section"><div class="ls-step">STEP {no} / 07</div>'
        f'<h2>{safe(title)}</h2><p>{safe(description)}</p></div>',
        unsafe_allow_html=True,
    )


def kpi(label, value, note="", tone="blue"):
    st.markdown(
        f'<div class="ls-kpi is-{safe(tone)}"><div class="ls-kpi-label">{safe(label)}</div>'
        f'<div class="ls-kpi-value">{safe(value)}</div>'
        f'<div class="ls-kpi-foot">{safe(note)}</div></div>',
        unsafe_allow_html=True,
    )


def yen(value):
    return f"¥{value:,.0f}"


def cost_trend_label(change):
    """コスト増減（改善案−現行案）：マイナスなら削減、プラスなら増加。"""
    return "コストDOWN（削減）" if change < 0 else ("コストUP（増加）" if change > 0 else "コスト変化なし")


def signed_yen(change):
    """金額を -¥200,000 / +¥200,000 / ¥0 の形式で表示する。"""
    if change < 0:
        return f"−{yen(abs(change))}"
    if change > 0:
        return f"＋{yen(change)}"
    return yen(0)


st.markdown("""
<div class="ls-hero">
  <div class="ls-eyebrow">SUPPLY CHAIN / DECISION SUPPORT</div>
  <h1>LogiScope <span>物流ネットワーク評価</span></h1>
  <p>物流ネットワークの現行案と改善案を、コスト・輸送効率・品質・安定供給・BCPの視点で比較。<br>
    意思決定に必要な数字とリスクをひとつの画面に整理します。</p>
  <span class="ls-pill">製造業向け</span><span class="ls-pill">7ステップ評価</span>
  <span class="ls-pill">AIによる追加分析</span><span class="ls-pill">研究プロトタイプ</span>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="ls-sidebar-logo">◈ LogiScope</div>'
                '<div class="ls-sidebar-txt">LOGISTICS NETWORK EVALUATOR<br>Prototype / University Research</div>',
                unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="ls-sidebar-label">EVALUATION FLOW</div>', unsafe_allow_html=True)
    for step_name in (
        "01　改善テーマ", "02　現状の物流条件", "03　改善後の物流条件", "04　コスト比較",
        "05　定性評価", "06　総合レポート", "07　AI追加分析",
    ):
        st.markdown(f'<div class="ls-sidebar-step">{step_name}</div>', unsafe_allow_html=True)
    st.markdown('<div class="ls-sidebar-label">DATA PRIVACY</div>', unsafe_allow_html=True)
    st.markdown('<div class="ls-sidebar-note">会社名・取引先名・実原価などの機密情報は使用せず、匿名化または架空データで評価してください。</div>',
                unsafe_allow_html=True)
    st.caption("AI分析を実行した場合、入力情報は外部AIサービス（Groq）に送信されます。")

# タブでは非表示のタブ内のPythonも毎回実行され、評価値を一括集計できる。
tab_theme, tab_flow, tab_cost, tab_risk, tab_report = st.tabs([
    "01  テーマ設定", "02  物流条件", "03  コスト分析", "04  リスク評価", "05  総合レポート",
])

with tab_theme:
    section("01", "改善テーマを設定", "検討する改善案と、物流ネットワークの変更内容を整理します。")
    st.markdown('<div class="ls-banner">選んだ改善テーマに合わせ、後半の「リスク評価」で確認すべき項目を自動で切り替えます。</div>', unsafe_allow_html=True)
    improvement_theme = st.selectbox(
        "検討する改善テーマ",
        ["物流拠点の変更", "委託加工先の変更", "輸送ルートの変更", "保管場所の変更", "その他の物流改善"],
        help="評価対象となる変更を選択してください。",
    )
    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.markdown("**CURRENT  /  現行ルート**")
            current_network = st.text_area(
                "現在の物流の流れ",
                placeholder="例：工場 → DC → OEM → DC → 顧客",
                height=115,
            )
    with right:
        with st.container(border=True):
            st.markdown("**PROPOSED  /  改善ルート**")
            improved_network = st.text_area(
                "改善後の物流の流れ",
                placeholder="例：工場 → OEM → DC → 顧客",
                height=115,
            )
    improvement_reason = st.text_area(
        "改善の狙い・背景（任意）",
        placeholder="例：中間輸送の削減により、物流費とリードタイムを低減したい",
        height=86,
    )
    st.caption("入力例は架空のケースです。実務で利用する際も固有名詞や機密情報は入力しないでください。")

with tab_flow:
    section("02–03", "物流条件の比較", "現行案と改善案を並べて入力し、距離・回数・リードタイムの変化を見える化します。")
    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.markdown("### ◉ 現行案")
            monthly_quantity = st.number_input("月間取扱数量（個）", min_value=0, value=100000, step=1000)
            current_distance = st.number_input("輸送距離（km）｜現行", min_value=0, value=300, step=10)
            current_frequency = st.number_input("月間輸送回数（回）｜現行", min_value=0, value=20, step=1)
            current_leadtime = st.number_input("リードタイム（日）｜現行", min_value=0.0, value=5.0, step=0.5)
    with right:
        with st.container(border=True):
            st.markdown("### ◉ 改善案")
            st.caption("数量は現行案と同一として比較します。")
            improved_distance = st.number_input("輸送距離（km）｜改善後", min_value=0, value=180, step=10)
            improved_frequency = st.number_input("月間輸送回数（回）｜改善後", min_value=0, value=12, step=1)
            improved_leadtime = st.number_input("リードタイム（日）｜改善後", min_value=0.0, value=3.0, step=0.5)

    distance_difference = current_distance - improved_distance
    frequency_difference = current_frequency - improved_frequency
    leadtime_difference = current_leadtime - improved_leadtime
    distance_reduction_rate = distance_difference / current_distance * 100 if current_distance else 0
    frequency_reduction_rate = frequency_difference / current_frequency * 100 if current_frequency else 0
    leadtime_reduction_rate = leadtime_difference / current_leadtime * 100 if current_leadtime else 0
    st.markdown("#### 物流効率の変化")
    cols = st.columns(3)
    for col, label, old, new, unit, rate in zip(
        cols,
        ["輸送距離", "月間輸送回数", "リードタイム"],
        [current_distance, current_frequency, current_leadtime],
        [improved_distance, improved_frequency, improved_leadtime],
        ["km", "回", "日"],
        [distance_reduction_rate, frequency_reduction_rate, leadtime_reduction_rate],
    ):
        # 利用者に表示する「変化率」は改善案−現行案の向きに統一。
        # 距離・回数・リードタイムが減る場合はマイナス＝改善。
        change_rate = -rate
        tone = "good" if change_rate < 0 else ("warn" if change_rate > 0 else "blue")
        with col:
            kpi(label, f"{new:,.1f} {unit}" if unit == "日" else f"{new:,.0f} {unit}",
                f"現行 {old:,.1f} → {new:,.1f} / 変化率 {change_rate:+.1f}%", tone)

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

# ------------------------------------------
# 改善テーマに対応する評価項目
# ------------------------------------------
selected_questions = checklists[improvement_theme]

with tab_cost:
    section("04", "コスト条件と削減効果", "物流費・加工費・保管費を統一した基準で比較します。金額は月間ベースで入力してください。")
    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.markdown("### ◉ 現行案のコスト")
            current_transport = st.number_input("月間物流費（円）｜現行", min_value=0, value=1000000, step=10000)
            current_processing_unit = st.number_input("加工単価（円／個）｜現行", min_value=0.0, value=50.0, step=1.0)
            current_storage = st.number_input("月間保管費（円）｜現行", min_value=0, value=200000, step=10000)
    with right:
        with st.container(border=True):
            st.markdown("### ◉ 改善案のコスト")
            improved_transport = st.number_input("月間物流費（円）｜改善後", min_value=0, value=600000, step=10000)
            improved_processing_unit = st.number_input("加工単価（円／個）｜改善後", min_value=0.0, value=52.0, step=1.0)
            improved_storage = st.number_input("月間保管費（円）｜改善後", min_value=0, value=150000, step=10000)

    current_processing = monthly_quantity * current_processing_unit
    improved_processing = monthly_quantity * improved_processing_unit
    current_monthly_total = current_transport + current_processing + current_storage
    improved_monthly_total = improved_transport + improved_processing + improved_storage
    current_annual_total = current_monthly_total * 12
    improved_annual_total = improved_monthly_total * 12
    # 内部の改善効果判定には従来どおり「現行−改善」（削減なら正）を使用。
    monthly_difference = current_monthly_total - improved_monthly_total
    annual_difference = current_annual_total - improved_annual_total

    # 画面上の「増減」はすべて改善案−現行案（削減なら負）に統一する。
    monthly_cost_change = improved_monthly_total - current_monthly_total
    annual_cost_change = improved_annual_total - current_annual_total
    annual_cost_change_rate = annual_cost_change / current_annual_total * 100 if current_annual_total else 0

    if monthly_quantity == 0:
        st.warning("月間取扱数量が0のため、加工費は0円として計算されています。")
    st.markdown("#### コストインパクト")
    cols = st.columns(3)
    with cols[0]:
        kpi("年間総コスト｜現行案", yen(current_annual_total), "現行案を12か月換算", "blue")
    with cols[1]:
        kpi("年間総コスト｜改善案", yen(improved_annual_total), "改善案を12か月換算", "blue")
    with cols[2]:
        kpi(f"年間コスト増減｜{cost_trend_label(annual_cost_change)}",
            signed_yen(annual_cost_change),
            f"現行比 {annual_cost_change_rate:+.1f}% ／ −は削減・＋は増加",
            "good" if annual_cost_change < 0 else "warn" if annual_cost_change > 0 else "blue")

    st.markdown("#### コスト構造の比較")
    yearly_costs = pd.DataFrame({
        "費目": ["物流費", "加工費", "保管費"],
        "現行案": [current_transport*12, current_processing*12, current_storage*12],
        "改善案": [improved_transport*12, improved_processing*12, improved_storage*12],
    })
    st.bar_chart(yearly_costs, x="費目", y=["現行案", "改善案"],
                 color=["#829bbd", "#2877c8"], stack=False, height=310)
    cost_table = pd.DataFrame({
        "費目": ["物流費／月", "加工費／月", "保管費／月", "合計／月", "合計／年"],
        "現行案": [current_transport, current_processing, current_storage, current_monthly_total, current_annual_total],
        "改善案": [improved_transport, improved_processing, improved_storage, improved_monthly_total, improved_annual_total],
    })
    cost_table["増減（改善−現行）"] = cost_table["改善案"] - cost_table["現行案"]
    st.dataframe(cost_table.style.format({"現行案": yen, "改善案": yen, "増減（改善−現行）": signed_yen}),
                 hide_index=True, use_container_width=True)
    st.caption("※ 増減＝改善案−現行案。マイナス（−）はコスト削減、プラス（＋）はコスト増加です。")
    st.caption("※ 加工費＝月間取扱数量×加工単価。年間費用は月間費用×12で試算し、初期投資や在庫評価額などは含みません。")

with tab_risk:
    section("05", "コスト以外の定性評価", "改善テーマごとに変化する確認項目を評価。悪化・不明の項目だけ、追加確認ポイントを表示します。")
    st.markdown(
        f'<div class="ls-banner">評価テーマ：<b>{safe(improvement_theme)}</b>　｜　'
        f'確認項目：<b>{len(selected_questions)}項目</b></div>', unsafe_allow_html=True,
    )
    evaluation_results = []
    assessment_basis = {}
    for idx, item in enumerate(selected_questions):
        with st.container(border=True):
            st.markdown(f'<span class="ls-category">{safe(item["category"])}</span>'
                        f'<div class="ls-question">{idx+1:02d}. {safe(item["question"])}</div>',
                        unsafe_allow_html=True)
            answer = st.radio("現行案との比較", ["未評価", "改善する", "変わらない", "悪化する", "不明"],
                              horizontal=True, key=f"review_{improvement_theme}_{idx}",
                              label_visibility="collapsed")
            evaluation_results.append({"分類": item["category"], "確認項目": item["question"], "評価": answer})
            if answer in ("悪化する", "不明"):
                st.warning("対応前に、次のポイントを確認してください。" if answer == "悪化する"
                           else "判断に必要な情報が不足しています。次のポイントを確認してください。")
                for point in item["check"]:
                    st.markdown(f"- {point}")
            elif answer == "改善する":
                basis = st.text_area("改善すると判断した根拠（任意）",
                                     placeholder="例：委託先の設備能力を確認済み",
                                     key=f"review_basis_{improvement_theme}_{idx}", height=76)
                assessment_basis[str(idx+1)] = basis

    improved_count = sum(r["評価"] == "改善する" for r in evaluation_results)
    unchanged_count = sum(r["評価"] == "変わらない" for r in evaluation_results)
    worsened_count = sum(r["評価"] == "悪化する" for r in evaluation_results)
    unknown_count = sum(r["評価"] == "不明" for r in evaluation_results)
    unselected_count = sum(r["評価"] == "未評価" for r in evaluation_results)
    answered_count = len(evaluation_results) - unselected_count
    st.markdown("#### 定性評価の進捗")
    st.progress(answered_count / len(evaluation_results) if evaluation_results else 0,
                text=f"{answered_count} / {len(evaluation_results)} 項目を評価済み")
    riskcols = st.columns(4)
    for col, label, value, tone in zip(
        riskcols, ["改善", "変化なし", "悪化", "不明・未評価"],
        [improved_count, unchanged_count, worsened_count, unknown_count+unselected_count],
        ["good", "blue", "warn", "warn"],
    ):
        with col:
            kpi(label, f"{value} 項目", "定性評価結果", tone)

with tab_report:
    section("06", "意思決定レポート", "ここまでの入力値を統合し、数字とリスクを一画面で比較します。")
    report_cols = st.columns(3)
    with report_cols[0]:
        kpi(f"年間コスト増減｜{cost_trend_label(annual_cost_change)}", signed_yen(annual_cost_change),
            f"現行比 {annual_cost_change_rate:+.1f}% ／ −は削減・＋は増加",
            "good" if annual_cost_change < 0 else "warn" if annual_cost_change > 0 else "blue")
    with report_cols[1]:
        kpi("輸送距離変化", f"{-distance_reduction_rate:+.1f}%",
            f"{current_distance:,} → {improved_distance:,} km ／ −は短縮", "good" if distance_reduction_rate>0 else "warn" if distance_reduction_rate<0 else "blue")
    with report_cols[2]:
        kpi("要確認・悪化項目", f"{worsened_count+unknown_count+unselected_count} 件",
            "悪化・不明・未評価の合計", "warn" if worsened_count+unknown_count+unselected_count else "good")

    left, right = st.columns([1,1], gap="large")
    with left:
        with st.container(border=True):
            st.markdown("### 案件サマリー")
            st.markdown(f"**改善テーマ**：{safe(improvement_theme)}")
            st.markdown("**現行ネットワーク**")
            st.markdown(f'<div class="ls-route">{safe(current_network or "未入力")}</div>', unsafe_allow_html=True)
            st.markdown("**改善ネットワーク**")
            st.markdown(f'<div class="ls-route">{safe(improved_network or "未入力")}</div>', unsafe_allow_html=True)
            if improvement_reason:
                st.markdown("**検討理由**")
                st.write(improvement_reason)
    with right:
        with st.container(border=True):
            st.markdown("### 物流・コストの比較")
            logistics_df = pd.DataFrame({
                "指標": ["輸送距離", "月間輸送回数", "リードタイム", "月間総コスト", "年間総コスト"],
                "現行案": [f"{current_distance:,} km", f"{current_frequency:,} 回", f"{current_leadtime:,.1f} 日", yen(current_monthly_total), yen(current_annual_total)],
                "改善案": [f"{improved_distance:,} km", f"{improved_frequency:,} 回", f"{improved_leadtime:,.1f} 日", yen(improved_monthly_total), yen(improved_annual_total)],
            })
            st.dataframe(logistics_df, hide_index=True, use_container_width=True)
            st.caption("物流条件・数量・コストはユーザーが入力した仮定に基づきます。")

    st.markdown("#### 定性評価の一覧")
    evaluation_df = pd.DataFrame(evaluation_results)
    st.dataframe(evaluation_df, hide_index=True, use_container_width=True)
    attention_items = [r for r in evaluation_results if r["評価"] in ("悪化する", "不明", "未評価")]
    st.markdown("#### 総合コメント")
    if unselected_count:
        st.warning(f"定性評価に未評価が {unselected_count} 件あります。必要項目を確認したうえで総合判断してください。")
    elif annual_difference > 0 and worsened_count == 0 and unknown_count == 0:
        st.success(f"年間 {yen(annual_difference)} のコスト削減見込みです。現時点で悪化・不明の項目はありません。実施前に根拠を確認してください。")
    elif annual_difference > 0:
        st.warning(f"年間 {yen(annual_difference)} のコスト削減見込みですが、悪化 {worsened_count} 件・不明 {unknown_count} 件があります。コスト以外の影響も確認してください。")
    elif improved_count:
        st.info("コスト削減は確認できませんが、物流条件・品質・安定供給などの改善余地があります。複数の評価軸で判断してください。")
    else:
        st.warning("現在の入力条件だけでは、明確な改善効果を確認できません。条件とリスクを再点検してください。")
    if attention_items:
        with st.expander(f"⚠ 要確認リスト（{len(attention_items)} 件）", expanded=False):
            for item in attention_items:
                st.markdown(f'- **{item["分類"]}｜{item["評価"]}**：{item["確認項目"]}')

    st.divider()
    section("07", "AIによる追加分析", "入力内容から見落としがちなリスクと実行前に必要な確認事項を洗い出します。")
    st.info("AI分析の実行時、入力内容は外部AIサービス（Groq）に送信されます。機密情報は入力しないでください。")
    evaluation_text = "\n".join(
        f'- {r["分類"]}：{r["確認項目"]} → 評価：{r["評価"]}'
        for r in evaluation_results
    )
    basis_text = "\n".join(f"- 設問{i}：{v}" for i, v in assessment_basis.items() if v.strip())
    ai_prompt = f"""以下は製造業の物流ネットワーク改善案の入力情報です。
【改善テーマ】{improvement_theme}
【現行ネットワーク】{current_network}
【改善後ネットワーク】{improved_network}
【改善の理由】{improvement_reason}
【月間取扱数量】{monthly_quantity:,} 個
【物流条件】
輸送距離：{current_distance:,} → {improved_distance:,} km
月間輸送回数：{current_frequency:,} → {improved_frequency:,} 回
リードタイム：{current_leadtime:.1f} → {improved_leadtime:.1f} 日
【コスト】
現行年間総コスト：{current_annual_total:,.0f} 円
改善案年間総コスト：{improved_annual_total:,.0f} 円
年間コスト増減（改善−現行）：{annual_cost_change:,.0f} 円
※ マイナスはコスト削減、プラスはコスト増加。
【定性評価】
{evaluation_text}
【改善判断の根拠（任意）】
{basis_text or '記載なし'}

次の5項目について分析してください。
1. 改善案の主なメリット
2. 現在確認できる懸念点・リスク
3. 利用者が見落としている可能性があるリスク
4. 実施前に追加で確認すべき事項
5. 総合コメント

必ず守るルール：
・入力のない事実を断定せず、不明点は『確認が必要』とする
・コスト削減だけを根拠に推奨しない
・品質、安定供給、在庫、リードタイム、BCP、切替リスクを考慮する
・入力値の数値計算は再実施せず、与えられた数字に基づき解釈する
・利用者が見落としている可能性のある観点を積極的に提示する
・最終判断を断定せず、意思決定を支援する
・日本語で簡潔かつ分かりやすく回答する
"""
    signature_payload = {
        "theme":improvement_theme, "route":[current_network, improved_network, improvement_reason],
        "q":monthly_quantity,
        "logistics":[current_distance, improved_distance, current_frequency, improved_frequency,
                     current_leadtime, improved_leadtime],
        "cost":[current_transport, improved_transport, current_processing_unit,
                improved_processing_unit, current_storage, improved_storage],
        "evaluation":evaluation_results, "basis":assessment_basis,
    }
    current_signature = hashlib.sha256(json.dumps(signature_payload, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    if st.button("✦ AIで追加分析する", type="primary", use_container_width=True):
        if unselected_count:
            st.warning(f"未評価が {unselected_count} 件あります。すべて回答してからの分析を推奨します。")
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            with st.spinner("追加のリスクと確認ポイントを分析中…"):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role":"system", "content":"あなたは製造業のSCM・物流改善を支援する専門アドバイザーです。意思決定を代行せず、根拠とリスクを整理してください。"},
                        {"role":"user", "content":ai_prompt},
                    ],
                    temperature=0.3,
                )
            result = response.choices[0].message.content or "分析結果が空でした。再実行してください。"
            st.session_state["last_ai_result"] = {"signature":current_signature, "text":result}
        except KeyError:
            st.error("Groq APIキーが設定されていません。StreamlitのSecretsに GROQ_API_KEY を登録してください。")
        except Exception as exc:
            st.error("AI分析中にエラーが発生しました。接続設定を確認してください。")
            with st.expander("エラーの詳細を表示"):
                st.code(str(exc))
    saved_ai = st.session_state.get("last_ai_result")
    if saved_ai and saved_ai["signature"] == current_signature:
        st.markdown("### AI分析結果")
        with st.container(border=True):
            st.markdown(saved_ai["text"])
        st.caption("AIの回答は検討支援用です。現場条件や関係部署への確認が必要です。")
    elif saved_ai:
        st.caption("入力条件が変更されました。最新の条件に基づく分析が必要な場合は、AI分析を再実行してください。")

st.markdown('<div class="ls-footer">LogiScope · Logistics Network Evaluation Prototype ｜ 卒業研究用の評価支援ツール。表示結果は実施判断・成果を保証するものではありません。</div>',
            unsafe_allow_html=True)
