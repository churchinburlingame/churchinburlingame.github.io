import urllib3
import json


http_client = urllib3.PoolManager()

google_form_key = '1B4bbMEs5ov76fjzFjrJaNoc2PmFCbEcTBjfh6NMZNtw'
google_form_url = f'https://spreadsheets.google.com/feeds/cells/{google_form_key}/1/public/full?alt=json'


def get_subscription_cells():
    response = http_client.request('GET', google_form_url)

    if response.status != 200:
        return []

    entries = json.loads(response.data)['feed']['entry']

    header_cols = {}
    cells = {}

    for entry in entries:
        row = int(entry['gs$cell']['row'])
        col = int(entry['gs$cell']['col'])
        val = entry['gs$cell']['inputValue']

        if row <= 1:
            header_cols[col] = val
        else:
            header_col = header_cols[col]
            if row not in cells:
                cells[row] = {}
            else:
                cells[row][header_col] = val

    return cells
