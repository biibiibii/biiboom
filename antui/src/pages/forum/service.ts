import { request } from 'umi';
import type { TagType, SiteData } from './data';

export async function queryTags(): Promise<{ data: { list: TagType[] } }> {
  return request('/api/tags');
}

export async function querySiteNodes(): Promise<{ data: { site: SiteData[] } }> {
  console.log('querySiteNodes');

  return request('/api/rest/get_match_rule');
}
