import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from sqlalchemy import create_engine,text
import time
import seaborn as sns
import matplotlib.pyplot as plt

with st.sidebar:
    selected = option_menu("TMDB Movie Analytics", ["Filter", "Dashboard","Query Explorer"], icons=["sliders", "speedometer2", "search"], menu_icon="cast", default_index=0)

password = "dbms%40123"
#https://stackoverflow.com/questions/1423804/writing-a-connection-string-when-password-contains-special-characters

host = "127.0.0.1"
engine = create_engine(
    f"mysql+pymysql://root:{password}@{host}:3306/Movie_Analytis"
    #mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
)

movies_q = text("""SELECT * FROM Movies;""")
genres_q = text("""SELECT * FROM Genres;""")
movie_genres_q = text("""SELECT * FROM Movie_Genres;""")
cast_q = text("""SELECT * FROM Cast;""")

with engine.connect() as connection:
    movies = pd.read_sql(movies_q,connection)
    genres = pd.read_sql(genres_q,connection)
    movie_genres = pd.read_sql(movie_genres_q,connection)
    cast = pd.read_sql(cast_q,connection)

movies["Release_Date_yr"] = pd.to_datetime(movies["Release_Date"]).dt.year
hero_image, hero_content = st.columns([1, 2])
with hero_image:

    st.image(
        "image-1.png",
        width=250
    )
with hero_content:

    st.markdown("""
    <style>
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        text-align: center;
        color: #FFFFFF;  /* TMDB-inspired yellow */
        margin-bottom: 1rem;
        letter-spacing: 1px;

        /* Optional glow */
        text-shadow: 0 0 5px rgba(1, 180, 228, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="hero-title">TMDB Movie Analytics</div>',
        unsafe_allow_html=True
    )
temp=movies.merge(movie_genres,on="Movie_ID",how="inner").merge(genres,on="Genre_ID",how="inner")
language_map = {
    "en": "English",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "zh": "Chinese",
    "ja": "Japanese",
    "it": "Italian",
    "sv": "Swedish",
    "pt": "Portuguese",
    "ko": "Korean",
    "cn": "Chinese",
    "ru": "Russian",
    "hi": "Hindi",
    "el": "Greek",
    "sr": "Serbian",
    "id": "Indonesian",
    "da": "Danish",
    "tr": "Turkish",
    "pl": "Polish",
    "lv": "Latvian",
    "fi": "Finnish"}
reverse_language_map = {v: k for k, v in language_map.items()}
movies["Language_name"] = movies["Original_Language"].map(language_map)
 
if selected == "Filter":

    unique_genres = list(genres["Genres_name"].unique())
    st.multiselect("What are your favorite Genres ?",unique_genres,key="selected_genres")
    st.markdown("</br></br>",unsafe_allow_html=True)
    st.slider("Select Movie Year from below slider",min_value =movies["Release_Date_yr"].min(),max_value=movies["Release_Date_yr"].max(),key="selected_year")
    st.markdown("</br></br>",unsafe_allow_html=True)
    st.selectbox("Select the languag from below options",list(movies["Language_name"].unique()),key="selected_language")
    selected_genres = st.session_state["selected_genres"]
    selected_year = st.session_state["selected_year"]
    selected_language = st.session_state["selected_language"]
    count_under_filter = temp[(temp["Genres_name"].isin(selected_genres)) & (temp["Release_Date_yr"]==selected_year) & (temp["Original_Language"]==reverse_language_map[selected_language])]["Movie_ID"].nunique()
    x, y = st.columns([1, 1.3])
    with x:
        st.markdown("""
        <style>
        .count-text {
            font-size: 1rem;
            color: #FFFFFF;
            margin-top: 2.5rem;
            margin-bottom: 3rem;
            border: 2px solid #e1e1e1;
            border-radius: 0.5rem;
            padding: 1.5rem 1rem;
            height: 5rem;
            box-sizing: border-box;
            align-items:center;
        }
        .count-text:hover{
            transform: translateY(-5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            border-color: #999999; 
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="count-text">
                Count of movies with current filters:   <b><i>{count_under_filter}<i></b>
            </div>
            """,
            unsafe_allow_html=True
        )
elif selected == "Dashboard":
    st.markdown("</br></br>",unsafe_allow_html=True)
    try:
        selected_genres = st.session_state["selected_genres"]
        selected_year = st.session_state["selected_year"]
        selected_language = st.session_state["selected_language"]
        data_under_current_filter = temp[(temp["Genres_name"].isin(selected_genres)) & (temp["Release_Date_yr"]==selected_year) & (temp["Original_Language"]==reverse_language_map[selected_language])]
        col1, col2, col3, col4 = st.columns(4)
        st.markdown("""
        <style>

            div[data-testid="stMetric"] {
                background-color: #000000;
                border: 2px solid #e1e1e1;
                border-radius: 0.5rem;
                padding: 1rem 0.9rem;
                height: 6.875rem;
                box-sizing: border-box;
                transition: transform 0.2s, box-shadow 0.2s;
            }

            div[data-testid="stMetric"]:hover {
                transform: translateY(-5px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                border-color: #999999;
            }

            div[data-testid="stMetricLabel"] {
                color: #FFFFFF;
                font-size: 1rem;
            }

            div[data-testid="stMetricValue"] {
                color: #FFFFFF;
                font-size: 1.3rem;
                font-weight: 400;
            }
        </style>
        """, unsafe_allow_html=True)
        with col1:
            st.metric("Total Movies", data_under_current_filter["Movie_ID"].nunique())
        with col2:
            st.metric("Total Genres", data_under_current_filter["Genre_ID"].nunique())
        with col3:
            temp_actors=data_under_current_filter.merge(cast,on="Movie_ID",how="inner")
            st.metric("Total Actors",temp_actors["Person_ID"].nunique())
        with col4:
            st.metric("Average Rating",round(data_under_current_filter["Vote_Average"].mean(),3))

        top_10_movie_by_revenue = data_under_current_filter.sort_values(by="Revenue", ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=top_10_movie_by_revenue,x="Title",y="Revenue",ax=ax)
        ax.set_title("Top 10 Movies by Revenue")
        ax.set_xlabel("Movie Title")
        ax.set_ylabel("Revenue")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(data_under_current_filter["Genres_name"].value_counts(),labels=data_under_current_filter["Genres_name"].unique(),autopct="%1.1f%%",startangle=90,pctdistance=0.75)
        ax.set_title("Genre Distribution of Filtered Movies")
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.scatterplot(data_under_current_filter,x="Budget",y="Revenue",ax=ax)
        ax.set_title("Scatter plot of Budget V/S Revenue")
        st.pyplot(fig)

        df = data_under_current_filter

        if not df.empty:

            total_movies = df["Movie_ID"].nunique()
            highest_movie = df.loc[df["Revenue"].idxmax()]
            genre_revenue = df.groupby("Genres_name")["Revenue"].sum()
            highest_genre = genre_revenue.idxmax()
            popular_movie = df.loc[df["Popularity"].idxmax()]
            rated_movie = df.loc[df["Vote_Average"].idxmax()]
            start_year = df["Release_Date_yr"].min()
            end_year = df["Release_Date_yr"].max()

            insight = f"""
            The current selection contains **{total_movies} movies**, 
            spanning releases in **{start_year}**.

            **{highest_genre}** is the highest-grossing genre, while 
            **{highest_movie['Title']}** leads the selection with revenue 
            of **${highest_movie['Revenue']:,.0f}**.

            The most popular movie is **{popular_movie['Title']}** 
            (popularity: {popular_movie['Popularity']:.2f}), 
            whereas **{rated_movie['Title']}** has the highest audience 
            rating of **{rated_movie['Vote_Average']:.1f}/10**.
            """

            st.info(insight)

        else:
            st.warning("No movies found for the selected filters.")
    except Exception as err:
        st.warning(f"Please select the filter once again. Error : {err}",icon="⚠️")

elif selected == "Query Explorer":
    q1=text("""select M.Title,M.Release_Date FROM MOVIES M INNER JOIN Movie_Genres MG ON M.Movie_ID = MG.Movie_ID  WHERE MG.Genre_ID = (SELECT Genre_ID FROM Genres WHERE UCASE(Genres_NAME) LIKE '%ACTION%') and YEAR(M.Release_Date) > 2015;""")

    q2=text("""SELECT M.Title, GROUP_CONCAT(G.Genres_name ORDER BY G.Genres_Name SEPARATOR ' ') AS Genres FROM Movies M INNER JOIN Movie_Genres MG ON M.Movie_ID = MG.Movie_ID INNER JOIN Genres G ON MG.Genre_ID = G.Genre_ID GROUP BY M.Movie_ID, M.Title ORDER BY M.Revenue DESC LIMIT 10;""")

    q3=text("""SELECT G.Genres_Name,AVG(Budget) As "Budget Average",AVG(Revenue) As "Revenue Average" FROM MOVIES M INNER JOIN MOVIE_Genres MG ON M.Movie_ID = MG.Movie_ID INNER JOIN Genres G ON MG.Genre_ID = G.Genre_ID group by G.Genres_Name ORDER BY AVG(M.Revenue) DESC;""")

    q4=text("""SELECT C.Actor_Name,COUNT(DISTINCT M.Movie_ID) As Appearance FROM Movies M INNER JOIN Cast C ON M.Movie_ID = C.Movie_ID GROUP BY C.Actor_Name ORDER BY COUNT(DISTINCT M.Movie_ID) desc limit 10;""")

    q5=text("""SELECT C.Person_Name, Count(DISTINCT M.Movie_ID) As Movie_Count FROM Movies M INNER JOIN Crew C ON M.Movie_ID = C.Movie_ID WHERE ucase(C.Job) = "DIRECTOR" GROUP BY C.Person_Name HAVING COUNT(DISTINCT M.Movie_ID)>3 ORDER BY Movie_Count desc limit 10;""")

    q6=text("""SELECT Count(M.Movie_ID) AS Occurences ,MK.Keyword_Name FROM Movies M INNER JOIN Movie_Keywords MK ON M.Movie_ID = MK.Movie_ID GROUP BY MK.Keyword_Name ORDER BY Count(M.Movie_ID) desc limit 10;""")

    q7=text("""SELECT Title FROM Movies where Budget > (SELECT AVG(Budget) FROM Movies) AND Revenue < (SELECT AVG(Revenue) FROM Movies);""")

    q8=text("""SELECT DISTINCT Ca.Actor_Name,M.Title from Movies M INNER JOIN CREW Cr ON M.Movie_ID = Cr.Movie_ID INNER JOIN Cast Ca ON M.Movie_ID=Ca.Movie_ID where UCASE(Cr.Person_Name) = UCASE("Christopher Nolan") AND UCASE(Cr.Job) = UCASE("Director");""")

    q9=text("""SELECT G.Genres_Name FROM Movies M INNER JOIN Movie_Genres MG ON M.Movie_ID = MG.Movie_ID INNER JOIN Genres G ON MG.Genre_ID = G.Genre_ID GROUP BY G.Genres_Name HAVING COUNT(M.Movie_ID)>=20 ORDER BY AVG(M.Vote_Average) desc LIMIT 1;""")

    q10=text("""SELECT M.Title,Count(MK.Keyword_Name) As Keyword_Occurence FROM Movies M INNER JOIN Movie_Keywords MK ON M.Movie_ID = MK.Movie_ID GROUP BY M.Movie_ID,M.Title ORDER BY Count(MK.Keyword_Name) desc limit 10;""")

    with engine.connect() as connection:
        df_q1 = pd.read_sql(q1, connection)
        df_q2 = pd.read_sql(q2, connection)
        df_q3 = pd.read_sql(q3, connection)
        df_q4 = pd.read_sql(q4, connection)
        df_q5 = pd.read_sql(q5, connection)
        df_q6 = pd.read_sql(q6, connection)
        df_q7 = pd.read_sql(q7, connection)
        df_q8 = pd.read_sql(q8, connection)
        df_q9 = pd.read_sql(q9, connection)
        df_q10 = pd.read_sql(q10, connection)

    st.subheader("Query 1")
    st.dataframe(df_q1, use_container_width=True, hide_index=True)
    df_q1["Year"] = pd.to_datetime(df_q1["Release_Date"]).dt.year

    yearly_movies = df_q1.groupby("Year").size().reset_index(name="Movie_Count")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=yearly_movies, x="Year", y="Movie_Count", ax=ax)
    ax.set_title("Action Movies Released Per Year")
    ax.set_xlabel("Release Year")
    ax.set_ylabel("Number of Movies")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.subheader("Query 2")
    st.dataframe(df_q2, use_container_width=True, hide_index=True)
    if not df_q2.empty:
        st.markdown(f"Highest Revenue Movie is <b><i>{df_q2["Title"].head()[0]}<i></b>",unsafe_allow_html=True)

    st.subheader("Query 3")
    st.dataframe(df_q3, use_container_width=True, hide_index=True)
    df_q3_melted = df_q3.melt(id_vars="Genres_Name",value_vars=["Budget Average", "Revenue Average"],var_name="Metric",value_name="Amount")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=df_q3_melted,x="Genres_Name",y="Amount",hue="Metric",ax=ax)
    ax.set_title("Average Budget vs Revenue by Genre")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Average Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.subheader("Query 4")
    st.dataframe(df_q4, use_container_width=True, hide_index=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_q4.sort_values("Appearance", ascending=False),x="Appearance",y="Actor_Name",ax=ax)
    ax.set_title("Top 10 Actors by Movie Appearances")
    ax.set_xlabel("Number of Appearances")
    ax.set_ylabel("Actor")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.subheader("Query 5")
    st.dataframe(df_q5, use_container_width=True, hide_index=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_q5.sort_values("Movie_Count", ascending=False),x="Movie_Count",y="Person_Name",ax=ax)
    ax.set_title("Top Directors by Number of Movies")
    ax.set_xlabel("Number of Movies")
    ax.set_ylabel("Director")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.subheader("Query 6")
    st.dataframe(df_q6, use_container_width=True, hide_index=True)
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(data=df_q6.sort_values("Occurences", ascending=False),x="Occurences",y="Keyword_Name",ax=ax)

    ax.set_title("Top 10 Most Frequently Used Keywords")
    ax.set_xlabel("Occurrences")
    ax.set_ylabel("Keyword")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.subheader("Query 7")
    st.dataframe(df_q7, use_container_width=True, hide_index=True)
    if not df_q7.empty:
        st.markdown(f"Total number of Movies with above-average budget but below-average revenuee <b><i>{df_q7["Title"].nunique()}<i></b>",unsafe_allow_html=True)

    st.subheader("Query 8")
    st.dataframe(df_q8, use_container_width=True, hide_index=True)
    if not df_q9.empty:
        st.markdown(f"Total number of Movies directed by Christoper Nolan are <b><i>{df_q8["Title"].nunique()}<i></b>",unsafe_allow_html=True)

    st.subheader("Query 9")
    st.dataframe(df_q9, use_container_width=True, hide_index=True)
    if not df_q9.empty:
        st.markdown(f"Highest Rated Genre (20+ Movies) is <b><i>{df_q9["Genres_Name"].iloc[0]}<i></b>",unsafe_allow_html=True)

    st.subheader("Query 10")
    st.dataframe(df_q10, use_container_width=True, hide_index=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_q10.sort_values("Keyword_Occurence", ascending=False),x="Keyword_Occurence",y="Title",ax=ax)
    ax.set_title("Top 10 Movies by Keyword Occurrences")
    ax.set_xlabel("Keyword Occurrences")
    ax.set_ylabel("Movie")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
