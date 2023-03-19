export type NodeType = {
  url: string;
  title: string;
  posted_at: string;
  id: string;
  extra: {};
  desc: string;
  _updated_at: string;
};

export interface SiteData {
  name: string;
  url: string;
  rule_id: string;
  jump_base_url: string;
  id: string;
  nodes: NodeType[];
}
