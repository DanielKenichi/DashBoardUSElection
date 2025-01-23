# DashBoardUSElection

Project for a college subject at UFSCar which the objective of plotting a dashboard of the dataset [US elections](https://www.kaggle.com/datasets/essarabi/ultimate-us-election-dataset/discussion?sort=undefined).

# Installing the dependencies

To run this project locally, please get the dependencies with one of the following options.

## Option 1 - Install the requirements with poetry

```
    pipx install poetry
    poetry install --no-root
```


## Option 2 - Install the requirements with requirements.txt

```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
```

# Start the dashboard

To start the dashboard run `poetry run streamlit run main.py` or `streamlit run main.py`, according to the option you chose to install the dependencies.

# Initial exploratory analysis

Initial exploratory analysis of this dataset for pre-processing can be found [here](https://colab.research.google.com/drive/1t3aXp8CIESJKGAIBAsCVxGcHz1Xco0jI?usp=sharing).