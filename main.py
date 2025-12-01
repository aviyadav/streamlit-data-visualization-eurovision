import streamlit as st
import pandas as pd


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
    votes = pd.read_csv("https://github.com/Spijkervet/eurovision-dataset/releases/download/2023/votes.csv")
    votes = votes[votes["round"] == "final"]
    votes["points"] = votes["jury_points"].fillna(votes["total_points"])
    return votes


def favourites(votes):
    favourite_country = (
        votes[votes["points"] == 12]
        .groupby(["from_country", "to_country"])["points"]
        .count()
        .reset_index()
    )

    st.scatter_chart(favourite_country, x="from_country", y="to_country", size="points")


def country_chart(votes):
    all_countries = votes["to_country"].unique()
    all_countries.sort()
    selected_country = st.selectbox("Choose a country", all_countries)
    total_by_country = (
        votes[votes["to_country"] == selected_country]
        .groupby(["to_country", "year"])["points"]
        .sum()
        .reset_index()
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