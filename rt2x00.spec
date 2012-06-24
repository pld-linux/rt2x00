#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%ifarch sparc
%undefine	with_smp
%endif
#
Summary:	Linux driver for WLAN cards based on RT2500
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych opartych na uk�adzie RT2500
Name:		rt2x00
Version:	2.0.0
%define		_subver	b3
%define		_rel	0.%{_subver}.3
Release:	%{_rel}
Group:		Base/Kernel
License:	GPL v2
Source0:	http://rt2x00.serialmonkey.com/%{name}-%{version}-%{_subver}.tar.gz
# Source0-md5:	4881d742ee49d3ea12c435a91deacd41
URL:		http://rt2x00.serialmonkey.com/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.217
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A configuartion tool for WLAN cards based on RT2500.

%description -l pl
Program do konfiguracji kart bezprzewodowych opartych na uk�adzie
RT2500.

%package -n kernel-net-rt2500
Summary:	Linux driver for WLAN cards based on RT2500
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych opartych na uk�adzie RT2500
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel-net-rt2500
This is a Linux driver for WLAN cards based on RT2500.

This package contains Linux module.

%description -n kernel-net-rt2500 -l pl
Sterownik dla Linuksa do kart bezprzewodowych opartych na uk�adzie
RT2500.

Ten pakiet zawiera modu� j�dra Linuksa.

%package -n kernel-smp-net-rt2500
Summary:	Linux SMP driver for WLAN cards based on RT2500
Summary(pl):	Sterownik dla Linuksa SMP do kart bezprzewodowych opartych na uk�adzie RT2500
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel-smp-net-rt2500
This is a Linux driver for WLAN cards based on RT2500.

This package contains Linux SMP module.

%description -n kernel-smp-net-rt2500 -l pl
Sterownik dla Linuksa do kart bezprzewodowych opartych na uk�adzie
RT2500.

Ten pakiet zawiera modu� j�dra Linuksa SMP.

%prep
%setup -q -n %{name}-%{version}-%{_subver}

%build
%if %{with kernel}
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
%ifarch ppc ppc64
        install -d include/asm
        [ ! -d %{_kernelsrcdir}/include/asm-powerpc ] || ln -sf %{_kernelsrcdir}/include/asm-powerpc/* include/asm
        [ ! -d %{_kernelsrcdir}/include/asm-%{_target_base_arch} ] || ln -snf %{_kernelsrcdir}/include/asm-%{_target_base_arch}/* include/asm
%else
        ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
%endif
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
	touch include/config/MARKER
  %{__make} -C %{_kernelsrcdir} O=$PWD prepare scripts
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
%if "%{_target_base_arch}" != "%{_arch}"
                ARCH=%{_target_base_arch} \
                CROSS_COMPILE=%{_target_base_cpu}-pld-linux- \
%endif
                HOSTCC="%{__cc}" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	mkdir o-$cfg
	mv *.ko o-$cfg/
done
cd -
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net/wireless
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
install o-%cfg/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/rt2500.ko
%if %{with smp} && %{with dist_kernel}
install rt2500-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/rt2500.ko
%endif
cd -
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel-net-rt2500
%depmod %{_kernel_ver}

%postun -n kernel-net-rt2500
%depmod %{_kernel_ver}

%post -n kernel-smp-net-rt2500
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-rt2500
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files -n kernel-net-rt2500
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-rt2500
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/*.ko*
%endif
%endif
