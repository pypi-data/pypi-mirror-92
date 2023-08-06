# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Union
import random, os

# Pip
from amazon_platform import Platform
from kcu import kjson, ktime

# Local
from .proxy_details import ProxyDetails
from .amazon_settings import AmazonSettings

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# -------------------------------------------------------------- class: Acc -------------------------------------------------------------- #

class Acc:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        config_dict: dict,
        platform: Platform,
        cache_folder_path: str,
        default_max_uploads_per_day: int,
        default_tags: Optional[List[str]],
        default_affiliate_tag: Optional[str],
        default_bitly_tokens: Optional[Union[List[str], str]]
    ):
        self.platform = platform
        self.__config_max_uploads_per_day = config_dict['max_uploads_per_day'] if 'max_uploads_per_day' in config_dict else default_max_uploads_per_day
        self.__use_dynamic_max_uploads_per_day = config_dict['use_dynamic_max_uploads_per_day'] if 'use_dynamic_max_uploads_per_day' in config_dict else False
        self.proxy = ProxyDetails(config_dict['proxy']) #if 'proxy' else None
        self.amazon = AmazonSettings(config_dict['amazon'], default_affiliate_tag, default_bitly_tokens) if 'amazon' in config_dict else None

        os.makedirs(cache_folder_path, exist_ok=True)

        self.titles = config_dict['titles'] if 'titles' in config_dict else None
        self.descriptions = config_dict['descriptions'] if 'descriptions' in config_dict else None

        cache_file_path = os.path.join(cache_folder_path, 'cache.json')
        cache = kjson.load(
            cache_file_path,
            default_value={
                'start_ts_utc': ktime.time_utc()
            },
            save_if_not_exists=True
        )

        self.__config_start_ts_utc = config_dict['start_ts_utc'] if 'start_ts_utc' in config_dict else None

        if self.__config_start_ts_utc is not None and self.__config_start_ts_utc != cache['start_ts_utc']:
            cache['start_ts_utc'] = self.__config_start_ts_utc
            kjson.save(cache_file_path, cache)

        self.start_ts_utc = cache['start_ts_utc']

        if self.__use_dynamic_max_uploads_per_day:
            age_days = self.age_seconds / ktime.seconds_in_day

            self.max_uploads_per_day = age_days if age_days < self.__config_max_uploads_per_day else self.__config_max_uploads_per_day
        else:
            self.max_uploads_per_day = self.__config_max_uploads_per_day

        self.__tags = config_dict['tags'] if 'tags' in config_dict else default_tags


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @property
    def random_title(self) -> Optional[str]:
        return random.choice(self.titles) if self.titles else None

    @property
    def random_description(self) -> Optional[str]:
        return random.choice(self.descriptions) if self.descriptions else None

    @property
    def tags(self) -> List[str]:
        if not self.__tags:
            return []

        random.shuffle(self.__tags)

        return self.__tags

    @property
    def age_seconds(self) -> int:
        return int(ktime.time_utc() - self.start_ts_utc)


# ---------------------------------------------------------------------------------------------------------------------------------------- #