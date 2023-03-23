import time
import re
from scholarly import scholarly, ProxyGenerator

# raw paper infomation text
raw_papers = '''
[Redmon et al. 18] YOLOv3: An Incremental Improvement, Arxiv, 2018.
[Chen et al. 19] Learning Efficient Object Detection Models with Knowledge Distillation, NIPS, 2019.
[Kang et al. 21] Instance-Conditional Knowledge Distillation for Object Detection, NIPS, 2021.
[Fang et al. 21] You Only Look at One Sequence: Rethinking Transformer in Vision through Object Detection, NIPS, 2021.
[Ge et al. 21] YOLOX: Exceeding YOLO Series in 2021, Arxiv, 2021.
[Pramanik et al. 22] Granulated RCNN and Multi-Class Deep SORT for Multi-Object Detection and Tracking, IEEE TETCI, 2022.
[Wang et al. 21] You Only Learn One Representation: Unified Network for Multiple Tasks, Arxiv, 2021.
[Wang et al. 19] Towards Universal Object Detection by Domain Attention, CVPR, 2019.
[Huang et al. 19] Mask Scoring R-CNN, CVPR, 2019.
[Guo et al. 21] Distilling Object Detectors via Decoupled Features, CVPR, 2021.
[Chen et al. 18] Domain Adaptive Faster R-CNN for Object Detection in the Wild, CVPR, 2018.
[Wang et al. 21] Data-Uncertainty Guided Multi-Phase Learning for Semi-Supervised Object Detection, CVPR,2021.
[Zhou et al. 21] Instant-Teaching: An End-to-End Semi-Supervised Object Detection Framework, CVPR, 2021.
[Yang et al. 21] Interactive Self-Training with Mean Teachers for Semi-supervised Object Detection, CVPR, 2021.
[Wang et al. 23] YOLOv7: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors, CVPR, 2023.
[Feng et al. 22] Beyond Bounding Box: Multimodal Knowledge Learning for Object Detection, CVPR, 2022.
[Li et al. 22] Cross-Domain Adaptive Teacher for Object Detection, CVPR, 2022.
[Yang et al. 22] Focal and Global Knowledge Distillation for Detectors, CVPR, 2022.
'''

SCRAPER_KEY = '5370e242c68f7520a3b39a0aaacf2ea9'


# parse the raw paper information text into a dict{author: paper_title}
def parse_papers() -> dict:
    papers = {}
    for line in raw_papers.splitlines():
        if line == '':
            continue

        # regex to parse the author and paper title
        reg_author = re.compile(r'\[(.*?)\]')
        reg_paper_title = re.compile(r'\](.*?)\,')
        author = reg_author.findall(line)[0]
        paper_title = reg_paper_title.findall(line)[0][1:]

        # if not found, skip
        if author == '' or paper_title == '':
            continue
        # add to dict
        papers[author] = paper_title

        return papers


# test connection to google scholar
def test_connection():
    try:
        pg = ProxyGenerator()
        pg.ScraperAPI(SCRAPER_KEY)
        scholarly.use_proxy(pg)
        print("Connected to Google Scholar")
    # if not connected, print exception
    except Exception as e:
        print(e)
        print("Not connected to Google Scholar")
        exit(1)


# fetch the number of citations for each paper
def fetch_citations(papers: dict):
    for paper in papers:
        time.sleep(1)
        search_query = scholarly.search_pubs(query=papers[paper])
        try:
            pub = next(search_query)
            # format the output of dict
            # format a dict output
            print(paper + " has " + str(pub['num_citations']) + " citations.")
        except StopIteration:
            print(papers[paper] + " not found.")


# main function
if __name__ == '__main__':
    test_connection()
    papers = parse_papers()
    fetch_citations(papers)