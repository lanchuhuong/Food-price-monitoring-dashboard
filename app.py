import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import pycountry
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

external_stylesheets = [dbc.themes.BOOTSTRAP]

# import the data
<<<<<<< HEAD
# df = pd.read_csv(
#     "https://ec.europa.eu/eurostat/databrowser-backend/api/extraction/1.0/LIVE/true/sdmx/csv/PRC_FSC_IDX?i&compressed=false"
# )
# df.to_csv("data.csv", index=False)
df = pd.read_csv("data.csv")
=======
df = pd.read_csv(
    "https://ec.europa.eu/eurostat/databrowser-backend/api/extraction/1.0/LIVE/true/sdmx/csv/PRC_FSC_IDX?i&compressed=false"
)

>>>>>>> e9dec10153d4e2a46ea22b9d641ef0067b124417
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
    {"Country": country.name, "alpha_2": country.alpha_2, "alpha_3": country.alpha_3}
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
df["pct_diff"] = df.groupby(["geo", "coicop"], as_index=True)[
    "Percentage change m/m-12"
].pct_change(periods=12)

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
    ]
)

html_dropdown_country = (
    html.Div(
        [
            dbc.Label("Country"),
            dcc.Dropdown(
                id="dropdown_country",
                options=[{"value": x, "label": x} for x in df["Country"].unique()],
                value="Netherlands",
            ),
        ],
        className="mb-4",
    ),
)

html_dropdown_foodcategory = (
    html.Div(
        [
            dbc.Label("Food Category"),
            dcc.Dropdown(
                id="dropdown_food_category",
                options=[{"value": x, "label": x} for x in df["label"].unique()],
                value="Bread and cereals",
            ),
        ],
        className="mb-4",
    ),
)

countries = sorted(df["Country"].dropna().unique())


html_world_map = html.Div(
    dcc.Graph(id="choropleth"),
)

html_line_graph = html.Div(
    dcc.Graph(id="line"),
)


container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4(
                                        id="card_title_1",
                                        children=[
                                            "HICP inflation rate - Overall index "
                                        ],
                                        className="card-title",
                                    ),
                                    html.P(
                                        id="card_text_1",
<<<<<<< HEAD
                                        # children=["Sample text."],
=======
                                        # children=["text."],
>>>>>>> e9dec10153d4e2a46ea22b9d641ef0067b124417
                                    ),
                                ]
                            )
                        ]
                    ),
                    md=6,
                    style={"margin-bottom": "20px"},
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4(
                                        id="card_title_2",
                                        children=[
                                            "HICP inflation rate - Overall index "
                                        ],
                                        className="card-title",
                                    ),
                                    html.P(
                                        id="card_text_2",
<<<<<<< HEAD
                                        # children=["Sample text."],
=======
                                        # children=["text."],
>>>>>>> e9dec10153d4e2a46ea22b9d641ef0067b124417
                                    ),
                                ]
                            )
                        ]
                    ),
                    md=6,
                    style={"margin-bottom": "20px"},
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html_world_map,
                    width=6,
                ),
                dbc.Col(html_line_graph, width=6, style={"margin-bottom": "20px"}),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html_slider, width=4, style={"margin-bottom": "20px"}),
                dbc.Col(
                    html_dropdown_country, width=4, style={"margin-bottom": "20px"}
                ),
                dbc.Col(html_line_graph, width=6, style={"margin-bottom": "20px"}),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html_slider, width=6, style={"margin-bottom": "20px"}),
                dbc.Col(
                    html_dropdown_foodcategory, width=4, style={"margin-bottom": "20px"}
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4(
                                        id="card_title_3",
                                        children=["About this dataset "],
                                        className="card-title",
                                    ),
                                    html.P(
                                        id="card_text_3",
                                        children=[
                                            html.A(
                                                "Link to more information",
                                                href="https://ec.europa.eu/eurostat/cache/metadata/en/prc_fsc_idx_esms.htm",
                                            )
                                        ],
                                    ),
                                ]
                            )
                        ]
                    ),
                    md=6,
                    style={"margin-bottom": "20px"},
                ),
                # dbc.Col(
                #     html_dropdown_foodcategory, width=4, style={"margin-bottom": "20px"}
                # ),
            ]
        ),
    ]
)


layout = html.Div(
    [title, container],
    style={
        "color": "DarkBlue",
        "font-weight": "bold",
        "marginBottom": 100,
        "marginTop": 50,
    },
)


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
        labels={"Percentage change m/m-12": "Percentage change"},
        color_continuous_scale=px.colors.sequential.Blues,
        # width=500, height=400
    )
    fig_world_map.update_layout(
        # title="HICP inflation rate",
        margin=dict(l=10, r=0, t=20, b=0),
        paper_bgcolor="#d8e1ee",
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
        # title= 'HICP inflation rate'
    )
    fig_line.update_layout(
        # title="HICP inflation rate",
        xaxis_title="Period",
        legend=dict(
            font=dict(
                family="Arial",
                size=10,
                # color="black"
            )
        ),
        margin=dict(l=10, r=0, t=20, b=0),
        paper_bgcolor="#d8e1ee",
    )

    return fig_line


if __name__ == "__main__":
    dash_app.run_server(debug=False)
