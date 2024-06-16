import plotly.express as px
import streamlit as st


def pie_chart(df, x, y, title, title_x=0.20):
    fig = px.pie(df, names=x, values=y, hole=0.5, title=title)
    fig.update_layout(title_x=title_x, title_font_size=22)
    fig.update_traces(
        text=df[y],
        textinfo="percent+value",
        textposition="outside",
        textfont=dict(color="white"),
    )
    st.plotly_chart(fig, use_container_width=True)


def horizontal_bar_chart(df, x, y, text, color, title, title_x=0.25):
    fig = px.bar(df, x=x, y=y, labels={x: "", y: ""}, title=title)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(title_x=title_x, title_font_size=22)
    text_position = [
        "inside" if val >= max(df[x]) * 0.75 else "outside" for val in df[x]
    ]
    fig.update_traces(
        marker_color=color,
        text=df[text],
        textposition=text_position,
        texttemplate="%{x}<br>%{text}",
        textfont=dict(size=14),
        insidetextfont=dict(color="white"),
        textangle=0,
        hovertemplate="%{x}<br>%{y}",
    )
    st.plotly_chart(fig, use_container_width=True)


def vertical_bar_chart(df, x, y, text, color, title, title_x=0.25):
    fig = px.bar(df, x=x, y=y, labels={x: "", y: ""}, title=title)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(title_x=title_x, title_font_size=22)
    text_position = [
        "inside" if val >= max(df[y]) * 0.90 else "outside" for val in df[y]
    ]
    fig.update_traces(
        marker_color=color,
        text=df[text],
        textposition=text_position,
        texttemplate="%{y}<br>%{text}",
        textfont=dict(size=14),
        insidetextfont=dict(color="white"),
        textangle=0,
        hovertemplate="%{x}<br>%{y}",
    )
    st.plotly_chart(fig, use_container_width=True, height=100)


def line_chart(df, x, y, text, textposition, color, title, title_x=0.25):
    fig = px.line(df, x=x, y=y, labels={x: "", y: ""}, title=title, text=df[text])
    fig.update_layout(title_x=title_x, title_font_size=22)
    fig.update_traces(
        line=dict(color=color, width=3.5),
        marker=dict(symbol="diamond", size=10),
        texttemplate="%{x}<br>%{text}",
        textfont=dict(size=13.5),
        textposition=textposition,
        hovertemplate="%{x}<br>%{y}",
    )
    st.plotly_chart(fig, use_container_width=True, height=100)
