# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Union
from enum import Enum

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------ class: ProductCategoryType ------------------------------------------------------ #

from enum import Enum

class ProductCategoryType(Enum):
    GOOGLE = 0
    AMAZON = 1


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @staticmethod
    def get_category_type(category_value: Union[int, str]):
        if type(category_value) == int:
            return ProductCategoryType.GOOGLE

        return ProductCategoryType.AMAZON


# ---------------------------------------------------------------------------------------------------------------------------------------- #