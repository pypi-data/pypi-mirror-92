# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Union


# ---------------------------------------------------------------------------------------------------------------------------------------- #




# -------------------------------------------------------- class: AmazonSettings --------------------------------------------------------- #

class AmazonSettings:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        config_dict: Optional[dict],
        default_affiliate_tag: Optional[str],
        default_bitly_tokens: Optional[Union[List[str], str]]
    ):
        self.affiliate_tag = config_dict['affiliate_tag'] if config_dict and 'affiliate_tag' in config_dict else default_affiliate_tag
        self.bitly_tokens = config_dict['bitly_tokens'] if config_dict and 'bitly_tokens' in config_dict else default_bitly_tokens

        if isinstance(self.bitly_tokens, str):
            self.bitly_tokens = [self.bitly_tokens]


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @property
    def should_shorten_affiliate_url(self) -> bool:
        return self.bitly_tokens and True


# ---------------------------------------------------------------------------------------------------------------------------------------- #