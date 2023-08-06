# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# Local
from .product_category import ProductCategory
from .constants import Constants

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# -------------------------------------------------------- class: ProductDetails --------------------------------------------------------- #

class ProductDetails:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        config_dict: dict,
    ):
        self.trend_categories = [ProductCategory.from_dict(cat_dict) for cat_dict in config_dict['trend_categories']]
        self.min_price = config_dict['min_price'] if 'min_price' in config_dict else Constants.DEFAULT_MIN_PRODUCT_PRICE
        self.min_rating = config_dict['min_rating'] if 'min_rating' in config_dict else Constants.DEFAULT_MIN_PRODUCT_RATING
        self.min_reviews = config_dict['min_reviews'] if 'min_reviews' in config_dict else Constants.DEFAULT_MIN_PRODUCT_REVIEWS


# ---------------------------------------------------------------------------------------------------------------------------------------- #