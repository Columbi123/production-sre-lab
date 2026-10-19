
resource "mws_vpc_subnet" "app" {
  subnet  = "sre-app"
  network = mws_vpc_network.main.network
  cidr    = "10.10.20.0/24"
  project = "project-sofmishasof"

  metadata = {
    description  = "Application subnet for Production SRE Lab"
    display_name = "sre-app"
  }

  lifecycle {
    prevent_destroy = true
  }
}
