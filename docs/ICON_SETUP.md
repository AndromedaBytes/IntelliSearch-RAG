# IntelliSearch V2 - Icon Setup Guide

## Adding the Dragon Shield Icon to Your EXE

Your dragon shield icon will appear on:
- Windows taskbar
- File explorer
- Desktop shortcuts
- Task Manager
- Control Panel / Apps & Features

### Quick Setup (3 steps)

1. **Save the dragon icon image** 
   - Right-click the dragon image → Save image as `dragon_icon.png`
   - Place it in the project root directory: `C:\Users\saran\Downloads\Project Xeno\`

2. **Convert to ICO format**
   ```powershell
   cd "C:\Users\saran\Downloads\Project Xeno"
   .\.venv\Scripts\python.exe setup_icon.py dragon_icon.png
   ```

3. **Build the EXE**
   ```powershell
   python build_exe.py
   ```

### What happens:

- `setup_icon.py` converts your PNG → `assets/icon.ico` (6 sizes: 16x16 to 256x256)
- `build_exe.py` automatically detects the icon and includes it
- Your `.exe` will have the dragon shield icon

### Icon Requirements:

- **Format:** PNG, JPG, GIF, or BMP
- **Size:** Any size (will be scaled - 256x256+ recommended)
- **Background:** Can be any color (will be preserved)

### Troubleshooting:

- **Icon not showing after build?**
  - Delete `dist/` folder
  - Run `build_exe.py` again

- **Conversion error?**
  - Install Pillow: `.venv\Scripts\pip install Pillow`
  - Ensure image path is correct

---

**Ready?** Run `setup_icon.py` with your dragon image, then `build_exe.py`!
