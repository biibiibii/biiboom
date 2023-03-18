import { Card, Col, Row } from 'antd';
import type { FC } from 'react';
import { GridContent } from '@ant-design/pro-layout';
import styles from './style.less';
import { useRequest } from 'umi';
import { querySiteNodes } from './service';
import type { SiteData } from './data';
import moment from 'moment';

const Monitor: FC = () => {
  const { loading, data } = useRequest(querySiteNodes);

  const nodesData: SiteData[] = data?.site || [];
  const rowData = [1, 2, 3];

  return (
    <GridContent>
      <>
        <Row gutter={12} className={styles.nodesRow}>
          {nodesData.map((item) =>
            rowData.map((rowItem) => (
              <Col xl={6} lg={12} sm={12} xs={24} style={{ marginBottom: 12 }}>
                <Card
                  title={item.name}
                  bodyStyle={{ textAlign: 'center', fontSize: 0, padding: 6 }}
                  bordered={false}
                  size={'small'}
                  hoverable={true}
                >
                  <ul className={styles.nodesList}>
                    {item.nodes.map((node, i) => (
                      <a href={node.url} target="_blank">
                        <li key={node.title}>
                          <span
                            className={`${styles.nodesItemNumber} ${i < 3 ? styles.active : ''}`}
                          >
                            {i + 1}
                          </span>
                          <span className={styles.nodesItemTitle} title={node.url}>
                            {node.title}
                            <span className={styles.datetime}>
                              {node.posted_at
                                ? moment(node.posted_at).format('YYYY-MM-DD HH:mm')
                                : ''}
                            </span>
                          </span>
                        </li>
                      </a>
                    ))}
                  </ul>
                </Card>
              </Col>
            )),
          )}
        </Row>
      </>
    </GridContent>
  );
};

export default Monitor;
