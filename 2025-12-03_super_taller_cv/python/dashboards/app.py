"""
Dashboard Streamlit para monitorear métricas del taller.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

import pandas as pd
import streamlit as st
from sqlmodel import Session, select

from python.websockets_api.storage import CommandRecord, MetricRecord, Storage

DB_PATH = Path("results/backend/state.db")
storage = Storage(DB_PATH)


@st.cache_data(ttl=5)
def load_metric_df(limit: int = 200) -> pd.DataFrame:
    rows: List[MetricRecord] = storage.latest_metrics(limit)
    if not rows:
        return pd.DataFrame(columns=["timestamp", "module", "metric", "value"])
    data = [row.model_dump() for row in rows]
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.sort_values("timestamp")


@st.cache_data(ttl=5)
def load_commands(limit: int = 50) -> pd.DataFrame:
    rows = storage.recent_commands(limit)
    if not rows:
        return pd.DataFrame(columns=["timestamp", "module", "action", "source"])
    data = [row.model_dump() for row in rows]
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.sort_values("timestamp", ascending=False)


@st.cache_data
def load_training_metrics() -> pd.DataFrame:
    records = []
    for path in Path("results/training").glob("*/metrics.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        records.append(
            {
                "experiment": path.parent.name,
                "best_val_acc": payload.get("best_val_acc"),
                "epochs": payload.get("epochs"),
            }
        )
    return pd.DataFrame(records)


st.set_page_config(page_title="Super Taller CV Dashboard", layout="wide")
st.title("Super Taller CV - Dashboard de métricas")

tabs = st.tabs(["Detección", "Comandos", "Entrenamiento"])

with tabs[0]:
    st.subheader("Detección / rendimiento")
    metric_df = load_metric_df()
    if metric_df.empty:
        st.info("Aún no hay métricas almacenadas. Ejecuta `inference.py` enviando datos al WS.")
    else:
        col1, col2 = st.columns(2)
        fps_df = metric_df[metric_df["metric"] == "fps"]
        latency_df = metric_df[metric_df["metric"] == "latency_ms"]

        col1.metric("FPS promedio", f"{fps_df['value'].mean():.2f}")
        col2.metric("Latencia promedio (ms)", f"{latency_df['value'].mean():.2f}")

        st.line_chart(
            fps_df.set_index("timestamp")["value"],
            height=250,
            use_container_width=True,
        )
        st.line_chart(
            latency_df.set_index("timestamp")["value"],
            height=250,
            use_container_width=True,
        )

with tabs[1]:
    st.subheader("Comandos multimodales recientes")
    cmd_df = load_commands()
    if cmd_df.empty:
        st.info("Sin comandos registrados.")
    else:
        st.dataframe(cmd_df[["timestamp", "module", "action", "source"]], use_container_width=True)

with tabs[2]:
    st.subheader("Comparativa de entrenamiento")
    train_df = load_training_metrics()
    if train_df.empty:
        st.info("Aún no hay métricas de entrenamiento en `results/training/*/metrics.json`.")
    else:
        st.dataframe(train_df, use_container_width=True)
        st.bar_chart(train_df.set_index("experiment")["best_val_acc"], use_container_width=True)

st.caption("Actualiza la página para ver datos nuevos. Se recomienda ejecutar el servidor WebSocket antes de iniciar el dashboard.")

