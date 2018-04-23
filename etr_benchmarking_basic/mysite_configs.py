"""
General configuration options of the tool. It controles mostly visuals
and the content of the menu.
"""

APP_LOGO_SVG = None
"""
Defines the logo of your application in svg format. 
The svg file needs to be located in a static folder of your project.

Example:
APP_LOGO_SVG = 'Evaluator/images/capricorn_1.svg'

In the html file, the src for the <img> html tag will be build like this:

src="{% static project.app_logo_svg %}"
"""

APP_LOGO = 'fa fa-file-text'
"""
Defines the logo of your application if you do not have or want to use
and svg. Must be a class of font awesome.
For a list, see http://fontawesome.io/icons/.

Example:
APP_LOGO = 'fa fa-globe'
"""

SHOW_BRANDING = True
"""
Defines if the EY branding data has to be shown in the templates or not.
"""

userMenu = False
"""
 Each element of the menu is composed by one or more sub elements with the
 same basic structure. At the moment, each level is compatible with up to 2
 sub levels (the complete structure consist of maximum tree levels). Each
 element is a dictionary the same keys that define their actions

 1 level
   2 level
     3 level

The parameters for each level are:

* 'label': str: string to be shown in the template. This is what the user
  will see in the frontend.
* 'call': tuple : tuple with the form (string, value), where string is the
  app:namespace you call, and value an optional parameter to pass with the
  link. For nested elements, the call must be empty: () or [].
* 'permission': str/Iterable/None: as striong it should be a permission string
  of the form <app>.<permission>. It can also be an iterable (list/tuple) 
  of such strings or even None to requiere no permission,. In this case the
  element will be allways visible.
  does not require permissions or If no permission is requireed, none must be set.
* 'fontAwesomeIcon': str: class of the font awesome that will be used to
  shown an icon.
* 'subMenu': list or False : it can be False to declare no sub menu,
  or a list of sub items where each of them has the same structure shown in
  the following example.

Basic level:
  .. code-block:: rest

       {  # 1st Level
         'label': 'Super menu',
         'call': ['home'], # ['home', 1] , 1 would be an optional parameter
         'permission': ('app1.permission1', 'app2.permission1', ),# None if not required
         'fontAwesomeIcon': 'fa fa-archive',
         'subMenu': False
      },

"""

adminMenu = []
""" Admin menu, uses the Same structure as user menu """

HTML_MENU = [
    'etr_benchmarking/menu/menu.html',
]

"""
If you do not want to code your menu in here (i.e. in python)
but want to include a menu coded in html, specify here the the paths
to the html templates that includes the menus as a list.

Example: 

  .. code-block:: html

     HTML_MENU = ['ttaa_examples/partials/menu.html']
"""

# Main project info dictionary.
# Holds information relative to the project that required
# to be passed to the views
# every time such as name and menu
projectInfo = {
    'projectInfo': {
        'name': 'Predict ETR',
        'name_long': 'Predict ETR',

    },
    'showBranding': SHOW_BRANDING,
    'app_logo_svg': APP_LOGO_SVG,
    'app_logo': APP_LOGO,
    'userMenu': userMenu,
    'adminMenu': adminMenu,
    'html_menu': HTML_MENU
}
""" Contains the project information required by the context NO SETTINGS!"""
