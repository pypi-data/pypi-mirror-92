import os

import requests

from .OAuth2 import OAuth2
from .destiny_enums import MembershipType, Components

API_ROOT_PATH = "https://www.bungie.net/Platform"


class BungieAPI:
    def __init__(self, api_key: str):
        self.__HEADERS = {"X-API-Key": api_key}
        self.__OAuth2 = None
        self.__xbox_credentials_input = False
        os.environ["X-API-KEY"] = api_key

    def input_xbox_credentials(self, xbox_live_email: str, xbox_live_password: str):
        """ Required to authorize your app and start OAuth2.

        :param xbox_live_email: Your xbox live email
        :param xbox_live_password: Your xbox live password
        :return: None
        """
        self.__xbox_credentials_input = True
        os.environ["XBOX-EMAIL"] = xbox_live_email
        os.environ["XBOX-PASS"] = xbox_live_password

    def start_oauth2(self, client_id: str, client_secret: str):
        """ Starts a localhost HTTPS server, authorizes your app to access your account, and retrieves the necessary
        authorization code, and access tokens. Check for more details on the parameters:
            https://www.bungie.net/en/Application

        :param client_id: The client id associated with your app
        :param client_secret: The client id associated with your app
        :return: None
        """
        if self.__xbox_credentials_input:
            self.__OAuth2 = OAuth2(self, client_id, client_secret)
        else:
            print("OAuth2 can not be enabled without your xbox live credentials.")

    def close_oauth2(self):
        """ Disables OAuth2 integration, this will limit the endpoints you are able to access.

        :return: None
        """
        if self.__OAuth2 is not None:
            self.__OAuth2._enabled = False
            self.__OAuth2 = None
        else:
            print("OAuth2 is not enabled")

    def _renew_headers(self):
        self.__HEADERS["Authorization"] = f'Bearer {os.getenv("ACCESS-TOKEN")}'

    def get_bungie_user_by_id(self, membership_id: int) -> dict:
        """ Loads a bungie.net user by membership id.

        :param membership_id: The membership ID of the player.
        :return: dict
        """
        api_call = requests.get(f'{API_ROOT_PATH}/User/GetBungieNetUserById/{str(membership_id)}/',
                                headers=self.__HEADERS)
        return (api_call.json())['Response']

    def search_users(self, search_string: str) -> dict:
        """ Returns a list of possible users based on the search string

        :return: dict
        """
        api_call = requests.get(f'{API_ROOT_PATH}/User/SearchUsers/?q={search_string}', headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_profile(self, membership_type: MembershipType, membership_id: int, components: Components) -> dict:
        """ Returns Destiny Profile information for the supplied membership.

        :param components: See destiny_enums->Components
        :param membership_type: The membership type of the associated player in the search. See destiny_enums->MembershipType
        :param membership_id: The membership ID of the player.
        :return: dict
        """
        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membership_type.value}/Profile/{membership_id}/'
                                f'?components={components.value}', headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_clan_weekly_reward_state(self, group_id: int) -> dict:
        """ Returns information on the weekly clan rewards and if the clan has earned them or not. Note that this
        will always report rewards as not redeemed.

        :param group_id: A valid group id of a clan.
        :return: dict
        """
        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/Clan/{group_id}/WeeklyRewardState/',
                                headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_collectible_node_details(self, membership_type: MembershipType, membership_id: int, character_id: int,
                                     collectible_presentation_node_hash: int, components: Components) -> dict:
        """Given a Presentation Node that has Collectibles as direct descendants, this will return item details about
        those descendants in the context of the requesting character.

        :param membership_type: The membership type of the associated player in the search. See destiny_enums->MembershipType
        :param membership_id: The membership ID of the player.
        :param character_id: The character ID of the player.
        :param collectible_presentation_node_hash:
        :param components: See destiny_enums->Components
        :return: dict
        """
        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membership_type.value}/Profile/{membership_id}/Character/'
                                f'{character_id}/Collectibles/{collectible_presentation_node_hash}'
                                f'/?components={components.value}',
                                headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_linked_profiles(self, membership_type: MembershipType, membership_id: int) -> dict:
        """ Returns a summary information about all profiles linked to the requesting membership type/membership ID
        that have valid Destiny information. The passed-in Membership Type/Membership ID may be a Bungie.Net
        membership or a Destiny membership. It only returns the minimal amount of data to begin making more
        substantive requests, but will hopefully serve as a useful alternative to UserServices for people who just
        care about Destiny data. Note that it will only return linked accounts whose linkages you are allowed to view.

        :param membership_type: The membership type of the associated player in the search. See destiny_enums->MembershipType
        :param membership_id: The membership ID of the player.
        :return: dict
        """
        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membership_type.value}/Profile/{membership_id}'
                                f'/LinkedProfiles/', headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_character(self, membership_type: MembershipType, membership_id: int, character_id: int,
                      components: Components) -> dict:
        """ Returns character information for the supplied character.

        :param components: See destiny_enums->Components
        :param membership_type: The membership type of the associated player in the search. See destiny_enums->MembershipType
        :param membership_id: The membership ID of the player.
        :param character_id: The character ID of the player.
        :return: dict
        """
        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membership_type.value}/Profile/{membership_id}/Character/'
                                f'{character_id}/?components={components.value}',
                                headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_vendor(self, membership_type: MembershipType, membership_id: int, character_id: int,
                   vendor_hash: int, components: Components) -> dict:
        """ Get the details of a specific Vendor.

        :param membership_type: The membership type of the associated player in the search. See destiny_enums->MembershipType
        :param membership_id: The membership ID of the player.
        :param character_id: The character ID of the player.
        :param vendor_hash: The hash identifier for the specific Vendor you want returned.
        :param components: See destiny_enums->Components
        :return: dict
        """
        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membership_type.value}/Profile/{membership_id}/Character/'
                                f'{character_id}/Vendors/{vendor_hash}/?components={components.value}',
                                headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_vendors(self, membership_type: MembershipType, membership_id: int, character_id: int,
                    components: Components) -> dict:
        """Get currently available vendors from the list of vendors that can possibly have rotating inventory. Note
        that this does not include things like preview vendors and vendors-as-kiosks, neither of whom have
        rotating/dynamic inventories. Use their definitions as-is for those.

        :param membership_type: The membership type of the associated player in the search. See destiny_enums->MembershipType
        :param membership_id: The membership ID of the player.
        :param character_id: The character ID of the player.
        :param components: See destiny_enums->Components
        :return: dict
        """
        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membership_type.value}/Profile/{membership_id}/Character/'
                                f'{character_id}/Vendors/?components={components.value}', headers=self.__HEADERS)
        return (api_call.json())['Response']

    def manifest(self, entity_type: str, hash_identifier: int) -> dict:
        """ Manifests the specified entity. Returns general information about the entity, see API documentation for more details:
            https://bungie-net.github.io/#Destiny2.GetDestinyEntityDefinition

        :param entity_type: The type of entity for whom you would like results. These correspond to the entity's
            definition contract name. See destiny_enums->Definitions
        :param hash_identifier: The hash identifier for the specific Entity you want returned.
        :return: dict
        """
        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/Manifest/{entity_type}/{hash_identifier}',
                                headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_public_vendors(self, components: Components) -> dict:
        """Returns information on the requested vendor, see API documentation for more details:
            https://bungie-net.github.io/#Destiny2.GetPublicVendors

        :param components: See destiny_enums->Components
        :return: dict
        """
        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2//Vendors/?components={components.value}',
                                headers=self.__HEADERS)
        return (api_call.json())['Response']

    def search_entities(self, entity_type: str, search_term: str) -> dict:
        """Searches for the specified entity in the API, see API documentation for more details:
            https://bungie-net.github.io/#Destiny2.SearchDestinyEntities

        :param entity_type: The type of entity for whom you would like results. These correspond to the entity's
            definition contract name. See destiny_enums->Definitions
        :param search_term: The string to use when searching for Destiny entities.
        :return: dict
        """
        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/Armory/Search/{entity_type}/{search_term}/',
                                headers=self.__HEADERS)
        return (api_call.json())['Response']

    def search_destiny_player(self, membership_type: MembershipType, display_name: str,
                              return_original_profile=False) -> dict:
        """ Returns a list of Destiny memberships given a full Gamertag or PSN ID. Unless you pass
        return_original_profile=true, this will return membership information for the users' Primary Cross Save Profile
        if they are engaged in cross save rather than any original Destiny profile that is now being overridden.

        :param return_original_profile: (Optional) If passed in and set to true, we will return the original Destiny
            Profile(s) linked to that gamertag, and not their currently active Destiny Profile.
        :param membership_type: The membership type of the associated player in the search.
            See destiny_enums->MembershipType
        :param display_name: The display name of the associated player in the search.
        :return: dict
        """
        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/SearchDestinyPlayer/{membership_type.value}/'
                                f'{display_name}/?returnOriginalProfile={return_original_profile}',
                                headers=self.__HEADERS)
        return (api_call.json())['Response']
