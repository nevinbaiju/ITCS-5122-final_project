import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from vega_datasets import data
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
    y=alt.Y('price:Q', title='Volume'),
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
        width=550,
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
        width=550,
        height=400,
    )
    
    return chart

def plot_choropleth(df, var, model):
    df = df.copy()
    df = df[df['model'] == model]
    grouped_df = df.groupby(['state']).agg({'price': 'mean', 'year': 'count'}).reset_index()
    state_names = grouped_df.state.unique()
    state_ids = [x+1 for x in range(len(state_names))]
    state_mappings = pd.DataFrame({'state': state_names, 'id': state_ids})

    grouped_df = grouped_df.merge(state_mappings, on='state', how='left')

    states = alt.topo_feature(data.us_10m.url, 'states')

    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project('albersUsa').properties(
        width=600,
        height=400
    )

    ch_map = alt.Chart(states).mark_geoshape().encode(
                color='price:Q',
                tooltip=['id:O', 'price:Q']
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(grouped_df, 'id', ['price'])
            ).project(
                type='albersUsa'
            ).properties(
                width=600,
                height=400,
                title=f'Price of {model} for each states'
            )
    return background+ch_map

def plot_scatter_with_age(df, model, var):
    model_df = df[df['model'] == model]
    model_df = model_df[(model_df['price'] < 35000) & (model_df['age'] < 30) & (model_df['odometer'] < 300000)]
    model_df.dropna(subset=['condition'], inplace=True)

    scatter = alt.Chart(model_df).mark_point().encode(
        x='age',
        y=var,
        color='condition'
    ).properties(
        title=f'{var.capitalize()} vs Age marked by the condition',
        height=600, width=750,
    )
    
    return scatter