# Podcast Summarizer

Welcome to the Podcast Summarizer project! This tool allows you to automatically summarize podcast episodes by providing the RSS feed URL of the podcast. The underlying technology involves utilizing various AI models to extract meaningful content from podcast episodes and present them in a summarized form.

## Project Demo GIF

<div align="center">
   <img src="content/podcast/podcast.gif" width="100%" max-width="800"/>
</div>

## Demo

Here's a breakdown of what's happening in the demo GIF:

1. You open the app and navigate to the main page.
2. Find a podcast RSS feed URL from [Listen Notes](https://www.listennotes.com) or [Castos](https://castos.com/tools/find-podcast-rss-feed/).
3. You input the RSS feed URL of the podcast episode you want to summarize.
4. You click the "Process a Podcast Feed" button.
5. The app downloads the podcast episode in mp3 format.
6. The WhisperX model transcribes the speech to text.
7. The ChatGPT 3.5 Turbo model generates a summary.
8. [5.](#demo), [6.](#demo) and [7.](#demo) are running using GPU in [Modal](https://modal.com) backend.
9. The [Streamlit](https://streamlit.io) frontend displays the summary, episode details, guest info, and highlights.

Feel free to explore the interface and generate summaries for your favorite podcasts!

## Features

- **Automated Summarization:** Using the power of AI, this project can automatically download podcast episodes, transcribe the speech to text, and generate concise summaries.
- **WhisperX for Transcription:** The project employs the WhisperX model to convert spoken words in podcast episodes into text.
- **ChatGPT 3.5 Turbo for Summarization:** The OpenAI ChatGPT 3.5 Turbo model is used to create informative and coherent summaries based on the transcribed text.
- **Frontend with Streamlit:** The summarized content, along with episode details, guest information, and highlights are presented through an interactive and user-friendly Streamlit frontend.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/tekeburak/podcast-summarizer.git
   cd podcast-summarizer

2. Install the required dependencies using pip:
   ```bash
   pip install streamlit modal

3. Deploy backend to Modal:
   ```bash
   modal deploy /content/podcast/podcast_backend.py

4. Run the Streamlit app:
   ```bash
   streamlit run podcast_frontend.py

### Local Usage

1. Access the Streamlit frontend by opening a web browser and navigating to [http://localhost:8501](localhost:8501).
2. On the homepage, you'll find an input field where you can paste the RSS feed URL of the podcast you want to summarize.
3. Click the "Process a Podcast Feed" button to initiate the summarization process.
4. The app will start by downloading the podcast episode in mp3 format and then use the WhisperX model to transcribe the speech to text.
5. Once transcribed, the text data is fed into the ChatGPT 3.5 Turbo model to generate a summary.
6. The summary, along with episode details, guest information, and highlights, will be displayed on the Streamlit interface.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`.
3. Implement your feature and make necessary changes.
4. Commit and push your changes: `git commit -m "Add feature" && git push origin feature-name`.
5. Submit a pull request detailing the changes you've made.

## License

This project is licensed under the [MIT License](LICENSE).