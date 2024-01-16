import { Space, Switch } from 'antd';
import React from 'react';
import { useModel, SelectLang, FormattedMessage } from 'umi';
import styles from './index.less';
import { CheckOutlined } from '@ant-design/icons';

export type SiderTheme = 'light' | 'dark';

const GlobalHeaderRight: React.FC = () => {
  const { initialState, setInitialState } = useModel('@@initialState');

  if (!initialState || !initialState.settings) {
    return null;
  }

  const { navTheme, layout } = initialState.settings;
  let className = styles.right;

  if ((navTheme === 'dark' && layout === 'top') || layout === 'mix') {
    className = `${styles.right}  ${styles.dark}`;
  }

  return (
    <Space className={className}>
      <Switch
        checkedChildren={<CheckOutlined />}
        unCheckedChildren={<FormattedMessage id="component.globalHeader.darkTheme" />}
        checkedChildren={<FormattedMessage id="component.globalHeader.lightTheme" />}
        onChange={(checked: boolean) => {
          setInitialState({
            ...initialState,
            ...{ settings: { ...initialState.settings, navTheme: checked ? 'realDark' : 'light' } },
          });
        }}
      />
      <SelectLang className={styles.action} />
    </Space>
  );
};

export default GlobalHeaderRight;
