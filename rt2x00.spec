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
Summary:	Linux driver for WLAN cards based on RT2x00 chipsets
Summary(pl):	Sterownik dla Linuksa do kart WLAN opartych na uk³adach RT2x00
Name:		rt2x00
Version:	2.0.0
%define		_subver	b3
%define		_rel	0.%{_subver}.3
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
License:	GPL v2
Source0:	http://rt2x00.serialmonkey.com/%{name}-%{version}-%{_subver}.tar.gz
# Source0-md5:	4881d742ee49d3ea12c435a91deacd41
URL:		http://rt2x00.serialmonkey.com/
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.217
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A configuartion tool for WLAN cards based on RT2x00 chipsets.

%description -l pl
Narzêdzie konfiguracujne do kart WLAN opartych na uk³adach RT2x00.

%package -n kernel-net-rt2x00
Summary:	Linux kernel driver for WLAN cards based on RT2x00 chipsets
Summary(pl):	Sterownik j±dra Linuksa dla kart WLAN opartych na uk³adach RT2x00
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel-net-rt2x00
This is a Linux driver for WLAN cards based on RT2x00 chipsets.

%description -n kernel-net-rt2x00 -l pl
Sterownik j±dra Linuksa dla kart WLAN opartych na uk³adach RT2x00.

%package -n kernel-smp-net-rt2x00
Summary:	Linux SMP kernel driver for WLAN cards based on RT2x00 chipsets
Summary(pl):	Sterownik j±dra Linuksa SMP dla kart WLAN opartych na uk³adach RT2x00
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel-smp-net-rt2x00
This is a Linux driver for WLAN cards based on RT2x00 chipsets.

This package contains Linux SMP module.

%description -n kernel-smp-net-rt2x00 -l pl
Sterownik j±dra Linuksa dla kart WLAN opartych na uk³adach RT2x00.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q -n %{name}-%{version}-%{_subver}

%build
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
  %{__make} -C %{_kernelsrcdir} O=$PWD scripts
	%{__make} clean
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

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net/wireless
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
if [ $cfg = up -o $cfg = nondist ]; then
	ocfg=''
else
	ocfg=$cfg
fi
install o-$cfg/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}$ocfg/kernel/drivers/net/wireless
done

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel-net-rt2x00
%depmod %{_kernel_ver}

%postun -n kernel-net-rt2x00
%depmod %{_kernel_ver}

%post -n kernel-smp-net-rt2x00
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-rt2x00
%depmod %{_kernel_ver}smp

%files -n kernel-net-rt2x00
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-rt2x00
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/*.ko*
%endif
