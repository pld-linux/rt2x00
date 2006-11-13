#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%ifarch sparc
%undefine	with_smp
%endif
#
%define		_snap	2006082007
%define		_rel	0.%{_snap}.1
Summary:	Linux driver for WLAN cards based on RT2x00 chipsets
Summary(pl):	Sterownik dla Linuksa do kart WLAN opartych na uk³adach RT2x00
Name:		rt2x00
Version:	2.0.0
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://rt2x00.serialmonkey.com/%{name}-cvs-daily.tar.gz
# Source0-md5:	8f9aff9f03633d35e9bd21ead8a29706
Patch0:		%{name}-config.patch
Patch1:		%{name}-Makefile.patch
URL:		http://rt2x00.serialmonkey.com/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.17}
BuildRequires:	rpmbuild(macros) >= 1.326
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	modules	80211,crc-itu-t,rate_control,rfkill,rt2400pci,rt2500pci,rt2500usb,rt61pci,rt73usb

%description
A configuartion tool for WLAN cards based on RT2x00 chipsets.

%description -l pl
Narzêdzie konfiguracujne do kart WLAN opartych na uk³adach RT2x00.

%package -n kernel%{_alt_kernel}-net-rt2x00
Summary:	Linux kernel driver for WLAN cards based on RT2x00 chipsets
Summary(pl):	Sterownik j±dra Linuksa dla kart WLAN opartych na uk³adach RT2x00
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel%{_alt_kernel}-net-rt2x00
This is a Linux driver for WLAN cards based on RT2x00 chipsets.

%description -n kernel%{_alt_kernel}-net-rt2x00 -l pl
Sterownik j±dra Linuksa dla kart WLAN opartych na uk³adach RT2x00.

%package -n kernel%{_alt_kernel}-smp-net-rt2x00
Summary:	Linux SMP kernel driver for WLAN cards based on RT2x00 chipsets
Summary(pl):	Sterownik j±dra Linuksa SMP dla kart WLAN opartych na uk³adach RT2x00
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel%{_alt_kernel}-smp-net-rt2x00
This is a Linux driver for WLAN cards based on RT2x00 chipsets.

This package contains Linux SMP module.

%description -n kernel%{_alt_kernel}-smp-net-rt2x00 -l pl
Sterownik j±dra Linuksa dla kart WLAN opartych na uk³adach RT2x00.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q -n %{name}-cvs-%{_snap}
%patch0 -p1
%patch1 -p1

%build
./rt2x00_config.sh rt2x00_config.h
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

%post -n kernel%{_alt_kernel}-smp-net-rt2x00
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-net-rt2x00
%depmod %{_kernel_ver}smp

%files -n kernel%{_alt_kernel}-net-rt2x00
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-net-rt2x00
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/*.ko*
%endif
