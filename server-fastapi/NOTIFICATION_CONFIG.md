# Notification Toggle Configuration

## Environment Variable

Add this to your `.env` file to control notifications:

```bash
# Enable/disable real-time notifications (true/false)
ENABLE_NOTIFICATIONS=true
```

## Usage

### Server-Side Control

When `ENABLE_NOTIFICATIONS=false`:
- WebSocket routes are not registered
- No notification sending overhead
- API endpoints function normally without real-time features

When `ENABLE_NOTIFICATIONS=true` (default):
- Full real-time notification system enabled
- WebSocket connections accepted
- Real-time updates for requests and status changes

### Client-Side Control

The client automatically detects if notifications are disabled and will:
- Skip WebSocket connection attempts
- Hide notification UI components gracefully
- Continue normal app functionality

## Development Benefits

- **Testing**: Disable notifications to avoid WebSocket complexity during testing
- **Performance**: Reduce server overhead when not needed
- **Debugging**: Isolate issues by toggling notifications on/off
- **Demo**: Run app without real-time features for simple demos

## Implementation Details

### Server Files Modified:
- `.env.example` - Added `ENABLE_NOTIFICATIONS=true`
- `main.py` - Conditional WebSocket router inclusion
- `routes_items.py` - Conditional notification sending
- `routes_user_requests.py` - Conditional notification sending

### Client Files Modified:
- `services/notifications.ts` - Checks for enabled status before connecting

## Example Configurations

### Development with Notifications:
```bash
ENABLE_NOTIFICATIONS=true
```

### Testing without Notifications:
```bash
ENABLE_NOTIFICATIONS=false
```

### Production (usually enabled):
```bash
ENABLE_NOTIFICATIONS=true
```
