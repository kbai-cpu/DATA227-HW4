import altair as alt
import pandas as pd

def base_theme():
    return {
        "config": {
            "view": {"stroke": None},
            "axis": {"labelFontSize": 12, "titleFontSize": 14},
            "legend": {"labelFontSize": 12, "titleFontSize": 14},
        }
    }

def chart_hook_temp_over_time(df: pd.DataFrame) -> alt.Chart:
    return (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("temp_max:Q", title="Daily max temp (°C)"),
            tooltip=[alt.Tooltip("date:T"), alt.Tooltip("temp_max:Q", format=".1f")],
        )
        .properties(height=320)
    )

def chart_context_seasonality(df: pd.DataFrame) -> alt.Chart:
    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    return (
        alt.Chart(df)
        .mark_boxplot()
        .encode(
            x=alt.X("month_name:N", title="Month", sort=month_order),
            y=alt.Y("temp_max:Q", title="Daily max temp (°C)"),
        )
        .properties(height=320)
    )

def chart_surprise_extremes(df: pd.DataFrame) -> alt.Chart:
    q = float(df["temp_max"].quantile(0.99))
    df2 = df.copy()
    df2["extreme"] = df2["temp_max"] >= q

    base = (
        alt.Chart(df2)
        .mark_point(filled=True, size=35)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("temp_max:Q", title="Daily max temp (°C)"),
            color=alt.condition("datum.extreme", alt.value("red"), alt.value("lightgray")),
            tooltip=[alt.Tooltip("date:T"), alt.Tooltip("temp_max:Q", format=".1f")],
        )
        .properties(height=320)
    )

    rule = alt.Chart(pd.DataFrame({"q": [q]})).mark_rule(strokeDash=[6, 4]).encode(y="q:Q")
    return base + rule

def chart_explain_precip_vs_temp(df: pd.DataFrame) -> alt.Chart:
    return (
        alt.Chart(df)
        .mark_point(opacity=0.45)
        .encode(
            x=alt.X("precipitation:Q", title="Precipitation (in)"),
            y=alt.Y("temp_max:Q", title="Daily max temp (°C)"),
            tooltip=[
                "date:T",
                alt.Tooltip("precipitation:Q", format=".2f"),
                alt.Tooltip("temp_max:Q", format=".1f"),
            ],
        )
        .properties(height=320)
    )

def chart_dashboard(df: pd.DataFrame) -> alt.Chart:
    weather_types = sorted(df["weather"].unique())

    w_select = alt.selection_point(
        fields=["weather"],
        bind=alt.binding_select(options=weather_types, name="Weather: "),
    )
    brush = alt.selection_interval(encodings=["x"], name="Time window")

    line = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("temp_max:Q", title="Daily max temp (°C)"),
            color=alt.Color("weather:N", title="Weather"),
            tooltip=["date:T", "weather:N", alt.Tooltip("temp_max:Q", format=".1f")],
        )
        .add_params(w_select, brush)
        .transform_filter(w_select)
        .properties(height=260)
    )

    hist = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("temp_max:Q", bin=alt.Bin(maxbins=30), title="Daily max temp (°C)"),
            y=alt.Y("count():Q", title="Days"),
            tooltip=[alt.Tooltip("count():Q", title="Days")],
        )
        .transform_filter(w_select)
        .transform_filter(brush)
        .properties(height=260)
    )

    return alt.vconcat(line, hist).resolve_scale(color="independent")

def chart_interactive_wind_vs_temp(df: pd.DataFrame) -> alt.Chart:
    weather_dropdown = alt.binding_select(
    options=sorted(df['weather'].unique()),
    name='Highlight Weather: '
)

    selection = alt.selection_point(
    fields=['weather'],
    bind=weather_dropdown,
    empty='all'
)

    colors = alt.Scale(
    domain=['drizzle', 'fog', 'rain', 'snow', 'sun'],
    range=['#1f77b4','#ff7f0e','#d62728','#17becf','#2ca02c'] 
)

    chart = alt.Chart(df).mark_circle().encode(
    x='temp_max:Q',
    y='wind:Q',
    color=alt.Color('weather:N', scale=colors),
    opacity=alt.condition(
        selection,
        alt.value(1),      
        alt.value(0.115)    
    ),
    ).add_params(
    selection
    ).properties(
    width=500,
    height=400,
    title='Wind vs Max Temperature (Highlight by Weather Type)'
    )
    return chart

def chart_static_temp_weather(df: pd.DataFrame) -> alt.Chart:
    return (
        alt.Chart(df).mark_bar().encode(
    x=alt.X('temp_max:Q', bin=alt.Bin(maxbins=20)),
    y='count()'
).facet(
    column=alt.Column('weather:N', title='Weather Type')
).properties(
    title=alt.TitleParams(
        text='Temperature Distribution by Weather Type',
        anchor='middle'
    )
)
    )


# ── Premier League charts ────────────────────────────────────────────────────

def chart_team_performance(team_summary_long: pd.DataFrame):
    """Q1: Season-over-season performance. Returns (chart, team_select) so Q2 can share the selection."""
    metric_param = alt.param(
        name='SelectedMetric',
        bind=alt.binding_select(
            options=['Points', 'Win', 'GoalDiff'],
            name='Metric: ',
        ),
        value='Points',
    )
    team_select = alt.selection_point(fields=['Team'], on='click', empty='all')

    base = (
        alt.Chart(team_summary_long)
        .add_params(metric_param, team_select)
        .transform_filter(alt.datum.Metric == metric_param)
    )

    lines = (
        base.mark_line()
        .encode(
            x=alt.X('Season:N', title='Season'),
            y=alt.Y('Value:Q', title='Performance'),
            detail='Team:N',
            color=alt.condition(team_select, alt.value('#1f77b4'), alt.value('lightgray')),
            opacity=alt.condition(team_select, alt.value(1), alt.value(0.3)),
        )
    )
    points = (
        base.mark_circle(size=60)
        .encode(
            x='Season:N',
            y='Value:Q',
            detail='Team:N',
            color=alt.condition(team_select, alt.value('#1f77b4'), alt.value('lightgray')),
            opacity=alt.condition(team_select, alt.value(1), alt.value(0.3)),
            tooltip=['Team:N', 'Season:N', 'Metric:N', 'Value:Q'],
        )
    )

    chart = (lines + points).properties(
        width=300,
        height=500,
        title='Team Performance Comparison Across Seasons (2023–24 vs 2024–25)',
    )
    return chart, team_select


def chart_attacking_consistency(team_attack_long: pd.DataFrame, team_select) -> alt.Chart:
    """Q2: 3-match rolling average attacking consistency, faceted by season. Linked to Q1 via team_select."""
    attack_metric_param = alt.param(
        name='AttackMetric',
        bind=alt.binding_select(
            options=['Goals', 'Shots', 'ShotsOnTarget'],
            name='Attacking Metric: ',
        ),
        value='Goals',
    )
    return (
        alt.Chart(team_attack_long)
        .add_params(attack_metric_param)
        .transform_filter(team_select)
        .transform_filter(alt.datum.Metric == attack_metric_param)
        .mark_line()
        .encode(
            x=alt.X('Matchweek:Q', title='Matchweek'),
            y=alt.Y('RollingValue:Q', title='3-Match Rolling Average'),
            color=alt.value('#1f77b4'),
            tooltip=[
                'Team:N', 'Season:N', 'Matchweek:Q', 'Metric:N',
                alt.Tooltip('RollingValue:Q', format='.2f'),
            ],
        )
        .properties(width=500, height=350)
        .facet(column=alt.Column('Season:N', title='Season'))
        .properties(title='Attacking Consistency Within Each Season (3-Match Rolling Average)')
    )


def chart_home_advantage(q3_pivot: pd.DataFrame) -> alt.Chart:
    """Q3: Home vs Away scatter with diagonal parity line, brushed to a grouped bar of home advantage."""
    brush = alt.param(select='interval')

    max_pts = q3_pivot[['Points_Home', 'Points_Away']].max().max()
    diag_line = (
        alt.Chart(pd.DataFrame({'x': [0, max_pts], 'y': [0, max_pts]}))
        .mark_line(color='black', strokeDash=[4, 4])
        .encode(x='x:Q', y='y:Q')
    )

    scatter = (
        alt.Chart(q3_pivot)
        .add_params(brush)
        .mark_circle(size=80)
        .encode(
            x=alt.X('Points_Away:Q', title='Away Points'),
            y=alt.Y('Points_Home:Q', title='Home Points'),
            color=alt.condition(brush, alt.value('#1f77b4'), alt.value('lightgray')),
            tooltip=[
                'Team:N', 'Season:N',
                'Points_Home:Q', 'Points_Away:Q',
                'GoalDiff_Home:Q', 'GoalDiff_Away:Q',
            ],
        )
        .properties(width=500, height=500, title='Home vs Away Performance')
    )

    bar = (
        alt.Chart(q3_pivot)
        .transform_filter(brush)
        .mark_bar()
        .encode(
            x=alt.X('Team:N', sort='-y'),
            xOffset=alt.XOffset('Season:N'),
            y=alt.Y('HomeAdvantage:Q', title='Home Advantage (Points)'),
            color=alt.Color('Season:N'),
            tooltip=['Team:N', 'Season:N', 'HomeAdvantage:Q'],
        )
        .properties(width=500, height=300, title='Home Advantage by Season (Brushed Teams)')
    )

    return alt.vconcat(alt.layer(scatter, diag_line), bar)