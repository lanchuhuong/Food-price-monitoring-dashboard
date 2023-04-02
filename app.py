import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import pycountry
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template

external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.themes.YETI]
load_figure_template("YETI")


def get_data(url):
    # get data from api
    df = pd.read_csv(url)

    df = df[(df["indx"] == "HICP") & (df["unit"] == "PCH_M12")]
    df = df.rename(
        {"TIME_PERIOD": "period", "OBS_VALUE": "Percentage change m/m-12"}, axis=1
    )
    coicop_label = {
        "Food": "CP011",
        "Bread and cereals": "CP0111",
        "Bread": "CP01113",
        "Meat": "CP0112",
        "Beef and veal": "CP01121",
        "Pork": "CP01122",
        "Lamb and goat": "CP01123",
        "Poultry": "CP01124",
        "Fish and seafood": "CP0113",
        "Milk. Cheese and eggs": "CP0114",
        "Fresh whole milk": "CP01141",
        "Yogurt": "CP01144",
        "Cheese and curd": "CP01145",
        "Eggs": "CP01147",
        "Oils and fats": "CP0115",
        "Butter": "CP01151",
        "Olive oil": "CP01153",
        "Other dible oils": "CP01154",
        "Fruit": "CP0116",
        "Vegetables": "CP0117",
        "Potatoes": "CP01174",
        "Sugar": "CP01181",
        "Coffee, tea and cocoa": "CP0121",
        "Fruit and vegetables juices": "CP01223",
        "Wine from grapes": "CP02121",
        "Beer": "CP02123",
    }
    coicop_label = pd.DataFrame.from_dict(coicop_label, orient="index")
    coicop_label = coicop_label.reset_index().rename(
        {"index": "label", 0: "coicop"}, axis=1
    )
    df = df.merge(coicop_label, left_on="coicop", right_on="coicop", how="left")
    df = df[df["label"].notnull()]
    countries = [
        {
            "Country": country.name,
            "alpha_2": country.alpha_2,
            "alpha_3": country.alpha_3,
        }
        for country in pycountry.countries
    ]
    df.rename({"Country_name": "Country"}, axis=1)
    countries = pd.DataFrame(countries)
    df = df.merge(countries, left_on="geo", right_on="alpha_2", how="left")
    df = df[
        [
            "period",
            "indx",
            "Percentage change m/m-12",
            "coicop",
            "Country",
            "alpha_2",
            "geo",
            "alpha_3",
            "label",
        ]
    ]
    return df


df = get_data(
    "https://ec.europa.eu/eurostat/databrowser-backend/api/extraction/1.0/LIVE/true/sdmx/csv/PRC_FSC_IDX?i&compressed=false"
)

period = sorted(df["period"].unique())
mask = df["period"] == period[-1]
df_tmp = (
    df[mask]
    .dropna(subset=["Percentage change m/m-12"])[
        ["Country", "Percentage change m/m-12"]
    ]
    .fillna("")
)

years = np.arange(int(period[0][:4]), int(period[-1][:4]) + 1)
months = {
    "01": "Jan",
    "02": "Feb",
    "03": "Mar",
    "04": "Apr",
    "05": "May",
    "06": "Jun",
    "07": "Jul",
    "08": "Aug",
    "09": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
}

marks_months = {i: month for i, month in enumerate(months.values())}
period = list(df["period"].unique())
marks = {idx: period_str for idx, period_str in enumerate(period)}


## Layout

SIDEBAR_STYLE = {
    # "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "height": "100%",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


title = html.H2(
    "Food price monitoring tool - the harmonised index of consumer prices (HICP)",
    style={"text-align": "center"},
)
foodcategory = sorted(df["label"].dropna().unique())

foodcategory_option_columns = [{"value": x, "label": x} for x in foodcategory]


html_slider = html.Div(
    [
        dbc.Label("Date", id="slider_label"),
        dcc.Slider(
            id="slider_year",
            min=years[0],
            max=years[-1],
            marks={int(year): str(year) for year in [years[0], years[-1]]},
            step=1 / 12,
            value=2022.25,
        ),
        html.Br(),
    ]
)

html_dropdown_country = html.Div(
    [
        dbc.Label("Country"),
        dcc.Dropdown(
            id="dropdown_country",
            options=[{"value": x, "label": x} for x in df["Country"].unique()],
            value="Netherlands",
        ),
        html.Br(),
    ],
)

html_dropdown_foodcategory = html.Div(
    [
        dbc.Label("Food Category"),
        dcc.Dropdown(
            id="dropdown_food_category",
            options=[{"value": x, "label": x} for x in df["label"].unique()],
            value="Bread and cereals",
        ),
        html.Br(),
    ],
)

html_about = html.Div(
    [
        dbc.Label("About this data set"),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(
                            id="card_title_3",
                            children=[
                                html.A(
                                    "Link to more information",
                                    href="https://ec.europa.eu/eurostat/cache/metadata/en/prc_fsc_idx_esms.htm",
                                    style={},
                                )
                            ],
                            className="card-title",
                        ),
                    ]
                ),
            ]
        ),
    ]
)

sidebar = html.Div(
    [
        html.H2("Filters"),
        html.Hr(),
        dbc.Nav(
            [
                html_slider,
                html_dropdown_country,
                html_dropdown_foodcategory,
                html_about,
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


countries = sorted(df["Country"].dropna().unique())


html_world_map = html.Div(
    dcc.Graph(id="choropleth"),
)

html_line_graph = html.Div(
    dcc.Graph(id="line"),
)

html_center = html.Div(
    [
        html.Center(
            html.H1("Inflation dashboard app (HICP index)"),
            style={"margin-bottom": "20px", "margin-top": "20px"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html_world_map,
                                    width=12,
                                ),
                                dbc.Col(
                                    html_line_graph,
                                    width=12,
                                ),
                            ],
                            style={
                                "margin-right": "20px",
                            },
                        ),
                    ]
                ),
            ]
        ),
    ],
)

layout = html.Div(dbc.Row([dbc.Col(sidebar, width=3), dbc.Col(html_center, width=9)]))


# Run Server
dash_app = Dash(__name__, external_stylesheets=external_stylesheets)
dash_app.layout = layout
app = dash_app.server


# callbacks
@dash_app.callback(
    Output(component_id="slider_label", component_property="children"),
    Input(component_id="slider_year", component_property="drag_value"),
)
def update_slider_label(period):
    if period:
        # convert e.g. 2020.25 to 'Mar 2020'
        year = int(period)
        index = int(np.round(12 * (period - year)))
        month = list(months.values())[index]

        return f"{month} {year}"


@dash_app.callback(
    Output(component_id="choropleth", component_property="figure"),
    Input(component_id="slider_year", component_property="drag_value"),
    Input(component_id="dropdown_food_category", component_property="value"),
)
def update_world_map(date, foodcategory):
    # convert e.g. 2002.25 to '2002-03'
    year = int(date)
    index = int(np.round(12 * (date - year)))
    month = list(months.keys())[index]
    period = f"{year}-{month}"

    mask = (period == df["period"]) & (foodcategory == df["label"])
    fig_world_map = px.choropleth(
        df[mask].dropna(subset=["Percentage change m/m-12"]),
        locations="alpha_3",
        color="Percentage change m/m-12",
        hover_name="Country",
        featureidkey="properties.ISO_A3",
        projection="natural earth",
        scope="europe",
        color_continuous_scale=px.colors.sequential.Blues,
        # width=500, height=400
    )
    fig_world_map.update_layout(
        autosize=False,
        margin=dict(l=0, r=0, b=0, t=0, pad=4, autoexpand=True),
        # width=800,
        #     height=400,
    )
    return fig_world_map


@dash_app.callback(
    # Set the input and output of the callback to link the dropdown to the graph
    Output(component_id="line", component_property="figure"),
    Input(component_id="dropdown_country", component_property="value"),
    Input(component_id="dropdown_food_category", component_property="value"),
)
def update_line_plot(country, food_label):
    if country:
        mask = (df["Country"] == country) & (df["label"] == food_label)
        df_tmp = df[mask]
    else:
        mask = df["label"] == food_label
        df_tmp = df[mask]

    fig_line = px.line(
        df_tmp,
        x="period",
        y="Percentage change m/m-12",
        color="Country",
        markers=True,
        symbol="Country",
        #    width=500, height=400
    )

    return fig_line


if __name__ == "__main__":
    dash_app.run_server(debug=False)
