import streamlit as st
import modal
import json
import os
import base64

def main():
        
    # Set a background image
    set_png_as_page_bg('content/background_image.jpg')

    st.title("Podcast Summarizer")

    available_podcast_info = create_dict_from_json_files('content')

    # Left section - Input fields
    st.sidebar.header("Podcast RSS Feeds")

    # Dropdown box
    st.sidebar.subheader("Available Podcasts Feeds")
    
    # Get the list of available podcasts after updating
    updated_dropdown_list = list(available_podcast_info.keys())
    # Set the selected index to the index of the last podcast
    selected_podcast_index = len(updated_dropdown_list) - 1
    
    selected_podcast = st.sidebar.selectbox("Select Podcast", options=available_podcast_info.keys(),
                                            index=selected_podcast_index)

    if selected_podcast:

        podcast_info = available_podcast_info[selected_podcast]

        # Right section - Newsletter content
        st.header(podcast_info['podcast_details']['podcast_title'])

        # Display the podcast title
        st.subheader("Episode Title")
        st.write(podcast_info['podcast_details']['episode_title'])

        # Display the podcast summary and the cover image in a side-by-side layout
        col1, col2 = st.columns([7, 3])

        with col1:
            # Display the podcast episode summary
            st.subheader("Podcast Episode Summary")
            st.write(podcast_info['podcast_summary'])

        with col2:
            st.image(podcast_info['podcast_details']['episode_image'], caption="Podcast Cover", width=300, use_column_width=True)

        # Display the podcast guest and their details in a side-by-side layout
        col3, col4 = st.columns([3, 7])

        with col3:
            st.subheader("Podcast Guest")
            if podcast_info['podcast_guest']['wiki_img'] != "":
                st.image(podcast_info['podcast_guest']['wiki_img'], \
                    caption=podcast_info['podcast_guest']['name'] + ',' + \
                    podcast_info['podcast_guest']['job'], width=300, use_column_width="auto")
            else:
                st.write(podcast_info['podcast_guest']['name'] + ',' + podcast_info['podcast_guest']['job'])

        with col4:
            st.subheader("Podcast Guest Details")
            guest_details_text = podcast_info['podcast_guest']['wiki_title'] + " " + \
                                 podcast_info['podcast_guest']['wiki_summary'] + " " + \
                                 podcast_info['podcast_guest']['wiki_url'] + " " + \
                                 podcast_info['podcast_guest']['google_URL']
                                 
            st.write(guest_details_text)

        # Display the five key moments
        st.subheader("Key Moments")
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(
                f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

    # User Input box
    st.sidebar.subheader("Add and Process New Podcast Feed")
    url = st.sidebar.text_input("Link to RSS Feed")

    process_button = st.sidebar.button(":heavy_check_mark: Process Podcast Feed")
     
    st.sidebar.markdown("**Note**: Processing a 30-minute podcast takes about a minute \
                        due to the 70x faster whisper model called WhisperX used in this project. \
                        Once processing is done, the select box updates instantly, \
                        displaying the summary of the podcast."
                        )

    if process_button:
        
        # Call the function to process the URLs and retrieve podcast guest information
        podcast_info = process_podcast_info(url)
        
        if podcast_info["podcast_summary"] == "" or \
           podcast_info["podcast_highlights"] == "":
            st.error("Error processing RSS URL.\n \
                     Most likely, the podcast episode you are trying to process is quite lengthy. \
                     Currently, we support extracting summaries for podcasts that are shorter than 1 hour. \
                     Please select a different podcast with episodes lasting under an hour.")
            
        # Update the dropdown with the processed podcast title
        new_podcast_name = get_next_available_name(available_podcast_info)
        available_podcast_info[new_podcast_name] = podcast_info
        selected_podcast = new_podcast_name

        # Save processed podcast info to a JSON file
        save_path = os.path.join('content', new_podcast_name)
        with open(save_path, 'w') as json_file:
            json.dump(podcast_info, json_file, indent=4)
            
        # Clear the previous content by rerendering the main() function
        st.experimental_rerun()

def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    json_files = sorted(json_files)
    data_dict = {}

    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            podcast_info = json.load(file)
            podcast_name = podcast_info['podcast_details']['podcast_title']
            # Process the file data as needed
            data_dict[podcast_name] = podcast_info

    return data_dict

def process_podcast_info(url):
    f = modal.Function.lookup("podcast-project", "process_podcast")
    output = f.remote(url, '/tmp/podcast/')
    return output

def get_next_available_name(existing_podcasts):
    idx = len(existing_podcasts.keys()) + 1
    return f"podcast-{idx}.json"

@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    opacity: 0.8;  /* Adjust opacity as needed */
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
