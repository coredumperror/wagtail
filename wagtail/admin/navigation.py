from django.conf import settings

from wagtail.core.models import Collection, Page


def get_pages_with_direct_explore_permission(user):
    # Get all pages that the user has direct add/edit/publish/lock permission on
    if user.is_superuser:
        # superuser has implicit permission on the root node
        return Page.objects.filter(depth=1)
    else:
        return Page.objects.filter(
            group_permissions__group__in=user.groups.all(),
            group_permissions__permission_type__in=['add', 'edit', 'publish', 'lock']
        )


def get_collections_with_management_permission(user):
    # Get all Collections that the User has permissions for.
    qs = Collection.objects

    if user.is_superuser:
        # Superusers have permission on all Collections.
        return qs.filter(depth=1)

    return qs.filter(
        group_manage_permissions__group__in=user.groups.all(),
        group_manage_permissions__permission_type__in=['add', 'edit', 'bulk_delete']
    ).distinct()


def get_manageable_root_collection(user):
    # Get the highest common manageable ancestor for the given user. If the user
    # has no permissions over any collections, this method will return None.
    collections = get_collections_with_management_permission(user)
    if collections:
        return collections.first_common_ancestor(
            include_self=True,
            strict=True
        )
    else:
        return None


def get_explorable_root_page(user):
    # Get the highest common explorable ancestor for the given user. If the user
    # has no permissions over any pages, this method will return None.
    pages = get_pages_with_direct_explore_permission(user)
    try:
        root_page = pages.first_common_ancestor(
            include_self=True,
            strict=True
        )
    except Page.DoesNotExist:
        root_page = None

    return root_page


def get_site_for_user(user):
    root_page = get_explorable_root_page(user)
    if root_page:
        root_site = root_page.get_site()
    else:
        root_site = None
    real_site_name = None
    if root_site:
        real_site_name = root_site.site_name if root_site.site_name else root_site.hostname
    return {
        'root_page': root_page,
        'root_site': root_site,
        'site_name': real_site_name if real_site_name else settings.WAGTAIL_SITE_NAME,
    }
