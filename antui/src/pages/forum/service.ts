import { request } from 'umi';
import type { SiteData } from './data';

export async function querySiteNodes(tag: string = ''): Promise<{ data: { site: SiteData[] } }> {
  let filter = ``;
  if (tag.length > 0) {
    filter = `tags: { _contains: ${tag} } `;
  }
  const payload = {
    query: `
query GetSiteNodes {
  site(limit: 30, where: {${filter}}) {
    name
    sub_name
    url
    rule_id
    jump_base_url
    original_url
    id
    nodes(limit: 30, order_by: {posted_at: desc}) {
      url
      title
      site_id
      posted_at
      id
      extra
      desc
      _updated_at
    }
  }
}
`,
    variables: null,
    operationName: 'GetSiteNodes',
  };
  const resp = request('/v1/graphql', {
    method: 'post',
    data: payload,
  });
  return resp;
}
