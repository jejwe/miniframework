import base64
import mimetypes
import random
import string
import os
import html
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import urllib.parse
# For more advanced features, consider adding 'requests' or 'Pillow' to requirements.txt

# --- Functions from App/Function/Extend.func.php ---

def test_func():
    """
    Equivalent to testFunc() from App/Function/Extend.func.php
    Original: echo 'Test Function.';
    """
    print('Test Function.')

# --- Functions from MiniFramework/Function/Global.func.php ---

def get_client_ip():
    """
    Gets the client IP address.
    CherryPy provides this via cherrypy.request.remote.ip or headers.
    This function provides a more basic interpretation if not in a CherryPy context,
    or can be adapted to use cherrypy.request if available.
    For direct CherryPy use:
    ip = cherrypy.request.headers.get('X-Forwarded-For', cherrypy.request.remote.ip)
    """
    # This is a simplified version. In a web context (e.g., Flask, Django, CherryPy),
    # the framework usually provides a safer way to get the remote IP,
    # especially when dealing with proxies (e.g., 'X-Forwarded-For').
    # For CherryPy: return cherrypy.request.remote.ip
    # or for X-Forwarded-For:
    # x_forwarded_for = cherrypy.request.headers.get('X-Forwarded-For')
    # if x_forwarded_for:
    #     return x_forwarded_for.split(',')[0].strip()
    # return cherrypy.request.remote.ip

    # Placeholder if used outside a web request context or for basic simulation:
    # This part is non-trivial to replicate exactly without a request context.
    # The PHP version checks various $_SERVER variables.
    # A full translation would require passing a dictionary like os.environ
    # or specific header values.
    # For now, returning a placeholder or relying on framework features is best.
    # In CherryPy: cherrypy.request.remote.ip or cherrypy.request.headers.get('X-Forwarded-For')
    return "127.0.0.1" # Placeholder

def chg_array_key(list_of_dicts, key_field):
    """
    Changes a list of dictionaries to be keyed by a specific field's value.
    Equivalent to chgArrayKey().
    Example: [{id:1, name:'a'}, {id:2, name:'b'}], 'id' -> {1:{id:1, name:'a'}, 2:{id:2, name:'b'}}
    """
    if not isinstance(list_of_dicts, list):
        return False # Or raise TypeError
    return {item[key_field]: item for item in list_of_dicts if key_field in item}

def get_random_string(length=8):
    """
    Generates a random alphanumeric string of a given length.
    Equivalent to getRandomString().
    For cryptographically secure random strings, consider using 'secrets' module.
    """
    if not isinstance(length, int) or length <= 0:
        length = 8
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def base64_encode_image(image_filepath):
    """
    Reads an image file and returns its base64 encoded version with a data URI prefix.
    Equivalent to base64EncodeImage().
    Uses mimetypes to guess image type; Pillow would be more robust for validation.
    """
    if not os.path.isfile(image_filepath):
        return False
    try:
        with open(image_filepath, 'rb') as f:
            image_data = f.read()
        
        mime_type, _ = mimetypes.guess_type(image_filepath)
        if not mime_type or not mime_type.startswith('image/'):
            # Fallback or raise error if not a known image mime type
            # For more robust check, Pillow: from PIL import Image; Image.open(filepath).format
            return False # Or try a default like 'image/unknown'

        base64_encoded_data = base64.b64encode(image_data).decode('utf-8')
        return f"data:{mime_type};base64,{base64_encoded_data}" # chunk_split is not standard in Python base64 data URIs
    except Exception:
        return False

def push_json_data(data, push=True):
    """
    Encodes data to JSON. If push is True, it would typically involve sending
    HTTP response (handled by CherryPy controllers). Here, it just returns the string
    or prints if push is True (for CLI testing).
    Equivalent to pushJson().
    CherryPy's @cherrypy.tools.json_out() is preferred in controllers.
    """
    json_string = json.dumps(data, ensure_ascii=False) # JSON_UNESCAPED_UNICODE equivalent
    if push:
        # In a web context, this would be:
        # cherrypy.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        # return json_string (or let json_out tool handle it)
        # die() is not Pythonic.
        print(json_string) # For CLI testing
    return json_string

def is_date_valid(date_string, formats=('Y-m-d', 'Y/m/d')):
    """
    Validates if a string is a valid date according to given formats.
    Equivalent to isDate().
    Note: Python's strptime format codes differ from PHP's date().
    E.g., PHP 'Y-m-d' is Python '%Y-%m-%d'.
    """
    py_formats = [fmt.replace('Y', '%Y').replace('m', '%m').replace('d', '%d').replace('H', '%H').replace('i', '%M').replace('s', '%S') for fmt in formats]
    try:
        dt_timestamp = float(date_string) # Check if it's a numeric timestamp first
        # This part of PHP's strtotime is tricky to replicate perfectly for all string dates
        # For numeric timestamps, PHP strtotime returns the number.
        # If date_string is numeric, check if it's a valid timestamp
        datetime.fromtimestamp(dt_timestamp) # Will raise error if invalid
        # Then check if formatting it back matches one of the original formats (if date_string was supposed to be already formatted)
        # This part of the PHP logic is a bit circular.
        # A direct numeric string is unlikely to match 'Y-m-d' format.
        # PHP's strtotime is very flexible. Python is stricter.
        # Focusing on the format matching part:
    except ValueError: # Not a simple numeric timestamp, try parsing with formats
        pass

    for fmt_py, fmt_php in zip(py_formats, formats):
        try:
            dt_obj = datetime.strptime(str(date_string), fmt_py)
            # Additionally, PHP's check re-formats the timestamp.
            # This ensures that '2023-02-30' (invalid day) is caught if strptime is lenient
            # or if the timestamp produced by strtotime was for a corrected date.
            # Python's strptime is usually strict.
            if dt_obj.strftime(fmt_py) == str(date_string):
                 return True
        except ValueError:
            continue
    return False


def dump_var(var, label=None, echo=True):
    """
    A simple var_dump equivalent for debugging.
    Equivalent to dump().
    For CLI, uses pprint. For web, basic pre-formatted HTML.
    """
    import pprint
    output = pprint.pformat(var, indent=2)
    
    is_cli = not hasattr(cherrypy.request, 'config') # Simplified check for CLI/web context

    if is_cli:
        if label:
            full_output = f"\n{label}\n{output}\n"
        else:
            full_output = f"\n{output}\n"
    else: # Web context
        if label:
            full_output = f"<pre>\n<strong>{html.escape(str(label))}</strong>\n{html.escape(output)}\n</pre>\n"
        else:
            full_output = f"<pre>\n{html.escape(output)}\n</pre>\n"
            
    if echo:
        print(full_output)
    return full_output

def _parse_data_to_xml_recursive(builder, data, item_name, id_name):
    if isinstance(data, dict):
        for key, val in data.items():
            element = ET.SubElement(builder, str(key))
            _parse_data_to_xml_recursive(element, val, item_name, id_name)
    elif isinstance(data, list):
        for i, val in enumerate(data):
            attrs = {id_name: str(i)} if id_name else {}
            element = ET.SubElement(builder, item_name, attrib=attrs)
            _parse_data_to_xml_recursive(element, val, item_name, id_name)
    else:
        builder.text = str(data)

def push_xml_data(data, push=True, indent=False, root_name='data', item_name='item', id_name='id', encoding='utf-8'):
    """
    Converts data to XML string.
    Equivalent to pushXml() and parseDataToXml().
    CherryPy controllers should return the XML string and set Content-Type.
    """
    root_element = ET.Element(root_name)
    _parse_data_to_xml_recursive(root_element, data, item_name, id_name)
    
    if indent:
        ET.indent(root_element, space="  ", level=0)
        
    xml_string = ET.tostring(root_element, encoding=encoding, xml_declaration=True).decode(encoding)
    
    if push:
        # In CherryPy:
        # cherrypy.response.headers['Content-Type'] = 'application/xml; charset=' + encoding
        # return xml_string
        print(xml_string) # For CLI testing
    return xml_string

def is_image_valid(filepath):
    """
    Checks if a file is a valid image.
    Equivalent to isImage().
    Uses mimetypes, but Pillow (PIL) is more robust for actual image format validation.
    """
    if not os.path.isfile(filepath):
        return False
    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type and mime_type.startswith('image/'):
        # For a deeper check like PHP's imagecreatefromjpeg etc., Pillow would be needed:
        # try:
        #     from PIL import Image
        #     img = Image.open(filepath)
        #     img.verify() # Verifies headers, doesn't fully decode
        #     return True
        # except ImportError:
        #     # Pillow not installed, rely on mimetype
        #     return True
        # except Exception:
        #     return False
        return True # Mimetype check is basic
    return False

def get_string_len_mixed(text):
    """
    Calculates string length considering multibyte characters (PHP's specific logic).
    Equivalent to getStringLen(). Python's len() is usually sufficient.
    PHP: (strlen($string) + mb_strlen($string, 'UTF8')) / 2
    This seems like an attempt to average byte length and char length, unusual.
    Python's len(str) gives character count directly.
    """
    # Replicating the exact PHP logic:
    # utf8_char_count = len(text)
    # byte_count = len(text.encode('utf-8')) # This is what strlen would do on UTF-8
    # return (byte_count + utf8_char_count) / 2
    # However, standard Python len(text) is typically what's needed.
    return len(text) # Standard Python way

def serve_file_download(filepath, custom_filename=None):
    """
    Serves a file for browser download.
    Equivalent to browserDownload().
    In CherryPy, use cherrypy.lib.static.serve_file().
    This is a conceptual translation; actual implementation is framework-dependent.
    """
    if not os.path.isfile(filepath):
        return False # Or raise error
    
    # In CherryPy:
    # from cherrypy.lib.static import serve_file
    # download_name = custom_filename if custom_filename else os.path.basename(filepath)
    # return serve_file(filepath, "application/x-download", "attachment", name=download_name)
    
    print(f"Conceptual download: File '{filepath}', Download as: '{custom_filename or os.path.basename(filepath)}'")
    return True # Placeholder

def get_file_ext_name(filename):
    """
    Gets file extension.
    Equivalent to getFileExtName().
    """
    if '.' not in filename:
        return '' # Or handle as per original if it expected specific behavior
    return filename.split('.')[-1]
    # A more robust way:
    # name, ext = os.path.splitext(filename)
    # return ext[1:] if ext else ''

def get_hash_crc32_mod(text, length=4):
    """
    Calculates CRC32 hash and then modulo.
    Equivalent to getHash().
    """
    import binascii
    h = binascii.crc32(text.encode('utf-8')) & 0xffffffff # Ensure unsigned
    if length == 0: return 0 # Avoid division by zero, though PHP fmod might handle it differently
    return h % length

def html_encode_string(text, double_encode=True):
    """
    HTML encodes a string.
    Equivalent to htmlEncode().
    Python's html.escape() by default does not double-encode.
    To replicate ENT_QUOTES, all of ', ", <, > need to be escaped.
    html.escape() escapes &, <, >. For quotes, manual replacement or a library like markupsafe might be needed
    if exact PHP behavior for ENT_QUOTES | ENT_SUBSTITUTE is required.
    """
    # html.escape() handles &, <, >.
    # For quotes, we might need to add them.
    # PHP's ENT_SUBSTITUTE replaces invalid code unit sequences with a Unicode Replacement Character.
    # Python's string handling usually manages encoding/decoding issues at boundaries.
    # A simple html.escape is often sufficient for basic XSS prevention.
    return html.escape(text, quote=True) # quote=True escapes ", ' as well.

def is_index_array(data):
    """
    Checks if a list/dict is numerically indexed consecutively from 0.
    Equivalent to isIndexArray().
    """
    if not isinstance(data, (list, dict)):
        return False
    if isinstance(data, list): # Python lists are always indexed like this
        return True 
    # For dicts:
    keys = list(data.keys())
    for i, k in enumerate(keys):
        if not isinstance(k, int) or k != i:
            return False
    return True

def is_valid_timestamp(timestamp_val):
    """
    Checks if a value is a valid Unix timestamp.
    Equivalent to isTimestamp().
    """
    try:
        ts = int(timestamp_val)
        datetime.fromtimestamp(ts)
        # PHP's check also ensures that formatting the timestamp back gives the same date,
        # which is a bit redundant if fromtimestamp() succeeds.
        # PHP: strtotime(date('Y-m-d H:i:s', intval($timestamp))) == $timestamp
        # This is to catch cases where $timestamp might be "123.45" or out of typical int range
        # but still parsable by strtotime. Python's int() and fromtimestamp() are stricter.
        return True
    except (ValueError, TypeError, OverflowError):
        return False

def array_to_url_params(data_dict, type_val=1):
    """
    Converts a dictionary to URL GET parameters or path-like segments.
    Equivalent to arrayToUrlParams().
    """
    if not isinstance(data_dict, dict):
        return ""
        
    if type_val == 1: # Standard query string: a=1&b=2
        return urllib.parse.urlencode({k: v for k, v in data_dict.items() if not isinstance(v, (list, dict))})
    
    # Path-like segments: a/1/b/2 or a_1_b_2 or a-1-b-2
    join_symbol, split_symbol = '', ''
    if type_val == 2: join_symbol = split_symbol = '/'
    elif type_val == 3: join_symbol = split_symbol = '_'
    elif type_val == 4: join_symbol = split_symbol = '-'
    else: return "" # Unknown type

    parts = []
    for key, val in data_dict.items():
        if isinstance(val, (list, dict)): # PHP version skips arrays/objects
            continue
        parts.append(f"{key}{join_symbol}{val}")
    return split_symbol.join(parts)

def get_remote_file_size(url):
    """
    Gets remote file size via HTTP HEAD request.
    Equivalent to getRemoteFileSize().
    Requires 'requests' library for a robust solution, or use urllib.
    """
    try:
        # Using urllib (standard library)
        with urllib.request.urlopen(url, timeout=5) as response: # Add timeout
            # In Python 3, get_headers() is on the response object.
            # PHP's get_headers makes a GET by default unless context options specify HEAD.
            # To truly mimic, a HEAD request is better.
            # For simplicity, this uses urlopen which makes a GET.
            meta = response.info()
            return int(meta.get('Content-Length', 0))
    except Exception: # Broad exception for network errors, timeouts, etc.
        return 0
    # Using requests library (more user-friendly, needs to be installed):
    # import requests
    # try:
    #     response = requests.head(url, timeout=5)
    #     response.raise_for_status() # Raise an exception for bad status codes
    #     return int(response.headers.get('content-length', 0))
    # except requests.exceptions.RequestException:
    #     return 0

def check_sql_inject_keywords(text_input):
    """
    Basic SQL injection check by looking for keywords.
    Equivalent to checkInject().
    WARNING: This is not a robust way to prevent SQL injection.
    Use parameterized queries (prepared statements) with an ORM or database connectors.
    This function is translated for completeness but its use is discouraged for security.
    """
    black_list = [
        'select', 'insert', 'update', 'delete',
        'drop', 'union', 'or', 'and', 'into', 'load_file', 'outfile', 'exec',
        '*', '/*', '*/', './', '../'
    ]
    text_input_lower = str(text_input).lower()
    for keyword in black_list:
        if keyword in text_input_lower:
            return True
    return False

if __name__ == '__main__':
    # Example usages (for testing)
    print("--- Testing utils.py ---")
    test_func()
    
    print(f"Random string: {get_random_string(10)}")
    
    my_list = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
    print(f"chg_array_key: {chg_array_key(my_list, 'id')}")

    # To test base64_encode_image, create a dummy image file 'test.png'
    # with open('test.png', 'wb') as f: f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\xf8\xff\xff?\x03\x00\x01\x00\x00\x00\x00\x00\xfe\x0f\x00\x01\x01\x01\x00\x00\x00 \xd8\x95\xc7@\x00\x00\x00\x00IEND\xaeB`\x82')
    # print(f"Base64 image: {base64_encode_image('test.png')}")
    # if os.path.exists('test.png'): os.remove('test.png')

    print(f"is_date_valid '2023-10-26': {is_date_valid('2023-10-26')}")
    print(f"is_date_valid '2023/10/26': {is_date_valid('2023/10/26', formats=['Y/m/d'])}")
    print(f"is_date_valid '2023-13-01': {is_date_valid('2023-13-01')}") # Invalid month
    
    sample_data_xml = {'user': {'id': '1', 'name': 'John Doe', 'email': 'john@example.com'}}
    print(f"push_xml_data (printed):\n{push_xml_data(sample_data_xml, push=False, indent=True)}")

    print(f"get_file_ext_name 'document.pdf': {get_file_ext_name('document.pdf')}")
    print(f"html_encode_string '<script>alert(\"hi\")</script>': {html_encode_string('<script>alert(\"hi\")</script>')}")
    
    print(f"is_index_array {{0:'a', 1:'b'}}: {is_index_array({0:'a', 1:'b'})}")
    print(f"is_index_array {{0:'a', 2:'b'}}: {is_index_array({0:'a', 2:'b'})}")
    print(f"is_index_array ['a', 'b']: {is_index_array(['a', 'b'])}")

    print(f"is_valid_timestamp '1678886400': {is_valid_timestamp('1678886400')}") # Example timestamp
    print(f"is_valid_timestamp 'not-a-timestamp': {is_valid_timestamp('not-a-timestamp')}")

    url_params = {'name': 'John Doe', 'age': 30, 'city': 'New York'}
    print(f"array_to_url_params (type 1): {array_to_url_params(url_params, 1)}")
    print(f"array_to_url_params (type 2): {array_to_url_params(url_params, 2)}")

    print(f"check_sql_inject_keywords 'select * from users': {check_sql_inject_keywords('select * from users')}")
    print(f"check_sql_inject_keywords 'safe string': {check_sql_inject_keywords('safe string')}")

```
