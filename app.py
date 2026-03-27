import streamlit as st
import httpx
import urllib.parse

API_BASE = "http://localhost:8000"   

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080b10 !important;
    color: #e8e0d5 !important;
    font-family: 'DM Sans', sans-serif;
}

#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display:none !important; }

.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Hero ── */
.hero {
    position: relative;
    width: 100%;
    min-height: 340px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3.5rem 2rem 2.5rem;
    overflow: hidden;
    background: linear-gradient(135deg, #0d1117 0%, #12111a 50%, #0a0f18 100%);
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 70% 60% at 20% 40%, rgba(220,160,40,.08) 0%, transparent 60%),
        radial-gradient(ellipse 50% 50% at 80% 60%, rgba(140,60,180,.07) 0%, transparent 60%),
        repeating-linear-gradient(0deg, transparent, transparent 79px, rgba(255,255,255,.018) 80px),
        repeating-linear-gradient(90deg, transparent, transparent 79px, rgba(255,255,255,.018) 80px);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: .7rem;
    font-weight: 500;
    letter-spacing: .25em;
    text-transform: uppercase;
    color: #c9983a;
    margin-bottom: .7rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.8rem, 5vw, 5rem);
    font-weight: 900;
    line-height: 1.05;
    color: #f5ede0;
    text-align: center;
    letter-spacing: -.02em;
    text-shadow: 0 4px 40px rgba(0,0,0,.7);
}
.hero-title span { color: #c9983a; font-style: italic; }
.hero-sub {
    margin-top: .9rem;
    font-size: .95rem;
    color: rgba(232,224,213,.5);
    text-align: center;
    max-width: 480px;
    line-height: 1.6;
}

/* ── Search ── */
[data-testid="stTextInput"] > div > div {
    background: rgba(255,255,255,.04) !important;
    border: 1.5px solid rgba(201,152,58,.35) !important;
    border-radius: 50px !important;
    padding: .1rem 1.4rem !important;
    transition: border-color .3s, box-shadow .3s;
}
[data-testid="stTextInput"] > div > div:focus-within {
    border-color: rgba(201,152,58,.8) !important;
    box-shadow: 0 0 0 3px rgba(201,152,58,.12) !important;
}
[data-testid="stTextInput"] input {
    background: transparent !important;
    color: #f5ede0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    caret-color: #c9983a !important;
}
[data-testid="stTextInput"] label { display: none !important; }
[data-testid="stTextInput"] ::placeholder { color: rgba(232,224,213,.35) !important; }

/* ── Section heading ── */
.sec-head {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #f5ede0;
    padding: 1.6rem 2rem .6rem;
    letter-spacing: -.01em;
}
.sec-head .accent { color: #c9983a; font-style: italic; }

/* ── Movie card ── */
.movie-card {
    position: relative;
    border-radius: 10px;
    overflow: hidden;
    background: #111420;
    border: 1px solid rgba(255,255,255,.06);
    transition: transform .25s, box-shadow .25s, border-color .25s;
    aspect-ratio: 2/3;
}
.movie-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 18px 50px rgba(0,0,0,.6), 0 0 0 1px rgba(201,152,58,.3);
    border-color: rgba(201,152,58,.4);
}
.card-rating {
    position: absolute;
    top: .5rem; right: .5rem;
    background: rgba(0,0,0,.75);
    backdrop-filter: blur(4px);
    color: #c9983a;
    font-size: .7rem;
    font-weight: 700;
    padding: .18rem .45rem;
    border-radius: 20px;
    border: 1px solid rgba(201,152,58,.3);
}
.card-no-poster {
    width: 100%; height: 100%;
    background: linear-gradient(135deg, #1a1d28, #0e1020);
    display: flex; align-items: center; justify-content: center;
    font-size: 2.5rem;
}

/* ── Score bar ── */
.score-bar-wrap {
    height: 3px;
    background: rgba(255,255,255,.08);
    border-radius: 10px;
    overflow: hidden;
    margin-top: .35rem;
}
.score-bar-fill {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #c9983a, #e8b84b);
}

/* ── Detail hero ── */
.detail-hero {
    position: relative;
    width: 100%;
    min-height: 420px;
    display: flex;
    align-items: flex-end;
    padding: 2.5rem;
    overflow: hidden;
}
.detail-backdrop {
    position: absolute; inset: 0;
    object-fit: cover;
    width: 100%; height: 100%;
    filter: brightness(.35) saturate(.8);
}
.detail-backdrop-gradient {
    position: absolute; inset: 0;
    background:
        linear-gradient(to right, rgba(8,11,16,.92) 35%, transparent 80%),
        linear-gradient(to top, rgba(8,11,16,1) 0%, transparent 50%);
}
.detail-content {
    position: relative;
    display: flex;
    gap: 2rem;
    align-items: flex-end;
    max-width: 900px;
}
.detail-poster {
    width: 140px;
    flex-shrink: 0;
    border-radius: 10px;
    border: 2px solid rgba(201,152,58,.4);
    box-shadow: 0 10px 40px rgba(0,0,0,.6);
}
.detail-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.8rem, 3vw, 2.8rem);
    font-weight: 900;
    color: #f5ede0;
    line-height: 1.1;
}
.detail-genres { display: flex; gap: .5rem; flex-wrap: wrap; margin: .6rem 0; }
.genre-tag {
    font-size: .72rem;
    font-weight: 500;
    letter-spacing: .04em;
    text-transform: uppercase;
    padding: .28rem .75rem;
    border-radius: 50px;
    border: 1px solid rgba(201,152,58,.5);
    color: #c9983a;
    background: rgba(201,152,58,.08);
}
.detail-overview {
    font-size: .9rem;
    color: rgba(232,224,213,.72);
    line-height: 1.65;
    max-width: 540px;
    margin-top: .5rem;
}

/* ── Gold divider ── */
.gold-divider {
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(201,152,58,.3), transparent);
    margin: .5rem 2rem;
}

/* ── Streamlit button — category nav ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(201,152,58,.18), rgba(201,152,58,.08)) !important;
    border: 1.5px solid rgba(201,152,58,.5) !important;
    color: #c9983a !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .75rem !important;
    font-weight: 500 !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    border-radius: 50px !important;
    padding: .4rem 1.2rem !important;
    width: 100% !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(201,152,58,.35), rgba(201,152,58,.15)) !important;
    border-color: #c9983a !important;
    box-shadow: 0 4px 20px rgba(201,152,58,.2) !important;
}

/* ── Card click button — looks like plain text, not a button ── */
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: none !important;
    border-top: 1px solid rgba(255,255,255,.05) !important;
    border-radius: 0 0 10px 10px !important;
    color: rgba(232,224,213,.45) !important;
    font-size: .72rem !important;
    font-weight: 400 !important;
    letter-spacing: .02em !important;
    text-transform: none !important;
    padding: .4rem .6rem !important;
    margin-top: -2px !important;
    text-align: left !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(201,152,58,.06) !important;
    color: #c9983a !important;
    box-shadow: none !important;
    border-color: rgba(201,152,58,.2) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #080b10; }
::-webkit-scrollbar-thumb { background: rgba(201,152,58,.3); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)


for key, default in [
    ("page", "home"),
    ("selected_movie", None),
    ("category", "popular"),
    ("search_query", ""),
    ("search_results", None),
    ("bundle", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def api_get(path: str, params: dict = {}) -> dict | list | None:
    try:
        with httpx.Client(timeout=20) as c:
            r = c.get(f"{API_BASE}{path}", params=params)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        st.error(f"⚠️ API error: {e}")
        return None


def render_card_col(col, movie: dict, btn_key: str, show_score: bool = False, score: float = 0.0):
    with col:
        poster   = movie.get("poster_url") or ""
        title    = movie.get("title", "Unknown")
        rating   = movie.get("vote_average")
        year     = (movie.get("release_date") or "")[:4]
        score_pct = int(min(score * 100 / max(score, 0.0001), 100)) if show_score else 0

        rating_badge = f"<div class='card-rating'>⭐ {rating:.1f}</div>" if rating else ""
        img_part = (
            f"<img src='{poster}' loading='lazy' "
            f"style='width:100%;height:100%;object-fit:cover;border-radius:10px 10px 0 0;display:block;' />"
            if poster
            else "<div style='height:220px;display:flex;align-items:center;"
                 "justify-content:center;font-size:2rem;"
                 "background:#111420;border-radius:10px 10px 0 0;'>🎬</div>"
        )

        score_html = (
            f"""
            <div class="score-bar-wrap" style="margin:0 .6rem .1rem;">
                <div class="score-bar-fill" style="width:{score_pct}%;"></div>
            </div>
            <div style="font-size:.62rem;color:#c9983a;padding:0 .6rem .5rem;">{score:.3f} match</div>
            """
            if show_score else '<div style="height:.5rem;"></div>'
        )

        st.markdown(
            f"""
            <div class="movie-card" style="cursor:pointer;border-radius:10px;overflow:hidden;
                 border:1px solid rgba(255,255,255,.06);background:#111420;
                 transition:transform .25s,box-shadow .25s,border-color .25s;"
                 onmouseover="this.style.transform='translateY(-5px) scale(1.02)';
                              this.style.boxShadow='0 18px 50px rgba(0,0,0,.6)';
                              this.style.borderColor='rgba(201,152,58,.4)'"
                 onmouseout="this.style.transform='';this.style.boxShadow='';this.style.borderColor='rgba(255,255,255,.06)'">
                <div style="position:relative;aspect-ratio:2/3;overflow:hidden;">
                    {img_part}
                    {rating_badge}
                </div>
                <div style="padding:.5rem .6rem .25rem;font-size:.78rem;font-family:'DM Sans',sans-serif;
                            color:#e8e0d5;line-height:1.3;font-weight:500;">{title}</div>
                <div style="font-size:.68rem;color:rgba(232,224,213,.4);padding:0 .6rem .3rem;">{year}</div>
                {score_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

        
        st.markdown(
            """<style>
            div[data-testid="stButton"] button.card-click-btn {
                position:absolute!important; inset:0!important;
                opacity:0!important; width:100%!important; height:100%!important;
                cursor:pointer!important; border:none!important;
            }
            </style>""",
            unsafe_allow_html=True,
        )
        
        if st.button(f"▶ {title[:22]}", key=btn_key, help=f"Open {title}"):
            st.session_state.selected_movie = movie
            st.session_state.bundle = None
            st.session_state.page = "detail"
            st.rerun()


def movies_grid(movies: list, section_title: str, accent: str = "", n_cols: int = 6):
    """Section heading + responsive card grid."""
    head = f'{section_title} <span class="accent">{accent}</span>' if accent else section_title
    st.markdown(f'<div class="sec-head">{head}</div>', unsafe_allow_html=True)
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    rows = [movies[i:i+n_cols] for i in range(0, len(movies), n_cols)]
    for row in rows:
        cols = st.columns(len(row))
        for col, m in zip(cols, row):
            render_card_col(col, m, btn_key=f"grid_{m.get('tmdb_id')}_{m.get('title','')[:6]}")


def page_home():
    
    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">✦ AI-Powered Discovery</div>
        <div class="hero-title">Your next favourite<br><span>film</span> is waiting.</div>
        <div class="hero-sub">
            Search any movie and get intelligent recommendations powered by
            TF-IDF content similarity &amp; genre analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)

    
    _, mid, _ = st.columns([1, 3, 1])
    with mid:
        query = st.text_input(
            label="search",
            placeholder="🔍  Search a movie title…",
            key="main_search",
            label_visibility="collapsed",
        )

    
    if query and query != st.session_state.search_query:
        st.session_state.search_query = query
        with st.spinner("Searching…"):
            data = api_get("/tmdb/search", {"query": query, "page": 1})
            st.session_state.search_results = (
                data.get("results", []) if data else []
            )
        st.rerun()

    if not query and st.session_state.search_query:
        st.session_state.search_query = ""
        st.session_state.search_results = None

    
    if st.session_state.search_results is not None:
        results = st.session_state.search_results
        if not results:
            st.markdown(
                '<div style="padding:3rem;text-align:center;color:rgba(232,224,213,.4);">'
                "No results found. Try a different title.</div>",
                unsafe_allow_html=True,
            )
            return

        cards = [
            {
                "tmdb_id": m["id"],
                "title": m.get("title", ""),
                "poster_url": (
                    f"https://image.tmdb.org/t/p/w500{m['poster_path']}"
                    if m.get("poster_path") else None
                ),
                "release_date": m.get("release_date"),
                "vote_average": m.get("vote_average"),
            }
            for m in results
        ]
        movies_grid(cards, "Search Results for", f'"{st.session_state.search_query}"')
        return

    
    cats = {
        "popular":   "Popular",
        "top_rated": "Top Rated",
        "trending":  "Trending",
    }
    st.markdown('<div style="height:.8rem;"></div>', unsafe_allow_html=True)
    nav_cols = st.columns([.5] + [1]*len(cats) + [.5])
    for i, (key, label) in enumerate(cats.items()):
        with nav_cols[i + 1]:
            if st.button(label, key=f"cat_{key}"):
                st.session_state.category = key
                st.rerun()

    
    cat = st.session_state.category
    with st.spinner(f"Loading {cats.get(cat, cat)}…"):
        movies = api_get("/home", {"category": cat, "limit": 24})

    if movies:
        movies_grid(movies, cats.get(cat, cat), "Movies")
    else:
        st.warning("Couldn't reach the API. Make sure your FastAPI server is running on port 8000.")



def page_detail():
    movie = st.session_state.selected_movie
    if not movie:
        st.session_state.page = "home"
        st.rerun()
        return

    
    _, btn_col, _ = st.columns([.1, 1, 8])
    with btn_col:
        if st.button("← Back"):
            st.session_state.page = "home"
            st.session_state.bundle = None
            st.rerun()

    
    cached_id = (st.session_state.bundle or {}).get("movie_details", {}).get("tmdb_id")
    if st.session_state.bundle is None or cached_id != movie.get("tmdb_id"):
        with st.spinner("Fetching details & recommendations…"):
            bundle = api_get(
                "/movie/search",
                {"query": movie.get("title", ""), "tfidf_top_n": 10, "genre_limit": 12},
            )
            st.session_state.bundle = bundle
    else:
        bundle = st.session_state.bundle

    if not bundle:
        st.error("Could not load movie details.")
        return

    details   = bundle.get("movie_details", {})
    tfidf_recs = bundle.get("tfidf_recommendations", [])
    genre_recs = bundle.get("genre_recommendations", [])

    backdrop = details.get("backdrop_url") or ""
    poster   = details.get("poster_url")   or ""
    title    = details.get("title", "")
    overview = details.get("overview", "No overview available.")
    genres   = details.get("genres", [])
    release  = (details.get("release_date") or "")[:4]

    genres_html = "".join(f'<span class="genre-tag">{g["name"]}</span>' for g in genres)
    backdrop_img = (
        f'<img src="{backdrop}" class="detail-backdrop" />'
        if backdrop
        else '<div class="detail-backdrop" style="background:linear-gradient(135deg,#1a1225,#0a1020);"></div>'
    )
    poster_img = (
        f'<img src="{poster}" class="detail-poster" />'
        if poster
        else '<div class="detail-poster" style="height:200px;background:#111420;'
             'display:flex;align-items:center;justify-content:center;font-size:3rem;'
             'border-radius:10px;border:2px solid rgba(201,152,58,.3);">🎬</div>'
    )

    st.markdown(
        f"""
        <div class="detail-hero">
            {backdrop_img}
            <div class="detail-backdrop-gradient"></div>
            <div class="detail-content">
                {poster_img}
                <div>
                    <div class="detail-title">{title}</div>
                    <div style="font-size:.82rem;color:rgba(232,224,213,.4);margin:.4rem 0 .2rem;">
                        {release}
                    </div>
                    <div class="detail-genres">{genres_html}</div>
                    <div class="detail-overview">{overview}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    
    if tfidf_recs:
        st.markdown(
            '<div class="sec-head">Similar by <span class="accent">Content</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="padding:.2rem 2rem .8rem;font-size:.8rem;'
            'color:rgba(232,224,213,.4);">'
            "Ranked by TF-IDF keyword &amp; genre similarity from our local dataset</div>",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

        n_cols = 5
        rows = [tfidf_recs[i:i+n_cols] for i in range(0, len(tfidf_recs), n_cols)]
        for row in rows:
            cols = st.columns(len(row))
            for col, rec in zip(cols, row):
                tmdb_data = rec.get("tmdb") or {}
                m = {
                    "tmdb_id":      tmdb_data.get("tmdb_id"),
                    "title":        rec.get("title", "Unknown"),
                    "poster_url":   tmdb_data.get("poster_url"),
                    "release_date": tmdb_data.get("release_date"),
                    "vote_average": tmdb_data.get("vote_average"),
                }
                render_card_col(
                    col, m,
                    btn_key=f"tfidf_{rec.get('title','')[:10]}_{tmdb_data.get('tmdb_id','')}",
                    show_score=True,
                    score=rec.get("score", 0),
                )

    
    if genre_recs:
        st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)
        genre_label = genres[0]["name"] if genres else "Similar"
        movies_grid(genre_recs, f"More {genre_label}", "Films")


if st.session_state.page == "home":
    page_home()
elif st.session_state.page == "detail":
    page_detail()