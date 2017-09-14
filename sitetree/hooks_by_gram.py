from django.urls.resolvers import get_resolver, RegexURLResolver
import re

def get_urls_from_resolver(resolver):
    base_rex = resolver.regex.pattern
    if base_rex.startswith('^'):
        base_rex = base_rex[1:]
    
    for pattern in resolver.url_patterns:
        if isinstance(pattern, RegexURLResolver):
            for name, rex in get_urls_from_resolver(pattern):
                if resolver.app_name:
                    name = '{}:{}'.format(resolver.app_name, name)
                rex = base_rex + rex
                yield name, rex
        else:
            name = pattern.name
            if resolver.app_name:
                name = '{}:{}'.format(resolver.app_name, name)
            rex = pattern.regex.pattern
            if rex.startswith('^'):
                rex = rex[1:]
            rex = base_rex + rex
            yield name, rex


def get_all_url_patterns():
    if get_all_url_patterns._cache:
        return get_all_url_patterns._cache
    else:
        get_all_url_patterns._cache = tuple(get_urls_from_resolver(get_resolver()))
        return get_all_url_patterns._cache
get_all_url_patterns._cache = None


def reverse_soft(url):
    for name, rex in get_all_url_patterns():
        if re.match(rex, url):
            return name

def url_soft(url_name):
    for name, rex in get_all_url_patterns():
        if url_name == name:
            return rex


if __name__ == '__main__':
    for name, rex in get_all_url_patterns():
        print(name, '|', rex)
