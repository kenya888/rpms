%global snapdate @DATE@
%global snaphash @HASH@

%define modulename themes

%global _grubdir /boot/grub2
%global _grubthemedir %{_grubdir}/themes

Summary:        Liri themes
Name:           liri-%{modulename}
Version:        @VERSION@
Release:        0.1%{?snaphash:.%{snapdate}git%(echo %{snaphash} | cut -c -13)}%{?dist}
License:        GPLv3+
URL:            https://liri.io
Source:         https://github.com/lirios/%{modulename}/%{?snaphash:archive}%{!?snaphash:releases/download}/%{?snaphash}%{!?snaphash:v%{version}}/%{name}-%{?snaphash}%{!?snaphash:%{version}}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  liri-rpm-macros

BuildArch:      noarch

%description
This package contains color schemes and themes for GRUB, Plymouth and SDDM.


%package -n liri-color-schemes
Summary:        Color schemes for Qt applications

%description -n liri-color-schemes
This package contains color schemes for Qt applications.


%package -n grub2-lirios-theme
Summary:        Liri OS theme for GRUB
%ifnarch aarch64
Requires:       grub2
%else
Requires:       grub2-efi
%endif

%description -n grub2-lirios-theme
This package contains the "Liri OS" theme for GRUB.


%package -n plymouth-theme-lirios
Summary:        Liri OS theme for Plymouth
Requires:       plymouth-plugin-two-step
Provides:       plymouth(system-theme) = %{version}-%{release}

%description -n plymouth-theme-lirios
This package contains the "Liri OS" theme for Plymouth.


%package -n sddm-theme-lirios
Summary:        Liri OS theme for SDDM
Requires:       sddm
Requires:       accountsservice

%description -n sddm-theme-lirios
This package contains the "Liri OS" theme for SDDM.


%prep
%setup -q -n %{?snaphash:%{modulename}-%{snaphash}}%{!?snaphash:%{name}-%{version}}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_liri} -DINSTALL_GRUBDIR=%{_grubdir} ..
popd
make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# Set SDDM theme
mkdir -p %{buildroot}/usr/lib/sddm/sddm.conf.d
cat > %{buildroot}/usr/lib/sddm/sddm.conf.d/00-lirios.conf <<EOF
[Theme]
Current=lirios
EOF


%post -n plymouth-theme-lirios
export LIB=%{_lib}
if [ $1 -eq 1 ]; then
    %{_sbindir}/plymouth-set-default-theme lirios
fi


%postun -n plymouth-theme-lirios
export LIB=%{_lib}
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "lirios" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
    fi
fi


%files -n liri-color-schemes
%defattr(-,root,root,-)
%{_datadir}/color-schemes/*.colors


%files -n grub2-lirios-theme
%defattr(-,root,root,-)
%doc AUTHORS.md README.md
%{_grubthemedir}/lirios/


%files -n plymouth-theme-lirios
%defattr(-,root,root,-)
%doc AUTHORS.md README.md
%{_datadir}/plymouth/themes/lirios/


%files -n sddm-theme-lirios
%defattr(-,root,root,-)
%doc AUTHORS.md README.md
%{_prefix}/lib/sddm/sddm.conf.d/00-lirios.conf
%{_datadir}/sddm/themes/lirios/
