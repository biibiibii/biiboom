import { Card, Col, Row } from 'antd';
import type { FC } from 'react';
import { GridContent } from '@ant-design/pro-layout';
import styles from './style.less';
import { useRequest } from 'umi';
import { querySiteNodes } from './service';
import type { SiteData } from './data';
const rankingListData: { title: string; total: number }[] = [];
for (let i = 0; i < 20; i += 1) {
  rankingListData.push({
    title: `工专路 ${i} 号店`,
    total: 323234,
  });
}

const Monitor: FC = () => {
  const { loading, data } = useRequest(querySiteNodes);
  console.log('site: ', data);
  console.log('home index');

  const nodesData: SiteData[] = data?.site || [];
  console.log('nodesData', nodesData);

  return (
    <GridContent>
      <>
        <Row gutter={12}>
          {nodesData.map((item) => (
            <Col xl={6} lg={12} sm={12} xs={12} style={{ marginBottom: 12 }}>
              <Card
                title={item.name}
                bodyStyle={{ textAlign: 'center', fontSize: 0 }}
                bordered={false}
                size={'small'}
              >
                <div className={styles.cardContainer}>
                  <div className={styles.cardContent}>
                    <ul className={styles.rankingList}>
                      {item.nodes.map((node, i) => (
                        <a href={node.url} target="_blank">
                          <li key={node.title}>
                            <span
                              className={`${styles.rankingItemNumber} ${
                                i < 3 ? styles.active : ''
                              }`}
                            >
                              {i + 1}
                            </span>
                            <span className={styles.rankingItemTitle} title={item.title}>
                              {node.title}
                            </span>
                            {/* <span className={styles.rankingItemValue}>
                          {numeral(node.total).format('0,0')}
                        </span> */}
                          </li>
                        </a>
                      ))}
                    </ul>
                  </div>
                </div>
              </Card>
            </Col>
          ))}
        </Row>
      </>
    </GridContent>
  );
};

export default Monitor;
