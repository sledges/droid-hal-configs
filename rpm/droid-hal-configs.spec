%define board_mappings_dir %{_datadir}/ssu/board-mappings.d

Name:       droid-hal-configs
Summary:    Some configs for Droid HAL adaptations
Version:    1
Release:    1
Group:      Configs
License:    GPLv2
Source0:    %{name}-%{version}.tar.bz2
BuildRequires: ssu-kickstart-configuration-jolla
BuildRequires: pkgconfig(android-headers)
BuildRequires: droid-hal
BuildRequires: droid-hal-devel
BuildRequires: droid-hal-kickstart-configuration

%description
%{summary}.

%package -n ssu-kickstarts-droid
Summary:    Kickstarts for Droid HAL
Provides:   image-configurations

%description -n ssu-kickstarts-droid
%{summary}.

%install
rm -rf %{buildroot}
# Obtain the DEVICE from the same source as used in /etc/os-release
. /usr/lib/droid-devel/hw-release.vars

mkdir -p $RPM_BUILD_ROOT/%{board_mappings_dir}
cp -f %{board_mappings_dir}/05-$MER_HA_VENDOR-$MER_HA_DEVICE.ini $RPM_BUILD_ROOT/%{board_mappings_dir}/
cp -rf %{_datadir}/ssu/kickstart $RPM_BUILD_ROOT/%{_datadir}/ssu/

echo "DISTURL = %{DISTURL}"
echo "DISTURL with jolla domain name removed = ${%{DISTURL}/jollamobile.com}"
# if we are building on Mer OBS, make a .ks which will work for HADK users
%if "${%{DISTURL}/jollamobile.com}" == "%{DISTURL}"
echo "Setting domain to sales"
%define ssu_override domain=sales
%else
echo "Setting domain to jolla"
%define ssu_override domain=jolla
%endif

# build rnd kickstarts on devel level, release kickstarts on all other levels
%if 0%{?qa_stage_devel:1}
KS_LEVELS=true %gen_ks $MER_HA_DEVICE
%else
KS_LEVELS=false %gen_ks $MER_HA_DEVICE
%endif

rm -rf $RPM_BUILD_ROOT/%{board_mappings_dir}
rm -rf $RPM_BUILD_ROOT/%{_datadir}/ssu/kickstart

%files
%defattr(-,root,root,-)

%files -n ssu-kickstarts-droid
%defattr(-,root,root,-)
%{_datadir}/kickstarts/*.ks

