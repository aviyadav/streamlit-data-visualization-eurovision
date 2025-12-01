import streamlit as st
import polars as pl


def main():
    st.title("Hello GOTO")

    votes = load_votes()
    tab1, tab2, tab3 = st.tabs(["Favourites", "Country", "Raw"])

    with tab1:
        favourites(votes)
    with tab2:
        country_chart(votes)
    with tab3:
        st.dataframe(votes)


@st.cache_data(ttl=3600)
def load_votes():
    votes = pl.read_csv("https://github.com/Spijkervet/eurovision-dataset/releases/download/2023/votes.csv")
    votes = votes.filter(pl.col("round") == "final")
    votes = votes.with_columns(
        pl.when(pl.col("jury_points").is_null())
        .then(pl.col("total_points"))
        .otherwise(pl.col("jury_points"))
        .alias("points")
    )
    votes = votes.with_columns(pl.col("points").cast(pl.Float64).cast(pl.Int32))
    return votes


def favourites(votes):
    favourite_country = (
        votes.filter(pl.col("points") == 12)
        .group_by(["from_country", "to_country"])
        .agg(pl.col("points").count())
    )

    st.scatter_chart(favourite_country, x="from_country", y="to_country", size="points")


def country_chart(votes):
    all_countries = votes["to_country"].unique().sort().to_list()
    selected_country = st.selectbox("Choose a country", all_countries)
    total_by_country = (
        votes.filter(pl.col("to_country") == selected_country)
        .group_by(["to_country", "year"])
        .agg(pl.col("points").sum())
        .sort("year")
    )

    st.line_chart(total_by_country, x="year", y="points")
    total_by_country


def typography():
    st.header("Live demo")
    st.subheader("Hopefully everything goes according to 'plan'")
    st.text("I'm running out of things to type")

    with open("README.md", "r") as file:
        readme = file.read()

    st.markdown(readme)

    st.divider()
    with st.echo():
        with st.echo():
            "I'm running out of things to type"
            1 + 2 + 3 + 4 + 5
    st.divider()


if __name__ == "__main__":
    main()