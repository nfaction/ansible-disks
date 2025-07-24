# ansible-disks

[![Ansible Molecule Test Matrix](https://github.com/nfaction/ansible-disks/actions/workflows/molecule.yml/badge.svg)](https://github.com/nfaction/ansible-disks/actions/workflows/molecule.yml)

Configure disks for use in monitoring, maintenance, formatting, and mounting.

## References

* SMART Roles
  * https://github.com/LibreIT/ansible-smartd
  * https://github.com/stuvusIT/smartd
  * https://blog.shadypixel.com/monitoring-hard-drive-health-on-linux-with-smartmontools/
  * https://wiki.archlinux.org/index.php/S.M.A.R.T.#Schedule_self-tests
* SSD Trim
  * https://wiki.archlinux.org/index.php/Solid_state_drive#Periodic_TRIM
  * https://www.digitalocean.com/community/tutorials/how-to-configure-periodic-trim-for-ssd-storage-on-linux-servers

## Features

* **Disk Discovery**: Automatically identifies SSDs, spinning disks, and RAID arrays
* **SMART Monitoring**: Configures smartmontools for disk health monitoring
* **SSD Maintenance**: Enables periodic TRIM for SSD longevity
* **Disk Formatting**: Format disks with specified filesystems using ansible.posix collection
* **Automatic Mounting**: Mount formatted disks and add entries to /etc/fstab

## Usage

### Basic SMART Monitoring (existing functionality)

The role automatically detects disks and configures SMART monitoring without additional configuration.

### Disk Formatting and Mounting (new functionality)

```yaml
- hosts: all
  roles:
    - ansible-disks
  vars:
    disks_to_format:
      - device: /dev/sdb
        filesystem: ext4
        mount_point: /mnt/data1
        mount_options: defaults,noatime
        state: present
      - device: /dev/sdc
        filesystem: ext4
        mount_point: /mnt/data2
        mount_options: defaults
        state: present
      - device: /dev/sdd
        filesystem: ext4
        mount_point: /mnt/backup
        mount_options: defaults,noatime,nodev
        state: present
```

### Selective Feature Usage

You can disable specific functionality by setting toggle variables:

```yaml
- hosts: all
  roles:
    - ansible-disks
  vars:
    # Only enable disk formatting, disable monitoring features
    enable_disk_discovery: false
    enable_smart_monitoring: false
    enable_ssd_trim: false
    enable_disk_formatting: true
    disks_to_format:
      - device: /dev/sdb
        filesystem: ext4
        mount_point: /mnt/data
```

```yaml
- hosts: all
  roles:
    - ansible-disks  
  vars:
    # Only enable SMART monitoring
    enable_disk_discovery: true
    enable_smart_monitoring: true
    enable_ssd_trim: false
    enable_disk_formatting: false
```

### Variables

#### Feature Toggle Variables

* `enable_disk_discovery`: Enable automatic disk discovery (default: `true`)
* `enable_smart_monitoring`: Enable SMART monitoring configuration (default: `true`)
* `enable_ssd_trim`: Enable SSD TRIM service configuration (default: `true`)
* `enable_disk_formatting`: Enable disk formatting and mounting (default: `true`)

#### Disk Formatting Variables

* `disks_to_format`: List of disks to format and mount (default: `[]`)
  * `device`: Block device path (e.g., `/dev/sdb`)
  * `filesystem`: Filesystem type (default: `ext4`)
  * `mount_point`: Mount point directory
  * `mount_options`: Mount options (default: `defaults`)
  * `state`: `present`/`mounted` to mount, `absent` to unmount (default: `present`)
  * `force`: Force filesystem creation (default: `false`)

* `default_filesystem`: Default filesystem type (default: `ext4`)
* `default_mount_options`: Default mount options (default: `defaults`)
* `create_mount_dirs`: Create mount point directories (default: `true`)

## Dependencies

* `ansible.posix` collection for filesystem and mount modules
* `e2fsprogs` package for ext4 filesystem support

## Tags

### Section Tags
* `disk-discovery`: Run only disk discovery tasks
* `smart-monitoring`: Run only SMART monitoring tasks
* `ssd-trim`: Run only SSD trim tasks
* `disk-formatting`: Run only disk formatting and mounting tasks

### Granular Tags
* `mount-dirs`: Run only mount directory creation
* `mount-disks`: Run only mounting tasks
* `unmount-disks`: Run only unmounting tasks
* `template-configs`: Run only configuration file tasks
