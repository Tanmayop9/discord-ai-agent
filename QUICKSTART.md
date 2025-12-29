# 🎮 Quick Reference Guide

## New Interactive Commands

### Dashboard & Menus
```bash
!dashboard          # Open interactive dashboard with all services
!calendar_menu      # Calendar quick actions with buttons
!service_menu       # Dropdown to select a service
!help              # Interactive help with categories
```

### Account Setup
```bash
!create_account    # Create account with modern UI
!authenticate      # Re-authenticate with button link
```

### Service Commands (Enhanced with Embeds)
```bash
# Calendar
!calendar <message>      # Natural language calendar management
!upcoming [count]        # List upcoming events (default: 10)

# Gmail
!gmail <message>         # Email operations

# GitHub  
!github <message>        # Repository operations

# Slack
!slack <message>         # Team messaging

# AI Multi-Service
!ai <message>           # AI across all services
```

## What's New? 🆕

### 1. Interactive Buttons
- Click buttons instead of typing commands
- Quick access to common operations
- Visual and intuitive

### 2. Dropdown Menus
- Select from multiple options
- Organized choices
- Easy navigation

### 3. Modal Forms
- Fill out forms for complex operations
- Create events with guided inputs
- User-friendly data entry

### 4. Rich Embeds
- Beautiful colored messages
- Organized information
- Visual status indicators

### 5. Real-time Updates
- Messages update in place
- No spam with multiple messages
- Clean chat experience

## Examples

### Open Dashboard
```
!dashboard
```
Then click any service button for quick actions.

### Create Event with Form
```
!calendar_menu
```
Click "➕ Create Event" and fill out the form.

### Get Quick Help
```
!help
```
Select a category from dropdown to see detailed help.

### View Upcoming Events
```
!calendar_menu
```
Click "📅 Upcoming Events" button.

## Tips 💡

1. **Start with the Dashboard**
   - Use `!dashboard` as your main menu
   - Explore each service button

2. **Interactive Menus Timeout**
   - Buttons expire after 60-300 seconds
   - Just run the command again if expired

3. **Buttons are Personal**
   - Only you can use buttons from your commands
   - Prevents accidental clicks by others

4. **All Old Commands Still Work**
   - You can use text commands as before
   - Interactive features are optional enhancements

5. **Use Embeds for Better Readability**
   - All responses now use colored embeds
   - Easier to read and understand

## Color Guide 🎨

- 📅 **Blue** - Calendar
- 📧 **Red** - Gmail  
- 🐙 **Gray** - GitHub
- 💬 **Purple** - Slack
- 🤖 **Gold** - AI
- ✅ **Green** - Success
- ⏳ **Orange** - Processing
- ❌ **Red** - Error

## Keyboard Shortcuts ⌨️

While these are still Discord commands, you can use Discord's command autocomplete:
- Type `!` to see all commands
- Type `!d` to see dashboard, etc.
- Use ↑/↓ arrows to navigate suggestions

## Getting Started (First Time Users)

1. **Setup** (one time)
   ```
   !create_account
   ```
   Click "Connect Services" button

2. **Explore**
   ```
   !dashboard
   ```
   Click buttons to explore features

3. **Get Help**
   ```
   !help
   ```
   Select topics you want to learn about

4. **Try Calendar**
   ```
   !calendar_menu
   ```
   Use quick action buttons

5. **Use Services**
   ```
   !calendar Create meeting tomorrow at 2pm
   !gmail Check my unread emails
   !github List issues in owner/repo
   !slack Send "Hi" to #general
   !ai Schedule meeting and notify on Slack
   ```

## Troubleshooting 🔧

**Button doesn't work?**
- Make sure you ran the command
- Check if it timed out (run command again)
- Only you can use your buttons

**Menu disappeared?**
- Menus timeout after a few minutes
- Just run the command again

**Service not working?**
- Make sure you authenticated the service
- Use `!authenticate` to reconnect

**Need more help?**
- Use `!help` for detailed information
- Check EXAMPLES.md for usage examples
- See FEATURES.md for all new features

## Command Summary

| Command | Purpose | Type |
|---------|---------|------|
| !dashboard | Main menu | Interactive |
| !calendar_menu | Calendar actions | Interactive |
| !service_menu | Service selector | Interactive |
| !help | Help system | Interactive |
| !create_account | Setup account | Enhanced |
| !authenticate | Re-auth services | Enhanced |
| !calendar | Calendar ops | Enhanced |
| !upcoming | List events | Enhanced |
| !gmail | Email ops | Enhanced |
| !github | GitHub ops | Enhanced |
| !slack | Slack ops | Enhanced |
| !ai | Multi-service AI | Enhanced |

**Interactive** = Buttons/Menus  
**Enhanced** = Embeds + Colors
