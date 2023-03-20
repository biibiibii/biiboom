from app.db.db_client import db_client
from app.model import RuleType, MatchRule

# https://forum.bnbchain.org/ => https://forum.bnbchain.org/latest.json?&page=0
# https://ethereum-magicians.org/ => https://ethereum-magicians.org/latest.json?no_definitions=true&page=0
forum_rule = MatchRule(
    container="topic_list.topics",
    title="title",
    url="id",
    rule_type=RuleType.json.value,
    posted_at="created_at",
    extra={
        "tags": "tags",
    },
)

db_client.put_item(forum_rule)
db_client.save()
