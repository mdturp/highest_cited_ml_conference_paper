"""Parse the list of iclr titles."""

import openreview
from collections import defaultdict
client = openreview.Client(baseurl='https://api.openreview.net')

submissions = openreview.tools.iterget_notes(
        client, invitation='ICLR.cc/2019/Conference/-/Blind_Submission')
submissions_by_forum = {n.forum: n for n in submissions}

reviews = openreview.tools.iterget_notes(
        client, invitation='ICLR.cc/2019/Conference/-/Paper.*/Official_Review')
reviews_by_forum = defaultdict(list)
for review in reviews:
    reviews_by_forum[review.forum].append(review)

print(reviews_by_forum)