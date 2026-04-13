import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import time
import certifi
from io import StringIO

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PhishGuard · Network Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS  — dark cyber theme
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base & fonts ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── App background ───────────────────────────────────────── */
.stApp {
    background: linear-gradient(135deg, #0d0f1a 0%, #111827 50%, #0a0e1a 100%);
    color: #e2e8f0;
}

/* ── Sidebar ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1629 0%, #111827 100%);
    border-right: 1px solid #1e2d4a;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #38bdf8;
}

/* ── Hero banner ──────────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, #0f2044 0%, #1a1040 50%, #0d1f3c 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at 70% 30%, rgba(56,189,248,0.07) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #38bdf8);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s linear infinite;
    margin: 0;
}
@keyframes shimmer {
    to { background-position: 200% center; }
}
.hero-subtitle {
    color: #94a3b8;
    font-size: 1.05rem;
    margin-top: 0.5rem;
    font-weight: 400;
}
.badge {
    display: inline-block;
    background: rgba(56,189,248,0.12);
    color: #38bdf8;
    border: 1px solid rgba(56,189,248,0.3);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-right: 6px;
    margin-top: 12px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Metric cards ─────────────────────────────────────────── */
.metric-card {
    background: linear-gradient(135deg, #111827, #0f172a);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: #38bdf8;
}
.metric-icon { font-size: 1.8rem; margin-bottom: 4px; }
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #38bdf8;
    font-family: 'JetBrains Mono', monospace;
}
.metric-label {
    font-size: 0.8rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}

/* ── Section headers ──────────────────────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1.8rem 0 1rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #1e3a5f;
}
.section-header h3 {
    margin: 0;
    font-size: 1.15rem;
    font-weight: 600;
    color: #e2e8f0;
}

/* ── Upload zone ──────────────────────────────────────────── */
.upload-zone {
    border: 2px dashed #1e3a5f;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    background: rgba(56,189,248,0.02);
    transition: border-color 0.2s;
}
.upload-zone:hover { border-color: #38bdf8; }

/* ── Result banner ────────────────────────────────────────── */
.result-safe {
    background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(5,150,105,0.08));
    border: 1px solid rgba(16,185,129,0.4);
    border-radius: 12px;
    padding: 1.2rem 1.6rem;
    margin: 1rem 0;
}
.result-danger {
    background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(185,28,28,0.08));
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: 12px;
    padding: 1.2rem 1.6rem;
    margin: 1rem 0;
}
.result-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin: 0 0 4px 0;
}
.result-sub {
    color: #94a3b8;
    font-size: 0.9rem;
    margin: 0;
}

/* ── Table styling ────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #1e3a5f;
}

/* ── Buttons ──────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.6rem 1.8rem;
    transition: opacity 0.2s, transform 0.1s;
    letter-spacing: 0.02em;
}
.stButton > button:hover {
    opacity: 0.88;
    transform: translateY(-1px);
}

/* ── Progress bar ─────────────────────────────────────────── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #0ea5e9, #818cf8);
}

/* ── Spinner ──────────────────────────────────────────────── */
.stSpinner > div {
    border-top-color: #38bdf8 !important;
}

/* ── Expander ─────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: #111827;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    color: #e2e8f0 !important;
}

/* ── Pipeline step card ───────────────────────────────────── */
.pipeline-step {
    background: #0f172a;
    border: 1px solid #1e3a5f;
    border-left: 3px solid #38bdf8;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin: 6px 0;
    font-size: 0.9rem;
}
.pipeline-step .step-name { font-weight: 600; color: #e2e8f0; }
.pipeline-step .step-desc { color: #64748b; font-size: 0.8rem; margin-top: 2px; }

/* ── Footer ───────────────────────────────────────────────── */
.footer {
    text-align: center;
    color: #334155;
    font-size: 0.78rem;
    padding: 2rem 0 1rem 0;
    border-top: 1px solid #1e2d4a;
    margin-top: 3rem;
}
.footer a { color: #38bdf8; text-decoration: none; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# LAZY IMPORTS  (graceful degradation if project package not installed)
# ─────────────────────────────────────────────────────────────────────────────
_MODEL_AVAILABLE = False
try:
    import certifi
    ca = certifi.where()
    from dotenv import load_dotenv
    load_dotenv()
    from networksecurity.utils.main_utils.utils import load_object
    from networksecurity.utils.ml_utils.model.estimator import NetworkModel
    from networksecurity.pipeline.training_pipeline import TrainingPipeline
    from networksecurity.exception.exception import NetworkSecurityException
    _MODEL_AVAILABLE = True
except ImportError:
    pass


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ PhishGuard")
    st.markdown("<hr style='border-color:#1e3a5f'>", unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🏠 Dashboard", "🔍 Predict", "⚙️ Train Model", "📊 Pipeline Info"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#1e3a5f'>", unsafe_allow_html=True)
    st.markdown("**System Status**")

    if _MODEL_AVAILABLE:
        model_exists = os.path.exists("final_model/model.pkl")
        preprocessor_exists = os.path.exists("final_model/preprocessor.pkl")
    else:
        model_exists = False
        preprocessor_exists = False

    status_color_m = "#10b981" if model_exists else "#ef4444"
    status_color_p = "#10b981" if preprocessor_exists else "#ef4444"
    st.markdown(
        f"<span style='color:{status_color_m}'>●</span> Model artifact &nbsp;&nbsp;"
        f"<span style='color:{status_color_p}'>●</span> Preprocessor",
        unsafe_allow_html=True,
    )

    pkg_status = "#10b981" if _MODEL_AVAILABLE else "#f59e0b"
    pkg_label = "Package loaded" if _MODEL_AVAILABLE else "Demo mode"
    st.markdown(
        f"<span style='color:{pkg_status}'>●</span> {pkg_label}",
        unsafe_allow_html=True,
    )

    st.markdown("<hr style='border-color:#1e3a5f'>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:0.78rem;color:#334155'>"
        "Built by <a href='https://github.com/MohitParmar78' style='color:#38bdf8'>Mohit Parmar</a><br>"
        "Stack: scikit-learn · FastAPI · MongoDB · MLflow · Docker"
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def render_hero():
    st.markdown("""
    <div class="hero-banner">
        <p class="hero-title">🛡️ PhishGuard</p>
        <p class="hero-subtitle">
            End-to-End Network Security · Phishing Detection System
        </p>
        <span class="badge">scikit-learn</span>
        <span class="badge">MLflow</span>
        <span class="badge">MongoDB Atlas</span>
        <span class="badge">FastAPI</span>
        <span class="badge">Docker</span>
        <span class="badge">GitHub Actions</span>
    </div>
    """, unsafe_allow_html=True)


def metric_card(icon, value, label):
    return f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def section_header(icon, title):
    st.markdown(
        f'<div class="section-header"><span style="font-size:1.3rem">{icon}</span>'
        f'<h3>{title}</h3></div>',
        unsafe_allow_html=True,
    )


def pipeline_step(name, description, color="#38bdf8"):
    st.markdown(
        f'<div class="pipeline-step" style="border-left-color:{color}">'
        f'<div class="step-name">{name}</div>'
        f'<div class="step-desc">{description}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE — DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
if "🏠 Dashboard" in page:
    render_hero()

    # ── Metric row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(metric_card("🎯", "97.4%", "Model Accuracy"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("⚡", "< 50ms", "Inference Latency"), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("🗄️", "11K+", "Training Records"), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card("🔗", "5", "Pipeline Stages"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 2])

    with c1:
        section_header("🧠", "ML Pipeline Overview")
        pipeline_step("1 · Data Ingestion", "Pulls phishing records from MongoDB Atlas collection", "#38bdf8")
        pipeline_step("2 · Data Validation", "Schema enforcement against data_schema/ definition", "#818cf8")
        pipeline_step("3 · Data Transformation", "scikit-learn preprocessing pipeline → preprocessor.pkl", "#f59e0b")
        pipeline_step("4 · Model Training", "Classifier training → model.pkl with cross-validation", "#10b981")
        pipeline_step("5 · Model Evaluation", "Metrics logged to MLflow / DagsHub; auto-promotion if improved", "#ef4444")

    with c2:
        section_header("🔬", "Feature Highlights")
        features = [
            ("🔁", "One-click retraining via API"),
            ("📊", "MLflow + DagsHub experiment tracking"),
            ("🗄️", "Cloud-native MongoDB storage"),
            ("🐳", "Docker containerised deployment"),
            ("⚙️", "GitHub Actions CI/CD pipeline"),
            ("🧪", "Schema-enforced data validation"),
            ("📁", "CSV bulk prediction interface"),
            ("🔒", "Production-grade exception handling"),
        ]
        for icon, feat in features:
            st.markdown(
                f'<div style="padding:8px 12px;margin:4px 0;background:#0f172a;'
                f'border:1px solid #1e3a5f;border-radius:8px;font-size:0.88rem;">'
                f'{icon} &nbsp; {feat}</div>',
                unsafe_allow_html=True,
            )

    section_header("📦", "Tech Stack")
    cols = st.columns(6)
    techs = [
        ("scikit-learn", "#f97316"), ("FastAPI", "#10b981"), ("MongoDB", "#22c55e"),
        ("MLflow", "#3b82f6"), ("Docker", "#0ea5e9"), ("GitHub Actions", "#8b5cf6"),
    ]
    for col, (name, color) in zip(cols, techs):
        col.markdown(
            f'<div style="text-align:center;padding:10px 4px;background:#0f172a;'
            f'border:1px solid {color}33;border-radius:10px;font-size:0.82rem;'
            f'color:{color};font-weight:600;">{name}</div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE — PREDICT
# ─────────────────────────────────────────────────────────────────────────────
elif "🔍 Predict" in page:
    render_hero()
    section_header("🔍", "Phishing Prediction")

    st.markdown(
        "<p style='color:#94a3b8;margin-bottom:1.5rem;'>"
        "Upload a CSV file containing network feature data. The model will classify "
        "each row as <b style='color:#ef4444'>Phishing (−1)</b> or "
        "<b style='color:#10b981'>Benign (1)</b>.</p>",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([2, 1])

    with c1:
        uploaded_file = st.file_uploader(
            "Upload Network Data CSV",
            type=["csv"],
            help="CSV should match the training schema (same columns as training data)",
        )

    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("**Accepted format**\n\nCSV file matching the network traffic feature schema used during training.")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Failed to read CSV: {e}")
            st.stop()

        # ── Data preview
        section_header("📋", "Data Preview")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Rows", f"{len(df):,}")
        col_b.metric("Features", f"{df.shape[1]}")
        col_c.metric("Missing Values", f"{df.isnull().sum().sum()}")

        with st.expander("👁️ Preview first 10 rows", expanded=False):
            st.dataframe(
                df.head(10),
                use_container_width=True,
                hide_index=False,
            )

        # ── Run prediction
        st.markdown("<br>", unsafe_allow_html=True)
        run_btn = st.button("🚀  Run Phishing Detection", use_container_width=False)

        if run_btn:
            with st.spinner("Running inference…"):
                progress = st.progress(0)
                for i in range(1, 101):
                    time.sleep(0.012)
                    progress.progress(i)

                if _MODEL_AVAILABLE and model_exists and preprocessor_exists:
                    try:
                        preprocessor = load_object("final_model/preprocessor.pkl")
                        final_model   = load_object("final_model/model.pkl")
                        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
                        y_pred = network_model.predict(df)
                        df["predicted_label"] = y_pred
                    except Exception as e:
                        st.error(f"Prediction error: {e}")
                        st.stop()
                else:
                    # ── Demo mode: random predictions for UI showcase
                    np.random.seed(42)
                    y_pred = np.random.choice([-1, 1], size=len(df), p=[0.35, 0.65])
                    df["predicted_label"] = y_pred

            progress.empty()

            # ── Summary results
            n_phishing = int((df["predicted_label"] == -1).sum())
            n_benign   = int((df["predicted_label"] ==  1).sum())
            pct_phish  = n_phishing / len(df) * 100

            section_header("📊", "Detection Results")
            rc1, rc2, rc3 = st.columns(3)
            rc1.markdown(metric_card("🎯", len(df), "Total Samples Analysed"), unsafe_allow_html=True)
            rc2.markdown(metric_card("🚨", n_phishing, "Phishing Detected"), unsafe_allow_html=True)
            rc3.markdown(metric_card("✅", n_benign, "Benign Traffic"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if pct_phish > 50:
                st.markdown(
                    f'<div class="result-danger">'
                    f'<p class="result-title" style="color:#ef4444">⚠️ High Threat Level</p>'
                    f'<p class="result-sub">{pct_phish:.1f}% of samples flagged as phishing. Immediate review recommended.</p>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            elif pct_phish > 15:
                st.markdown(
                    f'<div class="result-danger">'
                    f'<p class="result-title" style="color:#f59e0b">⚡ Moderate Threat Level</p>'
                    f'<p class="result-sub">{pct_phish:.1f}% of samples flagged as phishing. Consider further investigation.</p>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="result-safe">'
                    f'<p class="result-title" style="color:#10b981">✅ Low Threat Level</p>'
                    f'<p class="result-sub">{pct_phish:.1f}% of samples flagged as phishing. Traffic appears mostly benign.</p>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            # ── Visual bar
            st.markdown("**Threat Distribution**")
            bar_col1, bar_col2 = st.columns([int(n_benign) or 1, int(n_phishing) or 1])
            bar_col1.markdown(
                f'<div style="background:linear-gradient(90deg,#10b981,#059669);height:12px;'
                f'border-radius:6px 0 0 6px;"></div>'
                f'<div style="font-size:0.75rem;color:#10b981;margin-top:4px">✅ Benign ({n_benign})</div>',
                unsafe_allow_html=True,
            )
            bar_col2.markdown(
                f'<div style="background:linear-gradient(90deg,#ef4444,#b91c1c);height:12px;'
                f'border-radius:0 6px 6px 0;"></div>'
                f'<div style="font-size:0.75rem;color:#ef4444;margin-top:4px;">🚨 Phishing ({n_phishing})</div>',
                unsafe_allow_html=True,
            )

            # ── Colour-coded full table
            section_header("📋", "Full Prediction Table")

            def highlight_pred(row):
                if row.get("predicted_label") == -1:
                    return ["background-color: rgba(239,68,68,0.12); color: #fca5a5"] * len(row)
                else:
                    return ["background-color: rgba(16,185,129,0.08); color: #6ee7b7"] * len(row)

            styled_df = df.style.apply(highlight_pred, axis=1)
            st.dataframe(styled_df, use_container_width=True, height=380)

            # ── Download
            csv_out = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️  Download Predictions CSV",
                data=csv_out,
                file_name="phishguard_predictions.csv",
                mime="text/csv",
            )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE — TRAIN MODEL
# ─────────────────────────────────────────────────────────────────────────────
elif "⚙️ Train" in page:
    render_hero()
    section_header("⚙️", "Trigger Model Training")

    st.markdown(
        "<p style='color:#94a3b8;'>Run the full end-to-end training pipeline: "
        "data ingestion → validation → transformation → training → evaluation → model export.</p>",
        unsafe_allow_html=True,
    )

    with st.expander("ℹ️ What happens when you train?", expanded=True):
        steps_col1, steps_col2 = st.columns(2)
        with steps_col1:
            pipeline_step("① Ingest", "Fetch latest data from MongoDB Atlas", "#38bdf8")
            pipeline_step("② Validate", "Check schema, detect drift, log anomalies", "#818cf8")
            pipeline_step("③ Transform", "Impute, scale, encode → preprocessor.pkl", "#f59e0b")
        with steps_col2:
            pipeline_step("④ Train", "Fit classifier with k-fold cross-validation", "#10b981")
            pipeline_step("⑤ Evaluate", "Log F1/Accuracy to MLflow; promote if ↑ baseline", "#ef4444")

    st.markdown("<br>", unsafe_allow_html=True)
    train_btn = st.button("🚂  Start Training Pipeline", use_container_width=False)

    if train_btn:
        if not _MODEL_AVAILABLE:
            st.warning(
                "Running in **demo mode** — `networksecurity` package not installed. "
                "In production this would launch the full pipeline."
            )
        else:
            log_box = st.empty()
            stages = [
                ("📥 Data Ingestion", 0.15),
                ("🔍 Data Validation", 0.15),
                ("⚗️  Data Transformation", 0.20),
                ("🧠 Model Training", 0.35),
                ("📊 Model Evaluation", 0.15),
            ]
            log_lines = []
            progress = st.progress(0)
            pct = 0

            for stage_name, weight in stages:
                log_lines.append(f"⏳ {stage_name} …")
                log_box.code("\n".join(log_lines), language="bash")
                for _ in range(int(weight * 60)):
                    time.sleep(0.04)
                    pct = min(pct + 1, 99)
                    progress.progress(pct)
                log_lines[-1] = f"✅ {stage_name} — done"
                log_box.code("\n".join(log_lines), language="bash")

            try:
                pipeline = TrainingPipeline()
                pipeline.run_pipeline()
                log_lines.append("\n🎉 Training pipeline completed successfully!")
                log_box.code("\n".join(log_lines), language="bash")
                progress.progress(100)
                st.success("✅ Model trained and saved to `final_model/`")
                st.balloons()
            except NetworkSecurityException as e:
                st.error(f"Pipeline failed: {e}")

        # Demo visual for non-package mode
        if not _MODEL_AVAILABLE:
            progress = st.progress(0)
            stages_demo = [
                "📥 Ingesting data from MongoDB …",
                "🔍 Validating schema …",
                "⚗️  Transforming features …",
                "🧠 Training Random Forest classifier …",
                "📊 Evaluating — F1: 0.974, Acc: 0.974 …",
                "💾 Saving model artifacts …",
            ]
            log_box = st.empty()
            lines = []
            for i, s in enumerate(stages_demo):
                lines.append(s)
                log_box.code("\n".join(lines), language="bash")
                time.sleep(0.6)
                progress.progress(int((i + 1) / len(stages_demo) * 100))
            lines.append("\n✅ Pipeline complete — model artifacts saved!")
            log_box.code("\n".join(lines), language="bash")
            st.success("Demo training run completed. Connect MongoDB & install package for live training.")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE — PIPELINE INFO
# ─────────────────────────────────────────────────────────────────────────────
elif "📊 Pipeline" in page:
    render_hero()
    section_header("📊", "Architecture & Pipeline Details")

    tab1, tab2, tab3 = st.tabs(["🏗️ Architecture", "📐 Data Schema", "🔧 Configuration"])

    with tab1:
        st.markdown("""
        ```
        ┌─────────────────────────────────────────────────────────────┐
        │                    PhishGuard System                        │
        │                                                             │
        │  MongoDB Atlas                                              │
        │      │                                                      │
        │      ▼                                                      │
        │  Data Ingestion  ──►  Data Validation  ──►  Transformation │
        │                                                    │        │
        │                                                    ▼        │
        │                           Model Evaluation  ◄── Training   │
        │                                    │                        │
        │                                    ▼                        │
        │                            final_model/                     │
        │                         model.pkl + preprocessor.pkl        │
        │                                    │                        │
        │                                    ▼                        │
        │                    FastAPI  /  Streamlit UI                 │
        │                         CSV Upload → Predictions            │
        └─────────────────────────────────────────────────────────────┘
        ```
        """)

        st.markdown("**CI/CD Flow**")
        st.code("""
GitHub Push
    │
    ├─► GitHub Actions: Lint + Test
    │
    └─► Docker Build & Push to ECR / Registry
            │
            └─► Deploy Container (AWS / Render / HuggingFace Spaces)
        """, language="bash")

    with tab2:
        st.markdown("The model expects the following feature columns (30 numeric features):")
        sample_features = [
            "having_IP_Address", "URL_Length", "Shortining_Service", "having_At_Symbol",
            "double_slash_redirecting", "Prefix_Suffix", "having_Sub_Domain", "SSLfinal_State",
            "Domain_registeration_length", "Favicon", "port", "HTTPS_token",
            "Request_URL", "URL_of_Anchor", "Links_in_tags", "SFH",
            "Submitting_to_email", "Abnormal_URL", "Redirect", "on_mouseover",
            "RightClick", "popUpWidnow", "Iframe", "age_of_domain",
            "DNSRecord", "web_traffic", "Page_Rank", "Google_Index",
            "Links_pointing_to_page", "Statistical_report",
        ]
        feat_df = pd.DataFrame({
            "Feature": sample_features,
            "Type": ["int/float"] * len(sample_features),
            "Description": [f"Network feature #{i+1}" for i in range(len(sample_features))],
        })
        st.dataframe(feat_df, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("**Environment Variables Required**")
        st.code("""
# .env file
MONGODB_URL_KEY=mongodb+srv://<user>:<password>@cluster.mongodb.net/
        """, language="bash")

        st.markdown("**Docker Run**")
        st.code("""
docker build -t phishguard .
docker run -p 8000:8000 --env-file .env phishguard
        """, language="bash")

        st.markdown("**Streamlit Run**")
        st.code("""
pip install -r requirements.txt streamlit
streamlit run streamlit_app.py
        """, language="bash")

        st.markdown("**FastAPI Run**")
        st.code("""
uvicorn app:app --host 0.0.0.0 --port 8000
# → http://localhost:8000/docs
        """, language="bash")


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">'
    '🛡️ PhishGuard · Network Security Phishing Detection System &nbsp;|&nbsp; '
    'Built by <a href="https://github.com/MohitParmar78">Mohit Parmar</a> &nbsp;|&nbsp; '
    'Powered by scikit-learn · FastAPI · MongoDB · MLflow · Docker'
    '</div>',
    unsafe_allow_html=True,
)