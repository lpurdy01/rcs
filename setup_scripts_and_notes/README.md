# Setup Scripts and Installation Notes

This directory contains installation scripts and setup notes for configuring the RCS simulation environment.

## Installation Scripts

### Core Installation

#### install_openems.sh
Installs openEMS electromagnetic field solver and Python bindings.

**What it installs:**
- System dependencies (compilers, libraries)
- openEMS core from source
- CSXCAD (CAD library for openEMS)
- Python bindings for openEMS and CSXCAD

**Usage:**
```bash
bash setup_scripts_and_notes/install_openems.sh
```

**Installation location:** `~/opt/openEMS/`

**Note:** This script is designed for Ubuntu 22.04. Adjust package names for other distributions.

### Visualization Tools

#### install_paraview.sh
Installs ParaView for 3D electromagnetic field visualization.

**Usage:**
```bash
bash setup_scripts_and_notes/install_paraview.sh
```

ParaView is essential for:
- Viewing field distributions
- Animating time-domain results
- Creating publication-quality visualizations

#### install_openscad.sh
Installs OpenSCAD for creating and modifying 3D geometry models.

**Usage:**
```bash
bash setup_scripts_and_notes/install_openscad.sh
```

Use OpenSCAD to:
- Create parametric 3D models
- Export STL files for simulations
- Modify existing geometry files

### Development Environment

#### install_desktop_env.sh
Installs a desktop environment with RDP support for remote work.

**Usage:**
```bash
bash setup_scripts_and_notes/install_desktop_env.sh
```

Useful for:
- Remote GUI access to visualization tools
- Working on headless servers
- Remote ParaView sessions

### AI/ML Tools

#### install_shell_gpt.sh
Installs shell-gpt for AI-assisted command line operations.

**Usage:**
```bash
bash setup_scripts_and_notes/install_shell_gpt.sh
```

### Python Virtual Environment

#### setup_venv.sh
Creates a Python virtual environment for isolating project dependencies.

**Usage:**
```bash
bash setup_scripts_and_notes/setup_venv.sh
```

Creates a virtual environment in `venv/` directory with required packages.

#### activate_venv.sh
Activates the Python virtual environment.

**Usage:**
```bash
source setup_scripts_and_notes/activate_venv.sh
```

**Note:** Must use `source` to activate properly.

## Installation Order

Recommended installation sequence:

1. **System prerequisites**
   ```bash
   sudo apt update && sudo apt upgrade
   ```

2. **openEMS** (required)
   ```bash
   bash setup_scripts_and_notes/install_openems.sh
   ```

3. **Python environment** (recommended)
   ```bash
   bash setup_scripts_and_notes/setup_venv.sh
   source setup_scripts_and_notes/activate_venv.sh
   pip install -r requirements.txt
   ```

4. **Visualization tools** (optional but recommended)
   ```bash
   bash setup_scripts_and_notes/install_paraview.sh
   bash setup_scripts_and_notes/install_openscad.sh
   ```

5. **Desktop environment** (optional, for remote access)
   ```bash
   bash setup_scripts_and_notes/install_desktop_env.sh
   ```

## Manual Installation Notes

### openEMS from Source

If the installation script fails, follow these manual steps:

```bash
# Install dependencies
sudo apt install -y build-essential cmake git
sudo apt install -y libhdf5-dev libvtk7-dev libboost-all-dev
sudo apt install -y libcgal-dev libtinyxml-dev qtbase5-dev

# Clone repository
mkdir ~/repos
cd ~/repos
git clone --recursive https://github.com/thliebig/openEMS-Project.git

# Build and install
cd ~/repos/openEMS-Project
./update_openEMS.sh ~/opt/openEMS --python

# Install Python bindings
cd ~/repos/openEMS-Project/openEMS/python/
python setup.py install --user

cd ~/repos/openEMS-Project/CSXCAD/python/
python setup.py install --user
```

### Verifying Installation

Test openEMS installation:
```python
python -c "import openEMS; print('openEMS imported successfully')"
python -c "import CSXCAD; print('CSXCAD imported successfully')"
```

## Troubleshooting

### Common Issues

**Issue:** Build errors during openEMS compilation
- **Solution:** Ensure all dependencies are installed
- Check cmake version (should be 3.x or higher)

**Issue:** Python bindings not found
- **Solution:** Check PYTHONPATH or reinstall Python bindings
- Try: `export PYTHONPATH=~/opt/openEMS/python:$PYTHONPATH`

**Issue:** Missing system libraries
- **Solution:** Install missing packages with apt
- Check error messages for specific library names

**Issue:** Permission denied errors
- **Solution:** Ensure proper permissions on installation directory
- May need to use `sudo` for system-wide installations

### System-Specific Notes

**Ubuntu 22.04+**: Fully tested and supported

**Ubuntu 20.04**: May need to adjust package names
- `libvtk7-dev` → check available version
- `qtbase5-dev` → may already be installed

**Other Linux distributions**: 
- Adjust package manager commands (apt → yum/dnf/pacman)
- Package names may differ

**Windows/WSL**: Should work with WSL2, but GUI tools require X server

**macOS**: Not officially supported by these scripts
- Use Homebrew for dependencies
- Build process similar but with different package names

## Additional Resources

### Documentation
- [openEMS Official Docs](https://docs.openems.de/)
- [openEMS GitHub](https://github.com/thliebig/openEMS-Project)
- [ParaView Guide](https://www.paraview.org/documentation/)

### Support
- [openEMS Forum](https://openems.de/forum/)
- [openEMS Tutorials](https://docs.openems.de/Tutorials)

## Notes

- Installation may take 30-60 minutes depending on system
- Requires stable internet connection
- ~2-3 GB of disk space needed
- Root/sudo access required for system packages

## Maintaining Your Installation

### Updating openEMS

```bash
cd ~/repos/openEMS-Project
git pull --recurse-submodules
./update_openEMS.sh ~/opt/openEMS --python
```

### Updating Python Packages

```bash
pip install --upgrade numpy matplotlib h5py cython
```

### Cleaning Build Files

```bash
cd ~/repos/openEMS-Project
./update_openEMS.sh ~/opt/openEMS --python --clean
```

## Environment Variables

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# openEMS paths
export PATH=~/opt/openEMS/bin:$PATH
export LD_LIBRARY_PATH=~/opt/openEMS/lib:$LD_LIBRARY_PATH
export PYTHONPATH=~/opt/openEMS/python:$PYTHONPATH
```

Then reload:
```bash
source ~/.bashrc
```
