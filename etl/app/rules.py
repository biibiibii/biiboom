from app.db.db_client import db_client
from app.model import RuleType, MatchRule

# https://forum.bnbchain.org/ => https://forum.bnbchain.org/latest.json?&page=0
# https://ethereum-magicians.org/ => https://ethereum-magicians.org/latest.json?no_definitions=true&page=0
rule_forum = MatchRule(
    container="topic_list.topics",
    title="title",
    url="id",
    rule_type=RuleType.json.value,
    posted_at="created_at",
    extra={
        "tags": "tags",
    },
)
db_client.put_item(rule_forum)

# https://www.chainfeeds.xyz/
rule_chainfeeds = MatchRule(
    container="data.list",
    title="title",
    url="uuid",
    rule_type=RuleType.json.value,
    posted_at="show_time",
    extra={
        # todo support json array
        "tags": "tags.0.tag_name",
    },
)
db_client.put_item(rule_chainfeeds)

db_client.save()
