How to run the dashboard?

1. The dashboard has been deployed to the Streamlit cloud. so it can be accessed via:
   **https://asvrn-bike-sharing.streamlit.app/**

2. You can run locally with
   1. Download the project.
   2. Set up environment
      conda create --name main-ds
      conda activate main-ds
      pip install pandas matplotlib seaborn streamlit
   4. Note that the csv file does not move when used as a data source.
   5. Open VSCcode and run the file by clicking Terminal and typing _streamlit run dashboard.py._
