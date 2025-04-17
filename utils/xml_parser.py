
import xml.etree.ElementTree as ET
import re

def parse_law_xml(xml_content):
    try:
        root = ET.fromstring(xml_content)
        law_name = root.findtext("법령명한글")
        link = root.findtext("법령상세링크")
        articles = []
        for 조문 in root.findall(".//조문단위"):
            content = ""
            번호 = 조문.findtext("조문번호")
            제목 = 조문.findtext("조문제목")
            본문 = 조문.findtext("조문내용") or ""
            if 제목:
                content += f"제{번호}조({제목})"
            if 본문 and not 본문.startswith("제"):
                content += f" {본문.strip()}"
            항목들 = 조문.findall(".//항")
            for 항 in 항목들:
                항번호 = 항.findtext("항번호", "").strip()
                항내용 = 항.findtext("항내용", "").strip()
                if 항번호 and 항내용:
                    content += f"\n  {항번호} {항내용}"
                for 호 in 항.findall(".//호"):
                    호번호 = 호.findtext("호번호", "").strip()
                    호내용 = 호.findtext("호내용", "").strip()
                    if 호번호 and 호내용:
                        content += f"\n    {호번호} {호내용}"
                for 목 in 항.findall(".//목"):
                    목내용 = 목.findtext("목내용", "").strip()
                    if 목내용:
                        content += f"\n      - {목내용}"
            if content:
                articles.append(content)
        return {"법령명한글": law_name, "원문링크": link, "조문": articles}
    except Exception as e:
        return {"법령명한글": "오류 발생", "조문": [str(e)]}

def filter_by_logic(text, query, unit):
    terms = [t.strip() for t in query.replace("(", "").replace(")", "").split(",")]
    must_include = [t for t in terms if "-" not in t and "&" not in t]
    must_not = [t[1:] for t in terms if t.startswith("-")]
    must_all = [t for t in terms if "&" in t]

    if any(term not in text for term in must_not):
        for term in must_include:
            if term in text:
                return True
        for pair in must_all:
            and_terms = pair.split("&")
            if all(and_term.strip() in text for and_term in and_terms):
                return True
    return False
