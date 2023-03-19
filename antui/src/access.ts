/**
 * @see https://umijs.org/zh-CN/plugins/plugin-access
 * */
export default function access(initialState: undefined) {
  // const { currentUser } = initialState ?? {};
  // return {
  //   canAdmin: currentUser && currentUser.access === 'admin',
  // };
  return {
    canAdmin: true,
  };
}
