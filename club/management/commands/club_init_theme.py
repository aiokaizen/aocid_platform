import sys
import os
import logging

from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings


class Command(BaseCommand):
    help = """
        This command creates a default theme and activates it.
    """

    def handle(self, *args, **options):
        if "admin_interface" not in sys.modules:
            logging.error("Admin interface is not installed in this project!")
            return

        from admin_interface.models import Theme

        # Setup defaults
        default_theme_name = "AOCID default theme"


        # =========================
        #   Environnement
        # =========================
        env_name = "AOCID"
        env_color = "#E74C3C"
        env_visible_in_header = False
        env_visible_in_favicon = False


        # =========================
        #   Language
        # =========================
        language_chooser_active = True
        language_chooser_control = "default-select"
        language_chooser_display = "code"


        # =========================
        #   Logo
        # =========================
        logo_path = os.path.join(
            settings.BASE_DIR,
            "website/static/sandbox/assets/img/logo/logo.jpeg",
        )
        logo_max_width = 150
        logo_max_height = 80
        logo_color = "#FFFFFF"
        logo_visible = True

        # =========================
        #   Favicon
        # =========================
        favicon_path = os.path.join(
            settings.BASE_DIR, "website/static/sandbox/assets/img/logo/favicon.jpg"
        )


        # =========================
        #   Title
        # =========================
        title = "AOCID Admin Platform"
        title_color = "#F5DD5D"
        title_visible = False


        # =========================
        #   Header
        # =========================
        css_header_background_color = "#231D57"
        css_header_text_color = "#F5DD5D"
        css_header_link_color = "#FFFFFF"
        css_header_link_hover_color = "#FFFFCC"


        # =========================
        #   Breadcrumbs / Module headers
        # =========================
        css_module_background_color = "#231D57"
        css_module_background_selected_color = "#FFFFCC"
        css_module_text_color = "#FFFFFF"
        css_module_link_color = "#FFFFFF"
        css_module_link_selected_color = "#F5DD5D"
        css_module_link_hover_color = "#F5DD5D"
        css_module_rounded_corners = True


        # =========================
        #   Generic Links
        # =========================
        css_generic_link_color = "#231D57"
        css_generic_link_hover_color = "#B3A244"
        css_generic_link_active_color = "#3643A8"


        # =========================
        #   Save Buttons
        # =========================
        css_save_button_background_color = "#231D57"
        css_save_button_background_hover_color = "#2B3585"
        css_save_button_text_color = "#F5DD5D"


        # =========================
        #   Delete Buttons
        # =========================
        css_delete_button_background_color = "#BA2121"
        css_delete_button_background_hover_color = "#A41515"
        css_delete_button_text_color = "#FFFFFF"


        # =========================
        #   Navigation Bar
        # =========================
        foldable_apps = True


        # =========================
        #   Related model
        # =========================
        related_modal_active = True
        related_modal_background_color = "#231D57"
        related_modal_background_opacity = "0.2"
        related_modal_rounded_corners = True
        related_modal_close_button_visible = True


        # =========================
        #   Form Controls
        # =========================
        form_submit_sticky = True
        form_pagination_sticky = False


        # =========================
        #   List Filter
        # =========================
        list_filter_highlight = True
        list_filter_dropdown = True
        list_filter_sticky = True
        list_filter_removal_links = False


        # =========================
        #   Change form
        # =========================
        show_fieldsets_as_tabs = False
        show_inlines_as_tabs = True


        # =========================
        #   Inlines
        # =========================
        collapsible_stacked_inlines = False
        collapsible_stacked_inlines_collapsed = True
        collapsible_tabular_inlines = False
        collapsible_tabular_inlines_collapsed = True

        # =========================
        #   Recent actions
        # =========================
        recent_actions_visible = True


        try:
            theme = Theme.objects.get(name=default_theme_name)
            theme.name = default_theme_name
            theme.title = title
            theme.title_visible = title_visible
            theme.logo_max_width = logo_max_width
            theme.logo_max_height = logo_max_height
            theme.logo_visible = logo_visible
            theme.env_name = env_name
            theme.env_visible_in_header = env_visible_in_header
            theme.env_visible_in_favicon = env_visible_in_favicon
            theme.language_chooser_active = language_chooser_active
            theme.language_chooser_control = language_chooser_control
            theme.language_chooser_display = language_chooser_display
            theme.css_module_rounded_corners = css_module_rounded_corners
            theme.related_modal_active = related_modal_active
            theme.related_modal_rounded_corners = related_modal_rounded_corners
            theme.related_modal_close_button_visible = (
                related_modal_close_button_visible
            )
            theme.list_filter_highlight = list_filter_highlight
            theme.list_filter_dropdown = list_filter_dropdown
            theme.list_filter_sticky = list_filter_sticky
            theme.list_filter_removal_links = list_filter_removal_links
            theme.foldable_apps = foldable_apps
            theme.show_fieldsets_as_tabs = show_fieldsets_as_tabs
            theme.show_inlines_as_tabs = show_inlines_as_tabs
            theme.recent_actions_visible = recent_actions_visible
            theme.form_submit_sticky = form_submit_sticky
            theme.form_pagination_sticky = form_pagination_sticky
            theme.title_color = title_color
            theme.logo_color = logo_color
            theme.env_color = env_color
            theme.css_header_background_color = css_header_background_color
            theme.css_header_text_color = css_header_text_color
            theme.css_header_link_color = css_header_link_color
            theme.css_header_link_hover_color = css_header_link_hover_color
            theme.css_module_background_color = css_module_background_color
            theme.css_module_background_selected_color = (
                css_module_background_selected_color
            )
            theme.css_module_text_color = css_module_text_color
            theme.css_module_link_color = css_module_link_color
            theme.css_module_link_selected_color = css_module_link_selected_color
            theme.css_module_link_hover_color = css_module_link_hover_color
            theme.css_generic_link_color = css_generic_link_color
            theme.css_generic_link_hover_color = css_generic_link_hover_color
            theme.css_generic_link_active_color = css_generic_link_active_color
            theme.css_save_button_background_color = css_save_button_background_color
            theme.css_save_button_background_hover_color = (
                css_save_button_background_hover_color
            )
            theme.css_save_button_text_color = css_save_button_text_color
            theme.css_delete_button_background_color = (
                css_delete_button_background_color
            )
            theme.css_delete_button_background_hover_color = (
                css_delete_button_background_hover_color
            )
            theme.css_delete_button_text_color = css_delete_button_text_color
            theme.related_modal_background_color = related_modal_background_color
            theme.related_modal_background_opacity = related_modal_background_opacity
            theme.save()
            theme.logo.delete()
            theme.set_active()
            theme.favicon.delete()
            with open(logo_path, "rb") as logo_file:
                theme.logo.save("logo.png", File(logo_file))
            with open(favicon_path, "rb") as favicon:
                theme.favicon.save("favicon.png", File(favicon))
        except Theme.DoesNotExist:
            theme = Theme(
                name=default_theme_name,
                title=title,
                title_visible=title_visible,
                logo_max_width=logo_max_width,
                logo_max_height=logo_max_height,
                logo_visible=logo_visible,
                env_name=env_name,
                env_visible_in_header=env_visible_in_header,
                env_visible_in_favicon=env_visible_in_favicon,
                language_chooser_active=language_chooser_active,
                language_chooser_control=language_chooser_control,
                language_chooser_display=language_chooser_display,
                css_module_rounded_corners=css_module_rounded_corners,
                related_modal_active=related_modal_active,
                related_modal_rounded_corners=related_modal_rounded_corners,
                related_modal_close_button_visible=related_modal_close_button_visible,
                list_filter_highlight=list_filter_highlight,
                list_filter_dropdown=list_filter_dropdown,
                list_filter_sticky=list_filter_sticky,
                list_filter_removal_links=list_filter_removal_links,
                foldable_apps=foldable_apps,
                show_fieldsets_as_tabs=show_fieldsets_as_tabs,
                show_inlines_as_tabs=show_inlines_as_tabs,
                recent_actions_visible=recent_actions_visible,
                form_submit_sticky=form_submit_sticky,
                form_pagination_sticky=form_pagination_sticky,
                # Default colors
                title_color=title_color,
                logo_color=logo_color,
                env_color=env_color,
                # Header colors
                css_header_background_color=css_header_background_color,
                css_header_text_color=css_header_text_color,
                css_header_link_color=css_header_link_color,
                css_header_link_hover_color=css_header_link_hover_color,
                # Breadcrumbs colors
                css_module_background_color=css_module_background_color,
                css_module_background_selected_color=css_module_background_selected_color,
                css_module_text_color=css_module_text_color,
                css_module_link_color=css_module_link_color,
                css_module_link_selected_color=css_module_link_selected_color,
                css_module_link_hover_color=css_module_link_hover_color,
                css_generic_link_color=css_generic_link_color,
                css_generic_link_hover_color=css_generic_link_hover_color,
                css_generic_link_active_color=css_generic_link_active_color,
                css_save_button_background_color=css_save_button_background_color,
                css_save_button_background_hover_color=css_save_button_background_hover_color,
                css_save_button_text_color=css_save_button_text_color,
                css_delete_button_background_color=css_delete_button_background_color,
                css_delete_button_background_hover_color=css_delete_button_background_hover_color,
                css_delete_button_text_color=css_delete_button_text_color,
                related_modal_background_color=related_modal_background_color,
                related_modal_background_opacity=related_modal_background_opacity,
            )

            theme.save()
            theme.set_active()

            with open(logo_path, "rb") as logo_file:
                theme.logo.save("logo.png", File(logo_file))
            with open(favicon_path, "rb") as favicon:
                theme.favicon.save("favicon.png", File(favicon))
            logging.info("The default theme has been initialized successfully.")
