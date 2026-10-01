
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="Movie Rating Analysis",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_excel("Indian movies.xlsx")

# -----------------------------
# DATA CLEANING
# -----------------------------
df = df.replace("-", pd.NA)

df["Rating(10)"] = pd.to_numeric(
    df["Rating(10)"], errors="coerce"
)

df["Votes"] = pd.to_numeric(
    df["Votes"], errors="coerce"
)

df["Year"] = pd.to_numeric(
    df["Year"], errors="coerce"
)

df["Timing_num"] = (
    df["Timing(min)"]
    .astype(str)
    .str.extract(r"(\d+)")
    .astype(float)
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🎬 Movie Rating Analysis Dashboard")
st.write("Indian Movies Data Analysis")

st.divider()

# -----------------------------
# KPI CARDS
# -----------------------------
total_movies = len(df)
average_rating = df["Rating(10)"].mean()
highest_rating = df["Rating(10)"].max()
total_languages = df["Language"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("🎥 Total Movies", total_movies)
col2.metric("⭐ Average Rating", round(average_rating, 2))
col3.metric("🏆 Highest Rating", highest_rating)
col4.metric("🌐 Languages", total_languages)

st.divider()

# -----------------------------
# LANGUAGE FILTER
# -----------------------------
languages = df["Language"].dropna().unique()

selected_language = st.selectbox(
    "🌐 Select Language",
    ["All"] + sorted(languages.tolist())
)

if selected_language == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[
        df["Language"] == selected_language
    ]

# -----------------------------
# MOVIE TABLE
# -----------------------------
st.subheader("🎥 Movie Data")

st.dataframe(
    filtered_df[
        [
            "Movie Name",
            "Year",
            "Rating(10)",
            "Votes",
            "Genre",
            "Language"
        ]
    ],
    use_container_width=True
)

st.divider()

# -----------------------------
# RATING DISTRIBUTION
# -----------------------------
st.subheader("⭐ Rating Distribution")

fig, ax = plt.subplots(figsize=(10, 4))

ax.hist(
    filtered_df["Rating(10)"].dropna(),
    bins=10,
    edgecolor="black"
)

ax.set_xlabel("Rating")
ax.set_ylabel("Number of Movies")
ax.set_title("Movie Rating Distribution")

st.pyplot(fig)

# -----------------------------
# LANGUAGE RATING
# -----------------------------
st.subheader("🌐 Average Rating by Language")

language_rating = (
    filtered_df
    .groupby("Language")["Rating(10)"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(language_rating)

# -----------------------------
# YEAR ANALYSIS
# -----------------------------
st.subheader("📅 Average Rating by Year")

year_rating = (
    filtered_df
    .groupby("Year")["Rating(10)"]
    .mean()
    .sort_index()
)

st.line_chart(year_rating)

# -----------------------------
# TOP RATED MOVIES
# -----------------------------
st.subheader("🏆 Top Rated Movies")

top_movies = (
    filtered_df
    .dropna(subset=["Rating(10)"])
    .sort_values("Rating(10)", ascending=False)
    .head(10)
)

st.dataframe(
    top_movies[
        [
            "Movie Name",
            "Year",
            "Rating(10)",
            "Votes",
            "Genre",
            "Language"
        ]
    ],
    use_container_width=True
)
