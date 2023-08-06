# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Union
import string

# Pip
from amazon_buddy import Category as AmazonCategory

# Local
from .enums import ProductCategoryType

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# -------------------------------------------------------- class: ProductCategory -------------------------------------------------------- #

class ProductCategory:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        category: Union[int, str, AmazonCategory],
        letters: Optional[List[str]] = None
    ):
        if type(category) == int:
            self.type = ProductCategoryType.GOOGLE
            self.category = category
        else:
            self.type = ProductCategoryType.AMAZON

            if type(category) == str:
                category = AmazonCategory(category)

            self.category = category
            self.letters = letters.lower() if letters else string.ascii_lowercase


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def from_dict(cls, config_dict: dict):
        return cls(category=config_dict['category'], letters=config_dict['letters'] if 'letters' in config_dict else None)


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @property
    def str(self):
        return self.category.value if self.type == ProductCategoryType.AMAZON else str(self.category)


# ---------------------------------------------------------------------------------------------------------------------------------------- #