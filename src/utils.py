from flask import jsonify, url_for

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append(url)

    links_html = "".join(["<li><a href='" + y + "'>" + y + "</a></li>" for y in links])
    return """
        <div style="text-align: center;">
        <img src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJfBzLoGcy_Ig5Y4AJCWuXPQsahhTDVj5aLGjE7IqMgD9XW8UELQ-X86-6-LiVwAM3Ye4&usqp=CAU' />
        <h1>Family Static API with Flask!!</h1>
        This is your api home, remember to specify a real endpoint path like: <p style="text-align: center;">"""+links_html+"</p></div>"
