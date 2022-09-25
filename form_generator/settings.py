from django.conf import settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

DEFAULTS = {
    'FORM_RESPONSE_SAVE': 'form_generator.models.save_form_response',
    'FORM_EVALUATIONS': {'form_data': '{{form_data}}'},
    'MAX_UPLOAD_FILE_SIZE': 5242880,
    # 'CRISPY_ALLOWED_TEMPLATE_PACKS': 'bootstrap5',
    # 'CRISPY_TEMPLATE_PACK': 'bootstrap5',
    # 'RECAPTCHA_PUBLIC_KEY': 'test',
    # 'RECAPTCHA_PRIVATE_KEY': 'test',
    # 'SILENCED_SYSTEM_CHECKS': ['captcha.recaptcha_test_key_error']
}


IMPORT_STRINGS = [
    'FORM_RESPONSE_SAVE',
    'FORM_EVALUATIONS',
    'MAX_UPLOAD_FILE_SIZE',
    # 'RECAPTCHA_PUBLIC_KEY',
    # 'RECAPTCHA_PRIVATE_KEY',
    # 'CRISPY_ALLOWED_TEMPLATE_PACKS',
    # 'CRISPY_TEMPLATE_PACK',
    # 'SILENCED_SYSTEM_CHECKS',
]

def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for API setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)

class FormGeneratorSettings:
    def __init__(self, defaults=None, import_strings=None):
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'FORM_GENERATOR', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid Form generator setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


form_generator_settings = FormGeneratorSettings(DEFAULTS, IMPORT_STRINGS)


def reload_form_generator_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == 'FORM_GENERATOR':
        form_generator_settings.reload()


setting_changed.connect(reload_form_generator_settings)