from typing import Dict, List

import pandas as pd
from database import Category, Menu, Restraunt, engine
from sqlalchemy import insert
from sqlalchemy.orm import Session


class ETL:
    def __init__(self) -> None:
        self.restraunts: List[str] = []
        self.categories: List[str] = []

    def is_nan(self, data: str) -> bool:
        return data != data

    def _extract(self, path: str) -> pd.DataFrame:
        """
        Extracts data from the given path

        Args:
            path (str): Path to the file

        Returns:
            dict: extracted data dictionary
        """
        dataframe = pd.read_excel(path)
        return dataframe

    def _tranform(
        self, dataframe: pd.DataFrame
    ) -> Dict[str, List[Dict[str, str | None]] | List[Dict[str, str] | None]]:
        """
        Clean and transform data to the structure we need

        Returns:
            dict: Cleaned data dictionary
        """

        def extract_data(
            data: Dict[int, List[str]], model: Category | Restraunt
        ) -> List[Dict[str, str] | None]:
            def remove_existing(data: List[str]) -> List[Dict[str, str] | None]:
                """Removing data which is already in database"""
                unique_data: List[Dict[str, str] | None] = []
                with Session(engine) as db:
                    all_data = db.query(model.name).all()
                    all_data = [i[0] for i in all_data]

                for i in data:
                    if i not in all_data and not self.is_nan(i):
                        unique_data.append({"name": i})

                return unique_data

            unique_data = [i for i in set([value for value in data.values()])]
            if model == Restraunt:
                self.restraunts = unique_data
            elif model == Category:
                self.categories = unique_data
            # Removing duplication from recieved data
            cleaned_data = remove_existing(unique_data)

            return cleaned_data

        def is_valid_row(name: str, ingredients: str) -> bool:
            """
            Check if name and ingredient is avaiable and both are valid
            """
            if name and ingredients:
                # name != name is checking name is not nan
                # here isinstance is not working
                if type(name) == float and self.is_nan(name):  # type: ignore
                    return False
                if type(ingredients) == float and self.is_nan(ingredients):
                    return False
                return True
            else:
                return False

        def clean_value(data: str) -> str | None:
            if self.is_nan(data):
                return None
            return data

        length = len(dataframe)
        df_dict = dataframe.to_dict()

        menu: List[Dict[str, str | None]] = []
        restraunts = extract_data(df_dict.get("Store"), Restraunt)
        categories = extract_data(df_dict.get("Product category"), Category)

        for i in range(length):
            if is_valid_row(
                df_dict.get("Product Name", {}).get(i),
                df_dict.get("Ingredients on Product Page", {}).get(i),
            ):
                menu.append(
                    {
                        "name": clean_value(df_dict.get("Product Name", {}).get(i)),
                        "ingredients": clean_value(
                            df_dict.get("Ingredients on Product Page", {}).get(i)
                        ),
                        "allergens": clean_value(
                            df_dict.get("Allergens and Warnings", {}).get(i)
                        ),
                        "picture": clean_value(
                            df_dict.get("URL of primary product picture", {}).get(i)
                        ),
                        "category": clean_value(
                            df_dict.get("Product category", {}).get(i)
                        ),
                        "restraunt": clean_value(df_dict.get("Store", {}).get(i)),
                    }
                )

        return {
            "menu": menu,
            "categories": categories,
            "restraunts": restraunts,
        }

    def _load(self, cleaned_data: Dict[str, List[Dict[str, str]] | None]) -> None:
        def bulk_insertion(
            model: Category | Restraunt,
            session: Session,
            data: List[Dict[str, str] | None],
        ) -> None:
            if data:
                session.execute(insert(model), data)
                session.commit()

        def get_id(model: Category | Restraunt, session: Session, name: str) -> int:
            if name is not None:
                id = session.query(model).filter(model.name == name).first().id
                return id

        def update_menu_items(session: Session) -> None:
            visited: dict[str, int] = {}
            for data in cleaned_data.get("menu"):
                if data["category"] not in visited.keys():
                    visited[data["category"]] = get_id(
                        Category, session, data["category"]
                    )

                if data["restraunt"] not in visited.keys():
                    visited[data["restraunt"]] = get_id(
                        Restraunt, session, data["restraunt"]
                    )

                data["category"] = visited[data["category"]]
                data["restraunt"] = visited[data["restraunt"]]

        with Session(engine) as session:
            bulk_insertion(Category, session, cleaned_data.get("categories"))
            bulk_insertion(Restraunt, session, cleaned_data.get("restraunts"))
            update_menu_items(session)
            bulk_insertion(Menu, session, cleaned_data.get("menu"))

    def run_pipeline(self) -> None:
        data = self._extract("data/restaurant_data.xlsx")
        cleaned_data = self._tranform(data)
        self._load(cleaned_data)


if __name__ == "__main__":
    ETL().run_pipeline()
