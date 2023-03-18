import { Card, Col, Row } from 'antd';
import type { FC } from 'react';
import { GridContent } from '@ant-design/pro-layout';
import styles from './style.less';
import { useRequest } from 'umi';
import { querySiteNodes } from './service';
import type { SiteData } from './data';

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
            <Col xl={6} lg={12} sm={12} xs={24} style={{ marginBottom: 12 }}>
              <Card
                title={item.name}
                bodyStyle={{ textAlign: 'center', fontSize: 0 }}
                bordered={false}
                size={'small'}
              >
                <ul className={styles.nodesList}>
                  {item.nodes.map((node, i) => (
                    <a href={node.url} target="_blank">
                      <li key={node.title}>
                        <span className={`${styles.nodesItemNumber} ${i < 3 ? styles.active : ''}`}>
                          {i + 1}
                        </span>
                        <span className={styles.nodesItemTitle} title={item.title}>
                          {node.title}
                        </span>
                      </li>
                    </a>
                  ))}
                </ul>
              </Card>
            </Col>
          ))}
        </Row>
      </>
    </GridContent>
  );
};

export default Monitor;
