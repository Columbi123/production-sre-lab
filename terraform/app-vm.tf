
resource "mws_compute_virtual_machine" "app" {
  virtual_machine = "sre-app-01"
  vm_type         = "compute/vmTypes/base-2-4"
  project         = "project-sofmishasof"
  zone            = "ru-central1-a"

  metadata = {
    display_name = "sre-app-01"
    description  = "Application VM for Production SRE Lab"
  }

  hardware = {
    power                     = "ON"
    graceful_shutdown_timeout = "1m 30s"
  }

  network = {
    network_interfaces = [
      {
        name    = "nic0"
        primary = true

        addresses = [
          {
            address = {
              spec = {
                subnet     = mws_vpc_subnet.app.metadata.id
                ip_address = "10.10.20.10"
              }
            }
          }
        ]
      }
    ]
  }

  storage = {
    disks = [
      {
        name = "boot"
        boot = true

        disk = {
          spec = {
            disk_type = "diskTypes/nbs-pl2"
            size      = "30GB"
            iops      = 1000

            source = {
              image = "compute/projects/mws-ubuntu/images/mws-ubuntu-2404-lts-v20260916"
            }
          }
        }
      }
    ]
  }

  os = {
    hostname = "sre-app-01"

    metadata = {
      attributes = {
        "user-data" = <<-CLOUD
          #cloud-config
          users:
            - name: sre
              groups: [sudo]
              shell: /bin/bash
              sudo: "ALL=(ALL) NOPASSWD:ALL"
              ssh_authorized_keys:
                - ${trimspace(file(pathexpand("~/.ssh/id_ed25519_sre_app.pub")))}
        CLOUD
      }
    }
  }

  lifecycle {
    prevent_destroy = true
  }
}
