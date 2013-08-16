import os
from logging import getLogger
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
from django_diazo.models import Theme
from django_diazo.theme import registry


class Command(BaseCommand):
    help = _('Synchronize database with built-in themes that are registered via the registry.')
    requires_model_validation = True

    def handle(self, *args, **options):
        logger = getLogger('django_diazo')
        themes = dict([(t.slug, t) for t in Theme.objects.filter(builtin=True)])
        # Add/modify themes
        for theme in registry.get_themes():
            if theme.slug in themes:
                themes.pop(theme.slug)
            else:
                Theme.objects.create(
                    name=theme.name,
                    slug=theme.slug,
                    path=os.path.join(settings.STATIC_ROOT, theme.slug),
                    url=settings.STATIC_URL + theme.slug,
                    builtin=True
                )
                logger.info('Added new theme with name \'{0}\'.'.format(theme.name))
        # Delete themes
        for theme in themes:
            theme.delete()
        logger.info('Done syncing built-in themes.')