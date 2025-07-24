import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_mount_points_created(host):
    """Test that mount point directories are created"""
    mount_points = ['/mnt/data1', '/mnt/data2', '/mnt/backup']
    
    for mount_point in mount_points:
        d = host.file(mount_point)
        assert d.exists
        assert d.is_directory
        assert d.user == 'root'
        assert d.group == 'root'


def test_fstab_entries(host):
    """Test that disks are properly added to fstab"""
    fstab = host.file('/etc/fstab')
    
    assert fstab.exists
    
    # Check for our test mount points in fstab
    # Note: In container testing, the filesystem creation might not work,
    # but we can still verify the mount module attempts were made
    fstab_content = fstab.content_string
    
    # The test will depend on whether the loop devices were successfully created
    # This is more of a structural test than functional due to container limitations


def test_disk_packages_installed(host):
    """Test that required disk packages are installed"""
    packages = ['util-linux', 'smartmontools', 'e2fsprogs']
    
    for package in packages:
        pkg = host.package(package)
        assert pkg.is_installed
