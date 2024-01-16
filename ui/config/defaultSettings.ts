import { Settings as LayoutSettings } from '@ant-design/pro-layout';

const Settings: LayoutSettings & {
  pwa?: boolean;
  logo?: string;
} = {
  title: 'BiiBoom',
  // navTheme: 'realDark',
  navTheme: 'light',
  primaryColor: '#52C41A',
  layout: 'top',
  contentWidth: 'Fluid',
  fixedHeader: true,
  fixSiderbar: true,
  pwa: false,
  logo: '/logo.svg',
  headerHeight: 48,
  splitMenus: false,
};

export default Settings;
