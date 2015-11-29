import urllib.request


def configure_domain_password(credentials_dict):
    """
    Configures urllib.request to use the provided credentials on the provided domains.

    Parameters
    ----------
    credentials_dict : Dict[str, (str, str)]
        Dictionary that maps domain URLs to a tuple of username and password each.
    """
    for domain, credentials in credentials_dict.items():
        p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        p.add_password(None, domain, *credentials)
        handler = urllib.request.HTTPBasicAuthHandler(p)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
