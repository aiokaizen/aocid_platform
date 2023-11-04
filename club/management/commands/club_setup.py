from django.utils.translation import gettext_lazy as _
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.apps import apps
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import (
    User, Group, Permission
)

from club.constants import SYSTEM_GROUPS
from club.models import Club


base_permissions = [
    # "change_current_user",
    # "list_notification",
    # "view_notification",
    # "list_conversation",
    # "view_conversation",
    # "list_chatmessage",
    # "view_chatmessage",
]


def filter_permissions(
    model_in=None,
    codename_in=None,
    exclude_models=None,
    exclude_codenames=None,
):
    exclude_models = exclude_models or []
    exclude_codenames = exclude_codenames or []

    filters = Q()

    if model_in is not None:
        filters |= Q(content_type__model__in=model_in)
    if codename_in is not None:
        filters |= Q(codename__in=[*codename_in])

    perms = Permission.objects.all()
    if filters:
        perms = perms.filter(
            filters | Q(codename__in=[*base_permissions])
        )

    perms = perms.exclude(
        Q(content_type__model__in=exclude_models) | Q(codename__in=exclude_codenames)
    )

    return perms


class Command(BaseCommand):
    help = """
        This command adds some demo content to invoice app.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-perms",
            action="store_true",
            help="If this argument is set, all permissions will be removed and recreated (This action is irreversible!!).",
        )

    def handle(self, *args, **options):

        # Create default Club if it does not exist
        club = Club.objects.first()
        if not club:
            club = Club(
                name="AOCID"
            )
            club.save()

        # Reset permissions:
        reset_perms = options["reset_perms"]
        if reset_perms:
            print("Resetting permissions...")
            Permission.objects.all().delete()

            # Create permissions
            for model in apps.get_models():
                opts = model._meta
                content_type = ContentType.objects.get_for_model(model)

                # Create default permissions (From Meta.default_permissions)
                for perm in opts.default_permissions:
                    codename = f"{perm}_{opts.model_name}"
                    name = f"Can {perm} {opts.verbose_name}"

                    if "club" in codename:
                        print("codename:", codename)
                        print("name:", name)

                    Permission.objects.get_or_create(
                        codename=codename,
                        content_type=content_type,
                        defaults={"name": name},
                    )

                # Create other permissions (From Meta.permissions)
                for perm in opts.permissions:
                    codename = perm[0]
                    name = perm[1]

                    Permission.objects.get_or_create(
                        codename=codename,
                        content_type=content_type,
                        defaults={"name": name},
                    )

        # Create default groups
        groups = SYSTEM_GROUPS

        group_admin, _created = Group.objects.get_or_create(
            name=groups["admin"]["name"],
        )
        group_board_manager, _created = Group.objects.get_or_create(
            name=groups["board_manager"]["name"],
        )
        group_finance_manager, _created = Group.objects.get_or_create(
            name=groups["finance_manager"]["name"],
        )
        group_subscriptions_manager, _created = Group.objects.get_or_create(
            name=groups["subscriptions_manager"]["name"],
        )
        group_content_manager, _created = Group.objects.get_or_create(
            name=groups["content_manager"]["name"],
        )
        group_committee_manager, _created = Group.objects.get_or_create(
            name=groups["committee_manager"]["name"],
        )
        group_technician, _created = Group.objects.get_or_create(
            name=groups["technician"]["name"],
        )

        admin_perms = filter_permissions(
            # All permissions
            exclude_models=[
                "counter",
                "newsletter",
            ]
        )
        group_admin.permissions.set(admin_perms)

        board_manager_perms = filter_permissions(
            model_in=[
                "club",
                "member",
                "committeemembers",
                "committee",
                "player",
            ],
            exclude_codenames=[
                "add_club",
                "delete_club"
            ]
        )
        group_board_manager.permissions.set(board_manager_perms)

        finance_manager_perms = filter_permissions(
            model_in=[
                "insurance",
                "payment",
                "expense"
                "club",
            ],
            exclude_codenames=[
                "add_club",
                "delete_club"
            ]
        )
        group_finance_manager.permissions.set(finance_manager_perms)

        subscriptions_manager_perms = filter_permissions(
            model_in=[
                "plan",
                "subscription"
                "family",
                "guardian",
                "player"
            ],
        )
        group_subscriptions_manager.permissions.set(subscriptions_manager_perms)

        committee_manager_perms = filter_permissions(
            model_in=[
                "committeemembers",
                "committee"
            ],
        )
        group_committee_manager.permissions.set(committee_manager_perms)

        content_manager_perms = filter_permissions(
            model_in=[
                "book",
                "album",
                "media",

                "author",
                "category",
                "tag",
                "post",
                "comment",

                "slide",
                "button",
                # "counter",
                "message",
                # "newsLetter",
            ],
        )
        group_content_manager.permissions.set(content_manager_perms)

        technician_perms = filter_permissions(
            model_in=[
                "theme",
                "user",
                "group"
            ],
        )
        group_technician.permissions.set(technician_perms)

        # Users
        """
            + Hicham Lemcherfi
                - l.hicham
                - hichamadm_pass

            + Ferdaous Faris
                - f.ferdaous
                - ferdaousadm_pass

            + AbdErrahim Ait Ouaarab
                - a.abderrahim
                - abderrahimadmin_pass

            + Youssef Oubouali
                - o.youssef
                - youssefadm_pass
        """
