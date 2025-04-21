
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns

def plot_bar_chart(df, x, y, title="Chart"):
    st.markdown(f"#### {title}")
    fig, ax = plt.subplots()
    df.plot(kind='bar', x=x, y=y, legend=False, ax=ax)
    st.pyplot(fig)

def plot_radar_chart(data_dict, title="Radar Chart"):
    categories = list(data_dict.keys())
    values = list(data_dict.values())
    values += values[:1]  # repeat first to close radar chart
    categories += categories[:1]

    angles = [n / float(len(categories)) * 2 * 3.14159 for n in range(len(categories))]

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories[:-1])
    ax.set_title(title)
    st.pyplot(fig)

def plot_sankey(labels, sources, targets, values, title="Customer Journey"):
    st.markdown(f"#### {title}")
    fig = go.Figure(data=[go.Sankey(
        node=dict(label=labels, pad=15, thickness=20),
        link=dict(source=sources, target=targets, value=values)
    )])
    st.plotly_chart(fig)

def plot_emotion_map(emotion_data, title="Emotion Map"):
    st.markdown(f"#### {title}")
    fig, ax = plt.subplots()
    sns.barplot(x=list(emotion_data.keys()), y=list(emotion_data.values()), ax=ax)
    ax.set_ylabel("Intensity")
    ax.set_title("Emotional Landscape")
    st.pyplot(fig)
