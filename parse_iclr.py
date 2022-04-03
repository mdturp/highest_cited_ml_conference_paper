"""Parse the list of iclr titles."""

import openreview
import json

client = openreview.Client(baseurl='https://api.openreview.net')


def query_iclr_2021_paper():
    paper_title = []
    submissions = openreview.tools.iterget_notes(
        client, invitation='ICLR.cc/2021/Conference/-/Blind_Submission')
    submissions_by_forum = {n.forum: n for n in submissions}

    decisions = openreview.tools.iterget_notes(
        client, invitation='ICLR.cc/2021/Conference/Paper.*/-/Decision')
    decisions_by_forum = {n.forum: n for n in decisions}

    for forum in submissions_by_forum:
        forum_decision = decisions_by_forum[forum]
        decision = forum_decision.content['decision']
        if "Accept" in decision:
            paper_title.append(
                submissions_by_forum[forum].content['title'])
    return paper_title


def query_iclr_2020_paper():
    paper_title = []
    submissions = openreview.tools.iterget_notes(
        client, invitation='ICLR.cc/2020/Conference/-/Blind_Submission')
    submissions_by_forum = {n.forum: n for n in submissions}

    decisions = openreview.tools.iterget_notes(
        client, invitation='ICLR.cc/2020/Conference/Paper.*/-/Decision')
    decisions_by_forum = {n.forum: n for n in decisions}

    for forum in submissions_by_forum:
        forum_decision = decisions_by_forum[forum]
        decision = forum_decision.content['decision']
        if "Accept" in decision:
            paper_title.append(
                submissions_by_forum[forum].content['title'])
    return paper_title


def query_iclr_2019_paper():
    paper_title = []
    submissions = openreview.tools.iterget_notes(
        client, invitation='ICLR.cc/2019/Conference/-/Blind_Submission')
    submissions_by_forum = {n.forum: n for n in submissions}

    meta_reviews = openreview.tools.iterget_notes(
        client, invitation='ICLR.cc/2019/Conference/-/Paper.*/Meta_Review')
    meta_reviews_by_forum = {n.forum: n for n in meta_reviews}

    for forum in submissions_by_forum:
        forum_meta_review = meta_reviews_by_forum[forum]
        decision = forum_meta_review.content['recommendation']
        if "Accept" in decision:
            paper_title.append(
                submissions_by_forum[forum].content['title'])
    return paper_title


def query_iclr_2018_paper():
    paper_title = []
    submissions = openreview.tools.iterget_notes(
        client, invitation='ICLR.cc/2018/Conference/-/Blind_Submission')
    submissions_by_forum = {n.forum: n for n in submissions}

    acceptance_decision = openreview.tools.iterget_notes(
        client, invitation='ICLR.cc/2018/Conference/-/Acceptance_Decision')
    acceptance_decision_by_forum = {n.forum: n for n in acceptance_decision}
    ln = []
    for forum in submissions_by_forum:
        forum_decision = acceptance_decision_by_forum[forum]
        decision = forum_decision.content['decision']
        if "Accept" in decision:
            paper_title.append(
                submissions_by_forum[forum].content['title'])
    return paper_title


def query_iclr_2017_paper():
    paper_title = []
    submissions = openreview.tools.iterget_notes(
        client, invitation='ICLR.cc/2017/conference/-/submission')
    submissions_by_forum = {n.forum: n for n in submissions}

    acceptance_decision = openreview.tools.iterget_notes(
        client, invitation='ICLR.cc/2017/conference/-/paper.*/acceptance')
    acceptance_decision_by_forum = {n.forum: n for n in acceptance_decision}
    ln = []
    for forum in submissions_by_forum:
        forum_decision = acceptance_decision_by_forum[forum]
        decision = forum_decision.content['decision']
        if "Accept" in decision:
            paper_title.append(
                submissions_by_forum[forum].content['title'])
    return paper_title


if __name__ == "__main__":

    iclr_conferences = [
        {"year": 2021,
         "title": query_iclr_2021_paper()},
        {"year": 2020,
         "title": query_iclr_2020_paper()},
        {"year": 2019,
         "title": query_iclr_2019_paper()},
        {"year": 2018,
         "title": query_iclr_2018_paper()},
        {"year": 2017,
         "title": query_iclr_2017_paper()}
    ]
    with open("data/iclr/title.json", "w") as f:
        json.dump(iclr_conferences, f)
