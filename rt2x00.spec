#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%ifarch sparc
%undefine	with_smp
%endif
#
%define		_snap	2007032610
%define		_rel	0.%{_snap}.1
Summary:	Linux driver for WLAN cards based on RT2x00 chipsets
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart WLAN opartych na układach RT2x00
Name:		rt2x00
Version:	2.0.0
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://rt2x00.serialmonkey.com/%{name}-cvs-daily.tar.gz
# Source0-md5:	371557c5f055a596109c235f802524d5
Patch0:		%{name}-config.patch
Patch1:		%{name}-Makefile.patch
URL:		http://rt2x00.serialmonkey.com/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.17}
BuildRequires:	rpmbuild(macros) >= 1.330
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	modules	80211,crc-itu-t,eeprom_93cx6,rc80211_simple,rfkill,rt2x00lib,rt2400pci,rt2500pci,rt2500usb,rt61pci,rt73usb,rt2x00debug

%description
A configuartion tool for WLAN cards based on RT2x00 chipsets.

%description -l pl.UTF-8
Narzędzie konfiguracujne do kart WLAN opartych na układach RT2x00.

%package -n kernel%{_alt_kernel}-net-rt2x00
Summary:	Linux kernel driver for WLAN cards based on RT2x00 chipsets
Summary(pl.UTF-8):	Sterownik jądra Linuksa dla kart WLAN opartych na układach RT2x00
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-net-rt2x00
This is a Linux driver for WLAN cards based on RT2x00 chipsets.

%description -n kernel%{_alt_kernel}-net-rt2x00 -l pl.UTF-8
Sterownik jądra Linuksa dla kart WLAN opartych na układach RT2x00.

%prep
%setup -q -n %{name}-cvs-%{_snap}
%patch0 -p1
%patch1 -p1

%build
%{__perl} -nle 'next if /DEBUG/; /^(CONFIG_.+)=([yn])\b/ and print $2 eq "y" ? "#ifndef $1\n#define $1\n#endif\n" : "#undef $1\n"' config >rt2x00_config.h
%build_kernel_modules -m %{modules}

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m %{modules} -d kernel/drivers/net/wireless

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{_alt_kernel}-net-rt2x00
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-net-rt2x00
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-net-rt2x00
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*.ko*
