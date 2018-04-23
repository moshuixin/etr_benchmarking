"""
This File is meant to contain all the context processors required in order
to be used in the templates.
The advantage is much less imports from the different packages to
dataMapper.projectinfo variable and avoiding circular imports that end up
crashing
"""
from . import mysite_configs as configs  # Substitute your project name for mysite here!
from datetime import datetime
from . import __version__


def app_info_menu(request):
    """
    Used to bring all the app information required for context such as
    menus and further constants

    :param request: httprequest
    :return: dict : dictionary containing context required by the app
    """
    full_context = {}
    full_context.update(configs.projectInfo)
    full_context['year'] = datetime.now().year
    full_context['tool_version'] = __version__
    return {'project': full_context}
