import { request } from 'umi';
import type { SiteData } from './data';

export async function querySiteNodes(): Promise<{ data: { site: SiteData[] } }> {
  const payload = {
    query:
      'query GetMatchRule {\n  site(limit: 20) {\n    name\n    url\n    rule_id\n    jump_base_url\n    id\n    nodes(limit: 20, order_by: {posted_at: desc}) {\n      url\n      title\n      site_id\n      posted_at\n      id\n      extra\n      desc\n      _updated_at\n    }\n  }\n}\n',
    variables: null,
    operationName: 'GetMatchRule',
  };
  const resp = request('/v1/graphql', {
    method: 'post',
    data: payload,
  });
  return resp;
}
