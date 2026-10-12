
resource "mws_vpc_network" "main" {
  network = "sre-lab-vpc"
  project = "project-sofmishasof"
  mtu     = 1500

  metadata = {
    description  = "Production SRE Lab network"
    display_name = "sre-lab-vpc"
  }

  lifecycle {
    prevent_destroy = true
  }
}
