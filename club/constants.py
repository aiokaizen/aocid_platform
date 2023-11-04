from django.utils.translation import gettext_lazy as _


SYSTEM_GROUPS = {
    "admin": {
        "name": _("ADMINISTRATEURS"),
    },
    "finance_manager": {
        "name": _("Gestionnaire financière")
    },
    "board_manager": {
        "name": _("Conseil d'administration")
    },
    "committee_manager": {
        "name": _("Gestionnaire de communauté")
    },
    "subscriptions_manager": {
        "name": _("Gestionnaire  d'adhésions")
    },
    "content_manager": {
        "name": _("Gestionnaire de contenue")
    },
    "technician": {
        "name": _("Technicien")
    },
}
