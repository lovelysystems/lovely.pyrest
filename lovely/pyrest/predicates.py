# Shared Source Software
# Copyright (c) 2013, Lovely Systems GmbH


class ContentTypePredicate(object):
    """
    Predicate for matching the `Content-type` request header.
    See: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hooks.html#view-and-route-predicates
    """
    def __init__(self, val, config):
        self.val = val

    # The result of phash is not seen in output anywhere, it just informs the
    # uniqueness constraints for view configuration.
    def text(self):
        return 'content_type = %s' % (self.val,)

    phash = text

    def __call__(self, context, request):
        return request.content_type == self.val
