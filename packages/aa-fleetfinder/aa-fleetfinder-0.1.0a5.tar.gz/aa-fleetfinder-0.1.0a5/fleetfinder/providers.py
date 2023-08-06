"""
providers
"""

from fleetfinder import __user_agent__

from esi.clients import EsiClientProvider

esi = EsiClientProvider(app_info_text=__user_agent__)
