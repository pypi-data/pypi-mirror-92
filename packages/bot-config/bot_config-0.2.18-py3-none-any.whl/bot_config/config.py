# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Dict, Tuple, Callable
import time, os, random, string

# Pip
from kcu import kjson
from amazon_platform import Platform

from selenium_uploader_account import SeleniumUploaderAccount
from selenium_youtube import Youtube
from selenium_facebook import Facebook
from selenium_twitter import Twitter
from selenium_tiktok import TikTok
from selenium_instagram import Instagram

from simple_multiprocessing import MultiProcess, Task

# Local
from .models import Acc, FacebookAcc, Constants

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ class: Config ------------------------------------------------------------- #

class Config:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        config_dict: dict,
        channel_id: str,
        global_config_cache_folder_path: str
    ):
        self.channel_id = channel_id
        cache_folder_path = os.path.join(global_config_cache_folder_path, channel_id)
        os.makedirs(cache_folder_path, exist_ok=True)

        self.youtube = Acc(
            config_dict['youtube'],
            Platform.Youtube,
            os.path.join(cache_folder_path, 'youtube'),
            Constants.DEFAULT_MAX_UPLOADS_PER_DAY_YT or Constants.DEFAULT_MAX_UPLOADS_PER_DAY,
            Constants.DEFAULT_VIDEO_TAGS_YT or Constants.DEFAULT_MAIN_VIDEO_TAGS or Constants.DEFAULT_SECONDARY_VIDEO_TAGS,
            Constants.DEFAULT_MAIN_AFFILIATE_TAG or Constants.DEFAULT_SECONDARY_AFFILIATE_TAG,
            Constants.DEFAULT_MAIN_BITLY_TOKENS
        )
        self.facebook = FacebookAcc(
            config_dict['facebook'],
            Platform.Facebook,
            os.path.join(cache_folder_path, 'facebook'),
            Constants.DEFAULT_MAX_UPLOADS_PER_DAY_FB or Constants.DEFAULT_MAX_UPLOADS_PER_DAY,
            Constants.DEFAULT_VIDEO_TAGS_FB or Constants.DEFAULT_SECONDARY_VIDEO_TAGS or Constants.DEFAULT_MAIN_VIDEO_TAGS,
            Constants.DEFAULT_SECONDARY_AFFILIATE_TAG or Constants.DEFAULT_MAIN_AFFILIATE_TAG,
            Constants.DEFAULT_SECONDARY_BITLY_TOKENS
        ) if 'facebook' in config_dict else None
        self.twitter = Acc(
            config_dict['twitter'],
            Platform.Twitter,
            os.path.join(cache_folder_path, 'twitter'),
            Constants.DEFAULT_MAX_UPLOADS_PER_DAY_TW or Constants.DEFAULT_MAX_UPLOADS_PER_DAY,
            Constants.DEFAULT_VIDEO_TAGS_TW or Constants.DEFAULT_SECONDARY_VIDEO_TAGS or Constants.DEFAULT_MAIN_VIDEO_TAGS,
            Constants.DEFAULT_SECONDARY_AFFILIATE_TAG or Constants.DEFAULT_MAIN_AFFILIATE_TAG,
            Constants.DEFAULT_SECONDARY_BITLY_TOKENS
        ) if 'twitter' in config_dict else None
        self.tiktok = Acc(
            config_dict['tiktok'],
            Platform.TikTok,
            os.path.join(cache_folder_path, 'tiktok'),
            Constants.DEFAULT_MAX_UPLOADS_PER_DAY_TT or Constants.DEFAULT_MAX_UPLOADS_PER_DAY,
            Constants.DEFAULT_VIDEO_TAGS_TT or Constants.DEFAULT_SECONDARY_VIDEO_TAGS or Constants.DEFAULT_MAIN_VIDEO_TAGS,
            Constants.DEFAULT_SECONDARY_AFFILIATE_TAG or Constants.DEFAULT_MAIN_AFFILIATE_TAG,
            Constants.DEFAULT_SECONDARY_BITLY_TOKENS
        ) if 'tiktok' in config_dict else None
        self.instagram = Acc(
            config_dict['instagram'],
            Platform.Instagram,
            os.path.join(cache_folder_path, 'instagram'),
            Constants.DEFAULT_MAX_UPLOADS_PER_DAY_IG or Constants.DEFAULT_MAX_UPLOADS_PER_DAY,
            Constants.DEFAULT_VIDEO_TAGS_IG or Constants.DEFAULT_SECONDARY_VIDEO_TAGS or Constants.DEFAULT_MAIN_VIDEO_TAGS,
            Constants.DEFAULT_SECONDARY_AFFILIATE_TAG or Constants.DEFAULT_MAIN_AFFILIATE_TAG,
            Constants.DEFAULT_SECONDARY_BITLY_TOKENS
        ) if 'instagram' in config_dict else None

        active_from = config_dict['active_from'] if 'active_from' in config_dict else 0
        self.active = active_from >= 0 and active_from < int(time.time())

        cache_file_path = os.path.join(cache_folder_path, 'cache.json')
        cache = kjson.load(
            cache_file_path,
            default_value={
                'start_ts': int(time.time())
            },
            save_if_not_exists=True
        )
        self.start_ts = cache['start_ts']


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @property
    def age_seconds(self) -> int:
        return int(time.time()) - self.start_ts

    @property
    def available_platforms(self) -> List[Platform]:
        return [p for p, o in self.__accs_platforms.items() if o]

    @property
    def all_platforms(self) -> List[Platform]:
        return list(self.__accs_platforms.values())

    @property
    def available_accs(self) -> List[Acc]:
        return [o for o in self.__accs_platforms.values() if o]

    @property
    def proxies(self) -> List[str]:
        return [acc.proxy.string for acc in self.available_accs if acc.proxy]


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def acc_for_platform(
        self,
        platform: Platform
    ) -> Optional[Acc]:
        return self.__accs_platforms[platform]

    def all_selenium_accs(
        self,
        cookies_folder_path: str = None,
        extensions_folder_path: Optional[str] = None,
        screen_size: Optional[Tuple[int, int]] = None,
        full_screen: bool = True,
        headless: bool = False,
        user_agent: Optional[str] = None,
        prompt_user_input_login: bool = True,
        login_prompt_callback: Optional[Callable[[str], None]] = None,
        login_prompt_timeout_seconds: Optional[float] = None,
        youtube: Optional[Youtube] = None,
        facebook: Optional[Facebook] = None,
        instagram: Optional[Instagram] = None,
        twitter: Optional[Twitter] = None,
        tiktok: Optional[TikTok] = None,
        selenium_accs: Optional[Dict[Platform, SeleniumUploaderAccount]] = None
    ) -> Dict[Platform, SeleniumUploaderAccount]:
        youtube, facebook, instagram, twitter, tiktok = self.all_selenium_accs_arr(
            cookies_folder_path=cookies_folder_path,
            extensions_folder_path=extensions_folder_path,
            screen_size=screen_size,
            full_screen=full_screen,
            headless=headless,
            user_agent=user_agent,
            prompt_user_input_login=prompt_user_input_login,
            login_prompt_callback=login_prompt_callback,
            login_prompt_timeout_seconds=login_prompt_timeout_seconds,
            youtube=youtube,
            facebook=facebook,
            instagram=instagram,
            twitter=twitter,
            tiktok=tiktok,
            selenium_accs=selenium_accs
        )

        return {
            Platform.Youtube:   youtube,
            Platform.Facebook:  facebook,
            Platform.Instagram: instagram,
            Platform.Twitter:   twitter,
            Platform.TikTok:    tiktok
        }

    def all_selenium_accs_arr(
        self,
        cookies_folder_path: str = None,
        extensions_folder_path: Optional[str] = None,
        screen_size: Optional[Tuple[int, int]] = None,
        full_screen: bool = True,
        headless: bool = False,
        user_agent: Optional[str] = None,
        prompt_user_input_login: bool = True,
        login_prompt_callback: Optional[Callable[[str], None]] = None,
        login_prompt_timeout_seconds: Optional[float] = None,
        youtube: Optional[Youtube] = None,
        facebook: Optional[Facebook] = None,
        instagram: Optional[Instagram] = None,
        twitter: Optional[Twitter] = None,
        tiktok: Optional[TikTok] = None,
        selenium_accs: Optional[Dict[Platform, SeleniumUploaderAccount]] = None
    ) -> List[SeleniumUploaderAccount]:
        kwargs = {
            'cookies_folder_path':cookies_folder_path,
            'extensions_folder_path':extensions_folder_path,
            'screen_size':screen_size,
            'full_screen':full_screen,
            'headless':headless,
            'user_agent':user_agent,
            'prompt_user_input_login':prompt_user_input_login,
            'login_prompt_callback':login_prompt_callback,
            'login_prompt_timeout_seconds':login_prompt_timeout_seconds
        }

        selenium_accs = {
            Platform.Youtube:   youtube   or selenium_accs[Platform.Youtube]   if Platform.Youtube   in selenium_accs else None,
            Platform.Facebook:  facebook  or selenium_accs[Platform.Facebook]  if Platform.Facebook  in selenium_accs else None,
            Platform.Instagram: instagram or selenium_accs[Platform.Instagram] if Platform.Instagram in selenium_accs else None,
            Platform.Twitter:   twitter   or selenium_accs[Platform.Twitter]   if Platform.Twitter   in selenium_accs else None,
            Platform.TikTok:    tiktok    or selenium_accs[Platform.TikTok]    if Platform.TikTok    in selenium_accs else None
        }

        available_platforms = self.available_platforms

        def __simple_return(acc: SeleniumUploaderAccount) -> SeleniumUploaderAccount:
            return acc

        tasks = [
            None if p not in available_platforms
            else Task(__simple_return, acc) if acc
            else Task(self.selenium_acc, p, **kwargs)
            for p, acc in selenium_accs.items()
        ]

        return [acc if isinstance(acc, SeleniumUploaderAccount) else None for acc in MultiProcess(tasks).solve()]

    def selenium_acc(
        self,
        platform: Platform,
        cookies_folder_path: str = None,
        extensions_folder_path: Optional[str] = None,
        screen_size: Optional[Tuple[int, int]] = None,
        full_screen: bool = True,
        headless: bool = False,
        user_agent: Optional[str] = None,
        prompt_user_input_login: bool = True,
        login_prompt_callback: Optional[Callable[[str], None]] = None,
        login_prompt_timeout_seconds: Optional[int] = 60*5
    ) -> Optional[SeleniumUploaderAccount]:
        acc = self.acc_for_platform(platform)

        if not acc:
            return None

        c = {
            Platform.Youtube:   Youtube,
            Platform.Facebook:  Facebook,
            Platform.Instagram: Instagram,
            Platform.Twitter:   Twitter,
            Platform.TikTok:    TikTok
        }[platform]

        sel_acc = c(
            cookies_folder_path=cookies_folder_path,
            extensions_folder_path=extensions_folder_path,
            screen_size=screen_size,
            full_screen=full_screen,
            headless=headless,
            user_agent=user_agent,
            prompt_user_input_login=prompt_user_input_login,
            login_prompt_callback=login_prompt_callback,
            login_prompt_timeout_seconds=login_prompt_timeout_seconds
        )

        return sel_acc if sel_acc.did_log_in_at_init else None


    # ------------------------------------------------------ Private properties ------------------------------------------------------ #

    @property
    def __accs_platforms(self) -> Dict[Platform, Optional[Acc]]:
        return {
            Platform.Youtube:   self.youtube,
            Platform.Facebook:  self.facebook,
            Platform.Instagram: self.instagram,
            Platform.Twitter:   self.twitter,
            Platform.TikTok:    self.tiktok
        }