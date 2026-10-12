
resource "mws_vpc_subnet" "management" {
  subnet  = "sre-management"
  network = mws_vpc_network.main.network
  cidr    = "10.10.10.0/24"
  project = "project-sofmishasof"

  metadata = {
    description  = "Management-сервер"
    display_name = "sre-management"
  }

  lifecycle {
    prevent_destroy = true
  }
}
