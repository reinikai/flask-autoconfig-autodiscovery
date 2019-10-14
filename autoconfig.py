from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import Response

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('https://yourdomain/nothing-here/')

# Typical of M$ not to pay attention to case...
@app.route('/Autodiscover/Autodiscover.xml', methods=['POST'])
@app.route('/autodiscover/autodiscover.xml', methods=['POST'])
def outlook():
    """
    Parses an Autodiscover Request:
    https://msdn.microsoft.com/en-us/library/bb204189(v=exchg.150).aspx

    and replies with a Autodiscover Response:
    https://msdn.microsoft.com/en-us/library/bb204082(v=exchg.150).aspx

    https://testconnectivity.microsoft.com/
    """

    import defusedxml.ElementTree as ElemTree

    data = request.get_data()
    # fromstring() parses XML from a string directly into an Element, which is the root element of the parsed tree.
    root = ElemTree.fromstring(data)
    username = root[0][0].text

    if not username:
        username = ''

    xml = render_template('autodiscover.xml', username=username)
    r = Response(xml, status=200, mimetype='text/xml')
    r.headers['Content-Type'] = 'text/xml; charset=utf-8'
    return r


@app.route('/mail/config-v1.1.xml')
def thunderbird():
    """
    https://wiki.mozilla.org/Thunderbird:Autoconfiguration:ConfigFileFormat
    :return:
    """
    username = request.args.get('emailaddress')

    if not username:
        username = ''

    xml = render_template('config-v1.1.xml', username=username)
    r = Response(xml, status=200, mimetype='text/xml')
    r.headers['Content-Type'] = 'text/xml; charset=utf-8'
    return r


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
