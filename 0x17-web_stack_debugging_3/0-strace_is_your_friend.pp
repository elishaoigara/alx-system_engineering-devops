# This Puppet manifest ensures Apache is installed, running, and fixes common issues
class web_debugging {
  
  # Ensure Apache2 is installed
  package { 'apache2':
    ensure => installed,
  }

  # Ensure Apache2 service is running
  service { 'apache2':
    ensure    => running,
    enable    => true,
    require   => Package['apache2'],
  }

  # Fix missing modules or permissions
  exec { 'fix_apache_permissions':
    command => '/bin/chmod -R 755 /var/www/html',
    onlyif  => '/usr/bin/test -d /var/www/html',
    require => Service['apache2'],
  }

  # Restart Apache to apply changes
  exec { 'restart_apache':
    command => '/usr/sbin/service apache2 restart',
    require => Service['apache2'],
  }

}

include web_debugging
