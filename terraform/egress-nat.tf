
resource "mws_vpc_egress_nat" "app" {
  egress_nat = "sre-app-egress"
  network    = mws_vpc_network.main.network
  project    = "project-sofmishasof"

  metadata = {
    display_name = "sre-app-egress"
    description  = "Outbound internet access for sre-app subnet"
  }

  external = {
    addresses = [
      {
        spec = {}
      }
    ]
  }

  internal = {
    subnets = [
      mws_vpc_subnet.app.metadata.id
    ]
  }
}
