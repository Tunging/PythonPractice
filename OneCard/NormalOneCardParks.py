import json
import requests
from bs4 import BeautifulSoup

from OneCard.Park import Park


class nNormalOneCardParks:
    html = requests.get("https://mp.weixin.qq.com/s/5X0qfT7VjqsYq163EWrq3g")
    soup = BeautifulSoup(html.text, "html.parser")
    output = ''
    parks = []

    def request_html_content(self):
        tags = self.soup.find_all("tbody", "", True)

        count = 0
        for item in tags:
            for child in item.children:
                # 掠过表头
                if not count == 0:
                    output_str = ""

                    # 掠过只有一列的
                    if len(list(child.children)) == 1:
                        continue

                    park = Park()
                    uid = child.td
                    output_str = output_str + uid.span.text + "\t"
                    park.uid = uid.span.text

                    name = uid.next_sibling
                    # bool
                    now_avaliable = name.a is not None
                    if now_avaliable:
                        if name.a.span is not None:
                            output_str = output_str + name.a.span.text + "\t"
                            park.uname = name.a.span.text
                            park.url = name.a["href"]
                        else:
                            output_str = output_str + name.a.text + "\t"
                            park.uname = name.a.text
                            park.url = name.a["href"]
                        output_str = output_str + name.a["href"] + "\t"
                    else:
                        output_str = output_str + name.span.text + "\t"
                        park.uname = name.span.text
                        output_str = output_str + " " + "\t"

                    price = name.next_sibling
                    if price.span is not None:
                        output_str = output_str + price.span.text + "\t"
                        park.uprice = price.span.text
                    else:
                        output_str = output_str + "0" + "\t"
                        park.uprice = "0"
                    right = price.next_sibling
                    # right_temp = ""
                    # for r in right.children:
                    #     right_temp = right_temp.join(r.)

                    self.output += output_str + "\n"
                    self.parks.append(park)
                count = count + 1

    def write_result_to_file(self):
        print(self.output)
        print(json.dumps(self.parks, default= lambda obj:obj.__dict__))


t = nNormalOneCardParks()
t.request_html_content()
t.write_result_to_file()
