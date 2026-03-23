import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

plt.style.use('dark_background')
RED   = '#E50914'
DARK  = '#141414'
DARK2 = '#1a1a1a'
WHITE = '#F5F5F5'

def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, '..', 'data', 'cleaned_movies.csv')
    return pd.read_csv(path)

def _title_col(df):
    for c in ['title','title_x','title_y']:
        if c in df.columns:
            return c
    return df.columns[0]

def plot_revenue_distribution(df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), facecolor=DARK)
    axes[0].hist(df['revenue'], bins=50, color=RED, alpha=0.85, edgecolor='none')
    axes[0].set_title('Raw Revenue (skewed)', color=WHITE, fontsize=13, pad=10)
    axes[0].set_xlabel('Revenue ($)', color=WHITE)
    axes[1].hist(np.log1p(df['revenue']), bins=50, color='#FF6666', alpha=0.85, edgecolor='none')
    axes[1].set_title('Log Revenue (model target)', color=WHITE, fontsize=13, pad=10)
    axes[1].set_xlabel('log(Revenue)', color=WHITE)
    for ax in axes:
        ax.set_facecolor(DARK2)
        ax.tick_params(colors=WHITE)
        for spine in ax.spines.values():
            spine.set_color('#333')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    plt.tight_layout()
    return fig

def plot_correlation(df):
    cols = ['budget','revenue','popularity','runtime','vote_average','vote_count']
    corr = df[[c for c in cols if c in df.columns]].corr()
    fig, ax = plt.subplots(figsize=(8, 6), facecolor=DARK)
    ax.set_facecolor(DARK)
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='Reds', ax=ax,
                linecolor='#333333', linewidths=0.5,
                annot_kws={'color': WHITE, 'fontsize': 10})
    ax.set_title('Feature Correlation Matrix', color=WHITE, fontsize=14, pad=14)
    plt.xticks(color=WHITE, rotation=30, ha='right')
    plt.yticks(color=WHITE, rotation=0)
    plt.tight_layout()
    return fig

def plot_genre_revenue(df):
    dfc = df.copy()
    dfc['genres'] = dfc['genres'].str.split(',')
    exploded = dfc.explode('genres')
    exploded['genres'] = exploded['genres'].str.strip()
    genre_rev = (exploded.groupby('genres')['revenue'].mean()
                 .sort_values(ascending=False).head(10))
    fig = px.bar(x=genre_rev.values, y=genre_rev.index, orientation='h',
                 title='Average Revenue by Genre (Top 10)',
                 color=genre_rev.values, color_continuous_scale='Reds',
                 labels={'x':'Avg Revenue ($)','y':'Genre'})
    fig.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK2, font_color=WHITE,
                      coloraxis_showscale=False, margin=dict(l=10,r=10,t=40,b=10))
    fig.update_traces(marker_line_width=0)
    return fig

def plot_monthly_trend(df):
    monthly = df.groupby('release_month')['revenue'].mean().reindex(range(1,13))
    months  = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    fig = px.line(x=months, y=monthly.values, markers=True,
                  title='Average Revenue by Release Month',
                  labels={'x':'Month','y':'Avg Revenue ($)'})
    fig.update_traces(line_color=RED, marker_color=WHITE, marker_size=8, line_width=2)
    fig.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK2, font_color=WHITE,
                      margin=dict(l=10,r=10,t=40,b=10))
    return fig

def plot_budget_revenue(df):
    tc = _title_col(df)
    fig = px.scatter(df, x='budget', y='revenue', hover_name=tc,
                     size='popularity', color='vote_average',
                     color_continuous_scale='Reds',
                     title='Budget vs Revenue (bubble size = popularity)',
                     opacity=0.65)
    fig.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK2, font_color=WHITE,
                      margin=dict(l=10,r=10,t=40,b=10))
    return fig

def plot_top_movies(df):
    tc = _title_col(df)
    top = df.nlargest(20, 'revenue')[[tc,'revenue']].copy()
    top.columns = ['title','revenue']
    fig = px.bar(top.sort_values('revenue'), x='revenue', y='title',
                 orientation='h', title='Top 20 Highest Grossing Movies',
                 color='revenue', color_continuous_scale='Reds',
                 labels={'revenue':'Revenue ($)','title':''})
    fig.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK2, font_color=WHITE,
                      height=560, coloraxis_showscale=False,
                      margin=dict(l=10,r=10,t=40,b=10))
    fig.update_traces(marker_line_width=0)
    return fig

def plot_decade_revenue(df):
    dfc = df.copy()
    dfc['decade'] = (dfc['release_year'] // 10 * 10).astype(str) + 's'
    decade_data = dfc.groupby('decade')['revenue'].median().reset_index()
    decade_data = decade_data[decade_data['decade'] != 'nans']
    fig = px.bar(decade_data, x='decade', y='revenue',
                 title='Median Revenue by Decade',
                 color='revenue', color_continuous_scale='Reds',
                 labels={'revenue':'Median Revenue ($)','decade':'Decade'})
    fig.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK2, font_color=WHITE,
                      coloraxis_showscale=False, margin=dict(l=10,r=10,t=40,b=10))
    fig.update_traces(marker_line_width=0)
    return fig