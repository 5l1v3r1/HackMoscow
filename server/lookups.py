from ajax_select import register, LookupChannel
from .models import Tag

@register('tags')
class TagsLookup(LookupChannel):

    model = Tag

    def get_query(self, q, request):
        v = self.model.objects.filter(tagname__icontains=q.capitalize()).order_by('tagname')[:50]
        if len(v) == 0:
            v = self.model.objects.all().order_by('tagname')[:50]
        return v

    def format_match(self, item):
        return item.tagname

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.tagname

    def check_auth(self, request):
        return request.user.is_authenticated()