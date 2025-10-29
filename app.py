import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Define the URLs for the logos
youtube_logo_url = "https://www.freeiconspng.com/thumbs/youtube-logo-png/hd-youtube-logo-png-transparent-background-20.png"
spotify_logo_url = "https://www.freepnglogos.com/uploads/spotify-logo-png/file-spotify-logo-png-4.png"


# Display the YouTube and Spotify logos side by side in the sidebar
st.sidebar.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="{youtube_logo_url}" width="96" height="80" style="margin-right: 10px;">
        <img src="{spotify_logo_url}" width="80" height="75">
    </div>
""", unsafe_allow_html=True)

st.sidebar.title("YouTube & Spotify Dataset")

# Load the dataset
file_path = "E:\Intern\Streamlit\Spotify_Youtube.csv"  # Replace with the correct file path
data = pd.read_csv(file_path, encoding='ISO-8859-1')


# Overview
# Sunburst Chart
def piechart(df, current_slider_value):
    # Step 1: Count the number of tracks per genre
    genre_track_count = df.groupby('Genre')['Track'].nunique().reset_index()
    genre_track_count.columns = ['Genre', 'Number of Tracks']

    # Step 2: Calculate the total streams per artist
    artist_stream_sum = df.groupby(['Genre', 'Artist Cleaned'])['Stream'].sum().reset_index()
    artist_stream_sum.columns = ['Genre', 'Artist Cleaned', 'Total Streams']

    # Step 3: Limit to the top 10 artists per genre based on total streams
    artist_stream_sum['Rank'] = artist_stream_sum.groupby('Genre')['Total Streams'].rank(method='first', ascending=False)
    top_artists = artist_stream_sum[artist_stream_sum['Rank'] <= 15]

    # Step 4: Merge the top artists with the genre track count data
    merged_data = pd.merge(df, top_artists[['Genre', 'Artist Cleaned']], on=['Genre', 'Artist Cleaned'], how='inner')

    # Filter for the top genres based on the number of tracks
    top_genres = genre_track_count.nlargest(current_slider_value, 'Number of Tracks')
    filtered_data = merged_data[merged_data['Genre'].isin(top_genres['Genre'])]

    # Step 5: Create the Sunburst chart
    fig = px.sunburst(
        filtered_data,
        path=['Genre', 'Artist Cleaned', 'Track'],  # Add tracks to the path
        values='Stream',  # Use stream values for track level
        hover_data={'Stream': True},  # Show total streams on hover
        color='Genre',  # Color based on total streams for artists
        title="Sunburst Chart: Tracks per Genre, Artist, and Track"
    )

    # Update layout to adjust text properties
    fig.update_layout(
        width=800,
        height=600,
        font=dict(
            family="Arial",   # Choose the font family
            size=14,          # Adjust font size
            color="black"     # Adjust font color
        ),
        title_font=dict(
            family="Arial",
            size=18,
            color="white"
        ),
        paper_bgcolor="dark blue",  # Background color of the chart
        margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins for better readability
    )

    st.plotly_chart(fig, use_container_width=True)

def dual_axis_area_plot(df, current_slider_value):
    # Variables to choose from
    variables = ['Views', 'Likes', 'Comments', 'Stream']
    
    # Dropdowns for selecting variables (disable typing)
    y1_axis = st.selectbox("Select first variable:", options=variables, format_func=lambda x: x)
    
    # Ensure that y2_axis is different from y1_axis
    y2_axis_options = [var for var in variables if var != y1_axis]
    y2_axis = st.selectbox("Select second variable:", options=y2_axis_options, format_func=lambda x: x)

    # Calculate total number of tracks per genre
    genre_track_count = df.groupby('Genre')['Track'].nunique().reset_index()
    genre_track_count.columns = ['Genre', 'Total Tracks']

    # Grouping data by genre and calculating the average of the selected variables
    grouped_data = df.groupby('Genre').agg({y1_axis: 'mean', y2_axis: 'mean'}).reset_index()

    # Merge the total track count data
    grouped_data = pd.merge(grouped_data, genre_track_count, on='Genre')

    # Filter top genres based on total number of tracks
    top_genres = grouped_data.nlargest(current_slider_value, 'Total Tracks')
    grouped_data = grouped_data[grouped_data['Genre'].isin(top_genres['Genre'])]

    # Create the figure with dual Y-axes
    fig = go.Figure()

    # Add the first trace for the left Y-axis as an area plot with rounded peaks
    fig.add_trace(
        go.Scatter(
            x=grouped_data['Genre'],
            y=grouped_data[y1_axis],
            mode='lines',
            fill='tozeroy',
            name=y1_axis,
            line=dict(color='cyan', shape='spline'),
            yaxis='y1'
        )
    )

    # Add the second trace for the right Y-axis as an area plot with rounded peaks
    fig.add_trace(
        go.Scatter(
            x=grouped_data['Genre'],
            y=grouped_data[y2_axis],
            mode='lines',
            fill='tonexty',
            name=y2_axis,
            line=dict(color='magenta', shape='spline'),
            yaxis='y2'
        )
    )

    # Update the layout to include dual Y-axes
    fig.update_layout(
        title=f"Dual-Axis Area Plot: Average {y1_axis} and {y2_axis} by Genre",
        xaxis=dict(title='Genre', titlefont=dict(color='white'), tickfont=dict(color='white')),
        yaxis=dict(title=f"Average {y1_axis}", titlefont=dict(color='cyan'), tickfont=dict(color='cyan')),
        yaxis2=dict(title=f"Average {y2_axis}", titlefont=dict(color='magenta'), tickfont=dict(color='magenta'), overlaying='y', side='right'),
        width=800,
        height=600,
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        title_font=dict(
            family="Arial",
            size=18,
            color="white"
        ),
        paper_bgcolor="dark blue",
        margin=dict(l=50, r=50, t=50, b=50)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Display tables for top 5 genres by selected variables
    top_5_y1 = grouped_data.nlargest(5, y1_axis)[['Genre', y1_axis]].reset_index(drop=True)
    top_5_y2 = grouped_data.nlargest(5, y2_axis)[['Genre', y2_axis]].reset_index(drop=True)
    top_5_y1.index = top_5_y1.index + 1  # Adjust index to start from 1
    top_5_y2.index = top_5_y2.index + 1  # Adjust index to start from 1

    # Display tables side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Top 5 Genres by Average {y1_axis}")
        st.table(top_5_y1)

    with col2:
        st.subheader(f"Top 5 Genres by Average {y2_axis}")
        st.table(top_5_y2)


# Scatter plot function
def scatter_plot(df, selected_genres, aggregation_method):
    st.title("Scatter Plot: Likes vs Comments")

    # Filter the data based on the selected genres
    filtered_df = df[df['Genre'].isin(selected_genres)]

    # Selecting relevant columns
    numeric_cols = ['Likes', 'Comments', 'Views']
    
    # Grouping by Genre and applying the selected aggregation method
    if aggregation_method == "Mean":
        grouped_df = filtered_df.groupby('Genre')[numeric_cols].mean().reset_index()
    else:
        grouped_df = filtered_df.groupby('Genre')[numeric_cols].sum().reset_index()

    # Creating the scatter plot
    fig = px.scatter(
        grouped_df,
        x='Comments',
        y='Likes',
        size='Views',
        color='Genre',
        hover_name='Genre',
        title='Bubble Size = Views & Color = Genre',
        size_max=60,  # Maximum size of bubbles
        color_discrete_sequence=px.colors.qualitative.Safe  # Use a nicer color palette
    )

    fig.update_layout(width=800, height=600)

    # Display the scatter plot
    st.plotly_chart(fig, use_container_width=True)
 




def combined_line_plot(df):
    # Streamlit application setup
    st.title("Artist Comparison")

    # Dropdown for choosing y-axis
    y_axis = st.selectbox("Select variable:", ['Likes', 'Comments', 'Views', 'Stream'], index=0)

    # Radio for choosing x-axis (Track or Album)
    x_axis = st.radio("Compare by:", ['Track', 'Album'], index=0, horizontal=True)

    # Dropdowns for selecting artists
    artist1 = st.selectbox("Select Artist 1:", sorted(df['Artist Cleaned'].unique()))
    artist2_options = [artist for artist in sorted(df['Artist Cleaned'].unique()) if artist != artist1]
    artist2 = st.selectbox("Select Artist 2:", artist2_options)

    artist3_options = [artist for artist in artist2_options if artist != artist2]
    artist3 = st.selectbox("Select Artist 3 (optional):", ['None'] + artist3_options)
    if artist3 == 'None':
        artist3 = None

    selected_artists = [artist1, artist2]
    if artist3:
        selected_artists.append(artist3)
    
    # Filter the data based on selected artists
    df_filtered = df[df['Artist Cleaned'].isin(selected_artists)]
    
    # Handle track or album selection
    if x_axis == 'Track':
        df_filtered = df_filtered.groupby(['Artist Cleaned', 'Track'])[y_axis].sum().reset_index()
        top_x = 10
    else:  # Album
        df_filtered = df_filtered.groupby(['Artist Cleaned', 'Album'])[y_axis].sum().reset_index()
        top_x = 5

    # Sort and get the top X values, then index them
    df_filtered = df_filtered.sort_values(by=y_axis, ascending=False)
    df_filtered['Index'] = df_filtered.groupby('Artist Cleaned').cumcount() + 1
    df_filtered = df_filtered[df_filtered['Index'] <= top_x]

    # Convert the index to string for x-axis labeling
    df_filtered['Index'] = df_filtered['Index'].astype(str)
    
    # Determine hover data based on x-axis choice
    hover_data = [x_axis] if x_axis == 'Track' else ['Album']
    
    # Create a combined line plot
    fig = px.line(df_filtered, x='Index', y=y_axis, color='Artist Cleaned', markers=True, line_shape='linear',
                  hover_data=hover_data)
    
    # Update layout
    fig.update_layout(
        xaxis_title=f'Top {top_x} {x_axis}s (Ranked)',
        yaxis_title=y_axis,
        xaxis=dict(tickvals=[str(i) for i in range(1, top_x + 1)]),  # Ensure x-axis has values 1 to 10
    )
    
    st.plotly_chart(fig)
    
    # Prepare the table for most liked/streamed tracks/albums
    st.subheader(f"{x_axis}s With The Most {y_axis}")
    table_data = {}
    for artist in selected_artists:
        artist_top_item = df_filtered[df_filtered['Artist Cleaned'] == artist].nlargest(top_x, y_axis)
        if not artist_top_item.empty:
            artist_top_item = artist_top_item[[x_axis, y_axis]]
            artist_top_item.columns = [x_axis, y_axis]
            artist_top_item[y_axis] = artist_top_item[y_axis].astype(int)  # Remove decimal points
            artist_top_item.index = range(1, len(artist_top_item) + 1)  # Reset index starting from 1
            table_data[artist] = artist_top_item.reset_index(drop=True)

    # Combine tables
    if table_data:
        combined_table = pd.concat(table_data.values(), axis=1)
        combined_table.columns = pd.MultiIndex.from_tuples(
            [(artist, x_axis) if i % 2 == 0 else (artist, y_axis) for artist in selected_artists for i in range(2)]
        )
        combined_table.index = range(1, len(combined_table) + 1)  # Reset index starting from 1

        # Display the table with fixed column width
        st.markdown(
            combined_table.to_html(classes='table table-striped', index=False),
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <style>
            .table {
                width: 100%;
                border-collapse: collapse;
                color: #FFFFFF; /* Text color */
            }
            .table td, .table th {
                border: 1px solid #555555; /* Cell border color */
                padding: 8px;
                width: 300px;
            }
            .table th {
                background-color: #444444; /* Header background color */
                color: #FFFFFF; /* Header text color */
            }
            .table tr:nth-child(even) {
                background-color: #333333; /* Alternating row color */
            }
            .table tr:nth-child(odd) {
                background-color: #2E2E2E; /* Row color */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("No data available for the table.")



# Function to create the visualization
def create_artist_comparison(df, artist, comparison_level, variable, selected_items):
    # Filter the data for the selected artist
    artist_data = df[df['Artist Cleaned'] == artist]

    # Filter by selected tracks or albums
    if selected_items:
        artist_data = artist_data[artist_data[comparison_level].isin(selected_items)]

    # Group by Track or Album and calculate the sum of the selected variable
    comparison_data = artist_data.groupby(comparison_level)[variable].sum().reset_index()
    title = f"{artist}'s {comparison_level}s by {variable}"

    # Sort the data for better visualization
    comparison_data = comparison_data.sort_values(by=variable, ascending=False)

    # Create a more stylish bar chart with Track/Album on the x-axis and variable on the y-axis
    fig = px.bar(comparison_data, 
                 x=comparison_level, 
                 y=variable, 
                 color=comparison_level,
                 text=variable,
                 color_discrete_sequence=px.colors.qualitative.Set3)

    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig.update_layout(
        title=title,
        width=800,
        height=600,
        showlegend=False,
        xaxis_title=None,  # Remove x-axis title
        xaxis=dict(
            showticklabels=False,  # Hide x-axis tick labels
            showline=False,        # Hide x-axis line
            showgrid=False         # Hide x-axis grid lines
        )
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    # Display the artist's name as the title
    st.markdown(f"## {artist}")

    # Group by Album and Track (for Track comparison) and calculate the sum of the selected variable
    if comparison_level == 'Track':
        grouped_data = artist_data.groupby(['Album', 'Track'])[variable].sum().reset_index()
    else:
        grouped_data = artist_data.groupby('Album')[variable].sum().reset_index()

    title = f"{artist}'s {comparison_level}s by {variable}"

    # Sort the data for better visualization
    grouped_data = grouped_data.sort_values(by=variable, ascending=False)

    # Sort and display the top 3 most/least {variable} Tracks or Albums in separate tables
    if comparison_level == "Track":
        top_tracks = grouped_data.sort_values(by=variable, ascending=False).head(3).reset_index(drop=True)
        least_tracks = grouped_data.sort_values(by=variable, ascending=True).head(3).reset_index(drop=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### Top 3 Tracks With The Most {variable}")
            top_tracks.index += 1  # Start index from 1
            st.table(top_tracks[['Track', variable]].style.format({variable: '{:,.0f}'}))
            
        with col2:
            st.markdown(f"### Top 3 Tracks With The Least {variable}")
            least_tracks.index += 1  # Start index from 1
            st.table(least_tracks[['Track', variable]].style.format({variable: '{:,.0f}'}))
    
    if comparison_level == "Album":
        top_albums = grouped_data.sort_values(by=variable, ascending=False).head(3).reset_index(drop=True)
        least_albums = grouped_data.sort_values(by=variable, ascending=True).head(3).reset_index(drop=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f"### Top 3 Albums With The Most {variable}")
            top_albums.index += 1  # Start index from 1
            st.table(top_albums[['Album', variable]].style.format({variable: '{:,.0f}'}))
            
        with col4:
            st.markdown(f"### Top 3 Albums With The Least {variable}")
            least_albums.index += 1  # Start index from 1
            st.table(least_albums[['Album', variable]].style.format({variable: '{:,.0f}'}))


def variables(data):
    # Dropdowns for selecting variables
    variables = ['Danceability', 'Energy', 'Key', 'Loudness', 'Speechiness', 'Acousticness', 
                 'Instrumentalness', 'Liveness', 'Valence', 'Tempo']
    
    x_axis = st.selectbox("Select X-axis variable:", variables, index=0)
    y_axis = st.selectbox("Select Y-axis variable:", [var for var in variables if var != x_axis], index=1)

    # Dropdown for selecting an artist
    artist = st.selectbox("Select Artist:", sorted(data['Artist Cleaned'].unique()))
    data = data[data['Artist Cleaned'] == artist]

    # Handle NaN values in 'Stream' column
    data = data.dropna(subset=['Stream'])

    # Create the scatter plot
    fig = px.scatter(data, x=x_axis, y=y_axis, size='Stream', hover_name='Track',
                     title=f'{x_axis} vs {y_axis} Scatter Plot',
                     labels={x_axis: x_axis, y_axis: y_axis, 'Streams': 'Streams'},
                     template='plotly_white')

    # Update layout
    fig.update_layout(
        xaxis_title=x_axis,
        yaxis_title=y_axis,
    )

    st.plotly_chart(fig)


# Function to filter and display songs based on the selected variable and range
def filter_songs(df):
    # List of variables
    variables = ['Danceability', 'Energy', 'Key', 'Loudness', 'Speechiness', 'Acousticness', 
                 'Instrumentalness', 'Liveness', 'Valence', 'Tempo']
    
    # Dropdown to select the variable
    selected_variable = st.selectbox("Select the variable to filter by:", variables)
    
    # Dual-range slider for the selected variable
    min_val = df[selected_variable].min()
    max_val = df[selected_variable].max()
    selected_range = st.slider(
        f"Select the range for {selected_variable}:",
        min_value=float(min_val),
        max_value=float(max_val),
        value=(float(min_val), float(max_val)),
        step=0.01
    )
    
    # Filter the data based on the selected range
    filtered_songs = df[(df[selected_variable] >= selected_range[0]) & 
                        (df[selected_variable] <= selected_range[1])]
    
    # Sort the filtered data and provide an option to switch the order
    sort_order = st.radio("Sort order:", ["Descending", "Ascending"], horizontal=True)
    filtered_songs = filtered_songs.sort_values(by=selected_variable, ascending=(sort_order == "Ascending"))
    
    # Reset index and set it to start from 1
    filtered_songs = filtered_songs.reset_index(drop=True)
    filtered_songs.index = filtered_songs.index + 1
    
    # Display the filtered songs with index starting from 1
    if not filtered_songs.empty:
        st.subheader(f"Songs with {selected_variable} between {selected_range[0]} and {selected_range[1]}")
        st.table(filtered_songs[['Track', selected_variable]])
    else:
        st.warning("No songs found in the selected range.")


def search(df, search_term):
    # Convert search term to lowercase for case-insensitive search
    search_term = search_term.lower()

    # Filter data based on search term in Track, Artist, or Album
    filtered_data = df[
        df['Track'].str.lower().str.contains(search_term)
    ]

    # If there are results, display them
    if not filtered_data.empty:
        st.write(f"**Found {len(filtered_data)} results for:** `{search_term}`")
        
        # Display the results as a selectable list
        selected_track = st.selectbox("Select a track to see more details:", filtered_data['Track'].unique())

        # Get the details of the selected track
        track_details = filtered_data[filtered_data['Track'] == selected_track]

        if not track_details.empty:
            st.write(f"### {selected_track} by {track_details['Artist Cleaned'].values[0]}")
            st.write(f"**🎵 Danceability:** {track_details['Danceability'].values[0]}")
            st.write(f"**⚡ Energy:** {track_details['Energy'].values[0]}")
            st.write(f"**🎹 Key:** {track_details['Key'].values[0]}")
            st.write(f"**🔊 Loudness:** {track_details['Loudness'].values[0]}")
            st.write(f"**🗣️ Speechiness:** {track_details['Speechiness'].values[0]}")
            st.write(f"**🎼 Acousticness:** {track_details['Acousticness'].values[0]}")
            st.write(f"**🎻 Instrumentalness:** {track_details['Instrumentalness'].values[0]}")
            st.write(f"**🎤 Liveness:** {track_details['Liveness'].values[0]}")
            st.write(f"**🎭 Valence:** {track_details['Valence'].values[0]}")
            st.write(f"**⏱️ Tempo:** {track_details['Tempo'].values[0]}")
    else:
        st.write(f"No results found for `{search_term}`")




def search_data(df, search_term):
    # Convert search term to lowercase for case-insensitive search
    search_term = search_term.lower()

    # Filter data based on search term in Track, Artist, or Album
    filtered_data = df[
        df['Track'].str.lower().str.contains(search_term) |
        df['Artist Cleaned'].str.lower().str.contains(search_term) |
        df['Album'].str.lower().str.contains(search_term)
    ]

    # If there are results, display them
    if not filtered_data.empty:
        st.write(f"**Found {len(filtered_data)} results for:** `{search_term}`")
        
        # Display the results as a selectable list
        selected_track = st.selectbox("Select a track to see more details:", filtered_data['Track'].unique())

        # Get the details of the selected track
        track_details = filtered_data[filtered_data['Track'] == selected_track]

        if not track_details.empty:
            st.write(f"### {selected_track}")
            st.write(f"**👨🏻‍🎤 Artist:** {track_details['Artist Cleaned'].values[0]}")
            st.write(f"**📼 Album:** {track_details['Album'].values[0]}")
            st.write(f"**📀 Genre:** {track_details['Genre'].values[0]}")
            st.write(f"**📽️ Total Streams:** {int(track_details['Stream'].values[0])}")
            st.write(f"**▶️ YouTube Views:** {int(track_details['Views'].values[0])}")
            st.write(f"**👍🏻 YouTube Likes:** {int(track_details['Likes'].values[0])}")
            st.write(f"**💬 YouTube Comments:** {int(track_details['Comments'].values[0])}")
            st.write(f"**YouTube URL:** {track_details['Url_youtube'].values[0]}")
            st.write(f"**Spotify URL:** {track_details['Url_spotify'].values[0]}")
    else:
        st.write(f"No results found for `{search_term}`")








# Create a sidebar with navigation options
page = st.sidebar.radio("Select a page:", ["Overview", "Artist", "Track & Album","Variables", "Music Search"])

# Render the selected page
if page == "Overview":

    st.title("Music Data Overview")

    # Create tabs for Sunburst and Dual-Axis Line Plot
    tab1, tab2, tab3 = st.tabs(["Sunburst Chart", "Dual-Axis Area Plot", "Scatter Plot"])

    with tab1:
        genre_slider_sunburst = st.slider("Select number of top genres to display (Sunburst):", min_value=2, max_value=31, value=5)
        piechart(data, genre_slider_sunburst)

    with tab2:
        genre_slider_dualaxis = st.slider("Select number of top genres to display (Dual-Axis):", min_value=2, max_value=31, value=5)
        dual_axis_area_plot(data, genre_slider_dualaxis)

    with tab3:
        st.title("Scatter Plot Configuration")

        # Multi-select dropdown for choosing genres
        selected_genres = st.multiselect(
            "Select genres to include in the plot:",
            options=data['Genre'].unique(),
            default=data['Genre'].unique()  # Default to all genres
        )

        if not selected_genres:
            st.warning("Please select at least one genre.")
        else:
            # Radio button to select between mean and total
            aggregation_method = st.radio(
                "Choose aggregation method:",
                options=["Total", "Mean"],
                index=0  # Default to "Total"
            )

            scatter_plot(data, selected_genres, aggregation_method)

elif page == "Artist":
    # Create the combined line plot
    combined_line_plot(data)

elif page == "Track & Album":

    # Streamlit application setup
    st.title("Track & Album Comparison")

    # Sidebar for artist selection
    artist = st.selectbox("Select an artist:", data['Artist Cleaned'].unique())

    # Radio buttons to choose between Track and Album comparison, placed horizontally
    comparison_level = st.radio("Compare by:", ["Track", "Album"], horizontal=True)

    # Dropdown to choose the variable for the x-axis
    variable = st.selectbox("Select a variable:", ["Likes", "Comments", "Stream", "Views"])

    # Get the list of tracks or albums based on comparison level
    items_list = data[data['Artist Cleaned'] == artist][comparison_level].unique()

    # Multiselect to allow choosing specific tracks or albums
    selected_items = st.multiselect(f"Select {comparison_level}(s):", items_list)

    # Create the visualization
    create_artist_comparison(data, artist, comparison_level, variable, selected_items)

elif page == "Variables":
    st.title("Variables Comparison")
    tab1, tab2, tab3 = st.tabs(["Artist", "Range", "Search"])
    with tab1:
        variables(data)
    with tab2:
        filter_songs(data)
    with tab3:
        # Streamlit app setup
        st.title("Track Search")
        search_term = st.text_input("Search for a track:")

        if search_term:
            search(data, search_term)

elif page == "Music Search":
    # Streamlit application setup
    st.title("Music Search")

    # Search bar
    search_term = st.text_input("Search Track, Artist, or Album:", "")

    # Trigger search when the user enters a term
    if search_term:
        search_data(data, search_term)

