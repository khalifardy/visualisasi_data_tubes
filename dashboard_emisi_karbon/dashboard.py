import pandas as pd
import numpy as np
import panel as pn
pn.extension('tabulator')

import hvplot.pandas

df = pd.read_csv('owid-co2-data.csv')
df = df.fillna(0)
df['gdp_per_capita'] = np.where(df['population'] != 0, df['gdp']/df['population'],0)
idf = df.interactive()
slide_tahun = pn.widgets.IntSlider(name='Slider Tahun',start=1750,end=2020,step=5,value=1850 )

yaxis_co2 = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options = ['co2','co2_per_capita', ],
    button_type='success'
)

benua = [
    'world',
    'Asia',
    'Oceania',
    'Europe',
    'Africa',
    'North America',
    'South America',
    'Antartica'
    
    
]

co2_pipeline = (
        idf[(idf.year <= slide_tahun) & 
        (idf.country.isin(benua))
    ]
    .groupby(['country','year'])[yaxis_co2].mean()
    .to_frame()
    .reset_index()
    .sort_values(by='year')
    .reset_index(drop=True)
)

co2_plot = co2_pipeline.hvplot(x='year', by ='country', y=yaxis_co2, line_width = 2, title= 'Emisi CO2 berdasarkan kontinen')
co2_tabel = co2_pipeline.pipe(pn.widgets.Tabulator, pagination='remote', page_size=10, sizing_mode='stretch_width')


co2_gdp_scat_pipeline = (
    idf[(idf.year == slide_tahun) & 
        (~(idf.country.isin(benua)))
    ]
    .groupby(['country','year','gdp_per_capita'])['co2'].mean()
    .to_frame()
    .reset_index()
    .sort_values(by='year')
    .reset_index(drop=True)
)

co2_gdp_scat = co2_gdp_scat_pipeline.hvplot(x='gdp_per_capita', y='co2', kind='scatter',alpha=0.7, title='CO2 vs GDP per Capita', size=80, by='country',legend=False, height=500, width = 500)
yaxis_co2_source = pn.widgets.RadioButtonGroup(
    name = 'Y axis',
    options = ['coal_co2', 'oil_co2', 'gas_co2'],
    button_type='success'
)

kontinen_tanpa_world = [
    'Asia',
    'Oceania',
    'Europe',
    'Africa',
    'North America',
    'South America',
    'Antartica'
]

cos_source_bar_pipeline = (
    idf[(idf.year == slide_tahun) & 
        (idf.country.isin(kontinen_tanpa_world))
    ]
    .groupby(['country','year'])[yaxis_co2_source].sum()
    .to_frame()
    .reset_index()
    .sort_values(by='year')
    .reset_index(drop=True)
)


co2_source_bar_plot = cos_source_bar_pipeline.hvplot(x='country', y=yaxis_co2_source, title='CO2 Source by Continent', kind='bar')

# Layout usig Template

template = pn.template.FastListTemplate(
    title = 'World CO2 emission dashboard',
    sidebar = [
        pn.pane.Markdown("# CO2 Emisi dan perubahan iklim"),
        pn.pane.Markdown("#### Emisi KArbondiokasida adalah salah satu penyebab utama perubahan iklim global. Dashboard ini memungkinkan Anda untuk memeriksa emisi CO2 berdasarkan tahun, benua, dan sumber."),
        pn.pane.PNG('climate_day.png', sizing_mode='scale_both'),
        pn.pane.Markdown("## Settings"),
        slide_tahun
    ],
    main=[
        pn.Row(
            pn.Column(
                yaxis_co2,
                co2_plot.panel(width=700),margin=(0,25)
            ),
            co2_tabel.panel(width=500)
            
        ),
        pn.Row(
            pn.Column(
                co2_gdp_scat.panel(width=600),
                margin=(0,25)
            ),
            pn.Column(
                yaxis_co2_source,
                co2_source_bar_plot.panel(width=600),
            )
        )
    ],
    accent_base_color = '#88d8b0',
    header_background = '#88d8b0',
)

template.servable()