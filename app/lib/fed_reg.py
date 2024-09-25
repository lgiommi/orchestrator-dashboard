import os

import requests

from flask import current_app as app

def get_user_groups(timeout: int = 60, *, access_token: str, **kwargs):
    """Retrieve all user group details and related entities."""    
    url = os.path.join(app.settings.fed_reg_url, "user_groups")
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {**kwargs}

    app.logger.debug("Request URL: {}".format(url))
    app.logger.debug("Request params: {}".format(params))

    resp = requests.get(
        url, params=params, headers=headers, timeout=timeout
    )
    resp.raise_for_status()

    return resp.json()
