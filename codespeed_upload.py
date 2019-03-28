
import json
import urllib.error
import urllib.parse
import urllib.request


def post_data_to_server(codespeed_url, data, dry_run=False, verbose=False):
    json_data = {'json': json.dumps(data)}
    url = '%sresult/add/json/' % codespeed_url
    data_payload = urllib.parse.urlencode(json_data).encode('ascii')

    if dry_run:
        print('DRY_RUN would have sent request: ')
        print(' url: %s'%url)
        print(' data: %s'%data_payload)
        return

    if verbose:
        print('requesting url=%s  data=%s'%(url, data_payload))

    response = "None"
    try:
        f = urllib.request.urlopen(url, data_payload)
    except urllib.error.HTTPError as e:
        print(str(e))
        print(e.read())
        return
    response = f.read()
    f.close()

    print("Server (%s) response: %s\n" % (codespeed_url, response))

