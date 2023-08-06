import asyncio
import pop.hub
from dict_tools import data
from typing import Iterable, Dict, Any


def __init__(hub):
    # Remember not to start your app in the __init__ function
    # This function should just be used to set up the plugin subsystem
    # Add another function to call from your run.py to start the app
    hub.acct.SUB_PROFILES = data.NamespaceDict()
    hub.acct.PROFILES = data.NamespaceDict()
    hub.acct.UNLOCKED = False
    hub.pop.sub.load_subdirs(hub.acct, recurse=True)


def cli(hub):
    hub.pop.config.load(["acct"], cli="acct")
    key = hub.OPT["acct"]["acct_key"]
    fn = hub.OPT["acct"]["acct_file"]
    ret = hub.acct.enc.encrypt(fn, key)
    print(ret["msg"])


def unlock(hub, fn, key):
    """
    Initialize the file read, then store the authentication data on the hub
    as hub.acct.PROFILES
    """
    hub.pop.dicts.update(hub.acct.PROFILES, hub.acct.enc.data_decrypt(fn, key))

    # If a profile has credentials for an external profile backend, unlock it now
    for backend, kwargs in hub.acct.PROFILES.get("acct-backend", {}).items():
        if hasattr(hub, f"acct.{backend}"):
            plug = getattr(hub, f"acct.{backend}")
            if "unlock" in plug._funcs:
                hub.log.trace(f"Unlocking acct backend: acct.{backend}")
                provider_data = plug.unlock(**kwargs)
                hub.pop.dicts.update(hub.acct.PROFILES, provider_data)

    if "default" in hub.acct.PROFILES:
        hub.acct.DEFAULT = hub.acct.PROFILES
    else:
        hub.acct.DEFAULT = "default"
    hub.acct.UNLOCKED = True


async def process_subs(hub, subs: Iterable[pop.hub.Sub]):
    """
    Given the named plugins and profile, execute the acct plugins to
    gather the needed profiles if data is not present for it.
    """
    if not isinstance(subs, Iterable):
        hub.log.warning(f"Unexpected type for sub: {subs.__class__}")
        subs = []

    for sub in subs:
        if sub in hub.acct.SUB_PROFILES:
            continue

        if not hasattr(hub, f"acct.{sub}"):
            hub.log.trace(f"'{sub}' does not extend acct")
            continue

        hub.acct.SUB_PROFILES[sub] = {}

        for plug in getattr(hub, f"acct.{sub}"):
            hub.log.trace(f"Gathering account information for '{sub}.{plug.__name__}'")
            if "gather" in plug._funcs:
                p_data = plug.gather() or {}
                if asyncio.iscoroutine(p_data):
                    p_data = await p_data
                if p_data:
                    hub.acct.SUB_PROFILES[sub][plug.__name__] = p_data


async def gather(
    hub, subs: Iterable[pop.hub.Sub], profile: Dict[str, Dict[str, Any]]
) -> Dict[str, Dict[str, Any]]:
    ret = data.NamespaceDict()
    if not hub.acct.UNLOCKED:
        hub.log.error("Account is locked")
        return ret

    await hub.acct.init.process_subs(subs)

    for sub, plugin in hub.acct.SUB_PROFILES.items():
        hub.log.trace(f"Reading sub profile: {sub}")
        for sub_data in plugin.values():
            hub.log.trace(f"Reading plugin profile: {sub}")
            if profile in sub_data:
                hub.log.trace(f"Found profile in sub_data: {profile}")
                hub.pop.dicts.update(ret, sub_data[profile])
    for sub in subs:
        hub.log.trace(f"Reading acct profile: {sub}")
        if sub in hub.acct.PROFILES:
            hub.log.trace(f"Found sub in acct.PROFILES: {profile}")
            if profile in hub.acct.PROFILES[sub]:
                hub.log.trace(f"Found account in acct.PROFILES.{sub}: {profile}")
                hub.pop.dicts.update(ret, hub.acct.PROFILES[sub][profile])

    return ret
