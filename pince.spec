%global libscanmem_commit 03b28a7a673bee355a535d756de00d2caf2d10a8

Name:           pince
Version:        0.4.4
Release:        0%{?dist}
Summary:        Reverse engineering tool for Linux games
BuildArch:      x86_64

License:        GPL-3.0-or-later OR CC-BY-3.0
URL:            https://github.com/korcankaraokcu/PINCE
Source0:        https://github.com/korcankaraokcu/PINCE/archive/refs/tags/v%{version}.tar.gz
Source1:        https://github.com/brkzlr/libscanmem-PINCE/archive/%{libscanmem_commit}/libscanmem-PINCE-%{libscanmem_commit}.tar.gz
Source2:        https://github.com/kekeimiku/PointerSearcher-X/releases/download/v0.7.4-dylib/libptrscan_pince-x86_64-unknown-linux-gnu.tar.gz
Source3:        PINCE.desktop

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconf
BuildRequires:  python3-devel
BuildRequires:  qt6-linguist
BuildRequires:  sed

Requires:       gdb
# Requires:       python-keystone-engine
Requires:       python3-capstone
Requires:       python3-gobject
Requires:       python-keyboard
Requires:       python3-pexpect
Requires:       python3-pygdbmi
Requires:       python3-pyqt6

Recommends:     qt6-qtwayland

%description
PINCE is a front-end/reverse engineering tool for the GNU Project
Debugger (GDB), focused on games. However, it can be used for any
reverse-engineering related stuff. PINCE is an abbreviation for "PINCE
is not Cheat Engine".

%prep
%autosetup -n PINCE-%{version}
tar -xzf %{SOURCE1}
mkdir -p libpince/libptrscan
tar -xzf %{SOURCE2} -C libpince/libptrscan --strip-components 1

# Replace the script's directory and venv logic with the full execution command.
sed -i "/^SCRIPTDIR=/,/activate$/c\sudo -E --preserve-env=PATH PYTHONDONTWRITEBYTECODE=1 python3 %{_datadir}/PINCE/PINCE.py \\\"\\$@\\\" && exit" PINCE.sh

%build
%cmake -S libscanmem-PINCE-%{libscanmem_commit} -B build-libscanmem -DCMAKE_BUILD_TYPE=Release
%make_build -C build-libscanmem

# Compile translations
lrelease-qt6 i18n/ts/*
mkdir -p i18n/qm
mv i18n/ts/*.qm i18n/qm/

%install
install -d %{buildroot}%{_datadir}/PINCE
install -m755 PINCE.sh PINCE.py %{buildroot}%{_datadir}/PINCE
cp -r GUI libpince media tr i18n/qm %{buildroot}%{_datadir}/PINCE/

install -d %{buildroot}%{_datadir}/PINCE/libpince/libscanmem
install -m755 build-libscanmem/libscanmem.so %{buildroot}%{_datadir}/PINCE/libpince/libscanmem/
cp -r libscanmem-PINCE-%{libscanmem_commit}/wrappers/scanmem.py %{buildroot}%{_datadir}/PINCE/libpince/libscanmem/

install -d %{buildroot}%{_bindir}
ln -s %{_datadir}/PINCE/PINCE.sh %{buildroot}%{_bindir}/pince
ln -s %{_datadir}/PINCE/PINCE.sh %{buildroot}%{_bindir}/PINCE

install -d %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -m644 media/logo/ozgurozbek/pince_small_transparent.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/pince.png
install -d %{buildroot}%{_datadir}/applications
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE3}

%post
gtk-update-icon-cache -ftq %{_datadir}/icons/hicolor

%files
%license COPYING COPYING.CC-BY
%doc AUTHORS THANKS
%{_bindir}/pince
%{_bindir}/PINCE
%{_datadir}/PINCE/
%{_datadir}/applications/PINCE.desktop
%{_datadir}/icons/hicolor/256x256/apps/pince.png
