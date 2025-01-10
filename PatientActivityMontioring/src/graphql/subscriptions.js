export const onFallDetected = `
  subscription OnFallDetected {
    onFallDetected {
      timestamp
      activity
      position_x
      position_y
      position_z
    }
  }
`;
