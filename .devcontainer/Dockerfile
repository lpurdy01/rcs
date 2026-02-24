FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

# Enable universe repo and install system dependencies for openEMS + display
RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository universe \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        # Python
        python3-full \
        python3-pip \
        python-is-python3 \
        # Core build tools
        build-essential \
        cmake \
        git \
        libtool \
        # openEMS core dependencies
        libhdf5-dev \
        libvtk9-dev \
        libboost-all-dev \
        libcgal-dev \
        libtinyxml-dev \
        qtbase5-dev \
        libvtk9-qt-dev \
        # Parser generators
        bison \
        flex \
        gengetopt \
        # Documentation build tools (prevents cmake warnings)
        help2man \
        groff \
        # libHaru PDF library (used by openEMS)
        libhpdf-dev \
        # SSH client for git over SSH
        openssh-client \
        # X11 client libraries for GUI passthrough (CSX CAD, ParaView)
        libx11-dev \
        libxext-dev \
        libxrender-dev \
        libxi-dev \
        x11-utils \
        # OpenGL for CSX CAD (Qt5 OpenGL application)
        libgl1-mesa-dri \
        libglu1-mesa \
        # Qt5 GUI + XCB platform support
        # Note: libqt5xcbqpa5 was merged into libqt5gui5 in Ubuntu 22.04
        libqt5gui5 \
        libqt5x11extras5 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render-util0 \
        libxcb-xinerama0 \
        libxcb-xkb1 \
        libxkbcommon-x11-0 \
        # Utilities
        curl \
        wget \
        sudo \
    && rm -rf /var/lib/apt/lists/*

# Install Python scientific stack + scipy for analytical Mie series
RUN pip3 install --no-cache-dir numpy matplotlib cython h5py scipy

# Create the vscode non-root user (matches VS Code devcontainer convention)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

WORKDIR /workspaces/rcs
