sudo add-apt-repository universe
sudo apt update
sudo apt install -y python3-full
sudo apt install -y python3-pip
sudo apt install -y python-is-python3
sudo apt-get install -y build-essential cmake git libhdf5-dev libvtk7-dev libboost-all-dev libcgal-dev libtinyxml-dev qtbase5-dev libvtk7-qt-dev
sudo apt-get install -y gengetopt help2man groff pod2pdf bison flex libhpdf-dev libtool
pip install numpy matplotlib cython h5py
mkdir ~/repos
cd ~/repos
git clone --recursive https://github.com/thliebig/openEMS-Project.git
cd ~/repos/openEMS-Project
./update_openEMS.sh ~/opt/openEMS --python
cd ~/repos/openEMS-Project/openEMS/python/
python setup.py install --user
cd ~/repos/openEMS-Project/CSXCAD/python/
python setup.py install --user
