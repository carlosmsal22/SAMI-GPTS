
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def plot_bar_chart(df, x, y, title="Bar Chart"):
    fig, ax = plt.subplots()
    df.groupby(x)[y].mean().plot(kind='bar', ax=ax)
    ax.set_title(title)
    ax.set_ylabel(y)
    st.pyplot(fig)

def plot_radar_chart(categories, values, title="Radar Chart"):
    import numpy as np

    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, 'o-', linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_title(title, y=1.08)
    st.pyplot(fig)
