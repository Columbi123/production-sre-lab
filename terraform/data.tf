data "mws_vpc_network" "existing" {
  network = "sre-lab-vpc"
}

output "network_mtu" {
  description = "MTU existing VPC"
  value       = data.mws_vpc_network.existing.mtu
}

data "mws_vpc_subnet" "management" {
  network = "sre-lab-vpc"
  subnet  = "sre-management"
}

data "mws_compute_virtual_machine" "control" {
  virtual_machine = "sre-control"
}

output "management_subnet_cidr" {
  description = "Management subnet CIDR"
  value       = data.mws_vpc_subnet.management.cidr
}

output "control_vm_zone" {
  description = "Management VM availability zone"
  value       = data.mws_compute_virtual_machine.control.zone
}
