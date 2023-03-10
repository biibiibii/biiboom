from app.model import ResponseType, MatchRule

# https://forum.bnbchain.org/ => https://forum.bnbchain.org/latest.json?&page=0
# https://ethereum-magicians.org/ => https://ethereum-magicians.org/latest.json?no_definitions=true&page=0

forum_rule = dict(
    response_type=ResponseType.json,
    rule=MatchRule(
        container="//topic_list/topics",
        title="title/text()",
        url="slug/text()",
        created_at="created_at/text()",
        extra={
            "tags": "tags/item/text()",
        },
    ),
)
