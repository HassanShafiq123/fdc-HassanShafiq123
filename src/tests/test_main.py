from src.fig_data_challenge.main import ETL
import pandas as pd


def test_extraction():
    dataframe = ETL()._extract("data/restaurant_data.xlsx")
    assert isinstance(dataframe, pd.DataFrame)


def test_transform():
    etl = ETL()
    dataframe = etl._extract("data/restaurant_data.xlsx")
    clean_data = etl._tranform(dataframe)

    assert isinstance(clean_data["menu"], list)
    assert isinstance(clean_data["categories"], list)
    assert isinstance(clean_data["restraunts"], list)


def test_load():
    response = ETL().run_pipeline()
    assert response is None
