
import requests
import xml.etree.ElementTree as ET
from utils.xml_parser import parse_law_xml, filter_by_logic

def fetch_law_list_and_detail(query, unit):
    OC = "chetera"
    base_url = f"http://www.law.go.kr/DRF/lawSearch.do?OC={OC}&target=law&type=XML&display=20&search=2&knd=A0002&query={query}"
    res = requests.get(base_url)
    res.encoding = 'utf-8'
    result = []
    if res.status_code == 200:
        root = ET.fromstring(res.text)
        for law in root.findall("law"):
            law_id = law.findtext("법령일련번호")
            law_detail_url = f"http://www.law.go.kr/DRF/lawService.do?OC={OC}&target=law&type=XML&mst={law_id}"
            detail_res = requests.get(law_detail_url)
            if detail_res.status_code == 200:
                parsed = parse_law_xml(detail_res.content)
                조문들 = []
                for 조 in parsed["조문"]:
                    if filter_by_logic(조, query, unit):
                        조문들.append(조)
                if 조문들:
                    result.append({
                        "법령명한글": parsed["법령명한글"],
                        "원문링크": law.findtext("법령상세링크"),
                        "조문": 조문들
                    })
    return result
