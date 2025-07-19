# Fix for Undefined Telemetry Data Error

## Problem
The application was throwing a runtime error:
```
TypeError: Cannot read properties of undefined (reading 'toFixed')
```

This occurred in the `StatusDisplay` component when trying to format the battery level value, which was undefined.

## Root Cause
The telemetry data from the WebSocket connection might not always include all properties, especially during initial connection or when the drone is not fully initialized. The `battery_level` property was undefined, but the code was trying to call `toFixed()` on it.

## Solution

### 1. Updated formatNumber Function
Made the `formatNumber` function more defensive by:
- Accepting `number | undefined | null` as input type
- Checking for undefined, null, or NaN values
- Returning '--' as a default display value for invalid inputs

```typescript
const formatNumber = (num: number | undefined | null, decimals: number = 2) => {
  if (num === undefined || num === null || isNaN(num)) {
    return '--';
  }
  return num.toFixed(decimals);
};
```

### 2. Added Explicit Checks for battery_level
Updated the battery display logic to explicitly check if `battery_level` is defined before:
- Using it in comparisons for CSS classes
- Passing it to formatNumber

## Prevention Guidelines

When working with telemetry data or any external data source:

1. **Always check for property existence** before using it
2. **Use optional chaining** where appropriate: `telemetry?.property`
3. **Provide default values** for display when data is missing
4. **Make utility functions defensive** by handling edge cases

## Testing
To test this fix:
1. Start the frontend while the backend is not running
2. Start the frontend before the drone is connected
3. The UI should display '--' for missing values instead of crashing 