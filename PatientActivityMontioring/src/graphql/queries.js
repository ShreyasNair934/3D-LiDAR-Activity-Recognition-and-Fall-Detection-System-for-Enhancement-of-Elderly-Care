export const listLidarData = `
  query ListLidarData($limit: Int) {
    listLidarData(limit: $limit) {
      items {
        timestamp
        activity
        position_x
        position_y
        position_z
      }
    }
  }
`;
