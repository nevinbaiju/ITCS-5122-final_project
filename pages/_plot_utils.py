import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import pandas as pd

ticks_settings = {'fontsize':15}
label_settings = {'fontsize':25}

def plot_segment_volume(df):
    sub_df = df[df['year'] > 2011]
    grouped_df = sub_df.groupby(['model', 'year'], as_index=False).count()

    fig = plt.figure(figsize=(18, 10))
    plt.title('Resale volume by model year for different models', **label_settings)
    sns.barplot(y=grouped_df['price'], x=grouped_df['model'], hue=grouped_df['year'])
    plt.xticks(**ticks_settings)
    plt.xlabel("Models and their model years", **label_settings)
    plt.ylabel("Resale volume", **label_settings)

    return fig

def plot_segment_volume_altair(df):
    sub_df = df[df['year'] > 2011]
    grouped_df = sub_df.groupby(['model', 'year'], as_index=False).count()

    chart = alt.Chart(grouped_df).mark_bar().encode(
    x=alt.X('year:N', title='Year'),
    y=alt.Y('price:Q', title='Price'),
    color=alt.Color('year:N', title='Year')
    ).facet(
        column='model:N'
    )
    return chart

def plot_price_with_age(df):
    grouped_df = df.groupby(['model', 'age']).mean()[['price', 'odometer']].reset_index()
    grouped_df = grouped_df[grouped_df['age'] <= 15]
    # Create Altair chart
    chart = alt.Chart(grouped_df).mark_line().encode(
        x=alt.X('age:Q', title='Age'),
        y=alt.Y('price:Q', title='Price'),
        color=alt.Color('model:N', title='Model')
    ).properties(
        title='Price by Age and Model',
        width=800,
        height=400,
    )
    
    return chart

def plot_mileage_with_age(df):
    grouped_df = df.groupby(['model', 'age']).mean()[['price', 'odometer']].reset_index()
    grouped_df = grouped_df[grouped_df['age'] <= 15]
    # Create Altair chart
    chart = alt.Chart(grouped_df).mark_line().encode(
        x=alt.X('age:Q', title='Age'),
        y=alt.Y('odometer:Q', title='Mileage'),
        color=alt.Color('model:N', title='Model')
    ).properties(
        title='Mileage by Age and Model',
        width=800,
        height=400,
    )
    
    return chart