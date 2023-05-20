from urllib.parse import parse_qsl
from http import cookies


def parse(query: str) -> dict:
    params = {}
    if "?" in query:
        query_string = query.split('?')[1]
        params = dict(parse_qsl(query_string))
    elif "#" in query:
        query_string = query.split('#')[1]
        params = dict(parse_qsl(query_string))
    return params


if __name__ == '__main__':
    assert parse('https://example.com/path/to/page?name=ferret&color=purple') == {'name': 'ferret', 'color': 'purple'}
    assert parse('https://example.com/path/to/page?name=ferret&color=purple&') == {'name': 'ferret', 'color': 'purple'}
    assert parse('http://example.com/') == {}
    assert parse('http://example.com/?') == {}
    assert parse('http://example.com/?name=Dima') == {'name': 'Dima'}
    assert parse('https://rozetka.com.ua/apple/c4627486/#search_text=apple') == {'search_text': 'apple'}
    assert parse('https://rozetka.com.ua/apple/c4627486/?search_text=apple') == {'search_text': 'apple'}
    assert parse('https://rozetka.com.ua/apple/c4627486/?search_text=book') == {'search_text': 'book'}
    assert parse('https://rozetka.com.ua/apple/c4627486/?search_text=pig+book') == {'search_text': 'pig book'}
    assert parse('https://rozetka.com.ua/apple/c4627486/#') == {}
    assert parse('https://ideyka.com.ua/all-products?keyword=liltl+pony') == {"keyword": "liltl pony"}
    assert parse('https://ideyka.com.ua/all-products#keyword=liltl+pony') == {"keyword": "liltl pony"}
    assert parse('https://ideyka.com.ua/all-products?keyword=liltl+pony&capture=gift&') == {"keyword": "liltl pony", "capture": "gift"}
    assert parse('https://www.olx.ro/auto-masini-moto-ambarcatiuni/ambarcatiuni/?currency=EUR') == {'currency': 'EUR'}
    assert parse('https://www.olx.ro/d/oferta/organizator-papiote-ata-de-cusut-IDhemK9.html?reason'
                 '=extended_search_no_results_last_resort') == {'reason': 'extended_search_no_results_last_resort'}


def parse_cookie(query: str) -> dict:
    simple_cookie = cookies.SimpleCookie()
    simple_cookie.load(query)
    return {key: simple_cookie[key].value for key in simple_cookie}


if __name__ == '__main__':
    assert parse_cookie('name=Dima;') == {'name': 'Dima'}
    assert parse_cookie('') == {}
    assert parse_cookie('name=Dima;age=28;') == {'name': 'Dima', 'age': '28'}
    assert parse_cookie('name=Dima=User;age=28;') == {'name': 'Dima=User', 'age': '28'}
    assert parse_cookie('name=Dima;') == {'name': 'Dima'}
    assert parse_cookie('name=Dima;;') == {'name': 'Dima'}
    assert parse_cookie('name=Dima;age=28;name=Dima;age=28;') == {'name': 'Dima', 'age': '28', 'name': 'Dima', 'age': '28'}
    assert parse_cookie('name=Dima=User;age=28=28;') == {'name': 'Dima=User', 'age': '28=28'}
    assert parse_cookie('name=Dima=28;') == {'name': 'Dima=28'}
    assert parse_cookie('28=28') == {"28": "28"}
    assert parse_cookie('parse_parse=cookie;age=28;') == {'parse_parse': 'cookie', 'age': '28'}
    assert parse_cookie('parse_parse=Dima=User;age=28;') == {'parse_parse': 'Dima=User', 'age': '28'}
    assert parse_cookie('name=Dima;age=parse_parse;') == {'name': 'Dima', 'age': 'parse_parse'}
    assert parse_cookie('name=query=User;age=value;') == {'name': 'query=User', 'age': 'value'}
