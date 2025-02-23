import re
from bs4 import BeautifulSoup
from common import endoflife

URL = "https://access.redhat.com/articles/3078"
# https://regex101.com/r/877ibq/1
regex = r"RHEL (?P<major>\d)(\. ?(?P<minor>\d+))?(( Update (?P<minor2>\d))| GA)?"

print("::group::rhel")
response = endoflife.fetch_url(URL)
soup = BeautifulSoup(response, features="html5lib")

versions = {}
for tr in soup.findAll("tr"):
    td_list = tr.findAll("td")
    if len(td_list) > 0:
        version = td_list[0].get_text()
        m = re.match(regex, version.strip()).groupdict()
        version = m["major"]
        if m["minor"]:
            version += ".%s" % m["minor"]
        if m["minor2"]:
            version += ".%s" % m["minor2"]
        date = td_list[1].get_text()
        versions[version] = date
        print(f"{version}: {date}")

endoflife.write_releases('redhat', versions)
print("::endgroup::")
